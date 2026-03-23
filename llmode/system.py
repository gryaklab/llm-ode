import logging
import signal
import random
from dataclasses import dataclass
from functools import wraps

from findiff import FinDiff
import numpy as np
import sympy as sp
from scipy.integrate import solve_ivp
from scipy.optimize import minimize
class TimeoutException(Exception):
    pass
def timeout_handler(signum, frame):
    raise TimeoutException("Function timed out")
signal.signal(signal.SIGALRM, timeout_handler)


class System:
    '''
    A set of equations that describe the dynamics of a system.
    The system can contain coefficent placeholders, which are optimized to minimize the error
    between the predicted and observed trajectories.
    '''
    def __init__(self, equations_str: str):
        self._trajectory_cache = {}
        self.N = equations_str.count('|') + 1
        self.var_symbols = list(sp.symbols(f"x_:{self.N}"))
        self.skeleton = None

        num_coeffs = equations_str.count('C')
        for new_coeff in [f'c_{i}' for i in range(num_coeffs)]:
            equations_str = equations_str.replace('C', new_coeff, count=1)

        self.equations = [sp.sympify(eq) for eq in equations_str.split('|')]
        self._update_callable_fn()

    def num_equations(self) -> int:
        return self.N

    def _update_callable_fn(self):
        lambdified_equations = [sp.lambdify(self.var_symbols, eq, 'numpy') for eq in self.equations]
        self.callable_fn = lambda x: np.array([f(*x) for f in lambdified_equations])

    def get_skeleton(self) -> str:
        '''Get the skeleton of the system, where all coefficients are replaced with a `C` placeholder'''
        if self.skeleton is not None:
            return self.skeleton
        C = sp.Symbol('C')
        skleton_expr = [eq.replace(lambda e: e.is_Number or (e.is_Symbol and str(e).lower().startswith('c')), lambda _: C) for eq in self.equations]
        self.skeleton = " | ".join(map(str, skleton_expr))
        return self.skeleton

    def __repr__(self) -> str:
        return " | ".join(map(str, self.equations))

    def __str__(self) -> str:
        return self.__repr__()

    def __eq__(self, other) -> bool:
        return self.get_skeleton() == other.get_skeleton()


    def to_string(self, precision: int = 2) -> str:
        return ' | '.join([str(eq.evalf(precision)) for eq in self.equations])

    def evaluate_trajectory(self, initial_state: np.ndarray, time_stamps: np.ndarray) -> np.ndarray:
        key = (initial_state.tobytes(), time_stamps.tobytes())
        if key in self._trajectory_cache:
            return self._trajectory_cache[key]
        trajectory = self._evaluate_trajectory(initial_state, time_stamps)
        self._trajectory_cache[key] = trajectory
        return trajectory

    def _evaluate_trajectory(self, initial_state: np.ndarray, time_stamps: np.ndarray) -> np.ndarray:
        '''Simulate the trajectory of the equations at the given initial state and time steps'''
        callable_fn = lambda t, x: self.callable_fn(x)
        trajectory = None
        signal.alarm(2)
        try:
            sol = solve_ivp(callable_fn, t_span=(time_stamps[0], time_stamps[-1]), y0=initial_state, t_eval=time_stamps)
            trajectory = sol.y.T
        except Exception as e:
            # logging.warning(f"Warning in evaluating trajectory: {e}")
            pass
        finally:
            signal.alarm(0)
        return trajectory

    def evaluate_derivative(self, observed_trajectory: np.ndarray) -> np.ndarray:
        '''Evaluate the derivative of the equations at the given trajectory'''
        return self.callable_fn(observed_trajectory.T).T

    def _validate_equation(self):
        pass

    def complexity(self) -> int:
        '''Total number of symbols, operations, and constants in the equations'''
        return sum([len(list(sp.preorder_traversal(eq))) for eq in self.equations])

    def optimize_coefficients(self, trajectory: np.ndarray, derivative: np.ndarray) -> np.ndarray:
        '''Optimize the coefficients of the equations to minimize the MSE between the observed and predicted derivatives'''

        for i in range(self.N):
            equation = self.equations[i]
            variables = [s for s in equation.free_symbols if str(s).startswith('x')]
            constants = [s for s in equation.free_symbols if str(s).startswith('c')]

            variables = sorted(variables, key=lambda x: int(str(x)[2:]))
            constants = sorted(constants, key=lambda x: int(str(x)[2:]))

            if len(constants) == 0:
                '''No coefficients to optimize'''
                continue
            lhs = derivative[:, i]

            # Get the values of the variables in the equation from the observed trajectory
            rhs_var_indice = [int(str(s)[2:]) for s in variables]
            rhs_var_values = trajectory[:, rhs_var_indice]
            rhs_fn = sp.lambdify(variables + constants, equation, 'numpy')

            def objective_fn(coeffs: np.ndarray) -> float:
                rhs_values = rhs_fn(*rhs_var_values.T, *coeffs)
                return np.mean((lhs - rhs_values) ** 2)

            initial_coeffs = np.ones(len(constants)) * 0.1
            result = minimize(objective_fn, initial_coeffs, method='BFGS', tol=1e-6)
            coeffs = dict(zip(constants, result.x))
            self.equations[i] = equation.subs(coeffs)
        self._update_callable_fn()

def make_random_system(n_equations: int) -> System:
    variables = [f"x_{i}" for i in range(n_equations)]
    def generate_constant():
        generate_constant.n = 0
        constant = f"c_{generate_constant.n}"
        generate_constant.n += 1
        return constant

    def pick_variable():
        return random.choice(variables)

    def generate_equation():
        candidates = [
            '{constant} * {variable}',
            'sin ({variable})',
            'cos ({variable})',
            'log ({variable})',
            'exp ({variable})',
            # 'sqrt ({variable})',
            '{variable} ** {constant}',
            # '{constant} ** {variable}',
            '{constant} / {variable}',
        ]
        candidate = random.choice(candidates)
        constant = generate_constant() if 'constant' in candidate else None
        variable = pick_variable()
        return candidate.format(variable=variable, constant=constant)

    equations_str = [generate_equation() for _ in range(n_equations)]
    equations_str = ' | '.join(equations_str)
    return System(equations_str)

