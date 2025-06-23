## Module 5 Assignment

### How to run 
Create a virtual environment 
```
python3 -m venv venv
```

Activate virtual environment
```
source venv/bin/activate
```

Install dependencies
```
pip3 install -r requirements.txt
```

Create an .env file in the root directory with at least these environment variables
```
CALCULATOR_MAX_HISTORY_SIZE=100
CALCULATOR_AUTO_SAVE=true
CALCULATOR_DEFAULT_ENCODING=utf-8
```

Run main.py to excute program
```
python3 main.py
```

Calculator Commands
```
help - Displays the help menu
add, subtract, multiply, divide, power, root - Perform calculations
history - Show calculation history
clear - Clear calculation history
undo - Undo the last calculation
redo - Redo the last undone calculation
save - Save calculation history to file
load - Load calculation history from file
exit - Exit the calculator
```

Run tests by running the pytest command