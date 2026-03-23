import argparse
import logging
from pathlib import Path
from itertools import product
from typing import Dict
from concurrent.futures import ProcessPoolExecutor

import pandas as pd
import numpy as np
from findiff import Diff
from pysr import PySRRegressor

from llmode.system import System
from data.dataset import get_equations


def evaluate_system(
        system_str: str,
        init_train: np.ndarray,
        time_stamps_train_val: np.ndarray,
        trajectory_train_val: np.ndarray,
        init_test: np.ndarray,
        time_stamps_test: np.ndarray,
        trajectory_test: np.ndarray) -> Dict:

        system = System(system_str)
        try:
            predicted_trajectory_train_val = system.evaluate_trajectory(init_train, time_stamps_train_val)
            mse_train_val = np.mean((predicted_trajectory_train_val - trajectory_train_val) ** 2)
            predicted_trajectory_test = system.evaluate_trajectory(init_test, time_stamps_test)
            mse_test = np.mean((predicted_trajectory_test - trajectory_test) ** 2)
            nmse_test = np.mean((predicted_trajectory_test - trajectory_test) ** 2) / np.mean(trajectory_test ** 2)
        except Exception as e:
            mse_train_val = np.nan
            mse_test = np.nan
            nmse_test = np.nan
            logging.warning(f"Error evaluating system {system}: {e}")
        result = {
            'complexity': system.complexity(),
            'mse_val': mse_train_val,
            'mse_test': mse_test,
            'nmse_test': nmse_test,
            'system_str': system.to_string(),
        }
        return result

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=Path, required=True)
    return parser.parse_args()

def run_baseline(problem: Dict, save_dir: Path):
    true_system = System(problem['equation'])
    init_train = problem['init_train']
    init_test = problem['init_test']

    time_stamps_train = np.linspace(0, 5, 100)
    time_stamps_train_val = np.linspace(0, 10, 100)
    time_stamps_test = np.linspace(0, 10, 100)

    trajectory_train = true_system.evaluate_trajectory(init_train, time_stamps_train)
    trajectory_train_val = true_system.evaluate_trajectory(init_train, time_stamps_train_val)
    trajectory_test = true_system.evaluate_trajectory(init_test, time_stamps_test)

    observed_derivative_train = Diff(0, time_stamps_train[1] - time_stamps_train[0], acc=4)(trajectory_train)

    pysr = PySRRegressor(
        binary_operators=['+', '-', '*', '/', '^'],
        unary_operators=['sin', 'log', 'exp', 'abs'],
        populations=4,
        population_size=20,
        ncycles_per_iteration=3,
        warm_start=True,
        temp_equation_file=f'/tmp/temp-pysr/{problem["name"]}.txt',

        # for reproducibility
        parallelism="serial",
        deterministic=True,
        random_state=42
    )

    total_iterations = 0
    for fit_iterations in [5, 45, 50, 50, 50]:
        total_iterations += fit_iterations

        pysr.set_params(niterations=fit_iterations)


        pysr.fit(trajectory_train, observed_derivative_train)
        pareto_fronts = pysr.get_hof()
        if isinstance(pareto_fronts, pd.DataFrame):
            pareto_fronts = [pareto_fronts]
        equations_list = [[eq.replace('x0', 'x_0').replace('x1', 'x_1').replace('x2', 'x_2').replace('x3', 'x_3') for eq in eq_list['equation'].tolist()] for eq_list in pareto_fronts]

        system_perfs = []
        with ProcessPoolExecutor(max_workers=20) as executor:
            futures = [
                executor.submit(evaluate_system,
                                ' | '.join(map(str, system_str)),
                                init_train,
                                time_stamps_train_val,
                                trajectory_train_val,
                                init_test,
                                time_stamps_test,
                                trajectory_test) for system_str in product(*equations_list)]
            for future in futures:
                system_perfs.append(future.result())
        system_perfs = pd.DataFrame(system_perfs)
        system_perfs = system_perfs.sort_values(by='mse_val')
        system_perfs.to_csv(save_dir / f'{problem["name"]}_iteration_{total_iterations}.csv', index=False)

if __name__ == "__main__":
    args = parse_args()
    save_dir = args.save_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    problems = get_equations()
    for problem in problems:
        run_baseline(problem, save_dir)
