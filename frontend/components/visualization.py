import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd

def plot_bid_trends(df):
    """Visualizes bidding trends over rounds."""
    if df.empty:
        st.warning("No bid data available for visualization.")
        return

    st.subheader("📈 Bidding Trends Over Rounds")

    fig, ax = plt.subplots(figsize=(10, 5))
    
    sns.lineplot(data=df, x="Round", y="Bid", hue="Agent", marker="o", ax=ax)

    ax.set_title("Bidding Trends Over Rounds")
    ax.set_xlabel("Round Number")
    ax.set_ylabel("Bid Value")
    ax.legend(title="Agent")
    
    st.pyplot(fig)
