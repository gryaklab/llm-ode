import random
from typing import List

import sympy as sp
import numpy as np
from scipy.optimize import minimize

class Equation:
    def __init__(self, equation_str: str, all_variables: List[str]):
        '''
        Args:
            equation_str: the string representation of the equation, which can contain C or c_i for coefficients
            all_variables: all the variables in the system of equations. The equation might miss some variables.
                The variables are x_i, i = 0, 1, ..., N-1
        '''
        num_coeffs = equation_str.count('C')
        for new_coeff in [f'c_{i}' for i in range(num_coeffs)]:
            equation_str = equation_str.replace('C', new_coeff, count=1)
        self.equation = sp.sympify(equation_str)
        self.all_variables = all_variables
        self.variables = [str(s) for s in self.equation.free_symbols if str(s).startswith('x')]
        self.state_indice = [int(str(s)[2:]) for s in self.variables] # the indice of the variables present in the equation
        self.callable_fn = None
        if num_coeffs == 0:
            self._update_callable_fn()

    def optimize_coefficients(self, X: np.ndarray, y: np.ndarray):
        '''Optimize the coefficients of the equation to minimize the MSE between the observed and predicted values'''

        assert X.shape[1] == len(self.all_variables), "The number of columns of X should be equal to the number of variables in the system of equations"
        y = y.flatten()
        variables = [s for s in self.equation.free_symbols if str(s).startswith('x')]
        constants = [s for s in self.equation.free_symbols if str(s).startswith('c')]
        variables = sorted(variables, key=lambda x: int(str(x)[2:]))
        constants = sorted(constants, key=lambda x: int(str(x)[2:]))

        if len(constants) == 0:
            '''No coefficients to optimize'''
            return

        # Get the values of the variables in the equation from the observed trajectory
        rhs_var_indice = [int(str(s)[2:]) for s in variables]
        rhs_var_values = X[:, rhs_var_indice]
        rhs_fn = sp.lambdify(variables + constants, self.equation, 'numpy')

        def objective_fn(coeffs: np.ndarray) -> float:
            rhs_values = rhs_fn(*rhs_var_values.T, *coeffs).flatten()
            return np.mean((y - rhs_values) ** 2)

        initial_coeffs = np.ones(len(constants)) * 1
        result = minimize(objective_fn, initial_coeffs, method='BFGS', tol=1e-6)
        coeffs = dict(zip(constants, result.x))
        self.equation = self.equation.subs(coeffs)
        self._update_callable_fn()

    def complexity(self) -> int:
        return len([_ for _ in sp.preorder_traversal(self.equation)])

    def get_skeleton(self) -> str:
        '''Get the skeleton of the equation, where all constants are replaced with a `C` placeholder'''
        C = sp.Symbol('C')
        skleton_expr = self.equation.replace(lambda e: e.is_Number or (e.is_Symbol and str(e).lower().startswith('c')), lambda _: C)
        return str(skleton_expr)

    def _update_callable_fn(self):
        self.callable_fn = sp.lambdify(self.variables, self.equation, 'numpy')

    def to_string(self, precision: int = 2) -> str:
        return str(self.equation.evalf(precision))

    def __eq__(self, other):
        return self.get_skeleton() == other.get_skeleton()

    def __hash__(self):
        return hash((self.equation))

    def __repr__(self):
        return f"{self.equation}"

    def __call__(self, X: np.ndarray) -> np.ndarray:
        '''Evaluate the equation with the given values of the variables'''
        assert self.callable_fn is not None, "The equation has not been optimized yet"
        assert X.shape[1] == len(self.all_variables), "The number of columns of X should be equal to the number of variables in the system of equations"
        return self.callable_fn(*X[:, self.state_indice].T)

def make_random_equation(all_variables: List[str]) -> Equation:
    '''Make a random equation with the given left-hand-side variable and all variables'''
    candidates = [
            'C * {variable}',
            'C * sin ({variable})',
            'C * log ({variable})',
            '{variable} ** C',
            'C ** {variable}',
            'C / {variable}',
        ]
    candidate = random.choice(candidates)
    variable = random.choice(all_variables)
    equation_str = candidate.format(variable=variable)
    return Equation(equation_str, all_variables=all_variables)

