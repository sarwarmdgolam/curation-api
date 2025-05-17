# AI-Powered Content Curation API

> A scalable, secure, and AI-integrated REST API for content curation, summarization, and analysis, built with Django REST Framework, PostgreSQL, Docker, and JWT Authentication.

---

## 📁 Project Structure

```
ai-content-curation-api/
│
├── app/
│   ├── auth/               # Authentication app (register, login, JWT)
│   ├── contents/           # Content CRUD, categorization, AI analysis
│   ├── core/               # Core utilities, healthcheck etc.
│   ├── __init__.py
│   ├── settings.py
│   ├── urls.py
│   └── wsgi.py
│
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env.example
├── manage.py
├── tests/                  # Tests for all apps
│
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions workflow file
│
└── README.md

```

---


---

## 🚀 Features

- **Authentication & Authorization**
  - JWT Authentication using `djangorestframework-simplejwt`
  - Role-Based Access Control (Public, User, Admin)

- **Content Management**
  - CRUD operations on content with categories & metadata
  - Search & filter support

- **AI-Powered Features**
  - Content Summarization
  - Sentiment Analysis
  - Topic Extraction
  - Related Content Recommendations
  - Integrates GROQ API (or OpenAI as fallback)

- **Infrastructure**
  - PostgreSQL database
  - Redis caching
  - Docker & Docker Compose for containerization
  - GitHub Actions for CI/CD (linting, testing, building)
  - Ready for deployment (Render or other cloud)

---

## 🛠️ Setup & Installation

### Prerequisites

- Docker & Docker Compose
- (Optional) Python 3.11+, pip (for local dev without Docker)

### Clone the Repo

```bash
git clone https://github.com/yourusername/ai-content-curation-api.git
cd ai-content-curation-api
```


### Environment Variables
Copy .env.example to .env and fill in your secrets:

```
POSTGRES_DB=your_db_name
POSTGRES_USER=your_db_user
POSTGRES_PASSWORD=your_db_password
SECRET_KEY=your_django_secret_key
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
GROQ_API_KEY=your_groq_api_key
REDIS_URL=redis://redis:6379/1
```

### Build and Run
```bash
docker-compose up --build
```

- The API will be available at: http://localhost:8000/
- Access Django Admin at: http://localhost:8000/admin/


## 🧰 Usage

### API Endpoints (examples)
- Auth

    - POST /api/auth/register/ — Register user

    - POST /api/auth/login/ — Get JWT token

    - POST /api/auth/token/refresh/ — Refresh JWT token

- Content

    - GET /api/contents/ — List public contents
    
    - POST /api/contents/ — Create content (auth users)
    
    - GET /api/contents/{id}/ — Get content detail
    
    - PUT/PATCH /api/contents/{id}/ — Update content (owner/admin)
    
    - DELETE /api/contents/{id}/ — Delete content (owner/admin)
    
    - POST /api/contents/{id}/summarize/ — Summarize & analyze content

- Category

    - GET /api/categories/ — List categories


### Example: Summarize content (with JWT)

```bash
curl -X POST http://localhost:8000/api/contents/1/summarize/ \
-H "Authorization: Bearer <your_access_token>"
```


## 🧪 Running Tests

Run tests with coverage inside Docker:

```bash
docker-compose exec web pytest --cov
```
