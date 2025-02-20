import unittest
import os
import numpy as np
from src.agents.bidding_agent import BiddingAgent, NegotiationAgent
from src.market.market_threshold import dynamic_market_threshold
from src.utils.data_handler import DataHandler

class TestBiddingAgent(unittest.TestCase):
    """Tests for AI-based Bidding and Negotiation Agents."""

    def setUp(self):
        """Set up agents before each test."""
        self.agent = BiddingAgent("Test Agent")
        self.negotiation_agent = NegotiationAgent("Negotiation Agent")

    def test_generate_bid(self):
        """Test bid generation under market constraints."""
        bid = self.agent.generate_bid(100, 5)
        self.assertIsInstance(bid, float)
        self.assertGreater(bid, 0, "Bid should be greater than 0")
        self.assertLessEqual(bid, 150, "Bid should be within a reasonable range")

    def test_generate_bid_edge_cases(self):
        """Test bid generation under extreme conditions."""
        bid_low = self.agent.generate_bid(1, 1)  # Edge case: very low threshold
        bid_high = self.agent.generate_bid(10000, 1)  # Edge case: very high threshold
        
        self.assertGreaterEqual(bid_low, 1, "Bid should not be lower than 1")
        self.assertLessEqual(bid_high, 11000, "Bid should not be excessively high")

    def test_negotiation(self):
        """Test AI-powered negotiation adjustments."""
        competitor_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
        bid = self.negotiation_agent.negotiate(competitor_bids, 100)

        self.assertIsInstance(bid, float)
        self.assertGreater(bid, 0, "Negotiated bid should be positive")
        self.assertLessEqual(bid, 100, "Negotiated bid should not exceed market threshold")

    def test_negotiation_edge_cases(self):
        """Test negotiation when competitor bids are extreme."""
        bid_low_competitors = self.negotiation_agent.negotiate({"Agent 1": 1}, 100)
        bid_high_competitors = self.negotiation_agent.negotiate({"Agent 1": 10000}, 100)

        self.assertGreaterEqual(bid_low_competitors, 1, "Negotiated bid should not be lower than 1")
        self.assertLessEqual(bid_high_competitors, 10000, "Negotiated bid should not exceed maximum")

class TestMarketThreshold(unittest.TestCase):
    """Tests for Dynamic Market Threshold Adjustment."""

    def test_dynamic_market_threshold(self):
        """Test market threshold adjustment based on bidding trends."""
        previous_threshold = 100
        bid_history = [95, 102, 98, 105, 100, 97, 103]
        new_threshold = dynamic_market_threshold(previous_threshold, bid_history)

        self.assertIsInstance(new_threshold, float)
        self.assertGreater(new_threshold, 0, "Market threshold should be positive")
        self.assertNotEqual(previous_threshold, new_threshold, "Market threshold should change dynamically")

    def test_market_threshold_extremes(self):
        """Test threshold changes under extreme bidding conditions."""
        new_threshold_low = dynamic_market_threshold(100, [1, 2, 3, 1, 2])
        new_threshold_high = dynamic_market_threshold(100, [1000, 1200, 1500])

        self.assertGreaterEqual(new_threshold_low, 50, "Threshold should not collapse too much")
        self.assertLessEqual(new_threshold_high, 2000, "Threshold should not inflate too much")

class TestDataHandler(unittest.TestCase):
    """Tests for bid data saving and retrieval."""

    TEST_DATA_FILE = "test_bid_history.csv"

    def setUp(self):
        """Ensure clean test environment before each test."""
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def tearDown(self):
        """Clean up test files after each test."""
        if os.path.exists(self.TEST_DATA_FILE):
            os.remove(self.TEST_DATA_FILE)

    def test_save_and_load_bid_data(self):
        """Test saving and loading bid data."""
        test_bids = {"Agent 1": 95, "Agent 2": 100, "Agent 3": 98}
        winning_bid = min(test_bids.values())

        DataHandler.save_bid_data(self.TEST_DATA_FILE, round_num=1, bids=test_bids, winning_bid=winning_bid)
        df = DataHandler.load_bid_data(self.TEST_DATA_FILE)

        self.assertFalse(df.empty, "Dataframe should not be empty after saving")
        self.assertEqual(len(df), 3, "There should be 3 bids saved")
        self.assertIn("Agent", df.columns, "Agent column should be present in DataFrame")
        self.assertEqual(df["Bid"].dtype, np.float64, "Bid column should have float values")

    def test_load_empty_data_file(self):
        """Test loading an empty data file gracefully."""
        df = DataHandler.load_bid_data(self.TEST_DATA_FILE)
        self.assertTrue(df.empty, "Should return empty DataFrame if file is missing or empty")

if __name__ == "__main__":
    unittest.main()
