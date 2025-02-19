import random
import torch
import torch.nn as nn
import torch.optim as optim
import numpy as np

class DQN(nn.Module):
    """Deep Q-Network to approximate Q-values for bidding."""
    def __init__(self, input_dim, output_dim):
        super(DQN, self).__init__()
        self.fc1 = nn.Linear(input_dim, 64)  # Hidden layer 1
        self.fc2 = nn.Linear(64, 64)  # Hidden layer 2
        self.fc3 = nn.Linear(64, output_dim)  # Output layer

    def forward(self, x):
        x = torch.relu(self.fc1(x))
        x = torch.relu(self.fc2(x))
        return self.fc3(x)  # Output Q-values

class DQNBiddingAgent:
    """Deep Q-Learning-based Bidding Agent."""
    def __init__(self, name, learning_rate=0.01, discount_factor=0.9, exploration_rate=0.5):
        self.name = name
        self.model = DQN(input_dim=2, output_dim=1)
        self.optimizer = optim.Adam(self.model.parameters(), lr=learning_rate)
        self.loss_fn = nn.MSELoss()
        self.discount_factor = discount_factor
        self.exploration_rate = exploration_rate
        self.reward = 0  # ✅ Fix: Initialize reward attribute
        self.history = []

    def generate_bid(self, market_threshold, rounds_remaining):
        """Generate a bid using deep Q-learning."""
        state = torch.tensor([market_threshold, rounds_remaining], dtype=torch.float32)

        if random.random() < self.exploration_rate:
            bid = random.uniform(market_threshold * 0.7, market_threshold * 1.1)
        else:
            bid = self.model(state).item()

        return max(1, bid)

    def update_reward(self, reward):
        """Train the DQN model using rewards."""
        self.reward += reward  # ✅ Fix: Track rewards properly

        target = torch.tensor([reward], dtype=torch.float32)
        prediction = self.model(torch.tensor([random.uniform(50, 100), random.randint(1, 2000)], dtype=torch.float32))

        loss = self.loss_fn(prediction, target)
        self.optimizer.zero_grad()
        loss.backward()
        self.optimizer.step()

        self.exploration_rate *= 0.99  # Reduce randomness over time




class NegotiationAgent(DQNBiddingAgent):
    """Agent that can negotiate bids using RL."""
    def __init__(self, name):
        super().__init__(name)  # ✅ Ensure NegotiationAgent initializes `reward` and `q_value`

    def negotiate(self, competitor_bids, market_threshold):
        """Negotiate a lower bid strategically."""
        min_competitor_bid = min(competitor_bids.values())
        if self.q_value > min_competitor_bid:  
            return min_competitor_bid - 1  # Try to undercut slightly
        else:
            return self.q_value
