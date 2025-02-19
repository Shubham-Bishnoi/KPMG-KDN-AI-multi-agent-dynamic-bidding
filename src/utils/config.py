import os
import json
import pandas as pd

class Config:
    """Handles configuration settings for the bidding system."""
    CONFIG_FILE = "config.json"
    DEFAULT_CONFIG = {
        "OPENAI_API_KEY": "your-openai-api-key",
        "BIDDING_ROUNDS": 10,
        "INITIAL_THRESHOLD": 100,
        "DATA_FILE": "data/bid_history.csv"
    }

    @staticmethod
    def load_config():
        """Loads configuration from a JSON file or creates a default one."""
        if os.path.exists(Config.CONFIG_FILE):
            with open(Config.CONFIG_FILE, "r") as file:
                return json.load(file)
        else:
            Config.save_config(Config.DEFAULT_CONFIG)
            return Config.DEFAULT_CONFIG

    @staticmethod
    def save_config(config):
        """Saves configuration settings to a JSON file."""
        with open(Config.CONFIG_FILE, "w") as file:
            json.dump(config, file, indent=4)

class DataHandler:
    """Handles data storage and retrieval."""
    
    @staticmethod
    def save_bid_data(data_file, round_num, bids, winning_bid):
        """Stores bid data in a CSV file."""
        data = [{
            "Round": round_num,
            "Agent": agent,
            "Bid": bid,
            "Winning_Bid": bid == winning_bid
        } for agent, bid in bids.items()]
        
        df = pd.DataFrame(data)
        df.to_csv(data_file, mode='a', header=not os.path.exists(data_file), index=False)
    
    @staticmethod
    def load_bid_data(data_file):
        """Loads bid data from a CSV file for analysis."""
        if os.path.exists(data_file):
            return pd.read_csv(data_file)
        else:
            return pd.DataFrame(columns=["Round", "Agent", "Bid", "Winning_Bid"])

if __name__ == "__main__":
    # Example usage of Config
    config = Config.load_config()
    print("Loaded Configuration:", config)
    
    # Example usage of DataHandler
    data_file = config["DATA_FILE"]
    test_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
    winning_bid = min(test_bids.values())
    
    DataHandler.save_bid_data(data_file, round_num=1, bids=test_bids, winning_bid=winning_bid)
    df = DataHandler.load_bid_data(data_file)
    print(df.head())
