from datetime import datetime, timezone, timedelta
import os
import socket
import sys
import time
import importlib
import traceback
import signal
import json

from django.core.management.base import BaseCommand

from pipeline.models import Task


class Command(BaseCommand):
    working = True

    def tasks_completed_cleanup(self, max_time_completed=60 * 60 * 24 * 30):
        now = datetime.now(timezone.utc)
        n, _ = Task.objects.filter(
            status=Task.Status.COMPLETED,
            unlocked_at__lt=now - timedelta(seconds=max_time_completed),
        ).delete()
        if n > 0:
            print(
                "Deleted {} completed tasks older than {} seconds".format(
                    n, max_time_completed
                )
            )

    def retry_stalled_tasks(self, max_time_stalled=60 * 60 * 24):
        now = datetime.now(timezone.utc)
        n = Task.objects.filter(
            status=Task.Status.PROCESSING,
            locked_at__lt=now - timedelta(seconds=max_time_stalled),
        ).update(
            status=Task.Status.QUEUED,
            unlocked_at=now,
        )
        if n > 0:
            print(
                "Requeued {} stalled tasks older than {} seconds".format(
                    n, max_time_stalled
                )
            )

    def add_arguments(self, parser):
        parser.add_argument(
            "--wait",
            type=int,
            default=3,
            nargs="?",
            help="How many seconds to wait after no tasks; default 10",
        )
        parser.add_argument(
            "--max_time_completed",
            type=int,
            default=60 * 60 * 24 * 30,
            nargs="?",
            help="Max time in seconds to keep completed tasks; default 2592000 (30 days)",
        )
        parser.add_argument(
            "--max_time_stalled",
            type=int,
            default=60 * 60 * 24,
            nargs="?",
            help="Max time in seconds to retry stalled tasks; default 86400 (1 day)",
        )

    def signal_handler(self, signum, frame):
        self.working = False
        print("Exiting...")

    def handle(self, *args, **options):
        waiting = False
        worker_name = "{}_{}_{}".format(
            socket.gethostname(), os.getpid(), int(datetime.now().timestamp())
        )

        signal.signal(signal.SIGINT, self.signal_handler)
        signal.signal(signal.SIGTERM, self.signal_handler)

        while self.working:
            self.tasks_completed_cleanup(
                max_time_completed=options["max_time_completed"]
            )
            self.retry_stalled_tasks(max_time_stalled=options["max_time_stalled"])
            task = (
                Task.objects.exclude(
                    status__in=[Task.Status.COMPLETED, Task.Status.PROCESSING]
                )
                .order_by("?")
                .first()
            )
            if not task:
                if not waiting:
                    waiting = True
                    print("Waiting for tasks...")
                time.sleep(options["wait"])
            else:
                waiting = False

                task.locked_by = worker_name
                task.locked_at = datetime.now(timezone.utc)
                task.status = Task.Status.PROCESSING
                task.retries += 1
                task.save()
                try:
                    print("Task #{}, executing {}...".format(task.id, task.def_name))
                    # Dividir el nombre del módulo y función
                    # "main.tasks.saludar" -> module="main.tasks", function="saludar"
                    parts = task.def_name.split(".")
                    function_name = parts[-1]
                    module_name = ".".join(parts[:-1])
                    # Importar el módulo y obtener la función
                    module = importlib.import_module(module_name)
                    # Forzar recarga del módulo si ya estaba importado
                    if module_name in sys.modules:
                        module = importlib.reload(module)
                    func = getattr(module, function_name)
                    if task.def_kwargs is None or task.def_kwargs == "":
                        func()
                    else:
                        kwargs = json.loads(task.def_kwargs)
                        func(**kwargs)
                    task.status = Task.Status.COMPLETED
                    print("Task #{} done!".format(task.id))
                except:
                    traceback.print_exc()
                    task.status = Task.Status.FAILED
                    print("Task #{} failed!".format(task.id))
                finally:
                    task.unlocked_at = datetime.now(timezone.utc)
                    task.save()
