import os
import time
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt

# Ensure `data/bid_history.csv` is correctly located
data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/bid_history.csv"))

# ✅ Theme Toggle
st.set_page_config(
    page_title="📊 AI Bidding Dashboard",
    page_icon="💰",
    layout="wide",
    initial_sidebar_state="expanded",
)

# ✅ Sidebar: Theme Selection
st.sidebar.title("🎨 Theme Settings")
theme = st.sidebar.radio("Select Theme:", ["Light Mode", "Dark Mode"])
if theme == "Dark Mode":
    st.markdown(
        """
        <style>
        body { background-color: #121212; color: white; }
        .stDataFrame { background-color: #1E1E1E; color: white; }
        </style>
        """,
        unsafe_allow_html=True,
    )

# ✅ Load Data
@st.cache_data
def load_bid_data(data_file):
    if not os.path.exists(data_file):
        return pd.DataFrame()
    return pd.read_csv(data_file)

df = load_bid_data(data_file)

# ✅ Header
st.title("📊 AI Multi-Agent Bidding Dashboard")
st.write("Real-time insights into multi-agent AI bidding trends and performance.")

# ✅ No Data Warning
if df.empty:
    st.warning("⚠️ No bid data available. Please run the bidding simulation first.")
else:
    # ✅ Sidebar: Filters
    st.sidebar.header("🔍 Filters")
    rounds = st.sidebar.slider("Select Rounds:", min_value=int(df["Round"].min()), max_value=int(df["Round"].max()), value=(int(df["Round"].min()), int(df["Round"].max())))
    agents = st.sidebar.multiselect("Select Agents:", options=df["Agent"].unique(), default=df["Agent"].unique())

    # ✅ Filter Data
    filtered_df = df[(df["Round"].between(rounds[0], rounds[1])) & (df["Agent"].isin(agents))]

    # ✅ Data Table with Search
    st.subheader("📊 Bid Data Table")
    st.dataframe(filtered_df)

    # ✅ Line Chart - Bidding Trends
    st.subheader("📈 Bidding Trends Over Rounds")
    fig = px.line(filtered_df, x="Round", y="Bid", color="Agent", markers=True, title="Bidding Trends")
    st.plotly_chart(fig)

    # ✅ Winning Bids Heatmap
    st.subheader("🔥 Winning Bids Heatmap")
    # ✅ Aggregate duplicate bids by taking the average bid per (Round, Agent)
    df_unique = df.groupby(["Round", "Agent"], as_index=False)["Bid"].mean()

    # ✅ Pivot after resolving duplicates
    heatmap_data = df_unique.pivot(index="Round", columns="Agent", values="Bid")

    fig, ax = plt.subplots(figsize=(10, 6))
    sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.5, ax=ax)
    st.pyplot(fig)

    # ✅ Agent Performance (Bar Chart)
    st.subheader("🏆 Agent Performance")
    performance_df = df.groupby("Agent")["Winning_Bid"].sum().reset_index()
    fig = px.bar(performance_df, x="Agent", y="Winning_Bid", title="Winning Bids per Agent", color="Agent")
    st.plotly_chart(fig)

    # ✅ Animated Bid History
    st.subheader("🎬 Animated Bid History")
    animation_fig = px.scatter(filtered_df, x="Round", y="Bid", color="Agent", animation_frame="Round", title="Bid Evolution Over Time")
    st.plotly_chart(animation_fig)

    # ✅ Q-Value Evolution (if applicable)
    if "Q-Values" in df.columns:
        st.subheader("🧠 Q-Value Evolution")
        q_fig = px.line(df, x="Round", y="Q-Values", color="Agent", title="Q-Value Evolution of Agents")
        st.plotly_chart(q_fig)

    # ✅ Market Dynamics
    st.subheader("📊 Market Dynamics Over Time")
    market_fig = px.line(df, x="Round", y="Bid", color="Agent", title="Market Bidding Behavior")
    st.plotly_chart(market_fig)

    # ✅ Box Plot of Bids
    st.subheader("📦 Bid Distribution Analysis")
    fig, ax = plt.subplots(figsize=(10, 6))
    sns.boxplot(x="Agent", y="Bid", data=filtered_df, palette="coolwarm", ax=ax)
    st.pyplot(fig)

    # ✅ Summary Stats
    st.sidebar.subheader("📊 Summary Statistics")
    st.sidebar.write(filtered_df.describe())

    # ✅ Download CSV
    st.sidebar.download_button(
        label="📥 Download Bid Data",
        data=filtered_df.to_csv(index=False),
        file_name="bid_data.csv",
        mime="text/csv",
    )

    # ✅ Real-Time Updates Simulation
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()  # ✅ Newer method


    # ✅ Success Message
    st.sidebar.success("✨ AI-powered multi-agent bidding insights loaded successfully!")

