# tAInder 🤖💕

> A revolutionary dating app where you can meet and chat with unique and diverse AI personalities.

## 📖 Description

tAInder is a dating-inspired application that allows you to connect with dynamically created artificial intelligences. Each AI has its own unique personality, hobbies, job, sexual orientation, and lifestyle, generated through advanced prompts and the power of Ollama LLM.

### ✨ Key Features

- **Dynamic Profile Generation**: Each AI is created with unique characteristics using custom prompts
- **Interactive Chat**: Fluid and natural conversations with each AI
- **Persistent Conversations**: Each conversation maintains a summary for narrative continuity
- **Diverse Personalities**: AIs with different personality tags, hobbies, jobs, and lifestyles
- **REST API**: Robust and scalable architecture
- **Intuitive Interface**: User experience similar to popular dating apps

## 🛠️ Technologies Used

- **Backend**: Django 5, Django REST Framework 3
- **AI**: Ollama for content generation
- **Database**: SQLite / PostgreSQL
- **API**: RESTful API with Django REST Framework
- **Filtering**: django-filter
- **Documentation**: Markdown, Mermaid for UML diagrams

## 📋 Prerequisites

- Python 3.8+
- Ollama installed and running

## 🚀 Installation

### 1. Clone the repository
```bash
git clone https://github.com/MaribelSR/tAInder.git
cd tAInder
```

### 2. Create virtual environment
```bash
cd backend
python -m venv .venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate
```

### 3. Install dependencies
```bash
pip install -r requirements.txt
```

### 4. Configure Ollama
Make sure Ollama is installed and running on your system:
```bash
ollama serve
```

### 5. Run migrations
```bash
python manage.py migrate
```

### 6. Create superuser (optional)
```bash
python manage.py createsuperuser
```

### 7. Run development server
```bash
python manage.py runserver
```

The application will be available at `http://localhost:8000`

## 📚 Documentation

To see the complete database diagram, check [schema.md](docs/schema.md).

## 🎯 Features

### AI Profile Generation
```bash
cd backend
python manage.py generate_profile
```

### Chat System
- Persistent conversations with contextual memory
- Responses generated based on each AI's personality
- Automatic summaries to maintain coherence

### Personality Tags
- **Personality**: Extroverted, Introverted, Adventurous, Intellectual, etc.
- **Hobbies**: Sports, Art, Technology, Music, Travel, etc.
- **Profession**: Various professions and occupations
- **Sexuality**: Inclusive and diverse representation
- **Lifestyle**: Urban, Rural, Nomadic, Sedentary, etc.


## 📊 Diagrams

### Sequence Diagram
Typical interaction flow:
1. User requests new AI
2. System generates profile via Ollama
3. User starts conversation
4. AI responds based on its personality
5. System updates conversation summary

See [complete sequence diagram](docs/sequence.md)

## 🤝 Contributing

1. Fork the project
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Commit your changes (`git commit -am 'Add new feature'`)
4. Push to the branch (`git push --set-upstream origin feature/new-feature`)
5. Create a Pull Request

## 📄 License

This project is licensed under the Apache 2.0 License. See the `LICENSE` file for more details.

## 🙏 Acknowledgments

- **Ollama** for providing local AI infrastructure
- **Django** for the robust web framework
- **Django REST Framework** for API tools

## 📞 Contact

- GitHub: [@MaribelSR](https://github.com/MaribelSR/)
- Email: maribelsalvadorr@gmail.com
- LinkedIn: [maribelsalvadorr](https://www.linkedin.com/in/maribelsalvadorr/)

---

⭐ If you find this project useful, consider giving it a star!