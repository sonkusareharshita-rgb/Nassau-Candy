import streamlit as st
import pandas as pd
from pathlib import Path

# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Nassau Candy Factory Optimization",
    page_icon="🍫",
    layout="wide"
)

# =========================================================
# THEME
# =========================================================

st.markdown("""
<style>

.stApp {
    background-color: #f8f5f2;
}

.block-container {
    padding-top: 2rem;
    padding-bottom: 2rem;
}

.hero {
    background: linear-gradient(135deg, #3b1f16, #7a452f);
    padding: 30px;
    border-radius: 18px;
    color: white;
    margin-bottom: 25px;
}

.hero h1 {
    font-size: 36px;
    font-weight: 800;
    margin: 0;
}

.hero p {
    font-size: 16px;
    margin-top: 8px;
    opacity: 0.9;
}

.section {
    font-size: 23px;
    font-weight: 800;
    color: #3b2118;
    margin-top: 30px;
    margin-bottom: 15px;
}

.card {
    background: white;
    padding: 20px;
    border-radius: 15px;
    border: 1px solid #eadfd8;
    box-shadow: 0 4px 15px rgba(0,0,0,0.06);
}

.rec-card {
    background: linear-gradient(135deg, #fffaf5, #ffffff);
    border-left: 7px solid #7a452f;
    padding: 25px;
    border-radius: 15px;
    margin-top: 10px;
    box-shadow: 0 5px 18px rgba(0,0,0,0.07);
}

.rec-title {
    font-size: 13px;
    font-weight: 700;
    color: #806f66;
    text-transform: uppercase;
}

.rec-main {
    font-size: 27px;
    font-weight: 800;
    color: #3b2118;
    margin: 7px 0;
}

</style>
""", unsafe_allow_html=True)


# =========================================================
# LOAD DATA
# =========================================================

@st.cache_data
def load_data():

    file_path = Path(__file__).parent / "nassau_final.csv"

    data = pd.read_csv(file_path)

    if "Order Date" in data.columns:
        data["Order Date"] = pd.to_datetime(
            data["Order Date"],
            errors="coerce"
        )

    if "Ship Date" in data.columns:
        data["Ship Date"] = pd.to_datetime(
            data["Ship Date"],
            errors="coerce"
        )

    if "Lead Time" not in data.columns:
        data["Lead Time"] = (
            data["Ship Date"] - data["Order Date"]
        ).dt.days

    return data


# =========================================================
# DATA
# =========================================================

try:
    df = load_data()
except Exception as e:
    st.error("nassau_final.csv load nahi ho rahi.")
    st.code(str(e))
    st.stop()


# =========================================================
# FACTORY MAPPING
# =========================================================

factory_map = {

    "Wonka Bar - Milk Chocolate": "Lot's O' Nuts",
    "Wonka Bar - Triple Dazzle Caramel": "Lot's O' Nuts",
    "Wonka Bar - Nutty Crunch Surprise": "Lot's O' Nuts",
    "Wonka Bar -Scrumdiddlyumptious": "Wicked Choccy's",
    "Wonka Bar - Fudge Mallows": "Wicked Choccy's",
    "Wonka Gum": "Secret Factory",
    "Kazookles": "The Other Factory",
    "Lickable Wallpaper": "Secret Factory",
    "Fizzy Lifting Drinks": "Sugar Shack",
    "Laffy Taffy": "Sugar Shack",
    "SweeTARTS": "Sugar Shack",
    "Nerds": "Sugar Shack",
    "Hair Toffee": "The Other Factory",
    "Everlasting Gobstopper": "Secret Factory",
    "Fun Dip": "Sugar Shack"
}


if "Current Factory" not in df.columns:
    df["Current Factory"] = df["Product Name"].map(factory_map)


# =========================================================
# RECOMMENDATIONS
# =========================================================

recommendations = pd.DataFrame({

    "Product Name": [
        "Everlasting Gobstopper",
        "Fun Dip",
        "Hair Toffee",
        "Wonka Bar - Fudge Mallows",
        "Wonka Bar - Milk Chocolate",
        "Wonka Bar - Nutty Crunch Surprise",
        "Wonka Bar - Triple Dazzle Caramel",
        "Wonka Bar -Scrumdiddlyumptious",
        "Wonka Gum"
    ],

    "Current Factory": [
        "Secret Factory",
        "Sugar Shack",
        "The Other Factory",
        "Wicked Choccy's",
        "Lot's O' Nuts",
        "Lot's O' Nuts",
        "Lot's O' Nuts",
        "Wicked Choccy's",
        "Secret Factory"
    ],

    "Recommended Factory": [
        "Sugar Shack",
        "The Other Factory",
        "Secret Factory",
        "Sugar Shack",
        "The Other Factory",
        "The Other Factory",
        "The Other Factory",
        "The Other Factory",
        "Sugar Shack"
    ],

    "Lead Time Reduction %": [
        13.02,
        5.78,
        10.67,
        8.66,
        2.09,
        3.43,
        4.53,
        2.01,
        7.86
    ]
})


# =========================================================
# HERO
# =========================================================

st.markdown("""
<div class="hero">

<h1>🍫 Nassau Candy Factory Optimization</h1>

<p>
Decision Intelligence Dashboard for Factory Reallocation,
Shipping Efficiency & Lead-Time Optimization
</p>

</div>
""", unsafe_allow_html=True)


# =========================================================
# SIDEBAR
# =========================================================

with st.sidebar:

    st.title("🎛️ Filters")

    products = sorted(
        df["Product Name"].dropna().unique()
    )

    product = st.selectbox(
        "Select Product",
        products
    )

    regions = ["All"] + sorted(
        df["Region"].dropna().unique()
    )

    region = st.selectbox(
        "Select Region",
        regions
    )

    ship_modes = ["All"] + sorted(
        df["Ship Mode"].dropna().unique()
    )

    ship_mode = st.selectbox(
        "Select Ship Mode",
        ship_modes
    )


# =========================================================
# FILTER
# =========================================================

filtered_df = df[
    df["Product Name"] == product
].copy()


if region != "All":

    filtered_df = filtered_df[
        filtered_df["Region"] == region
    ]


if ship_mode != "All":

    filtered_df = filtered_df[
        filtered_df["Ship Mode"] == ship_mode
    ]


if filtered_df.empty:

    st.info("No data available for the selected filters. Please adjust your filter selection.")
    st.stop()


# =========================================================
# METRICS
# =========================================================

current_factory = filtered_df[
    "Current Factory"
].iloc[0]

avg_lead = filtered_df[
    "Lead Time"
].mean()

avg_cost = filtered_df[
    "Cost"
].mean()

total_sales = filtered_df[
    "Sales"
].sum()

total_profit = filtered_df[
    "Gross Profit"
].sum()


# =========================================================
# KPI
# =========================================================

st.markdown(
    '<div class="section">📊 Key Performance Indicators</div>',
    unsafe_allow_html=True
)

c1, c2, c3, c4, c5 = st.columns(5)

with c1:
    st.metric(
        "Current Factory",
        current_factory
    )

with c2:
    st.metric(
        "Avg Lead Time",
        f"{avg_lead:.0f} days"
    )

with c3:
    st.metric(
        "Avg Cost",
        f"${avg_cost:,.2f}"
    )

with c4:
    st.metric(
        "Sales",
        f"${total_sales:,.0f}"
    )

with c5:
    st.metric(
        "Gross Profit",
        f"${total_profit:,.0f}"
    )


# =========================================================
# MODEL RECOMMENDATION
# =========================================================

st.markdown(
    '<div class="section">🎯 Model Recommendation</div>',
    unsafe_allow_html=True
)

rec = recommendations[
    recommendations["Product Name"] == product
]


if not rec.empty:

    recommended_factory = rec[
        "Recommended Factory"
    ].iloc[0]

    improvement = rec[
        "Lead Time Reduction %"
    ].iloc[0]

    estimated_lead = avg_lead * (
        1 - improvement / 100
    )

    st.markdown(
        f"""
        <div class="rec-card">

        <div class="rec-title">
        Recommended Action
        </div>

        <div class="rec-main">
        🏭 {recommended_factory}
        </div>

        <p>
        Move <b>{product}</b>
        from <b>{current_factory}</b>
        → <b>{recommended_factory}</b>
        </p>

        <hr>

        <b>Current Lead Time:</b>
        {avg_lead:.0f} days
        &nbsp;&nbsp;&nbsp;

        <b>Estimated Lead Time:</b>
        {estimated_lead:.0f} days
        &nbsp;&nbsp;&nbsp;

        <b>Potential Reduction:</b>
        {improvement:.2f}%

        </div>
        """,
        unsafe_allow_html=True
    )


# =========================================================
# PRODUCT PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section">📦 Product Performance</div>',
    unsafe_allow_html=True
)

display_columns = [
    "Product Name",
    "Current Factory",
    "Region",
    "Ship Mode",
    "Sales",
    "Units",
    "Cost",
    "Gross Profit",
    "Lead Time"
]

available_columns = [
    c for c in display_columns
    if c in filtered_df.columns
]

st.dataframe(
    filtered_df[available_columns].head(20),
    width="stretch",
    hide_index=True
)


# =========================================================
# FACTORY PERFORMANCE
# =========================================================

st.markdown(
    '<div class="section">🏭 Factory Performance</div>',
    unsafe_allow_html=True
)

factory_summary = (
    df.groupby("Current Factory")
    .agg(
        Avg_Lead_Time=("Lead Time", "mean"),
        Avg_Cost=("Cost", "mean"),
        Total_Sales=("Sales", "sum"),
        Total_Profit=("Gross Profit", "sum")
    )
    .round(2)
)

st.dataframe(
    factory_summary,
    width="stretch"
)


# =========================================================
# FACTORY LEAD TIME CHART
# =========================================================
# =========================================================
# FACTORY LEAD TIME CHART
# =========================================================

st.markdown(
    '<div class="section">⚡ Factory Lead-Time Comparison</div>',
    unsafe_allow_html=True
)

import plotly.express as px

lead_chart = (
    factory_summary["Avg_Lead_Time"]
    .sort_values()
    .reset_index()
)

fig = px.bar(
    lead_chart,
    x="Avg_Lead_Time",
    y="Current Factory",
    orientation="h",
    text="Avg_Lead_Time"
)

fig.update_traces(
    marker_color="#8B5E3C",
    texttemplate="%{text:.0f} days",
    textposition="outside"
)

fig.update_layout(
    height=380,
    xaxis_title="Average Lead Time (Days)",
    yaxis_title="Factory",
    showlegend=False,
    plot_bgcolor="white",
    paper_bgcolor="white"
)

st.plotly_chart(fig, width="stretch")

# =========================================================
# RECOMMENDATION TABLE
# =========================================================

st.markdown(
    '<div class="section">🎯 Factory Reallocation Recommendations</div>',
    unsafe_allow_html=True
)

recommendation_view = recommendations.sort_values(
    "Lead Time Reduction %",
    ascending=False
)

st.dataframe(
    recommendation_view,
    width="stretch",
    hide_index=True
)


# =========================================================
# IMPROVEMENT CHART
# =========================================================

st.markdown(
    '<div class="section">📈 Potential Lead-Time Improvement</div>',
    unsafe_allow_html=True
)

improvement_chart = (
    recommendation_view
    .set_index("Product Name")
    ["Lead Time Reduction %"]
)

st.bar_chart(
    improvement_chart,
    width="stretch"
)


# =========================================================
# WHAT-IF SIMULATOR
# =========================================================

st.markdown(
    '<div class="section">🔄 What-If Factory Scenario</div>',
    unsafe_allow_html=True
)

w1, w2 = st.columns(2)

with w1:

    sim_product = st.selectbox(
        "Select Product",
        sorted(
            df["Product Name"]
            .dropna()
            .unique()
        ),
        key="sim_product"
    )

with w2:

    sim_factory = st.selectbox(
        "Select Alternative Factory",
        [
            "Lot's O' Nuts",
            "Wicked Choccy's",
            "Sugar Shack",
            "Secret Factory",
            "The Other Factory"
        ],
        key="sim_factory"
    )


sim_data = df[
    df["Product Name"] == sim_product
]


sim_rec = recommendations[
    recommendations["Product Name"] == sim_product
]


if not sim_data.empty:

    sim_current_factory = sim_data[
        "Current Factory"
    ].iloc[0]

    sim_current_lead = sim_data[
        "Lead Time"
    ].mean()

    if not sim_rec.empty:

        sim_recommended = sim_rec[
            "Recommended Factory"
        ].iloc[0]

        sim_improvement = sim_rec[
            "Lead Time Reduction %"
        ].iloc[0]

    else:

        sim_recommended = sim_factory
        sim_improvement = 0

    estimated_sim_lead = (
        sim_current_lead *
        (1 - sim_improvement / 100)
    )

    s1, s2, s3 = st.columns(3)

    s1.metric(
        "Current Factory",
        sim_current_factory
    )

    s2.metric(
        "Recommended Factory",
        sim_recommended
    )

    s3.metric(
        "Potential Improvement",
        f"{sim_improvement:.2f}%"
    )

    st.info(
        f"For **{sim_product}**, model recommends "
        f"**{sim_recommended}**. "
        f"Estimated lead time: "
        f"**{estimated_sim_lead:.0f} days**."
    )


# =========================================================
# RISK & IMPACT
# =========================================================

st.markdown(
    '<div class="section">⚠️ Risk & Impact</div>',
    unsafe_allow_html=True
)

avg_improvement = recommendations[
    "Lead Time Reduction %"
].mean()

max_improvement = recommendations[
    "Lead Time Reduction %"
].max()

r1, r2, r3 = st.columns(3)

r1.metric(
    "Average Improvement",
    f"{avg_improvement:.2f}%"
)

r2.metric(
    "Maximum Improvement",
    f"{max_improvement:.2f}%"
)

r3.metric(
    "Recommendations",
    len(recommendations)
)

st.warning(
    "Factory reassignment should be validated against "
    "manufacturing capacity, profitability, inventory "
    "availability and operational constraints."
)


# =========================================================
# FOOTER
# =========================================================

st.divider()

st.caption(
    "🍫 Nassau Candy Factory Optimization • "
    "Decision Intelligence Prototype"
)

st.caption(
    "Improvement percentages are model-based scenario estimates "
    "and should not be treated as guaranteed operational savings."
)