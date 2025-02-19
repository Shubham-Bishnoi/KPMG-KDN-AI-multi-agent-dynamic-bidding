from src.agents.bidding_agent import NegotiationAgent
import numpy as np

class NegotiationLogic:
    """Implements negotiation strategies for dynamic contract bidding."""
    def __init__(self, agents, negotiation_rounds=3):
        self.agents = agents
        self.negotiation_rounds = negotiation_rounds
    
    def negotiate_bids(self, market_threshold, competitor_bids):
        """Runs negotiation rounds where agents adjust bids based on competition."""
        for _ in range(self.negotiation_rounds):
            for agent in self.agents:
                new_bid = agent.negotiate(competitor_bids, market_threshold)
                competitor_bids[agent.name] = new_bid
        return competitor_bids
    
    def finalize_bids(self, bids):
        """Determines the final bid after negotiation rounds."""
        return {agent: bids[agent] for agent in sorted(bids, key=bids.get)}  # Sort bids in ascending order
    
if __name__ == "__main__":
    # Example Usage
    agents = [NegotiationAgent(name=f"Agent {i}") for i in range(1, 6)]
    negotiation_logic = NegotiationLogic(agents)
    
    market_threshold = 100
    initial_bids = {agent.name: np.random.uniform(80, 120) for agent in agents}
    
    print("Initial Bids:", initial_bids)
    negotiated_bids = negotiation_logic.negotiate_bids(market_threshold, initial_bids)
    finalized_bids = negotiation_logic.finalize_bids(negotiated_bids)
    
    print("Negotiated Bids:", finalized_bids)
