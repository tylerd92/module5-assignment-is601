import datetime
from pathlib import Path
import pandas as pd
import pytest
from unittest.mock import Mock, patch, PropertyMock
from decimal import Decimal
from tempfile import TemporaryDirectory
from app.calculator import Calculator
from app.calculator_repl import calculator_repl
from app.calculator_config import CalculatorConfig
from app.exceptions import OperationError, ValidationError
from app.history import LoggingObserver, AutoSaveObserver
from app.operations import OperationFactory

@patch('builtins.input', side_effect=['add', '6', '7', 'clear', 'exit'])
@patch('builtins.print')
def test_clear(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History cleared")

@patch('builtins.input', side_effect=['add', '6', '7', 'save', 'exit'])
@patch('builtins.print')
def test_save(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History saved successfully")

@patch('builtins.input', side_effect=['load', 'exit'])
@patch('builtins.print')
def test_load(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("History loaded successfully")

@patch('builtins.input', side_effect=['add', '3', '4', 'undo', 'exit'])
@patch('builtins.print')
def test_undo(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation undone")

@patch('builtins.input', side_effect=['undo', 'exit'])
@patch('builtins.print')
def test_no_undo(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to undo")

@patch('builtins.input', side_effect=['add', '3', '4', 'undo', 'redo', 'exit'])
@patch('builtins.print')
def test_redo(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation redone")

@patch('builtins.input', side_effect=['redo', 'exit'])
@patch('builtins.print')
def test_empty_redo(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Nothing to redo")

@patch('builtins.input', side_effect=['add', 'cancel', 'exit'])
@patch('builtins.print')
def test_cancel_first_operand(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=['add', '3', 'cancel', 'exit'])
@patch('builtins.print')
def test_cancel_second_operand(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Operation cancelled")

@patch('builtins.input', side_effect=[KeyboardInterrupt, 'exit'])
@patch('builtins.print')
def test_keyboard_interrupt(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nOperation cancelled")

@patch('builtins.input', side_effect=['history', 'exit'])
@patch('builtins.print')
def test_no_history(mock_print, mock_input):
    calculator_repl()
    mock_print.assery_any_call("No calculations in history")

@patch('builtins.input', side_effect=EOFError)
@patch('builtins.print')
def test_eof_error(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("\nInput terminated. Exiting...")

@patch('builtins.input', side_effect=['mod', 'exit'])
@patch('builtins.print')
def test_unknown_command(mock_print, mock_input):
    calculator_repl()
    mock_print.assery_any_call("Unknown command: mod. Type 'help' for available commands.")

@patch('builtins.input', side_effect=[Exception, 'exit'])
@patch('builtins.print')
def test_exception(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: ")

@patch('builtins.input', side_effect=['add','1e999', ValidationError, 'exit'])
@patch('builtins.print')
def test_validation_error(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Error: ")

@patch('builtins.input', side_effect=['add', Exception, 'exit'])
@patch('builtins.print')
def test_exception_after_add(mock_print, mock_input):
    calculator_repl()
    mock_print.assert_any_call("Unexpected error: ")