# DataForge - Shape Your Data Into Clarity

## 🎯 Project Overview
DataForge is a professional SaaS-style data cleaning and profiling application powered by AI. It automatically analyzes datasets, identifies quality issues, and provides intelligent cleaning recommendations.

## 🏗️ Architecture

### Backend (Flask)
- **Framework**: Flask 3.1.3
- **Port**: 5000
- **AI/ML**: scikit-learn (MICE algorithm, IQR outlier detection)
- **Data Processing**: pandas, numpy
- **File Support**: CSV, Excel (.xlsx)

### Frontend (React)
- **Framework**: React 19
- **Port**: 3000
- **UI Library**: Custom CSS with professional design system
- **Charts**: Recharts
- **API Client**: Axios

## 📁 Project Structure

```
/app/
├── backend/
│   ├── app.py                 # Flask application entry point
│   ├── config.py             # Configuration settings
│   ├── requirements.txt      # Python dependencies
│   ├── .env                  # Environment variables
│   ├── routes/
│   │   ├── data_routes.py    # Upload & download endpoints
│   │   └── clean_routes.py   # Cleaning action endpoints
│   └── services/
│       ├── ai_engine.py      # AI/ML cleaning logic (MICE, IQR)
│       └── profiler.py       # Data quality scoring
│
└── frontend/
    ├── package.json          # Node.js dependencies
    ├── .env                  # Frontend environment variables
    ├── public/               # Static assets
    └── src/
        ├── App.js            # Main application component
        ├── App.css           # Professional styling
        ├── components/
        │   ├── Header.js     # Top navigation
        │   ├── FileUpload.js # Drag & drop upload
        │   ├── StatsCard.js  # Quality score display
        │   ├── DataTable.js  # Data preview table
        │   ├── CleaningControls.js  # Action buttons
        │   └── Visualization.js     # Charts
        └── services/
            └── api.js        # Axios API configuration
```

## 🔌 API Endpoints

### POST /api/upload
Upload a dataset file (CSV or Excel)

**Request**: `multipart/form-data` with file

**Response**:
```json
{
  "message": "File uploaded successfully",
  "filename": "data.csv",
  "quality_score": 87.5,
  "summary": {
    "rows": 1000,
    "columns": 10,
    "missing_values": 45,
    "duplicates": 5
  },
  "chart_data": {
    "missing_data": [...],
    "type_data": [...]
  },
  "preview": [...]
}
```

### POST /api/action
Perform cleaning actions on the dataset

**Request**:
```json
{
  "action": "fill_missing" | "remove_duplicates" | "remove_outliers" | "clean_text",
  "strategy": "ai" | "mean" | "median" | "mode" | "constant" | "drop_rows",
  "fill_value": 0 (optional)
}
```

**Response**:
```json
{
  "message": "Filled missing values with AI prediction",
  "new_score": 95.2,
  "preview": [...]
}
```

### GET /api/download
Download the cleaned dataset as CSV

**Response**: CSV file download

## 🎨 Design System

### Colors
- **Background**: `#F7F9FC` - Light gray-blue
- **Primary**: `#4F46E5` - Indigo
- **Card Background**: `#FFFFFF` - White
- **Success**: `#10B981` - Green
- **Warning**: `#F59E0B` - Amber
- **Error**: `#EF4444` - Red
- **Border**: `#E5E7EB` - Light gray

### Typography
- **Font Family**: -apple-system, BlinkMacSystemFont, 'Inter', 'Segoe UI'
- **Primary Text**: `#111827`
- **Secondary Text**: `#6B7280`

## 🚀 Features

### Upload Page
- ✅ Centered drag & drop upload zone
- ✅ File validation (CSV, Excel, max 16MB)
- ✅ Loading states with spinner
- ✅ Error handling

### Dashboard
**Left Panel: Statistics**
- ✅ Circular quality score indicator (0-100%)
- ✅ Color-coded status (Green/Yellow/Red)
- ✅ Dataset summary (rows, columns, missing, duplicates)

**Center Panel: Data & Controls**
- ✅ Data table showing first 20 rows
- ✅ Missing values highlighted in red
- ✅ Cleaning strategy dropdown
- ✅ Action buttons (fill missing, remove duplicates, remove outliers, clean text)
- ✅ AI explanation panel with insights

**Right Panel: Visualizations**
- ✅ Bar chart: Missing values per column
- ✅ Pie chart: Data type distribution

**Header**
- ✅ DataForge logo
- ✅ Dataset name display
- ✅ Download clean data button
- ✅ Reset dataset button

## 🤖 AI Features

### Missing Value Strategies
1. **AI Prediction (MICE)**: Uses Multiple Imputation by Chained Equations
2. **Mean**: Fills with column average
3. **Median**: Fills with column median
4. **Mode**: Fills with most frequent value
5. **Fill with 0**: Constant value replacement
6. **Drop Rows**: Removes rows with missing values

### Outlier Detection
- Uses IQR (Interquartile Range) method
- Removes values outside 1.5 * IQR range

### Quality Scoring
- Calculated based on missing value percentage and duplicate rows
- Score = 100 - (missing_penalty + duplicate_penalty)

## 🔧 Configuration

### Backend (.env)
```env
SECRET_KEY=dataforge-secret-key-2024
FLASK_ENV=development
FLASK_DEBUG=True
```

### Frontend (.env)
```env
REACT_APP_BACKEND_URL=http://localhost:5000/api
```

For deployment, update `REACT_APP_BACKEND_URL` to your production backend URL.

## 📊 Technical Stack

### Backend Dependencies
- flask==3.1.3
- flask-cors==6.0.2
- pandas==3.0.1
- numpy==2.4.2
- scikit-learn==1.8.0
- openpyxl==3.1.5

### Frontend Dependencies
- react==19.2.4
- react-dom==19.2.4
- axios==1.13.6
- recharts==3.8.0
- react-scripts==5.0.1

## 🎯 User Workflow

1. **Upload**: User uploads CSV or Excel file
2. **Analysis**: System automatically calculates quality score and generates insights
3. **Review**: User reviews data preview, missing values, and charts
4. **Clean**: User selects cleaning strategy and applies actions
5. **Iterate**: User can apply multiple cleaning operations
6. **Download**: User downloads the cleaned dataset

## 📝 Notes

- Backend stores data in memory (CURRENT_DF global variable)
- Data is lost on server restart
- Maximum file size: 16MB
- Supports CSV and Excel (.xlsx) formats
- Backend logic was NOT modified as per requirements
- Frontend completely rebuilt with professional UI

## 🌐 Deployment

For deployment (e.g., Railway):
1. Update `REACT_APP_BACKEND_URL` in frontend/.env to production URL
2. Build frontend: `cd frontend && yarn build`
3. Serve backend on port 5000
4. Serve frontend build files
5. Ensure CORS is properly configured

## 👨‍💻 Development

**Start Backend**:
```bash
cd /app/backend
python app.py
```

**Start Frontend**:
```bash
cd /app/frontend
yarn start
```

Access application at: http://localhost:3000
Backend API at: http://localhost:5000

---

**Built with ❤️ using Flask + React + AI**
