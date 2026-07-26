"""BayesianSkillRating module.

Bayesian skill rating estimation with confidence intervals.
"""

from typing import Dict, Any, Tuple


class BayesianSkillRating:
    def __init__(self, mu: float = 50.0, sigma: float = 8.33) -> None:
        self.mu = mu
        self.sigma = sigma

    def update_rating(self, match_outcome_win: bool) -> Tuple[float, float]:
        """Updates Bayesian mean skill rating (mu) and uncertainty (sigma)."""
        if match_outcome_win:
            self.mu = min(100.0, self.mu + (self.sigma * 0.5))
        else:
            self.mu = max(0.0, self.mu - (self.sigma * 0.5))
        self.sigma = max(1.0, self.sigma * 0.95)
        return round(self.mu, 1), round(self.sigma, 2)
