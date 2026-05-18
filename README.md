# 📊 Insta Flow — AI-Assisted Business Analytics Dashboard

A professional, lightweight SaaS-style analytics platform for CSV datasets with constrained Gemini AI insights.

## Features

- **CSV Upload & Validation** — Auto-detects date, numeric, and categorical columns
- **Interactive Dashboards** — 9 chart types with instant switching (Bar, Line, Area, Pie, Donut, Scatter, Stacked Bar, Histogram, Heatmap)
- **KPI Cards** — Dynamic metrics with growth indicators
- **Date Range Filtering** — Current Week, Month, Last 6 Months, All Time, Custom Range
- **Gemini AI Integration** — Context-constrained analytics assistant (not a general chatbot)
- **PDF Reports** — Professional executive-style reports with All-Time analysis
- **Session State** — Persistent dashboard interactions during active session

## Tech Stack

| Component        | Technology              |
|-----------------|------------------------|
| Frontend/UI     | Streamlit              |
| Data Processing | Pandas, NumPy          |
| Visualization   | Plotly                 |
| AI Integration  | Gemini API             |
| PDF Generation  | ReportLab              |
| State Mgmt      | Streamlit Session State |

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Run the application
streamlit run app.py
```

## Project Structure

```
InstaFlow-v1/
├── app.py                 # Main Streamlit application
├── data_processor.py      # CSV validation & metadata extraction
├── analytics_engine.py    # KPI calculations & trend analysis
├── chart_builder.py       # Plotly chart factory (9 chart types)
├── gemini_handler.py      # Context-constrained Gemini AI handler
├── pdf_generator.py       # ReportLab PDF report generator
├── styles.py              # Custom CSS design system
├── sample_data.csv        # Sample business dataset for testing
└── requirements.txt       # Python dependencies
```

## Usage

1. **Connect Gemini API** — Enter your own API key in the sidebar (never stored permanently)
2. **Upload CSV** — Upload any structured business dataset
3. **Explore Dashboard** — View KPIs, switch charts, filter by date range
4. **Ask Your Data** — Ask constrained analytics questions via AI
5. **Export Report** — Download a professional PDF report

## AI Constraints

The AI assistant **only** answers questions about:
- Uploaded dataset metrics, trends, and KPIs
- Business analytics within the dataset scope

It will **reject** unrelated questions (sports, weather, politics, general knowledge, etc.)

## Sample Dataset

A `sample_data.csv` is included with columns: Date, Product, Region, Category, Sales, Revenue, Profit, Quantity, Loss spanning January–December 2024.

---

> **Disclaimer:** Users are responsible for monitoring usage associated with their own Gemini API credentials.