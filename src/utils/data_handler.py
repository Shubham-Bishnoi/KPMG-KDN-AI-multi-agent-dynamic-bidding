import pandas as pd
import os

def save_bid_data(data_file, round_num, bids, winning_bid):
    """Stores bid data in a CSV file."""
    data = [{
        "Round": int(round_num),  # Ensure Round is always an integer
        "Agent": agent,
        "Bid": bid,
        "Winning_Bid": bid == winning_bid
    } for agent, bid in bids.items()]
    
    df = pd.DataFrame(data)
    
    # Ensure the CSV file has headers when first created
    write_header = not os.path.exists(data_file) or os.stat(data_file).st_size == 0
    
    df.to_csv(data_file, mode='a', header=write_header, index=False)

def load_bid_data(data_file):
    """Loads bid data from a CSV file for analysis."""
    if os.path.exists(data_file):
        df = pd.read_csv(data_file)

        # Convert "Round" column to integer (fixes Seaborn plotting issue)
        if "Round" in df.columns:
            df["Round"] = df["Round"].astype(int)

        return df
    else:
        return pd.DataFrame(columns=["Round", "Agent", "Bid", "Winning_Bid"])

if __name__ == "__main__":
    # Example Usage
    data_file = "data/bid_history.csv"
    test_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
    winning_bid = min(test_bids.values())
    
    save_bid_data(data_file, round_num=1, bids=test_bids, winning_bid=winning_bid)
    df = load_bid_data(data_file)
    print(df.head())
