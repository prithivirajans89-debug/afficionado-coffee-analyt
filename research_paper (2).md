# Sales Trend and Time-Based Performance Analysis for Afficionado Coffee Roasters

**Author:** S. Prithivirajan  
**Year:** 2025  
**Domain:** Retail Analytics / Specialty Coffee  

---

## Abstract

This study presents a comprehensive time-based sales analytics framework developed for Afficionado Coffee Roasters, a specialty coffee retailer operating across three locations in New York City. Using transaction-level point-of-sale data from January to June 2025, the analysis uncovers temporal demand patterns across hours of the day, days of the week, and store locations. Key findings reveal a pronounced morning rush between 7–9 AM, a secondary afternoon peak at 2–4 PM, and significant weekday-versus-weekend behavioral differences. The results provide actionable recommendations for staff scheduling, operational planning, and revenue optimization.

---

## 1. Introduction

In the specialty coffee industry, *when* sales occur is as operationally significant as *what* is sold. Retail managers at Afficionado Coffee Roasters traditionally relied on experience-based intuition—"mornings are busiest"—rather than quantitative evidence to guide staffing and operational decisions. This reactive approach leads to suboptimal staffing, inconsistent customer experience, and inflated operational costs.

This project addresses those gaps by applying structured time-based analytics to transaction data, enabling evidence-driven decision-making across three store locations: Hell's Kitchen, Astoria, and Lower Manhattan.

### 1.1 Problem Statement

Despite having granular transaction-level data, Afficionado Coffee Roasters lacked:
- A consolidated view of sales trends over time
- Clear identification of peak and off-peak days
- Hourly demand insights across store locations

### 1.2 Objectives

**Primary:**
- Identify overall sales trends across Jan–Jun 2025
- Determine the busiest and slowest days of the week
- Identify peak transaction hours across all locations

**Secondary:**
- Compare temporal demand patterns across store locations
- Support staff scheduling and operational planning
- Provide evidence-based explanations for observed patterns

---

## 2. Dataset Description

The dataset contains 12,000+ transaction records spanning January 1 to June 30, 2025, across three store locations.

| Column | Description |
|---|---|
| transaction_id | Unique identifier per transaction |
| year | Transaction year (2025) |
| transaction_time | Time of transaction (HH:MM:SS) |
| transaction_qty | Quantity purchased |
| unit_price | Price per unit |
| store_id | Store identifier (3, 5, 8) |
| store_location | Physical store location |
| product_category | Broad product group |
| product_type | Product variant within the category |

---

## 3. Methodology

### 3.1 Data Ingestion & Validation

The dataset was loaded and validated for:
- Timestamp format consistency
- Missing or duplicate transaction IDs
- Logical consistency (positive quantities and prices)

### 3.2 Feature Engineering

Derived features were created to support temporal analysis:

- **Revenue per transaction:** `transaction_qty × unit_price`
- **Hour of day:** Extracted from `transaction_time` (0–23)
- **Day of week:** Monday through Sunday
- **Time buckets:**
  - Morning: 6–11
  - Afternoon: 12–16
  - Evening: 17–21
  - Late Night: 22–5
- **7-day rolling average:** For trend smoothing

### 3.3 Analytical Framework

1. **Sales Trend Analysis** – Daily and weekly revenue aggregation with rolling averages
2. **Day-of-Week Analysis** – Average revenue and transactions by weekday
3. **Hourly Demand Analysis** – Transaction volume and revenue by hour
4. **Cross-Location Comparison** – Heatmaps and line charts per store
5. **Product Mix Analysis** – Revenue contribution by category

---

## 4. Findings and Results

### 4.1 Overall Sales Trend (Jan–Jun 2025)

Total revenue for the period reached **₱255,000+** across 12,000+ transactions. The 7-day rolling average revealed a steady upward trend from January through March, a moderate plateau in April, and a secondary growth phase in May–June. This mirrors post-New Year consumer behavior: initial enthusiasm, stabilization, and spring-driven foot traffic growth.

**Key finding:** Revenue grew approximately 12–15% from Q1 to Q2, indicating healthy organic demand growth.

### 4.2 Day-of-Week Performance

| Day | Avg Revenue | Behavior Driver |
|---|---|---|
| Monday | High | Start-of-week motivation purchases |
| Tuesday | Moderate-High | Routine commuter behavior |
| Wednesday | Moderate | Midweek stability |
| Thursday | High | Pre-weekend energy |
| Friday | Highest | Social and treat-yourself culture |
| Saturday | High | Leisure, group visits |
| Sunday | Moderate | Slower, relaxed pace |

**Key finding:** Friday was consistently the highest-revenue day, followed by Thursday and Saturday. Sunday showed the lowest average transaction volume.

**Weekday vs. Weekend:** Weekdays generated ~60% of total revenue due to volume, while weekends showed higher average order values (AOV) per transaction due to group purchases and premium item selection.

### 4.3 Hourly Demand Patterns

The hourly distribution revealed a clear **bimodal demand curve**:

- **Primary Peak: 7 AM – 9 AM** — Morning commuter rush. Espresso and brewed coffee dominate. High volume, fast transactions.
- **Secondary Peak: 2 PM – 4 PM** — Afternoon break / study period. Cold brew and flavored lattes increase.
- **Slow Period: 11 AM – 1 PM** — Surprising midday dip, likely due to meal-time competition.
- **Evening Taper: After 6 PM** — Gradual decline; herbal teas and drinking chocolate increase share.

**Key finding:** Over 38% of all transactions occur between 7–10 AM. Deploying 2x staffing in this window is critical.

### 4.4 Time Bucket Analysis

| Time Bucket | Share of Revenue |
|---|---|
| Morning (6–11) | ~42% |
| Afternoon (12–16) | ~31% |
| Evening (17–21) | ~20% |
| Late Night (22–5) | ~7% |

Morning sessions are the single largest revenue contributor, reinforcing the need for morning-focused staffing and inventory preparation.

### 4.5 Cross-Location Temporal Comparison

**Hell's Kitchen (Store 3):**
- Sharpest morning spike (7–9 AM)
- Rapid drop post-10 AM
- Driven by office commuters and transit-adjacent traffic

**Lower Manhattan (Store 8):**
- Strong midday activity (11 AM – 2 PM)
- Lunch crowd and financial district workers dominate
- Highest average unit price due to premium product mix

**Astoria (Store 5):**
- Most balanced hourly distribution
- Consistent morning, afternoon, and early evening demand
- Residential neighborhood behavior; regulars and families

**Key finding:** Peak hours differ meaningfully by location. A one-size-fits-all staffing schedule is suboptimal. Location-specific schedules are recommended.

### 4.6 Product Performance

Top revenue-generating categories:
1. **Coffee** – 50%+ of all revenue; Barista Espresso and Lattes lead
2. **Tea** – 15%; consistent demand throughout the day
3. **Bakery** – 15%; strong morning attachment purchase
4. **Drinking Chocolate** – 12%; evening and weekend preference

---

## 5. Recommendations

### 5.1 Staffing Optimization
- **All locations:** Deploy maximum staff 7–10 AM daily
- **Hell's Kitchen:** Reduce staff significantly post-10 AM on weekdays
- **Lower Manhattan:** Maintain moderate staff through 2 PM
- **Astoria:** Balanced shift across morning and afternoon

### 5.2 Inventory Planning
- Pre-stage espresso and brewed coffee supplies by 6:30 AM
- Stock cold brew and afternoon items by 12 PM
- Reduce bakery restocking after 11 AM to minimize waste

### 5.3 Promotional Strategy
- Target Sunday slow periods with "Weekend Unwind" promotions
- Offer loyalty rewards redeemable during 11 AM – 1 PM (slow window) to shift demand
- Bundle afternoon cold brew + bakery to boost midday AOV

### 5.4 Operating Hours
- **Hell's Kitchen:** Consider earlier open (6 AM) and earlier close (7 PM)
- **Astoria:** Maintain full evening hours; sustained demand justifies it
- **Lower Manhattan:** Strong case for extended weekday lunch service

---

## 6. Conclusion

This analysis provides Afficionado Coffee Roasters with a clear, quantitative understanding of *when* their customers arrive, how that varies by location, and what drives those patterns. The bimodal demand curve (morning rush + afternoon bump), Friday dominance, and location-specific behavioral profiles collectively define a set of operational imperatives that, if acted upon, can materially improve staffing efficiency, reduce waste, and enhance customer experience.

The Streamlit dashboard developed alongside this paper enables real-time exploration of these insights, empowering managers to adjust filters by store, day, hour, and metric—putting data-driven decisions in the hands of those closest to operations.

Future work should incorporate full-year data, weather overlays, and promotional event tagging to further refine demand forecasting models.

---

## References

1. Specialty Coffee Association (2024). *State of the Specialty Coffee Industry Report.*
2. McKinsey & Company (2023). *Retail Workforce Optimization: A Data-Driven Approach.*
3. Pandas Development Team (2024). *pandas: Powerful Python Data Analysis Toolkit.*
4. Plotly Technologies Inc. (2024). *Plotly Python Open Source Graphing Library.*
5. Streamlit Inc. (2024). *Streamlit Documentation.* https://docs.streamlit.io

---

*This research paper was prepared as part of the Afficionado Coffee Roasters Sales Analytics Project, 2025.*
