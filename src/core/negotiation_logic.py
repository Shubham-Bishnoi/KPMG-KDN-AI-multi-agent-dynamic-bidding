import os
import numpy as np
import openai
from dotenv import load_dotenv
from src.agents.bidding_agent import NegotiationAgent

#  Load OpenAI API Key from Environment Variables
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
if not OPENAI_API_KEY:
    print("⚠️ WARNING: OpenAI API Key not found. AI-powered negotiation will be disabled.")
else:
    openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key globally


class NegotiationLogic:
    """Implements AI-powered negotiation strategies for contract bidding."""

    def __init__(self, agents, negotiation_rounds=20):
        self.agents = agents
        self.negotiation_rounds = negotiation_rounds

    def negotiate_bids(self, market_threshold, competitor_bids):
        """Runs negotiation rounds where agents adjust bids based on competition & AI insights."""
        for _ in range(self.negotiation_rounds):
            for agent in self.agents:
                #  Step 1: Get RL-Based Negotiation Bid
                new_bid = agent.negotiate(competitor_bids, market_threshold)

                #  Step 2: Get AI-Powered Negotiation Assistance
                ai_negotiation = self.get_ai_negotiation_bid(agent.name, new_bid, competitor_bids, market_threshold)
                if ai_negotiation:
                    new_bid = (new_bid + ai_negotiation) / 2  # Hybrid AI + RL adjustment
                
                competitor_bids[agent.name] = new_bid  # ✅ Update bid after AI & RL processing

        return competitor_bids

    def get_ai_negotiation_bid(self, agent_name, current_bid, competitor_bids, market_threshold):
        """AI-powered negotiation suggestion."""
        if not OPENAI_API_KEY:
            return None  # Skip AI if API Key is missing

        try:
            response = openai.ChatCompletion.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI specializing in market negotiations."},
                    {"role": "user", "content": f"Agent '{agent_name}' is negotiating a bid."
                                                 f" Market threshold: {market_threshold}, "
                                                 f"Competitor bids: {competitor_bids}, "
                                                 f"Current bid: {current_bid}. Suggest a counter-offer."}
                ]
            )
            suggested_bid = float(response["choices"][0]["message"]["content"])
            print(f"🤖 AI Suggested Counter-Bid for {agent_name}: {suggested_bid}")
            return suggested_bid
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return None

    def finalize_bids(self, bids):
        """Determines the final bid after negotiation rounds by sorting in ascending order."""
        return {agent: bids[agent] for agent in sorted(bids, key=bids.get)}  # ✅ Sort bids from lowest to highest


if __name__ == "__main__":
    # Initialize AI-powered Negotiation Agents
    agents = [NegotiationAgent(name=f"Agent {i}") for i in range(1, 6)]
    negotiation_logic = NegotiationLogic(agents)

    # Define Market & Initial Bids
    market_threshold = 100
    initial_bids = {agent.name: np.random.uniform(80, 120) for agent in agents}

    print("\n Initial Bids:", initial_bids)

    # Run AI-Powered Negotiation
    negotiated_bids = negotiation_logic.negotiate_bids(market_threshold, initial_bids)

    # Finalize Contract Bids
    finalized_bids = negotiation_logic.finalize_bids(negotiated_bids)

    print("\n Final Negotiated Bids (Sorted):", finalized_bids)
