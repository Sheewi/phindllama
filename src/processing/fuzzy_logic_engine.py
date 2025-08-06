# src/processing/fuzzy_logic_engine.py
"""Fuzzy logic implementation for decision making."""
from abc import ABC, abstractmethod
from typing import Dict, Any, List
import logging
import numpy as np
from ..config.settings import Settings

class FuzzyLogicEngine(ABC):
    """
    Base fuzzy logic engine class.
    
    Implements core fuzzy logic functionality for decision making.
    """
    def __init__(self):
        self.logger = logging.getLogger(__name__)
        self.settings = Settings().get_default_settings()['fuzzy_logic']
        
    @abstractmethod
    def fuzzify(self, inputs: Dict[str, Any]) -> List[float]:
        """Convert crisp inputs to fuzzy values."""
        pass
        
    def defuzzify(self, fuzzy_output: float) -> Any:
        """Convert fuzzy output to crisp value."""
        return round(fuzzy_output, self.settings['precision'])
        
    def calculate_confidence(self, inputs: Dict[str, Any], 
                           outputs: Dict[str, Any]) -> float:
        """Calculate confidence score for decisions."""
        weights = self.settings['confidence_weights']
        weighted_score = sum(
            w * v for w, v in zip(weights.values(), inputs.values())
        ) / sum(weights.values())
        return min(max(weighted_score, 0.0), 1.0)

class TradingFuzzyLogic(FuzzyLogicEngine):
    """Concrete implementation for trading decisions."""
    def fuzzify(self, inputs: Dict[str, Any]) -> List[float]:
        """Convert trading indicators to fuzzy values."""
        fuzzy_values = []
        
        # Fuzzify price momentum
        momentum = inputs.get('momentum', 0.0)
        fuzzy_momentum = max(min(momentum / 100.0, 1.0), -1.0)
        fuzzy_values.append(fuzzy_momentum)
        
        # Fuzzify volume indicator
        volume_change = inputs.get('volume_change', 0.0)
        fuzzy_volume = max(min(volume_change / 100.0, 1.0), -1.0)
        fuzzy_values.append(fuzzy_volume)
        
        return fuzzy_values
