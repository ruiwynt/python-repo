import pytest

from calculator_consumer import CalculatorConsumer
from generator_consumer import GeneratorConsumer


def test_calculate(mocker):
    calculator = mocker.patch("calculator.Calculator", spec=True)
    consumer = CalculatorConsumer(calculator)
    consumer.calculate("add", 1, 2)
    calculator.add.assert_called_with(1, 2)

def test_get_history(mocker):
    calculator = mocker.patch("calculator.Calculator", spec=True)
    consumer = CalculatorConsumer(calculator)
    calculator.configure_mock(**{'add.return_value': 2})
    consumer.calculate("add", 1, 2)
    assert [2] == consumer.get_history()

async def test_generator(mocker):
    mocker.patch("generator_consumer.generate", return_value=2)
    consumer = GeneratorConsumer()
    assert 3 == await consumer.calculate()