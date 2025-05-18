# AI-Powered Content Curation API

> A scalable, secure, and AI-integrated REST API for content curation, summarization, and analysis, built with Django REST Framework, PostgreSQL, Docker, and JWT Authentication.

---

## 📁 Project Structure

```
ai-content-curation-api/
│
├── app/
│   ├── core/               # Authentication app (register, login, JWT), Core utilities, healthcheck etc.
        ├── tests/                  # Tests 
│   ├── contents/           # Content CRUD, categorization, AI analysis
        ├── tests/                  # Tests
        ├── tasks/                  # Celery task  
│   ├── __init__.py
│   ├── settings.py
│   ├── asgi.py
│   ├── celery.py
│   ├── urls.py
│   └── wsgi.py
├── docker-compose.yml
├── Dockerfile
├── requirements.txt
├── .env
├── .env.template
├── constant.py
├── setup.cfg
├── manage.py
├── .github/
│   └── workflows/
│       └── ci-cd.yml       # GitHub Actions workflow file
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
  - Integrates GROQ API

- **Infrastructure**
  - PostgreSQL database
  - Redis caching
  - Celery worker to distribute contents' summarization, analysis and topics from content api
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
git clone https://github.com/sarwarmdgolam/curation-api.git
```


### Environment Variables
Copy .env.template to .env and fill in your secrets:

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

- The API will be available at: http://localhost:8085/
- Access Django Admin at: http://localhost:8085/admin/


## 🧰 Usage

### API Endpoints (examples)
- Auth

    - POST /api/auth/register/ — Register user
      ```
      sample payload:
        {
            "username": "usr",
            "email": "usr@gmail.com",
            "password": "abcd1234#."
        }
      ```

    - POST /api/auth/login/ — Get JWT token
      ```
      sample payload:
      {
          "username": "golamsarwar",
          "password": "abcd1234#."
      }
      ```
    - POST /api/auth/token/refresh/ — Refresh JWT token
      ```aiignore
      sample payload:
      {
          "refresh": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ0b2tlbl90eXBlIjoicmVmcmVzaCIsImV4cCI6MTc0NzU2MjM5NSwiaWF0IjoxNzQ3NDc1OTk1LCJqdGkiOiJmMDhhODM2MzExOGM0MWI5OTFkYjhkMTA2YTM5YmMyMyIsInVzZXJfaWQiOjJ9.aWxrAerOTNZwnTSQqOzDwB8jCa7r097dEIrWyjpLCqw"
      }
      ```

- Content (with JWT)

    - GET /api/contents/ — List public contents

      ```
        GET: localhost:8085/api/contents/contents/?search=inhaler
        Sample Res:
        [
            {
                "id": 12,
                "category": 1,
                "title": "Which is better for children with asthma: syrup, nebuliser, or inhaler?",
                "body": "Treating a child's asthma presents certain difficulties for paediatricians. The first is that parents are unwilling to acknowledge that asthma may strike youngsters as well. Child asthma is indicated by recurrent coughing, nighttime awakenings due to coughing, and temporary alleviation of respiratory symptoms following the use of certain medications, particularly nebulised treatments. These kids frequently have a runny nose, scaly scalp, itchy skin, and a family history of the same condition.",
                "source_url": "https://www.thedailystar.net/health/healthcare/news/which-better-children-asthma-syrup-nebuliser-or-inhaler-3897051",
                "summary": "Here's a summary of the content:\n\nTreating asthma in children can be challenging because some parents may not recognize that asthma can affect young children. Asthma in children is characterized by recurring coughing, nighttime awakenings due to coughing, and temporary relief of symptoms with medication, such as nebulized treatments. Children with asthma often exhibit additional symptoms like a runny nose, scalp irritation, itchy skin, and a family history of asthma.",
                "sentiment": "Neutral",
                "topics": [
                    "Here are the key topics extracted from the content as a Python list of strings:\n\n`['Childhood asthma', 'Symptoms of child asthma', 'Diagnosis of child asthma', 'Treatment of child asthma', 'Parental awareness of child asthma']`\n\nNote that these topics are inferred based on the content and may not be explicitly mentioned."
                ],
                "created_at": "2025-05-18T06:13:29.978191Z",
                "updated_at": "2025-05-18T06:13:32.384107Z",
                "author": 2
            }
        ] 
      ```

    
  - POST /api/contents/ — Create content (auth users) 

    ```
    After new content create send the content to Celley task to distribute contents' summarization, analysis and topics update by using GROK AI api
    sample payload:
      {
          "title": "Which is better for children with asthma: syrup, nebuliser, or inhaler?",
          "body": "Treating a child's asthma presents certain difficulties for paediatricians. The first is that parents are unwilling to acknowledge that asthma may strike youngsters as well. Child asthma is indicated by recurrent coughing, nighttime awakenings due to coughing, and temporary alleviation of respiratory symptoms following the use of certain medications, particularly nebulised treatments. These kids frequently have a runny nose, scaly scalp, itchy skin, and a family history of the same condition.",
          "source_url": "https://www.thedailystar.net/health/healthcare/news/which-better-children-asthma-syrup-nebuliser-or-inhaler-3897051",
          "category": 1
      }
    ```
    
  - GET /api/contents/{id}/ — Get content detail

    ```
    sample req: GET localhost:8085/api/contents/contents/11
    sample res:
    {
        "id": 11,
        "category": 1,
        "title": "Which is better for children with asthma: syrup, nebuliser, or inhaler?",
        "body": "Treating a child's asthma presents certain difficulties for paediatricians. The first is that parents are unwilling to acknowledge that asthma may strike youngsters as well. Child asthma is indicated by recurrent coughing, nighttime awakenings due to coughing, and temporary alleviation of respiratory symptoms following the use of certain medications, particularly nebulised treatments. These kids frequently have a runny nose, scaly scalp, itchy skin, and a family history of the same condition.",
        "source_url": "https://www.thedailystar.net/health/healthcare/news/which-better-children-asthma-syrup-nebuliser-or-inhaler-3897051",
        "summary": "Pediatricians face challenges when treating childhood asthma because some parents may not recognize that asthma can affect young children. Childhood asthma is characterized by recurring coughing, frequent nighttime awakenings due to coughing, and temporary relief of respiratory symptoms with medication, particularly nebulized treatments. Children with asthma may also exhibit symptoms such as a runny nose, scaly scalp, itchy skin, and a family history of the condition.",
        "sentiment": "Neutral",
        "topics": [
            "Here are the key topics extracted as a Python list of strings:\n\n```\ntopics = [\n    \"Treating child's asthma\",\n    \"Paediatrician difficulties\",\n    \"Child asthma symptoms\",\n    \"Asthma in youngsters\",\n    \"Asthma diagnosis\",\n    \"Asthma treatment\",\n    \"Nebulised treatments\",\n    \"Childhood asthma characteristics\"\n]\n```"
        ],
        "created_at": "2025-05-18T06:11:21.739740Z",
        "updated_at": "2025-05-18T06:11:27.346855Z",
        "author": 2
    }
    ```
        
  - PUT/PATCH /api/contents/{id}/ — Update content (owner/admin)
    
  - DELETE /api/contents/{id}/ — Delete content (owner/admin)
    
  - POST /api/contents/{id}/summarize/ — Summarize (Used GROK AI api)

    ```
    sample req:
    {
        "content": "Treating a child's asthma presents certain difficulties for paediatricians. The first is that parents are unwilling to acknowledge that asthma may strike youngsters as well. Child asthma is indicated by recurrent coughing, nighttime awakenings due to coughing, and temporary alleviation of respiratory symptoms following the use of certain medications, particularly nebulised treatments. These kids frequently have a runny nose, scaly scalp, itchy skin, and a family history of the same condition.Worldwide asthma treatment guidelines are established by the Global Initiative for Asthma (GINA), an international organisation. For specific reasons, medical professionals are recommending the use of inhalers for asthma medicine and discouraging the use of oral medications.1. The oral version of a certain medication is required in the greatest quantity, followed by the nebulised form and the inhaler in the least amount. Therefore, the latter version is likely to have the fewest adverse effects.2. In addition to the lungs, oral medications have adverse effects on the stomach, kidneys, liver, and heart. In contrast, inhaler drugs only directly affect the lungs.3. The cornerstone of asthma treatment is steroids. After extended use, they cause a number of adverse effects. These oral medications might cause short stature, mouth infections, heart problems, stomach issues, and other issues in growing children. It is surprising to learn that inhaled steroids virtually never cause these issues.4. Controlled asthma is achieved by using a regular inhaler.5. The cost of treatment is a significant concern. The initial cost of the inhaler and spacer is a clear worry. However, we can conclude that inhalers are reasonably priced when taking into account the limited usage of other treatments and overall health over time."
    }
    
    sample res:
    
    {
        "summary": "Here's a summary of the content:\n\nTreating childhood asthma can be challenging, as parents may not always recognize the symptoms. Asthma in children is characterized by recurring coughing, nighttime awakenings, and temporary relief with medication, particularly nebulized treatments. The Global Initiative for Asthma (GINA) provides worldwide treatment guidelines. Medical professionals recommend inhalers over oral medications due to several reasons. Inhalers have fewer adverse effects, affecting only the lungs, whereas oral medications can cause stomach, kidney, liver, and heart problems. Steroids, a cornerstone of asthma treatment, can cause issues in growing children when used orally, but not when inhaled. Regular use of an inhaler can control asthma, and while the initial cost of the inhaler and spacer may be a concern, it's relatively affordable when considering the long-term benefits and reduced need for other treatments."
    }
    
    ```


  - POST /api/contents/analyze/ - analyze content

    ```
    sample req:
    {
        "content": "Treating a child's asthma presents certain difficulties for paediatricians. The first is that parents are unwilling to acknowledge that asthma may strike youngsters as well. Child asthma is indicated by recurrent coughing, nighttime awakenings due to coughing, and temporary alleviation of respiratory symptoms following the use of certain medications, particularly nebulised treatments. These kids frequently have a runny nose, scaly scalp, itchy skin, and a family history of the same condition.Worldwide asthma treatment guidelines are established by the Global Initiative for Asthma (GINA), an international organisation. For specific reasons, medical professionals are recommending the use of inhalers for asthma medicine and discouraging the use of oral medications.1. The oral version of a certain medication is required in the greatest quantity, followed by the nebulised form and the inhaler in the least amount. Therefore, the latter version is likely to have the fewest adverse effects.2. In addition to the lungs, oral medications have adverse effects on the stomach, kidneys, liver, and heart. In contrast, inhaler drugs only directly affect the lungs.3. The cornerstone of asthma treatment is steroids. After extended use, they cause a number of adverse effects. These oral medications might cause short stature, mouth infections, heart problems, stomach issues, and other issues in growing children. It is surprising to learn that inhaled steroids virtually never cause these issues.4. Controlled asthma is achieved by using a regular inhaler.5. The cost of treatment is a significant concern. The initial cost of the inhaler and spacer is a clear worry. However, we can conclude that inhalers are reasonably priced when taking into account the limited usage of other treatments and overall health over time."
    }
    
    sample res:
    {
        "sentiment": "Neutral",
        "topics": [
            "Here are the key topics extracted from the content as a Python list of strings:\n\n```\ntopics = [\n    \"Child asthma\",\n    \"Asthma symptoms\",\n    \"Asthma treatment guidelines\",\n    \"Inhaler vs oral medications\",\n    \"Adverse effects of oral medications\",\n    \"Adverse effects of inhaler drugs\",\n    \"Steroids in asthma treatment\",\n    \"Controlled asthma\",\n    \"Cost of asthma treatment\"\n]\n```\n\nLet me know if you need any"
        ],
        "related_articles": "Based on the content provided, I analyzed the text and identified the top 2 most related articles/snippets. Here are the results:\n\n1. **Article 2**: This snippet discusses the adverse effects of oral medications on various organs, including the stomach"
    }
    
    ```

- Category

    - GET /api/categories/ — List of categories; This api will be "read through" cache and once there is new category is added or update the cache will be invalidated





## 🧪 Running Tests

Run tests with coverage inside Docker:

```bash
docker compose exec web pytest  # to test whole application
docker compose exec web flake8 .  # to lint whole application
```
