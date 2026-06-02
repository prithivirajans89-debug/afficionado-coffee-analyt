import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ── Page config ──────────────────────────────────────────────────────────────
st.set_page_config(
    page_title="Afficionado Coffee Roasters – Sales Analytics",
    page_icon="☕",
    layout="wide",
)

# ── Custom CSS ────────────────────────────────────────────────────────────────
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=DM+Sans:wght@300;400;500&display=swap');

html, body, [class*="css"] {
    font-family: 'DM Sans', sans-serif;
    background-color: #1a1008;
    color: #f0e6d3;
}
.stApp { background-color: #1a1008; }

h1, h2, h3 {
    font-family: 'Playfair Display', serif;
    color: #d4a96a;
}

.metric-card {
    background: linear-gradient(135deg, #2c1a0e 0%, #3d2412 100%);
    border: 1px solid #5c3d1e;
    border-radius: 12px;
    padding: 1.2rem 1.5rem;
    text-align: center;
}
.metric-label {
    font-size: 0.78rem;
    letter-spacing: 0.12em;
    text-transform: uppercase;
    color: #a07850;
    margin-bottom: 0.3rem;
}
.metric-value {
    font-family: 'Playfair Display', serif;
    font-size: 2rem;
    color: #d4a96a;
    font-weight: 700;
}
.metric-delta {
    font-size: 0.8rem;
    color: #80c080;
}

.section-header {
    font-family: 'Playfair Display', serif;
    font-size: 1.3rem;
    color: #d4a96a;
    border-bottom: 1px solid #3d2412;
    padding-bottom: 0.4rem;
    margin-bottom: 1rem;
}

[data-testid="stSidebar"] {
    background-color: #120c05 !important;
    border-right: 1px solid #3d2412;
}
[data-testid="stSidebar"] * { color: #c8b090 !important; }

div[data-testid="metric-container"] {
    background: #2c1a0e;
    border: 1px solid #5c3d1e;
    border-radius: 10px;
    padding: 1rem;
}
</style>
""", unsafe_allow_html=True)

# ── Load Data ─────────────────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_csv("afficionado_coffee_sales.csv")
    df["transaction_date"] = pd.to_datetime(df["transaction_date"])
    df["transaction_time"] = pd.to_datetime(df["transaction_time"], format="%H:%M:%S").dt.time
    df["revenue"] = df["transaction_qty"] * df["unit_price"]
    df["hour"] = df["transaction_time"].apply(lambda t: t.hour)
    df["day_of_week"] = df["transaction_date"].dt.day_name()
    df["day_num"] = df["transaction_date"].dt.dayofweek
    df["week"] = df["transaction_date"].dt.isocalendar().week.astype(int)
    df["month"] = df["transaction_date"].dt.month_name()
    df["month_num"] = df["transaction_date"].dt.month
    df["time_bucket"] = pd.cut(
        df["hour"],
        bins=[-1, 5, 11, 16, 21, 23],
        labels=["Late Night (22–5)", "Morning (6–11)", "Afternoon (12–16)", "Evening (17–21)", "Night (22+)"]
    )
    return df

df = load_data()
DAY_ORDER = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
COLORS = {"Astoria": "#d4a96a", "Hell's Kitchen": "#e07b54", "Lower Manhattan": "#7ab8c0"}
PLOTLY_TEMPLATE = "plotly_dark"
CHART_BG = "#1e1208"
PAPER_BG = "#1a1008"

# ── Sidebar Filters ───────────────────────────────────────────────────────────
st.sidebar.markdown("## ☕ Filters")

all_locations = sorted(df["store_location"].unique().tolist())
selected_locations = st.sidebar.multiselect(
    "Store Location", all_locations, default=all_locations
)

all_days = DAY_ORDER
selected_days = st.sidebar.multiselect(
    "Day of Week", all_days, default=all_days
)

hour_range = st.sidebar.slider("Hour Range", 0, 23, (0, 23))

metric_toggle = st.sidebar.radio("Primary Metric", ["Revenue ($)", "Transaction Count"])
use_revenue = metric_toggle == "Revenue ($)"
metric_col = "revenue" if use_revenue else "transaction_id"
metric_label = "Revenue ($)" if use_revenue else "Transactions"
agg_func = "sum" if use_revenue else "count"

# ── Filter Data ───────────────────────────────────────────────────────────────
filtered = df[
    df["store_location"].isin(selected_locations) &
    df["day_of_week"].isin(selected_days) &
    df["hour"].between(hour_range[0], hour_range[1])
].copy()

# ── Header ────────────────────────────────────────────────────────────────────
st.markdown("<h1>☕ Afficionado Coffee Roasters</h1>", unsafe_allow_html=True)
st.markdown("<p style='color:#a07850;letter-spacing:0.1em;'>SALES TREND & TIME-BASED PERFORMANCE ANALYTICS · 2025</p>", unsafe_allow_html=True)
st.markdown("---")

# ── KPI Row ───────────────────────────────────────────────────────────────────
k1, k2, k3, k4, k5 = st.columns(5)
total_rev = filtered["revenue"].sum()
total_txn = len(filtered)
avg_order = filtered["revenue"].mean()
peak_hour = filtered.groupby("hour")["transaction_id"].count().idxmax()
best_day = filtered.groupby("day_of_week")["revenue"].sum().idxmax() if not filtered.empty else "N/A"

with k1:
    st.metric("Total Revenue", f"${total_rev:,.0f}")
with k2:
    st.metric("Total Transactions", f"{total_txn:,}")
with k3:
    st.metric("Avg Order Value", f"${avg_order:.2f}")
with k4:
    st.metric("Peak Hour", f"{peak_hour}:00")
with k5:
    st.metric("Best Day", best_day)

st.markdown("---")

# ── Tab Layout ────────────────────────────────────────────────────────────────
tab1, tab2, tab3, tab4 = st.tabs(["📈 Sales Trends", "📅 Day-of-Week", "⏰ Hourly Demand", "🏪 Location Comparison"])

# ════════════════════════════════════════════════════════════════════════════════
# TAB 1 – SALES TRENDS
# ════════════════════════════════════════════════════════════════════════════════
with tab1:
    st.markdown('<div class="section-header">Daily Revenue Trend</div>', unsafe_allow_html=True)

    daily = (
        filtered.groupby(["transaction_date", "store_location"])["revenue"]
        .sum().reset_index()
    )
    daily_total = filtered.groupby("transaction_date")["revenue"].sum().reset_index()
    daily_total["rolling7"] = daily_total["revenue"].rolling(7).mean()

    fig_daily = go.Figure()
    fig_daily.add_trace(go.Scatter(
        x=daily_total["transaction_date"], y=daily_total["revenue"],
        mode="lines", name="Daily Revenue",
        line=dict(color="#5c3d1e", width=1),
        fill="tozeroy", fillcolor="rgba(92,61,30,0.2)"
    ))
    fig_daily.add_trace(go.Scatter(
        x=daily_total["transaction_date"], y=daily_total["rolling7"],
        mode="lines", name="7-Day Avg",
        line=dict(color="#d4a96a", width=2.5)
    ))
    fig_daily.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        legend=dict(font=dict(color="#c8b090")),
        xaxis=dict(title="Date", gridcolor="#2c1a0e"),
        yaxis=dict(title="Revenue ($)", gridcolor="#2c1a0e"),
        height=380, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_daily, use_container_width=True)

    st.markdown('<div class="section-header">Monthly Revenue Breakdown by Store</div>', unsafe_allow_html=True)
    monthly = (
        filtered.groupby(["month_num", "month", "store_location"])["revenue"]
        .sum().reset_index().sort_values("month_num")
    )
    fig_monthly = px.bar(
        monthly, x="month", y="revenue", color="store_location",
        barmode="group", color_discrete_map=COLORS,
        labels={"revenue": "Revenue ($)", "month": "Month", "store_location": "Store"}
    )
    fig_monthly.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        height=350, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_monthly, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 2 – DAY OF WEEK
# ════════════════════════════════════════════════════════════════════════════════
with tab2:
    col_a, col_b = st.columns(2)

    with col_a:
        st.markdown('<div class="section-header">Average Revenue by Day</div>', unsafe_allow_html=True)
        dow_rev = (
            filtered.groupby("day_of_week")["revenue"].mean().reindex(DAY_ORDER).reset_index()
        )
        fig_dow = px.bar(
            dow_rev, x="day_of_week", y="revenue",
            color="revenue", color_continuous_scale=["#3d2412", "#d4a96a"],
            labels={"revenue": "Avg Revenue ($)", "day_of_week": "Day"}
        )
        fig_dow.update_layout(
            template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
            coloraxis_showscale=False, height=350, margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_dow, use_container_width=True)

    with col_b:
        st.markdown('<div class="section-header">Avg Transaction Count by Day</div>', unsafe_allow_html=True)
        dow_txn = (
            filtered.groupby(["transaction_date", "day_of_week"])["transaction_id"]
            .count().reset_index()
            .groupby("day_of_week")["transaction_id"].mean()
            .reindex(DAY_ORDER).reset_index()
        )
        fig_txn = px.bar(
            dow_txn, x="day_of_week", y="transaction_id",
            color="transaction_id", color_continuous_scale=["#3d2412", "#e07b54"],
            labels={"transaction_id": "Avg Transactions", "day_of_week": "Day"}
        )
        fig_txn.update_layout(
            template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
            coloraxis_showscale=False, height=350, margin=dict(t=20, b=20)
        )
        st.plotly_chart(fig_txn, use_container_width=True)

    st.markdown('<div class="section-header">Weekday vs Weekend Comparison</div>', unsafe_allow_html=True)
    filtered["week_type"] = filtered["day_of_week"].apply(
        lambda d: "Weekend" if d in ["Saturday", "Sunday"] else "Weekday"
    )
    wknd = filtered.groupby("week_type").agg(
        avg_revenue=("revenue", "mean"),
        total_revenue=("revenue", "sum"),
        avg_transactions=("transaction_id", "count")
    ).reset_index()
    fig_wk = px.bar(
        wknd, x="week_type", y="avg_revenue",
        color="week_type", color_discrete_map={"Weekday": "#d4a96a", "Weekend": "#e07b54"},
        labels={"avg_revenue": "Avg Revenue per Transaction ($)", "week_type": ""},
        text_auto=".2f"
    )
    fig_wk.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        showlegend=False, height=320, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_wk, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 3 – HOURLY DEMAND
# ════════════════════════════════════════════════════════════════════════════════
with tab3:
    st.markdown('<div class="section-header">Hourly Transaction Volume</div>', unsafe_allow_html=True)
    hourly = filtered.groupby("hour").agg(
        transactions=("transaction_id", "count"),
        revenue=("revenue", "sum")
    ).reset_index()

    fig_hour = make_subplots(specs=[[{"secondary_y": True}]])
    fig_hour.add_trace(go.Bar(
        x=hourly["hour"], y=hourly["transactions"],
        name="Transactions", marker_color="#5c3d1e", opacity=0.8
    ), secondary_y=False)
    fig_hour.add_trace(go.Scatter(
        x=hourly["hour"], y=hourly["revenue"],
        name="Revenue ($)", mode="lines+markers",
        line=dict(color="#d4a96a", width=2.5),
        marker=dict(size=7)
    ), secondary_y=True)
    fig_hour.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        height=380, margin=dict(t=20, b=20),
        xaxis=dict(title="Hour of Day", dtick=1, gridcolor="#2c1a0e"),
    )
    fig_hour.update_yaxes(title_text="Transactions", secondary_y=False, gridcolor="#2c1a0e")
    fig_hour.update_yaxes(title_text="Revenue ($)", secondary_y=True, gridcolor="#2c1a0e")
    st.plotly_chart(fig_hour, use_container_width=True)

    st.markdown('<div class="section-header">Time Bucket Distribution</div>', unsafe_allow_html=True)
    bucket_order = ["Morning (6–11)", "Afternoon (12–16)", "Evening (17–21)", "Night (22+)", "Late Night (22–5)"]
    bucket = filtered.groupby("time_bucket").agg(
        revenue=("revenue", "sum"),
        transactions=("transaction_id", "count")
    ).reset_index()
    fig_bucket = px.pie(
        bucket, values="revenue", names="time_bucket",
        color_discrete_sequence=["#d4a96a", "#e07b54", "#7ab8c0", "#5c3d1e", "#a07850"],
        hole=0.45
    )
    fig_bucket.update_layout(
        template=PLOTLY_TEMPLATE, paper_bgcolor=PAPER_BG,
        height=350, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_bucket, use_container_width=True)

# ════════════════════════════════════════════════════════════════════════════════
# TAB 4 – LOCATION COMPARISON
# ════════════════════════════════════════════════════════════════════════════════
with tab4:
    st.markdown('<div class="section-header">Hourly Heatmap by Store</div>', unsafe_allow_html=True)

    for loc in selected_locations:
        loc_df = filtered[filtered["store_location"] == loc]
        heat = loc_df.groupby(["day_of_week", "hour"])["revenue"].sum().reset_index()
        heat_pivot = heat.pivot(index="day_of_week", columns="hour", values="revenue").reindex(DAY_ORDER).fillna(0)

        fig_heat = px.imshow(
            heat_pivot,
            labels=dict(x="Hour", y="Day", color="Revenue ($)"),
            color_continuous_scale=["#1a1008", "#5c3d1e", "#d4a96a"],
            aspect="auto",
            title=f"{loc}"
        )
        fig_heat.update_layout(
            template=PLOTLY_TEMPLATE, paper_bgcolor=PAPER_BG,
            height=300, margin=dict(t=40, b=20),
            title_font=dict(family="Playfair Display", color="#d4a96a", size=16)
        )
        st.plotly_chart(fig_heat, use_container_width=True)

    st.markdown('<div class="section-header">Store Revenue Comparison Over Time</div>', unsafe_allow_html=True)
    loc_weekly = (
        filtered.groupby(["week", "store_location"])["revenue"]
        .sum().reset_index()
    )
    fig_loc = px.line(
        loc_weekly, x="week", y="revenue", color="store_location",
        color_discrete_map=COLORS,
        labels={"revenue": "Weekly Revenue ($)", "week": "Week Number", "store_location": "Store"}
    )
    fig_loc.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        height=370, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_loc, use_container_width=True)

    st.markdown('<div class="section-header">Product Category Revenue by Store</div>', unsafe_allow_html=True)
    cat_loc = (
        filtered.groupby(["store_location", "product_category"])["revenue"]
        .sum().reset_index()
    )
    fig_cat = px.bar(
        cat_loc, x="product_category", y="revenue", color="store_location",
        barmode="group", color_discrete_map=COLORS,
        labels={"revenue": "Revenue ($)", "product_category": "Category", "store_location": "Store"}
    )
    fig_cat.update_layout(
        template=PLOTLY_TEMPLATE, plot_bgcolor=CHART_BG, paper_bgcolor=PAPER_BG,
        height=350, margin=dict(t=20, b=20)
    )
    st.plotly_chart(fig_cat, use_container_width=True)

# ── Footer ────────────────────────────────────────────────────────────────────
st.markdown("---")
st.markdown(
    "<p style='color:#5c3d1e;font-size:0.75rem;text-align:center;'>"
    "Afficionado Coffee Roasters · Sales Analytics Dashboard · 2025 · Built with Streamlit</p>",
    unsafe_allow_html=True
)
