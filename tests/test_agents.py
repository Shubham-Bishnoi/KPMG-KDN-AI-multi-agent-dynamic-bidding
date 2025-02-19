import unittest
import numpy as np
from src.agents.bidding_agent import BiddingAgent, NegotiationAgent
from src.market.market_threshold import dynamic_market_threshold
from src.utils.data_handler import DataHandler

class TestBiddingAgent(unittest.TestCase):
    def setUp(self):
        self.agent = BiddingAgent("Test Agent")
        self.negotiation_agent = NegotiationAgent("Negotiation Agent")

    def test_generate_bid(self):
        bid = self.agent.generate_bid(100, 5)
        self.assertIsInstance(bid, float)
        self.assertGreater(bid, 0)

    def test_negotiation(self):
        competitor_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
        bid = self.negotiation_agent.negotiate(competitor_bids, 100)
        self.assertIsInstance(bid, float)
        self.assertGreater(bid, 0)

class TestMarketThreshold(unittest.TestCase):
    def test_dynamic_market_threshold(self):
        previous_threshold = 100
        bid_history = [95, 102, 98, 105, 100, 97, 103]
        new_threshold = dynamic_market_threshold(previous_threshold, bid_history)
        self.assertIsInstance(new_threshold, float)
        self.assertGreater(new_threshold, 0)

class TestDataHandler(unittest.TestCase):
    def test_save_and_load_bid_data(self):
        data_file = "test_bid_history.csv"
        test_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
        winning_bid = min(test_bids.values())
        
        DataHandler.save_bid_data(data_file, round_num=1, bids=test_bids, winning_bid=winning_bid)
        df = DataHandler.load_bid_data(data_file)
        
        self.assertFalse(df.empty)
        self.assertEqual(len(df), 3)
        self.assertIn("Agent", df.columns)
        
if __name__ == "__main__":
    unittest.main()
