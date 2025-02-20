import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import plotly.express as px

def plot_bid_trends(df):
    """Visualizes bidding trends over rounds."""
    if df.empty:
        st.warning("⚠️ No bid data available for visualization.")
        return

    st.subheader("📈 Bidding Trends Over Rounds")

    fig, ax = plt.subplots(figsize=(10, 5))
    sns.lineplot(data=df, x="Round", y="Bid", hue="Agent", marker="o", ax=ax)

    ax.set_title("📊 Bidding Trends Over Rounds")
    ax.set_xlabel("Round Number")
    ax.set_ylabel("Bid Value")
    ax.legend(title="Agent")

    st.pyplot(fig)


def plot_heatmap(df):
    """Creates a heatmap of winning bids over rounds."""
    if df.empty:
        st.warning("⚠️ No bid data available for heatmap.")
        return

    st.subheader("🔥 Winning Bids Heatmap")

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
