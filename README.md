# UPTAC College Predictor

A comprehensive web application for predicting college admissions based on UPTAC 2024 data. This tool helps students find suitable colleges and programs based on their rank, category, quota, and other preferences.
The application is currently deployed and accessible at: https://uptac.onrender.com/

## 🚀 Features

- **Smart College Prediction**: Find colleges based on your UPTAC rank and category
- **Advanced Filtering**: Filter by institute, program, quota, category, and counseling round
- **Multiple Data Views**: 
  - Institute-wise distribution sorted by closing rank
  - Program-wise distribution sorted by closing rank
  - Average Package Data (Gemini 2.5 Pro)
- **Interactive Web Interface**: Modern Material Design 3 inspired UI
- **API Support**: RESTful API for programmatic access
- **Responsive Design**: Works seamlessly on desktop and mobile devices

## 📦 Installation

### Prerequisites

- Python 3.7+
- pip package manager

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/git-divy/uptac.git
   cd uptac
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Run the application**
   ```bash
   python app.py
   ```

4. **Access the application**
   - Open your browser and navigate to `http://localhost:5000`

## 🔧 Configuration

### Data Format

The application expects data in the following JSON format:
```json
[
  {
    "round": 1,
    "institute": "Institute Name",
    "program": "Program Name",
    "quota": "Quota Type",
    "category": "Category",
    "cr": 1234
  }
]
```

## 📊 API Reference

### Get Filtered Data

**POST** `/api/data`

**Request Body:**
```json
{
  "max_results": 25,
  "page": 1,
  "rank": 5000,
  "round": [1, 2],
  "institute": ["Institute Name"],
  "program": ["Program Name"],
  "quota": ["Quota Type"],
  "category": ["Category"]
}
```

**Response:**
```json
{
  "meta_data": {
    "total_results": 150,
    "max_results": 25,
    "current_page": 1,
    "total_pages": 6
  },
  "results": "Formatted table data..."
}
```

### Get Available Filters

**GET** `/api/filters`

**Response:**
```json
{
  "round": [1, 2, 3],
  "institute": ["Institute 1", "Institute 2"],
  "program": ["Program 1", "Program 2"],
  "quota": ["General", "OBC"],
  "category": ["Open", "EWS"]
}
```

## 🌐 Deployment

### Using Gunicorn

```bash
gunicorn -w 4 -b 0.0.0.0:8000 app:app
```

## 📁 Project Structure

```
uptac/
├── app.py                 # Main Flask application
├── analysis.py           # Institute-wise analysis generator
├── analysis_2.py         # Program-wise analysis generator
├── tabulator.py          # Table formatting utility
├── aliver.py             # Keep-alive functionality
├── requirements.txt      # Python dependencies
├── dat_2024.json        # UPTAC 2024 data
├── templates/
│   └── index.html       # Main web interface
├── res/                 # Generated institute-wise reports
└── res2/                # Generated program-wise reports
```

## 🔍 Usage Examples

### Web Interface

1. **Basic Search**: Enter your rank and click "SEARCH"
2. **Advanced Filtering**: Use dropdown menus to filter by specific criteria
3. **Pagination**: Navigate through results using Previous/Next buttons
4. **View Reports**: Access additional resources through the provided links

### API Usage

```python
import requests

# Get filtered data
response = requests.post('http://localhost:5000/api/data', json={
    'rank': 5000,
    'category': ['Open'],
    'max_results': 10
})

data = response.json()
print(data['results'])
```

## 📋 Features in Detail

### College Prediction Algorithm
- Filters colleges based on closing rank (CR) being higher than your rank
- Sorts results by closing rank for better decision making
- Supports multiple category and quota combinations

### Data Analysis
- **Institute-wise Analysis**: Groups programs by institute for easy comparison
- **Program-wise Analysis**: Shows all programs sorted by closing rank
- **Round-wise Data**: Includes information about counseling rounds

### User Interface
- **Material Design 3**: Modern, accessible design system
- **Responsive Layout**: Optimized for all screen sizes
- **Dark Mode Support**: Automatic dark mode based on system preference


## ⚠️ Disclaimer

This tool provides predictions based on historical data (UPTAC 2024). Actual admission results may vary based on various factors including:
- Changes in seat matrix
- Variation in student preferences
- Policy changes by the admission authority

Always refer to official UPTAC/AKTU sources for final admission decisions.

## 📞 Support

- **Data Source**: [Official UPTAC Reports](https://admissions.nic.in/UPTAC/applicant/report/orcrreport.aspx?enc=yVQCIiq12npg+pcvNJRdcww8ijHE0M3JICo+UehfedimJjvXET+LsPwN9AEcJEnE)
- **Issues**: Please report bugs and feature requests through GitHub Issues

## 🏷️ Version

Current Version: **v1.3.1**

---

Made with ❤️ for UPTAC/AKTU students
