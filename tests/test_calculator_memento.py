import datetime
import pytest
from app.calculator_memento import CalculatorMemento
from app.calculation import Calculation

class DummyCalculation(Calculation):
    # Minimal Calculation stub for testing
    def __init__(self, value):
        self.value = value

    def to_dict(self):
        return {'value': self.value}

    @classmethod
    def from_dict(cls, data):
        return cls(data['value'])

@pytest.fixture
def calculation_patch(monkeypatch):
    # Patch Calculation in calculator_memento to use DummyCalculation
    import app.calculator_memento
    monkeypatch.setattr(app.calculator_memento, "Calculation", DummyCalculation)

def test_to_dict_and_from_dict(calculation_patch):
    calc1 = DummyCalculation(10)
    calc2 = DummyCalculation(20)
    history = [calc1, calc2]
    timestamp = datetime.datetime(2023, 1, 1, 12, 0, 0)
    memento = CalculatorMemento(history=history, timestamp=timestamp)

    memento_dict = memento.to_dict()
    assert memento_dict['history'] == [{'value': 10}, {'value': 20}]
    assert memento_dict['timestamp'] == "2023-01-01T12:00:00"

    # Test from_dict
    restored = CalculatorMemento.from_dict(memento_dict)
    assert isinstance(restored, CalculatorMemento)
    assert len(restored.history) == 2
    assert all(isinstance(c, DummyCalculation) for c in restored.history)
    assert restored.history[0].value == 10
    assert restored.history[1].value == 20
    assert restored.timestamp == timestamp

def test_to_dict_empty_history(calculation_patch):
    timestamp = datetime.datetime(2022, 5, 5, 8, 30, 0)
    memento = CalculatorMemento(history=[], timestamp=timestamp)
    memento_dict = memento.to_dict()
    assert memento_dict['history'] == []
    assert memento_dict['timestamp'] == "2022-05-05T08:30:00"

def test_from_dict_empty_history(calculation_patch):
    data = {
        'history': [],
        'timestamp': "2022-05-05T08:30:00"
    }
    memento = CalculatorMemento.from_dict(data)
    assert isinstance(memento, CalculatorMemento)
    assert memento.history == []
    assert memento.timestamp == datetime.datetime(2022, 5, 5, 8, 30, 0)