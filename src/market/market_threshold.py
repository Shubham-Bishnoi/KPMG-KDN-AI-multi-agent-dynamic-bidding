import numpy as np
import random

def dynamic_market_threshold(current_threshold, all_bids):
    """Adjust market threshold based on bidding trends dynamically."""
    avg_bid = np.mean(all_bids)
    
    # Introduce small randomness in market threshold
    fluctuation = random.uniform(-2, 2)  # ✅ Add minor fluctuation

    if avg_bid < current_threshold * 0.85:
        new_threshold = current_threshold * 0.98 + fluctuation
    elif avg_bid > current_threshold * 1.1:
        new_threshold = current_threshold * 1.02 + fluctuation
    else:
        new_threshold = current_threshold + fluctuation  # ✅ Add randomness

    return max(500, new_threshold)  # Ensure it never drops too low
