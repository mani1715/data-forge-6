# Data Forge Backend

Professional AI-powered data cleaning platform - Backend API

## Local Development

```bash
pip install -r requirements.txt
python run_server.py
```

## Railway Deployment

1. Connect your GitHub repo to Railway
2. Railway will auto-detect the Procfile
3. Deploy!

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/` | GET | Health check |
| `/health` | GET | Health status |
| `/upload` | POST | Upload CSV/Excel file |
| `/action` | POST | Perform cleaning action |
| `/download` | GET | Download cleaned data |

## Environment Variables

- `PORT` - Server port (auto-set by Railway)
- `SECRET_KEY` - Flask secret key (optional)

## Features

- AI-powered data cleaning (MICE algorithm)
- Quality scoring
- Outlier detection (IQR method)
- Missing value handling
- Duplicate removal
- Text data cleaning
