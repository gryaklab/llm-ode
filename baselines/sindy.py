
import logging
import argparse
from pathlib import Path
from typing import Union, List
from itertools import product
import re

import pysindy as ps
import pandas as pd
import numpy as np
from pysindy import PolynomialLibrary, CustomLibrary, ConcatLibrary

from llmode.system import System
from data.dataset import get_equations
from findiff import Diff

hyperparameters = {
    'optimizer_threshold': [0.05, 0.1, 0.15],
    'optimizer_alpha': [0.025, 0.05, 0.075],
    'max_iterations': [20, 100],
    'polynomial_degree': [1, 2, 3, 4, 5, 6, 7, 8, 9, 10],
    'basis_functions': [
        [], # only polynomials
        ['sin', 'cos', 'exp'],
        ['sin', 'cos', 'log', 'exp', 'sqrt', 'one_over_x'],
    ],
}

class Sindy:
    def __init__(self):
        self.best_model = None
        self.best_mse = np.inf
        self.history = None

    def train(self,
              X_train: np.ndarray,
              y_train: np.ndarray,
              X_val: np.ndarray,
              t_train: np.ndarray,
              t_val: np.ndarray) -> np.ndarray:
        hp_names, hp_values = zip(*hyperparameters.items())
        hp_combinations = [dict(zip(hp_names, hp)) for hp in product(*hp_values)]
        models = [_create_sindy_model(hp) for hp in hp_combinations]
        mse_vals = []
        complexities = []
        equations_strs = []
        for model in models:
            try:
                model.fit(x=X_train, t=t_train, x_dot=y_train)
                equations_str = [_format_equation(eq) for eq in model.equations()]
            except Exception as e:
                logging.warning(f"Warning fitting model: {e}")
                continue
            equations_str = [_format_equation(eq) for eq in model.equations()]
            equations_str = '|'.join(equations_str)
            system = System(equations_str)
            mse = np.inf
            try:
                predicted_trajectory_val = system.evaluate_trajectory(X_val[0], t_val)
                assert predicted_trajectory_val.shape == X_val.shape, f"Predicted trajectory shape {predicted_trajectory_val.shape} does not match observed trajectory shape {X_val.shape}"
                mse = np.mean((predicted_trajectory_val - X_val) ** 2)
            except Exception as e:
                logging.warning(f"Warning evaluating system {equations_str}: {e}")
            mse_vals.append(mse)
            complexities.append(system.complexity())
            equations_strs.append(equations_str)
        self.history = pd.DataFrame({'complexity': complexities, 'mse_val': mse_vals, 'system_str': equations_strs}).sort_values(by='mse_val')
        return


    def get_history(self):
        return self.history


def _logarithm_with_error(x):
    y = np.log(x)
    if np.any(~np.isfinite(y)):
        raise ValueError("log(x) is not finite")
    return y

def _exponential_with_error(x):
    y = np.exp(x)
    if np.any(~np.isfinite(y)):
        raise ValueError("exp(x) is not finite")
    return y

def _sqrt_with_error(x):
    y = np.sqrt(x)
    if np.any(~np.isfinite(y)):
        raise ValueError("sqrt(x) is not finite")
    return y

def _one_over_x_with_error(x):
    y = 1.0 / x
    if np.any(~np.isfinite(y)):
        raise ValueError("1/x is not finite")
    return y

def create_library(
    degree: Union[None, int] = 3,
    functions: Union[None, str, List[str]] = None,
):
    if functions is None:
        functions = ["sin", "cos", "exp", "log", "sqrt", "one_over_x"]
    elif isinstance(functions, str):
        functions = [functions]
    assert degree >= 0, f"Degree may not be negative but is {degree}."
    _basis_functions = {
        "sin": lambda x: np.sin(x),
        "cos": lambda x: np.cos(x),
        "exp": lambda x: _exponential_with_error(x),
        "log": lambda x: _logarithm_with_error(x),
        "sqrt": lambda x: _sqrt_with_error(x),
        "one_over_x": lambda x: _one_over_x_with_error(x),
        "square": lambda x: x ** 2,
        "abs": lambda x: np.abs(x),
    }
    _basis_function_names = {
        "sin": lambda x: f"* sin({x})",
        "cos": lambda x: f"* cos({x})",
        "exp": lambda x: f"* exp({x})",
        "log": lambda x: f"* log({x})",
        "sqrt": lambda x: f"* sqrt({x})",
        "one_over_x": lambda x: f"* 1/({x})",
        "square": lambda x: f"* ({x})^2",
        "abs": lambda x: f"* abs({x})",
    }

    libs = []
    if degree:
        libs.append(
            PolynomialLibrary(
                degree=int(degree),
                include_interaction=True,
                include_bias=True
            )
        )
    if len(functions) > 0:
        used_funcs = {}
        used_names = {}
        for f in functions:
            used_funcs[f] = _basis_functions[f]
            used_names[f] = _basis_function_names[f]
        custom_lib = CustomLibrary(
            library_functions=list(used_funcs.values()),
            function_names=list(used_names.values()),
        )
        libs.append(custom_lib)
    return ConcatLibrary(libs)

def _create_sindy_model(hp):
    optimizer_threshold = hp.get('optimizer_threshold')
    optimizer_alpha = hp.get('optimizer_alpha')
    max_iterations = hp.get('max_iterations')
    basis_functions = hp.get('basis_functions')
    polynomial_degree = hp.get('polynomial_degree')

    library = create_library(polynomial_degree, basis_functions)

    optimizer = ps.STLSQ(threshold=optimizer_threshold, alpha=optimizer_alpha, max_iter=max_iterations)
    return ps.SINDy(feature_library=library, optimizer=optimizer)

def _format_equation(expr: str) -> str:
        '''From https://github.com/sdascoli/odeformer'''
        # x0, x1, ... -> x_0, x_1, ...
        expr = re.sub(fr"(x)(\d)", repl=r"\1_\2", string=expr)
        # <coef> <space> 1 -> <coef> * 1
        expr = re.sub(r"(\d+\.?\d*) (1)", repl=r"\1 * \2", string=expr)
        # <coef> <space> <var> -> <coef> * <var>
        expr = re.sub(r"(\d+\.?\d*) (x_\d+)", repl=r"\1 * \2", string=expr)
        # <var> <space> <var> -> <coef> * <var>
        expr = re.sub(r"(x_\d+) (x_\d+)", repl=r"\1 * \2", string=expr)
        # python power symbol
        expr = expr.replace("^", "**")
        return expr

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=Path, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    save_dir = args.save_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    for problem in get_equations():
        true_system = System(problem['equation'])
        init_train = problem['init_train']
        init_test = problem['init_test']

        time_stamps_train = np.linspace(0, 5, 100)
        time_stamps_train_val = np.linspace(0, 10, 100)
        time_stamps_test = np.linspace(0, 10, 100)

        trajectory_train = true_system.evaluate_trajectory(init_train, time_stamps_train)
        observed_derivative_train = Diff(0, time_stamps_train[1] - time_stamps_train[0], acc=4)(trajectory_train)

        trajectory_train_val = true_system.evaluate_trajectory(init_train, time_stamps_train_val)
        observed_derivative_train_val = Diff(0, time_stamps_train_val[1] - time_stamps_train_val[0], acc=4)(trajectory_train_val)

        trajectory_test = true_system.evaluate_trajectory(init_test, time_stamps_test)
        observed_derivative_test = Diff(0, time_stamps_test[1] - time_stamps_test[0], acc=4)(trajectory_test)

        X_train = trajectory_train
        y_train = observed_derivative_train
        X_val = trajectory_train_val
        sindy = Sindy()
        sindy.train(X_train, y_train, X_val, t_train=time_stamps_train, t_val=time_stamps_train_val)
        history = sindy.get_history()

        mses_test = []
        nmse_test = []
        proposed_systems = history['system_str'].tolist()
        for proposed_system in proposed_systems:
            mse = np.nan
            nmse = np.nan
            try:
                predicted_trajectory_test = System(proposed_system).evaluate_trajectory(init_test, time_stamps_test)
                assert predicted_trajectory_test.shape == trajectory_test.shape, f"Predicted trajectory shape {predicted_trajectory_test.shape} does not match observed trajectory shape {trajectory_test.shape}"
                mse = np.mean((predicted_trajectory_test - trajectory_test) ** 2)
                nmse = np.mean((predicted_trajectory_test - trajectory_test) ** 2) / np.mean(trajectory_test ** 2)
            except Exception as e:
                logging.warning(f"Error evaluating system {proposed_system}: {e}")
            finally:
                mses_test.append(mse)
                nmse_test.append(nmse)
        history['mse_test'] = mses_test
        history['nmse_test'] = nmse_test
        columns = history.columns.tolist()
        columns[-2], columns[-1] = columns[-1], columns[-2]
        history = history[columns]
        filename = save_dir / f'{problem["name"]}.csv'
        Path(filename).parent.mkdir(parents=True, exist_ok=True)
        history.to_csv(filename, index=False)
