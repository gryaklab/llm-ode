import logging

import numpy as np

from llmode.equation import Equation, make_random_equation


class Program:
    '''A program contains an equation and its mse score'''
    def __init__(self, equation: Equation, score: float):
        self.equation = equation
        self.score = score

    def __repr__(self):
        return f"{self.equation.to_string(precision=2)}"

    def __hash__(self):
        return hash((self.equation))

    def to_json(self):
        return {
            'equation': str(self.equation),
            'score': self.score,
        }

    def __eq__(self, other):
        return self.equation == other.equation

def make_random_program(X: np.ndarray, y: np.ndarray) -> Program:
    while True:
        try:
            all_variables = [f"x_{i}" for i in range(X.shape[1])]
            equation = make_random_equation(all_variables=all_variables)
            equation.optimize_coefficients(X, y)
            score = np.mean((y - equation(X)) ** 2)
            if np.isnan(score) or np.isinf(score):
                raise ValueError("Score is NaN or Inf")
            return Program(equation, score)
        except Exception as e:
            logging.warning(f"Error making random program: {e}")
            continue