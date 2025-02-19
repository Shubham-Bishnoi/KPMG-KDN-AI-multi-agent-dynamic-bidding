import os  # ✅ Fix: Import missing os module
import numpy as np
import pandas as pd
import random
import torch
from src.agents.bidding_agent import DQNBiddingAgent, NegotiationAgent
from src.market.market_threshold import dynamic_market_threshold


class BiddingSimulation:
    """Runs the multi-agent bidding and negotiation process."""
    def __init__(self, agents, rounds=10, initial_threshold=100, data_file="data/bid_history.csv"):
        self.agents = agents
        self.rounds = rounds
        self.current_threshold = initial_threshold
        self.bid_history = []
        self.data_file = data_file

    def run_simulation(self):
        """Executes the bidding simulation with negotiation steps."""
        for round_num in range(1, self.rounds + 1):
            print(f"\nRound {round_num} - Market Threshold: {self.current_threshold}")
            
            bids = {}
            for agent in self.agents:
                bid = agent.generate_bid(self.current_threshold, self.rounds - round_num)
                bids[agent.name] = bid
            
            self.bid_history.append(bids)

            # ✅ Fix: Correctly check if an agent supports negotiation
            for agent in self.agents:
                if isinstance(agent, NegotiationAgent): 
                    bid = agent.negotiate(bids, self.current_threshold)
                    bids[agent.name] = bid
                    
            winning_bid = min(bids.values()) if bids else None  # Assume lowest bid wins

            # ✅ Fix: Move reward update inside the loop
            for agent in self.agents:
                reward = 10 if bids[agent.name] == winning_bid else -5  
                agent.update_reward(reward)  
            
            # ✅ Update market threshold dynamically
            self.current_threshold = dynamic_market_threshold(
                self.current_threshold, 
                [b for round_bids in self.bid_history for b in round_bids.values()]
            )
            
            print(f"Bids: {bids}, Winning Bid: {winning_bid}")
            self.save_bid_data(round_num, bids, winning_bid)

    
    def save_bid_data(self, round_num, bids, winning_bid):
        """Stores bid data in a CSV file."""
        data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/bid_history.csv"))  # ✅ Use absolute path

    
        if not os.path.exists("data"):  # ✅ Ensure directory exists
            os.makedirs("data")

        # ✅ Fix: Properly check if CSV exists and is non-empty
        file_exists = os.path.exists(data_file) and os.stat(data_file).st_size > 0

        df = pd.DataFrame([{
            "Round": round_num, "Agent": agent, "Bid": bid, "Winning_Bid": (bid == winning_bid)
        } for agent, bid in bids.items()])
    
        df.to_csv(data_file, mode='a', header=not file_exists, index=False)  # ✅ Fix header condition

        print(f"✅ Saved bid data for Round {round_num}")

    def summarize_results(self):
        """Displays final results of the bidding simulation."""
        results = {agent.name: agent.reward for agent in self.agents}
        print("\nFinal Rewards:", results)

        # ✅ Fix: Improved logging for Q-value retrieval
        for agent in self.agents:
            sample_states = [torch.tensor([100, 10], dtype=torch.float32),
                             torch.tensor([80, 5], dtype=torch.float32),
                             torch.tensor([50, 1], dtype=torch.float32)]
         
            q_values = [agent.model(state).item() for state in sample_states]
         
            print(f"Agent {agent.name} Sample Q-Values: {q_values}")  # Show 3 Q-values

        print("\n📈 Q-Value Evolution Tracking Done!")


if __name__ == "__main__":
    # ✅ Fix: Use DQNBiddingAgent instead of NegotiationAgent
    agents = [DQNBiddingAgent(name=f"Agent {i}") for i in range(1, 6)]
    
    # Run simulation with deep Q-learning agents
    simulation = BiddingSimulation(agents=agents, rounds=10)
    simulation.run_simulation()
    simulation.summarize_results()
