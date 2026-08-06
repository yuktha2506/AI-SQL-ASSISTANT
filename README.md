# AI SQL Assistant

AI SQL Assistant is a production-quality full-stack application that converts natural-language questions into safe, readable SQLite queries and explains the generated SQL. It uses a React + Vite frontend, a FastAPI backend, LangChain with the OpenAI API, SQLAlchemy models, Pydantic validation, and a local SQLite database seeded with realistic academic data.

## Features

- Natural language to SQLite SQL generation
- GPT-4.1 / GPT-5 compatible OpenAI model configuration
- Professional prompt that restricts the model to the known schema
- SQL explanation returned with every generated query
- SQL validation before returning results
- Dangerous SQL protection for `DROP`, `DELETE`, `ALTER`, `UPDATE`, and `TRUNCATE`
- SQLite database auto-created and seeded on first backend startup
- Modern responsive React UI with Tailwind CSS
- Dark mode
- SQL syntax highlighting
- Copy SQL and download SQL actions
- Query history sidebar
- Export history as JSON
- Example prompts
- Toast notifications
- Backend logging and error handling
- Unit tests for API health and SQL validation

## Architecture

```text
User
↓
React Frontend
↓
FastAPI Backend
↓
LangChain
↓
OpenAI API
↓
SQL Generator
↓
SQL Validator
↓
SQLite Database
```

Architecture files:

- `architecture.drawio`
- `architecture.png`

## Technologies Used

Frontend:

- React
- Vite
- Tailwind CSS
- Axios
- react-hot-toast
- lucide-react

Backend:

- Python
- FastAPI
- LangChain
- OpenAI API
- SQLAlchemy
- SQLite
- Pydantic
- python-dotenv
- pytest

## Folder Structure

```text
AI_SQL_Assistant/
├── backend/
│   ├── app/
│   │   ├── __init__.py
│   │   ├── config.py
│   │   ├── database.py
│   │   ├── init_db.py
│   │   ├── main.py
│   │   ├── models.py
│   │   ├── prompt.py
│   │   ├── routes.py
│   │   ├── schemas.py
│   │   ├── sql_generator.py
│   │   ├── utils.py
│   │   └── validator.py
│   ├── database/
│   │   └── ai_sql_assistant.db
│   ├── sql/
│   │   ├── sample_data.sql
│   │   └── schema.sql
│   ├── tests/
│   │   ├── test_api.py
│   │   └── test_validator.py
│   ├── .env.example
│   └── requirements.txt
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── pages/
│   │   ├── App.jsx
│   │   ├── index.css
│   │   └── main.jsx
│   ├── .env.example
│   ├── index.html
│   ├── package.json
│   ├── postcss.config.js
│   ├── tailwind.config.js
│   └── vite.config.js
├── .gitignore
├── architecture.drawio
├── architecture.png
└── README.md
```

## SQLite Setup

The application uses:

```text
backend/database/ai_sql_assistant.db
```

Default database URL:

```text
sqlite:///backend/database/ai_sql_assistant.db
```

The backend creates all tables and inserts sample data automatically on first startup. SQL files are also included for review or manual setup:

- `backend/sql/schema.sql`
- `backend/sql/sample_data.sql`

Tables:

- `departments`
- `students`
- `courses`
- `enrollments`

## Backend Setup

```powershell
cd D:\AI_SQL_Assistant\backend
python -m venv .venv
.\.venv\Scripts\activate
pip install -r requirements.txt
copy .env.example .env
```

Edit `.env`:

```env
AI_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash

# Optional OpenAI fallback. Set AI_PROVIDER=openai to use these.
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
ALLOW_DANGEROUS_SQL=False
FRONTEND_ORIGIN=http://localhost:5173
```

Run backend:

```powershell
uvicorn app.main:app --reload
```

Backend URL:

```text
http://localhost:8000
```

Health check:

```text
http://localhost:8000/health
```

## Frontend Setup

```powershell
cd D:\AI_SQL_Assistant\frontend
npm install
copy .env.example .env
npm run dev
```

Frontend URL:

```text
http://localhost:5173
```

## Environment Variables

Backend:

```env
AI_PROVIDER=gemini
GOOGLE_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-3.6-flash

# Optional OpenAI fallback. Set AI_PROVIDER=openai to use these.
OPENAI_API_KEY=your_openai_api_key_here
OPENAI_MODEL=gpt-4.1-mini
# Optional. The app defaults to backend/database/ai_sql_assistant.db automatically.
# DATABASE_URL=sqlite:///backend/database/ai_sql_assistant.db
ALLOW_DANGEROUS_SQL=False
FRONTEND_ORIGIN=http://localhost:5173
ENVIRONMENT=development
```

Frontend:

```env
VITE_API_BASE_URL=http://localhost:8000
```

## API Documentation

### Generate SQL

```http
POST /generate
Content-Type: application/json
```

Request:

```json
{
  "question": "Show top five departments with highest placement percentage"
}
```

Response:

```json
{
  "sql": "SELECT department_name, placement_percentage\nFROM departments\nORDER BY placement_percentage DESC\nLIMIT 5;",
  "explanation": "This query selects department names and placement percentages, sorts departments by placement percentage from highest to lowest, and returns the top five rows."
}
```

Curl:

```powershell
curl -X POST http://localhost:8000/generate `
  -H "Content-Type: application/json" `
  -d "{\"question\":\"Show top five departments with highest placement percentage\"}"
```

## SQL Safety

By default, generated SQL is rejected if it contains:

- `DROP`
- `DELETE`
- `ALTER`
- `UPDATE`
- `TRUNCATE`

To allow these commands in a controlled local environment:

```env
ALLOW_DANGEROUS_SQL=True
```

For production and interview demos, keep it set to `False`.

## Testing

Backend tests:

```powershell
cd D:\AI_SQL_Assistant\backend
pytest
```

Frontend production build:

```powershell
cd D:\AI_SQL_Assistant\frontend
npm run build
```

## Screenshots

Add screenshots here after running the app:

- Home page
- Generated SQL view
- Dark mode
- Query history export

## Future Improvements

- Execute validated read-only SQL and show tabular results
- Add authentication
- Add persistent user query history
- Add schema upload support
- Add rate limiting
- Add Docker and Docker Compose
- Add OpenTelemetry tracing
- Add deployment configs for Render, Railway, and Vercel
