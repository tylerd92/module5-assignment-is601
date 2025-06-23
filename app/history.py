from abc import ABC, abstractmethod
import logging
from typing import Any
from app.calculation import Calculation

class HistoryObserver(ABC):
    """
    An abstract observer class that listens for updates to a Calculation.

    This class should be implemented by any observer that wants to receive
    updates when a Calculation is created or modified.
    @param Calculation: The Calculation object that is being observed.
    """
    @abstractmethod
    def update(self, calulation: Calculation) -> None:
        pass # pragma: no cover

class LoggingObserver(HistoryObserver):
    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        logging.info(
            f"Calculation performed: {calculation.operation} "
            f"({calculation.operand1}, {calculation.operand2}) = "
            f"{calculation.result}"
        )

class AutoSaveObserver(HistoryObserver):
    def __init__(self, calculator: Any) -> None:
        if not hasattr(calculator, 'config') or not hasattr(calculator, 'save_history'):
            raise TypeError("Calculator must have 'config' and 'save_history' attributes")
        self.calculator = calculator

    def update(self, calculation: Calculation) -> None:
        if calculation is None:
            raise AttributeError("Calculation cannot be None")
        if self.calculator.config.auto_save:
            self.calculator.save_history()
            logging.info("History auto-saved")