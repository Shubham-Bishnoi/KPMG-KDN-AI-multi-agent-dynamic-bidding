import random
import torch
import torch.nn as nn
import torch.optim as optim
import openai
import os
from dotenv import load_dotenv

# ✅ Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# ✅ Initialize OpenAI Client
client = openai.OpenAI(api_key=OPENAI_API_KEY)

class DQN(nn.Module):
    """Deep Q-Network for bidding."""
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)
        self.fc2 = nn.Linear(64, 64)
        self.fc3 = nn.Linear(64, output_dim)

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)

class DQNBiddingAgent:
    """Deep Q-Learning-based Bidding Agent with AI-powered strategy."""
    def __init__(self, name, learning_rate=0.01, discount_factor=0.9, exploration_rate=0.2, ai_enabled=False):
        self.name = name
        self.model = DQN(input_dim=2, output_dim=1)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate  # Reduced for better RL performance
        self.reward = 0
        self.history = []
        self.ai_enabled = ai_enabled  

    def generate_bid(self, market_threshold, rounds_remaining):
        """Generate a bid using deep Q-learning or AI-powered reasoning."""
        state = torch.tensor([market_threshold, rounds_remaining], dtype=torch.float32)

        if random.random() < self.exploration_rate:
            bid = random.uniform(market_threshold * 0.9, market_threshold * 1.1)
        else:
            bid = self.model(state).item()

        # ✅ AI-Powered Bidding Optimization
        if self.ai_enabled:
            ai_bid = self.get_ai_bid_strategy(market_threshold, rounds_remaining)
            if ai_bid is not None:
                bid = (bid + ai_bid) / 2  

        return max(1, round(bid, 2))  # ✅ Ensuring valid bid

    def get_ai_bid_strategy(self, market_threshold, rounds_remaining):
        """AI-powered bidding strategy using OpenAI GPT."""
        if not OPENAI_API_KEY:
            return None  

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI market bidding expert. Return only a number."},
                    {"role": "user", "content": f"Market threshold is {market_threshold}, {rounds_remaining} rounds remain out of 20. Suggest an optimal bid."}
                ]
            )

            # ✅ Ensure AI returns only numbers (avoids 'string to float' conversion errors)
            ai_bid = float(response.choices[0].message.content.strip())
            return ai_bid

        except ValueError:
            print(f"⚠️ AI Error: Could not convert response to number.")
            return None
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return None

    def update_reward(self, reward):
        """Train the DQN model using rewards."""
        self.reward += reward  

        target = torch.tensor([reward], dtype=torch.float32)
        prediction = self.model(torch.tensor([random.uniform(50, 100), random.randint(1, 2000)], dtype=torch.float32))

        loss = self.loss_fn(prediction, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.exploration_rate *= 0.98  

class NegotiationAgent(DQNBiddingAgent):
    """Agent that can negotiate bids using RL and AI-powered strategy."""
    def __init__(self, name):
        super().__init__(name)  

    def negotiate(self, competitor_bids, market_threshold):
        """Negotiate a lower bid strategically with AI support."""
        min_competitor_bid = min(competitor_bids.values())

        # ✅ AI-powered negotiation support
        ai_negotiation = self.get_ai_negotiation_strategy(min_competitor_bid, market_threshold)
        if ai_negotiation:
            return ai_negotiation

        return min_competitor_bid - 1 if min_competitor_bid > 1 else 1  

    def get_ai_negotiation_strategy(self, min_competitor_bid, market_threshold):
        """Use OpenAI GPT for market negotiation strategies."""
        if not OPENAI_API_KEY:
            return None  

        try:
            response = client.chat.completions.create(
                model="gpt-4",
                messages=[
                    {"role": "system", "content": "You are an AI specializing in market negotiations. Return only a number."},
                    {"role": "user", "content": f"Lowest competitor bid is {min_competitor_bid}, market threshold is {market_threshold}. Suggest a counter-offer."}
                ]
            )
            return float(response.choices[0].message.content.strip())
        except Exception as e:
            print(f"⚠️ OpenAI API Error: {e}")
            return None
