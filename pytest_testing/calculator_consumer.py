from argparse import ArgumentError
from calculator import Calculator

class CalculatorConsumer:
    def __init__(self, calculator):
        self.calculator = calculator
        self.history = []

    def calculate(self, op, a, b):
        op = op.upper()
        res = None
        if op == "ADD":
            res = self.calculator.add(a, b)
        elif op == "SUB":
            res = self.calculator.sub(a, b)
        elif op == "MUL":
            res = self.calculator.mul(a, b)
        elif op == "DIV":
            res = self.calculator.div(a, b)
        else:
            raise ArgumentError("Invalid Operation")
        self.history.append(res)

    def get_history(self):
        return self.history

    def clear_history(self):
        pass