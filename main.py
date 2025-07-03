import sys
import os
import torch
import argparse
import openai
from dotenv import load_dotenv

# Ensure the src module is available
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "src")))

from src.agents.bidding_agent import DQNBiddingAgent, NegotiationAgent
from src.core.bidding_simulation import BiddingSimulation
from src.utils.data_handler import DataHandler

# Load OpenAI API Key
load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

def check_openai_api():
    """Checks if OpenAI API is working before running the simulation."""
    if not OPENAI_API_KEY:
        print("No OpenAI API key found. AI-enhanced bidding will be disabled.")
        return False
    try:
        client = openai.OpenAI(api_key=OPENAI_API_KEY)
        response = client.chat.completions.create(
            model="gpt-4",
            messages=[{"role": "system", "content": "Test OpenAI connection"}]
        )
        print("✅ OpenAI API Key is working!")
        return True
    except Exception as e:
        print(f"⚠️ OpenAI API Error: {e}")
        return False

def main():
    parser = argparse.ArgumentParser(description="Run AI-powered Multi-Agent Bidding Simulation")
    parser.add_argument("--visualize", action="store_true", help="Visualize bid trends after simulation")
    args = parser.parse_args()

    # Check if OpenAI API is working
    ai_enabled = check_openai_api()

    # Initialize bidding agents with OpenAI support
    agents = [DQNBiddingAgent(name=f"Agent {i}", ai_enabled=ai_enabled) for i in range(1, 6)]
    simulation = BiddingSimulation(agents=agents, rounds=50)

    # Run Simulation
    simulation.run_simulation()
    simulation.summarize_results()
    
    # Log Q-Values for Analysis
    for agent in agents:
        sample_states = [torch.tensor([100, 10], dtype=torch.float32),
                         torch.tensor([80, 5], dtype=torch.float32),
                         torch.tensor([50, 1], dtype=torch.float32)]
        q_values = [agent.model(state).item() for state in sample_states]
        print(f"Agent {agent.name} Sample Q-Values: {q_values}")

    # Visualization (if enabled)
    if args.visualize and hasattr(simulation, "visualize_bidding_trends"):
        simulation.visualize_bidding_trends()

if __name__ == "__main__":
    main()
