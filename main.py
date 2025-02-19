import sys
import os
import torch
import argparse

# Ensure the src module is available
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.agents.bidding_agent import DQNBiddingAgent, NegotiationAgent
from src.core.bidding_simulation import BiddingSimulation
from src.utils.data_handler import load_bid_data

def main():
    parser = argparse.ArgumentParser(description="Run AI-powered Multi-Agent Bidding Simulation")
    parser.add_argument("--visualize", action="store_true", help="Visualize bid trends after simulation")
    args = parser.parse_args()

    # Initialize bidding agents
    agents = [DQNBiddingAgent(name=f"Agent {i}") for i in range(1, 6)]  # Use DQN Agents
    simulation = BiddingSimulation(agents=agents, rounds=2000)  # Increase rounds for deep learning
    simulation.run_simulation()
    simulation.summarize_results()
    
    # ✅ Fix: Get Q-values from the neural network instead of q_table
    for agent in agents:
        sample_states = [torch.tensor([100, 10], dtype=torch.float32),
                         torch.tensor([80, 5], dtype=torch.float32),
                         torch.tensor([50, 1], dtype=torch.float32)]

        q_values = [agent.model(state).item() for state in sample_states]
        print(f"Agent {agent.name} Sample Q-Values: {q_values}")  # Show 3 Q-values
    
    # ✅ Fix: Ensure visualization method exists before calling
    if args.visualize and hasattr(simulation, "visualize_bidding_trends"):
        simulation.visualize_bidding_trends()

if __name__ == "__main__":
    main()
