import openai
from langchain.chat_models import ChatOpenAI

class BiddingAgent:
    """Defines an AI-powered bidding agent."""
    def __init__(self, name, llm_model="gpt-4", temperature=0.7):
        self.name = name
        self.model = ChatOpenAI(model_name=llm_model, temperature=temperature)
        self.previous_bids = []
        self.reward = 0

    def generate_bid(self, market_threshold, rounds_remaining):
        """Generates a bid based on market conditions."""
        prompt = f"""
        You are a competitive bidding AI agent.
        - Current market threshold: {market_threshold}
        - Your previous bids: {self.previous_bids}
        - Rounds remaining: {rounds_remaining}
        Generate a competitive bid within this context.
        """
        response = self.model.invoke(prompt)
        bid = float(response.content.strip())
        self.previous_bids.append(bid)
        return bid

    def update_reward(self, success):
        """Updates agent reward based on bid outcome."""
        self.reward += 1 if success else -1

class NegotiationAgent(BiddingAgent):
    """Extends BiddingAgent to support negotiation."""
    def negotiate(self, competitor_bids, market_threshold):
        """Adjusts bid dynamically based on competitors."""
        prompt = f"""
        You are an AI negotiation agent in a bidding process.
        - Competitor bids: {competitor_bids}
        - Market threshold: {market_threshold}
        Adjust your bid to maximize competitiveness while maintaining profitability.
        """
        response = self.model.invoke(prompt)
        negotiated_bid = float(response.content.strip())
        return negotiated_bid

# Example Usage
if __name__ == "__main__":
    agent = BiddingAgent("Agent 1")
    negotiation_agent = NegotiationAgent("Negotiation Agent 1")
    
    market_threshold = 100
    bid = agent.generate_bid(market_threshold, 5)
    print(f"Agent's bid: {bid}")
    
    competitor_bids = [95, 98, 102]
    negotiated_bid = negotiation_agent.negotiate(competitor_bids, market_threshold)
    print(f"Negotiated bid: {negotiated_bid}")
