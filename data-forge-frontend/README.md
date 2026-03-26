# Data Forge Frontend

Professional AI-powered data cleaning platform - Frontend

## Environment Variables Setup

**For Development (.env):**
```
REACT_APP_BACKEND_URL=http://localhost:5000
```

**For Railway Production:**
1. Go to Railway dashboard → Your project → Variables tab
2. Add: `REACT_APP_BACKEND_URL=https://your-backend-url.up.railway.app`

## Local Development

```bash
npm install
npm start
```

## Build & Deploy

```bash
npm install
npm run build
# Deploy build folder to Railway
```

## Features

- Professional Swiss-style UI design
- Drag & drop file upload (CSV, Excel)
- Real-time data quality scoring
- AI-powered data cleaning
- Interactive data visualizations
- Download cleaned data

## Tech Stack

- React 19
- Recharts for visualizations
- Lucide React for icons
- Axios for API calls
