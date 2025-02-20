import os
import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import seaborn as sns
import matplotlib.pyplot as plt
from openai import OpenAI
from dotenv import load_dotenv

#  Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

#  Initialize OpenAI Client
client = OpenAI(api_key=OPENAI_API_KEY)

#  File path for bid data
DATA_FILE = os.path.abspath(os.path.join(os.path.dirname(__file__), "../data/bid_history.csv"))

#  Streamlit UI Setup
st.set_page_config(
    page_title="AI Bidding Dashboard",
    page_icon="",
    layout="wide",
    initial_sidebar_state="expanded",
)

#  Sidebar: Theme Selection
st.sidebar.title(" Theme Settings")
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

#  Load Bid Data Function
@st.cache_data
def load_bid_data():
    """Loads bid data from CSV."""
    if not os.path.exists(DATA_FILE):
        return pd.DataFrame()
    return pd.read_csv(DATA_FILE)

#  Fetch AI-Powered Bidding Insights
def get_ai_bid_suggestion(market_threshold):
    """Fetch AI-powered bidding advice."""
    if not OPENAI_API_KEY:
        return "⚠️ OpenAI API Key is missing."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI expert in market bidding strategies."},
                {"role": "user", "content": f"The current market threshold is {market_threshold}. Suggest an optimal bid."}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ OpenAI API Error: {e}"

#  AI Chatbot Function
def chat_with_ai(user_input):
    """Chatbot to answer user questions about bidding strategies."""
    if not OPENAI_API_KEY:
        return "⚠️ OpenAI API Key is missing."

    try:
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[
                {"role": "system", "content": "You are an AI chatbot specialized in market bidding, auctions, and competitive bidding strategies."},
                {"role": "user", "content": user_input}
            ]
        )
        return response.choices[0].message.content.strip()
    except Exception as e:
        return f"⚠️ AI Chatbot Error: {e}"

#  Load Data
df = load_bid_data()

#  Header
st.title(" AI Multi-Agent Bidding Dashboard")
st.write("Real-time insights into multi-agent AI bidding trends and performance.")

#  AI Chatbot Section (Sidebar)
st.sidebar.subheader("💬 AI Bidding Chatbot")
user_query = st.sidebar.text_input("Ask me anything about market bidding!")

if user_query:
    ai_response = chat_with_ai(user_query)
    st.sidebar.write(f"🤖 AI: {ai_response}")

#  No Data Warning
if df.empty:
    st.warning("⚠️ No bid data available. Please run the bidding simulation first.")
else:
    #  Sidebar: Filters
    st.sidebar.header("🔍 Filters")
    rounds = st.sidebar.slider(
        "Select Rounds:",
        min_value=int(df["Round"].min()),
        max_value=int(df["Round"].max()),
        value=(int(df["Round"].min()), int(df["Round"].max())),
    )
    agents = st.sidebar.multiselect("Select Agents:", options=df["Agent"].unique(), default=df["Agent"].unique())

    #  AI Insights Toggle
    st.sidebar.header("🤖 AI Insights")
    enable_ai = st.sidebar.checkbox("Enable AI-powered Bidding Advice", value=True)

    #  Filter Data
    filtered_df = df[(df["Round"].between(rounds[0], rounds[1])) & (df["Agent"].isin(agents))]

    # Data Table with Search
    st.subheader(" Bid Data Table")
    st.dataframe(filtered_df)

    # AI-Powered Insights
    if enable_ai:
        st.subheader("🤖 AI-Powered Bidding Advice")
        latest_round = df["Round"].max()
        market_threshold = df[df["Round"] == latest_round]["Bid"].mean()
        ai_suggestion = get_ai_bid_suggestion(market_threshold)
        st.info(f" AI Suggestion for Next Round: {ai_suggestion}")

    #  Data Visualizations

    def plot_bid_trends(df):
        """Visualizes bidding trends over rounds."""
        if df.empty:
            st.warning("⚠️ No bid data available for visualization.")
            return

        st.subheader("📈 Bidding Trends Over Rounds")

        fig, ax = plt.subplots(figsize=(10, 5))
        sns.lineplot(data=df, x="Round", y="Bid", hue="Agent", marker="o", ax=ax)

        ax.set_title(" Bidding Trends Over Rounds")
        ax.set_xlabel("Round Number")
        ax.set_ylabel("Bid Value")
        ax.legend(title="Agent")

        st.pyplot(fig)

    def plot_heatmap(df):
        """Creates a heatmap of winning bids over rounds."""
        if df.empty:
            st.warning("⚠️ No bid data available for heatmap.")
            return

        st.subheader(" Winning Bids Heatmap")

        df_unique = df.groupby(["Round", "Agent"], as_index=False)["Bid"].mean()
        heatmap_data = df_unique.pivot(index="Round", columns="Agent", values="Bid")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.heatmap(heatmap_data, cmap="coolwarm", annot=True, fmt=".1f", linewidths=0.5, ax=ax)

        st.pyplot(fig)

    def plot_bid_distribution(df):
        """Displays a box plot of bid distribution."""
        if df.empty:
            st.warning("⚠️ No bid data available for box plot.")
            return

        st.subheader("📦 Bid Distribution Analysis")

        fig, ax = plt.subplots(figsize=(10, 6))
        sns.boxplot(x="Agent", y="Bid", data=df, palette="coolwarm", ax=ax)
        st.pyplot(fig)

    def plot_agent_performance(df):
        """Visualizes agent performance based on winning bids."""
        if df.empty:
            st.warning("⚠️ No bid data available for performance analysis.")
            return

        st.subheader("🏆 Agent Performance")

        performance_df = df.groupby("Agent")["Winning_Bid"].sum().reset_index()
        fig = px.bar(performance_df, x="Agent", y="Winning_Bid", title="Winning Bids per Agent", color="Agent")

        st.plotly_chart(fig)

    def plot_market_dynamics(df):
        """Visualizes market bidding dynamics over rounds."""
        if df.empty:
            st.warning("⚠️ No bid data available for market dynamics.")
            return

        st.subheader("📊 Market Dynamics Over Time")

        fig = px.line(df, x="Round", y="Bid", color="Agent", title="Market Bidding Behavior")
        st.plotly_chart(fig)

    #  Run Visualizations
    plot_bid_trends(filtered_df)
    plot_heatmap(filtered_df)
    plot_bid_distribution(filtered_df)
    plot_agent_performance(filtered_df)
    plot_market_dynamics(filtered_df)

    # Summary Stats
    st.sidebar.subheader(" Summary Statistics")
    st.sidebar.write(filtered_df.describe())

    # Download CSV
    st.sidebar.download_button(
        label="📥 Download Bid Data",
        data=filtered_df.to_csv(index=False),
        file_name="bid_data.csv",
        mime="text/csv",
    )

    #  Real-Time Updates Simulation
    if st.sidebar.button("🔄 Refresh Data"):
        st.rerun()

    #  Success Message
    st.sidebar.success("✨ AI-powered multi-agent bidding insights loaded successfully!")
