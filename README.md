# 🏏 Flames Cricket Dashboard

A comprehensive cricket analytics dashboard for Flames CC, featuring detailed match analysis, player statistics, and fielding insights.

## 📊 Features

- **Match Analysis**: Comprehensive match-by-match breakdown
- **Player Statistics**: Batting, bowling, and fielding performance tracking
- **Performance Trends**: Visual analytics of team and individual performance
- **AI-Powered Insights**: Intelligent analysis and recommendations
- **Responsive Design**: Works seamlessly across all devices

## 🗂️ Project Structure

```
Cricket Dashboard/
├── advanced_dashboard.html      # Main dashboard interface
├── advanced_script.js           # Dashboard JavaScript logic
├── advanced_styles.css          # Dashboard styling
├── extract_format1_with_fielding.py  # Data extractor for Format 1 PDFs
├── requirements.txt             # Python dependencies
├── README.md                    # Project documentation
└── Flames/                      # Data directory
    ├── Stats - FLAMES CC - v2.xlsx  # Excel statistics file
    ├── Old Data/                # 37 match scorecards (2020-2022)
    └── New Data/                # 100 match scorecards (2023-2024)
```

## 📋 Data Sources

- **Total Matches**: 137 PDF scorecards
- **Old Data**: 37 matches from 2020-2022
- **New Data**: 100 matches from 2023-2024
- **Excel File**: Historical player statistics

## 🔧 Data Extraction

### PDF Format Types

We have identified 3 distinct PDF formats:

1. **Format 1 - Full Scorecard** (1 PDF)
   - Complete batting/bowling statistics
   - Detailed player performance
   - Fielding analysis (catches, stumpings, run-outs)
   - Example: `08 - 27-Feb-21 - Sledgers VS Flames.pdf`

2. **Format 2 - AllStar Championship** (36 PDFs)
   - Tournament-style scorecards
   - Best performances section
   - Match officials data
   - Example: `13 - 26-Sep-21 - CLASSIC XI KARACHI VS Flames.pdf`

3. **Format 3 - CricHeroes** (100 PDFs)
   - Digital platform generated scorecards
   - Modern format with detailed stats
   - Example: `Scorecard_10640768.pdf`

### Extractor Features

The `extract_format1_with_fielding.py` script extracts:

- **Match Information**: Date, opponent, venue, series, result
- **Batting Stats**: Runs, balls, 4s, 6s, strike rate, dismissal info
- **Bowling Stats**: Overs, runs, wickets, maidens, economy
- **Fielding Stats**: Catches, stumpings, run-outs per player

## 🚀 Setup

### Prerequisites

```bash
pip install -r requirements.txt
```

### Running the Dashboard

Simply open `advanced_dashboard.html` in a web browser.

### Extracting Data

```bash
python extract_format1_with_fielding.py
```

## 📈 Dashboard Features

### Overview Tab
- Total matches, wins, losses, draws
- Win percentage
- Recent form
- Key statistics

### Matches Tab
- Complete match list
- Scores and results
- Filter by date, opponent, result

### Players Tab
- Individual player statistics
- Top performers
- Career averages

### Trends Tab
- Performance graphs
- Win/loss trends
- Scoring patterns

### AI Insights Tab
- Automated analysis
- Strengths and weaknesses
- Recommendations

## 🎯 Roadmap

- [x] Identify PDF formats
- [x] Create Format 1 extractor with fielding analysis
- [ ] Create Format 2 extractor (AllStar Championship)
- [ ] Create Format 3 extractor (CricHeroes)
- [ ] Consolidate all data into single database
- [ ] Update dashboard with real data
- [ ] Deploy to GitHub Pages

## 📝 License

This project is created for Flames CC team analysis.

## 👥 Contributors

Developed for Flames Cricket Club
