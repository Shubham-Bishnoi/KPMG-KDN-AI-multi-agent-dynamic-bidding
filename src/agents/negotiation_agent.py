import os
import re
import openai
from dotenv import load_dotenv
from langchain.chat_models import ChatOpenAI

# ✅ Load OpenAI API Key Securely
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not OPENAI_API_KEY:
    print("⚠️ WARNING: OpenAI API Key not found. AI-powered bidding will be disabled.")
else:
    openai.api_key = OPENAI_API_KEY  # Set OpenAI API Key globally


class BiddingAgent:
    """Defines an AI-powered bidding agent using LangChain's OpenAI model."""
    
    def __init__(self, name, llm_model="gpt-4", temperature=0.7):
        self.name = name
        self.model = ChatOpenAI(model_name=llm_model, temperature=temperature)
        self.previous_bids = []
        self.reward = 0

    def generate_bid(self, market_threshold, rounds_remaining):
        """Generates a bid using AI based on market conditions."""
        prompt = f"""
        You are a competitive bidding AI agent participating in a multi-agent auction.
        Your goal is to place the most competitive bid.
        - Current Market Threshold: {market_threshold}
        - Your Previous Bids: {self.previous_bids}
        - Rounds Remaining: {rounds_remaining}
        Suggest a competitive bid within this context (Provide ONLY a numerical value).
        """

        bid = self.invoke_ai(prompt)
        self.previous_bids.append(bid)
        return bid

    def update_reward(self, success):
        """Updates agent reward based on bid outcome."""
        self.reward += 1 if success else -1

    def invoke_ai(self, prompt):
        """Sends a prompt to OpenAI and processes the response."""
        if not OPENAI_API_KEY:
            print("⚠️ AI disabled, falling back to random bidding.")
            return 100  # Default fallback bid

        try:
            response = self.model.invoke(prompt)
            bid = self.extract_numerical_value(response.content)
            print(f"🤖 AI-Suggested Bid for {self.name}: {bid}")
            return bid
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return 100  # Default fallback bid

    @staticmethod
    def extract_numerical_value(text):
        """Extracts numerical bid from AI response using regex."""
        match = re.search(r"\d+(\.\d+)?", text)  # Match integer or decimal numbers
        return float(match.group()) if match else 100  # Default bid


class NegotiationAgent(BiddingAgent):
    """Extends BiddingAgent to support negotiation using AI."""

    def negotiate(self, competitor_bids, market_threshold):
        """Adjusts bid dynamically based on competitors using AI."""
        prompt = f"""
        You are an AI negotiation agent participating in a bidding process.
        Your goal is to adjust your bid to maximize competitiveness while maintaining profitability.
        - Competitor Bids: {competitor_bids}
        - Market Threshold: {market_threshold}
        Suggest an optimal counter-bid that increases the chances of winning without overbidding.
        Provide ONLY a numerical value.
        """

        return self.invoke_ai(prompt)


#  Example Usage
if __name__ == "__main__":
    agent = BiddingAgent("Agent 1")
    negotiation_agent = NegotiationAgent("Negotiation Agent 1")
    
    market_threshold = 100
    bid = agent.generate_bid(market_threshold, 5)
    print(f"🔹 Agent's Bid: {bid}")
    
    competitor_bids = [95, 98, 102]
    negotiated_bid = negotiation_agent.negotiate(competitor_bids, market_threshold)
    print(f"🔹 Negotiated Bid: {negotiated_bid}")
