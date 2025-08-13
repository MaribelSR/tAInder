from datetime import datetime, timezone
import os
import socket
import sys
import time
import importlib
from django.core.management.base import BaseCommand

from main.models import Task


class Command(BaseCommand):
    def handle(self, *args, **options):
        worker_name = "{}_{}_{}".format(
            socket.gethostname(), os.getpid(), int(datetime.now().timestamp())
        )
        while True:
            task = (
                Task.objects.exclude(
                    status__in=[Task.Status.COMPLETED, Task.Status.PROCESSING]
                )
                .order_by("?")
                .first()
            )
            if not task:
                print("Waiting 60s for tasks to be available...")
                time.sleep(60)
            else:
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
                    func()

                    task.status = Task.Status.COMPLETED
                    print("Task #{} done!".format(task.id))
                except Exception as e:
                    print(e)
                    task.status = Task.Status.FAILED
                    print("Task #{} failed!".format(task.id))
                finally:
                    task.unlocked_at = datetime.now(timezone.utc)
                    task.save()
