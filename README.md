# ☕ Sales Trend & Time-Based Performance Analysis
### Afficionado Coffee Roasters · 2025

![Python](https://img.shields.io/badge/Python-3.10+-blue)
![Streamlit](https://img.shields.io/badge/Streamlit-1.35+-red)
![Plotly](https://img.shields.io/badge/Plotly-5.x-purple)
![License](https://img.shields.io/badge/License-MIT-green)

A complete sales analytics dashboard and research project analyzing **when** customers buy at Afficionado Coffee Roasters — across hours, days, and store locations — to drive data-informed staffing and operational decisions.

---

## 🚀 Live Demo

👉 [View Deployed App on Streamlit Cloud](https://your-app.streamlit.app)

---

## 📋 Project Overview

| Item | Detail |
|---|---|
| Domain | Retail Analytics / Specialty Coffee |
| Data Period | January – June 2025 |
| Stores | Hell's Kitchen · Astoria · Lower Manhattan |
| Records | 12,000+ transactions |
| Stack | Python · Streamlit · Plotly · Pandas · NumPy |

---

## 📁 Project Structure

```
afficionado-coffee-analysis/
│
├── app.py                  # Main Streamlit dashboard
├── research_paper.md       # Full research paper
├── requirements.txt        # Python dependencies
└── README.md               # This file
```

---

## 🔧 Setup & Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/YOUR_USERNAME/afficionado-coffee-analysis.git
cd afficionado-coffee-analysis

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

---

## 📊 Dashboard Features

- **KPI Cards** – Total revenue, transactions, avg order value, peak hour, busiest day
- **Sales Trend** – Daily revenue with 7-day rolling average
- **Day-of-Week Analysis** – Bar charts and weekday vs weekend pie
- **Hourly Demand** – Histogram of transactions by hour + time bucket breakdown
- **Heatmap** – Hour × Day demand intensity per store
- **Location Comparison** – Hourly lines and grouped bars across 3 stores
- **Product Mix** – Revenue by category and top products

### Filters
- Store Location selector
- Day of Week multi-select
- Hour Range slider
- Revenue vs Transaction Count toggle

---

## 🔑 Key Findings

1. **38% of all transactions occur between 7–10 AM** — morning rush is critical
2. **Friday is the highest-revenue day** across all locations
3. **Hell's Kitchen peaks sharply at 8 AM**; Lower Manhattan peaks midday
4. **Astoria has the most balanced demand** — residential community behavior
5. **Coffee accounts for 50%+ of revenue**; bakery drives morning attachment purchases

---

## 💡 Recommendations

- Staff 2x during 7–10 AM across all locations
- Location-specific schedules (not one-size-fits-all)
- Sunday promotions to boost slow-day revenue
- Cold brew + bakery bundles for the 2–4 PM afternoon window

---

## 📄 Research Paper

Full analysis, methodology, and recommendations available in [`research_paper.md`](./research_paper.md)

---

## 👤 Author

**S. Prithivirajan**  
Sales Analytics Project · 2025

---

*Built with ❤️ and ☕*
