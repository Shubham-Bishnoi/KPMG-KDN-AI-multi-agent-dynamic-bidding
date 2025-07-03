import os
import numpy as np
import pandas as pd
import random
import torch
import openai
from dotenv import load_dotenv
from src.agents.bidding_agent import DQNBiddingAgent, NegotiationAgent
from src.market.market_threshold import dynamic_market_threshold
from src.utils.logger import logger

# Load OpenAI API Key from Environment Variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OpenAI API Key not found. AI-powered bidding will be disabled.")
else:
    openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key globally


class BiddingSimulation:
    """Runs the multi-agent bidding and negotiation process with AI insights."""

    def __init__(self, agents, rounds=20, initial_threshold=100, data_file="data/bid_history.csv"):
        self.agents = agents
        self.rounds = rounds
        self.current_threshold = initial_threshold
        self.bid_history = []
        self.data_file = data_file
        logger.info("Bidding simulation initialized.")

    def run_simulation(self):
        logger.info("Simulation started...")
        """Executes the bidding simulation with AI-powered insights and negotiation steps."""
        for round_num in range(1, self.rounds + 1):
            print(f"\n🛒 Round {round_num} - Market Threshold: {self.current_threshold}")

            bids = {}
            for agent in self.agents:
                bid = agent.generate_bid(self.current_threshold, self.rounds - round_num)
                
                # Integrate AI Assistance for Better Bidding Strategy
                ai_suggestion = self.get_ai_bid_suggestion(agent.name, self.current_threshold, self.rounds - round_num)
                if ai_suggestion:
                    bid = (bid + ai_suggestion) / 2  # Hybrid AI + RL bidding strategy
                
                bids[agent.name] = bid

            self.bid_history.append(bids)

            #  Fix: AI-Assisted Negotiation
            for agent in self.agents:
                if isinstance(agent, NegotiationAgent): 
                    bid = agent.negotiate(bids, self.current_threshold)
                    bids[agent.name] = bid

            winning_bid = min(bids.values()) if bids else None  # Assume lowest bid wins

            # Fix: Move reward update inside the loop
            for agent in self.agents:
                reward = 10 if bids[agent.name] == winning_bid else -5
                agent.update_reward(reward)

            #  Update market threshold dynamically
            self.current_threshold = dynamic_market_threshold(
                self.current_threshold, 
                [b for round_bids in self.bid_history for b in round_bids.values()]
            )

            print(f"📌 Bids: {bids}, 🏆 Winning Bid: {winning_bid}")
            self.save_bid_data(round_num, bids, winning_bid)
            logger.info("Simulation completed.")

    def get_ai_bid_suggestion(self, agent_name, market_threshold, rounds_remaining):
        """AI-powered bidding strategy suggestion."""
        if not OPENAI_API_KEY:
            return None  # Skip AI if API Key is missing

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI expert in competitive market bidding."},
                    {"role": "user", "content": f"Agent '{agent_name}' is in a bidding war. "
                                                 f"Market threshold: {market_threshold}, Rounds left: {rounds_remaining}. "
                                                 f"Suggest an optimal bid."}
                ]
            )
            bid_suggestion = float(response["choices"][0]["message"]["content"])
            print(f"🤖 AI Suggested Bid for {agent_name}: {bid_suggestion}")
            return bid_suggestion
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return None

    def save_bid_data(self, round_num, bids, winning_bid):
        """Stores bid data in a CSV file."""
        data_file = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../data/bid_history.csv"))

        if not os.path.exists("data"):  # ✅ Ensure directory exists
            os.makedirs("data")

        file_exists = os.path.exists(data_file) and os.stat(data_file).st_size > 0

        df = pd.DataFrame([{
            "Round": round_num, "Agent": agent, "Bid": bid, "Winning_Bid": (bid == winning_bid)
        } for agent, bid in bids.items()])

        df.to_csv(data_file, mode='a', header=not file_exists, index=False)  # ✅ Fix header condition
        print(f" Saved bid data for Round {round_num}")

    def summarize_results(self):
        """Displays final results of the bidding simulation."""
        results = {agent.name: agent.reward for agent in self.agents}
        print("\n🏁 Final Rewards:", results)

        for agent in self.agents:
            sample_states = [torch.tensor([100, 10], dtype=torch.float32),
                             torch.tensor([80, 5], dtype=torch.float32),
                             torch.tensor([50, 1], dtype=torch.float32)]

            q_values = [agent.model(state).item() for state in sample_states]
            print(f"📊 Agent {agent.name} Sample Q-Values: {q_values}")

        print("\n📈 Q-Value Evolution Tracking Done!")


if __name__ == "__main__":
    # Fix: Use DQNBiddingAgent instead of NegotiationAgent
    agents = [DQNBiddingAgent(name=f"Agent {i}") for i in range(1, 6)]
    
    # Run simulation with AI-enhanced deep Q-learning agents
    simulation = BiddingSimulation(agents=agents, rounds=10)
    simulation.run_simulation()
    simulation.summarize_results()
