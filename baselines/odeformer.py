
import logging
from pathlib import Path
from typing import Dict
import argparse

import pandas as pd
import numpy as np
import torch

from odeformer.model import SymbolicTransformerRegressor

from llmode.system import System
from data.dataset import get_equations

def run_baseline(problem: Dict, save_dir: Path):
    true_system = System(problem['equation'])
    init_train = problem['init_train']
    init_test = problem['init_test']

    time_stamps_train_val = np.linspace(0, 10, 100)
    time_stamps_test = np.linspace(0, 10, 100)

    trajectory_train_val = true_system.evaluate_trajectory(init_train, time_stamps_train_val)
    trajectory_test = true_system.evaluate_trajectory(init_test, time_stamps_test)

    dstr = SymbolicTransformerRegressor(from_pretrained=True)
    model_args = {'beam_size':50, 'beam_temperature':0.1}
    dstr.set_model_args(model_args)
    dstr.model = dstr.model.to("cuda:0")

    print("Fitting ODEFormer on problem: ", problem["name"])
    candidates = dstr.fit(time_stamps_train_val, trajectory_train_val)
    print("Done fitting ODEFormer on problem: ", problem["name"])
    systems = [System(str(candidate)) for candidate in candidates[0]]

    system_perfs = []
    for predicted_system in systems:
        mse_train_val = np.nan
        mse_test = np.nan
        nmse_test = np.nan
        try:
            predicted_trajectory_train_val = predicted_system.evaluate_trajectory(init_train, time_stamps_train_val)
            assert predicted_trajectory_train_val.shape == trajectory_train_val.shape, f"Predicted trajectory shape {predicted_trajectory_train_val.shape} does not match observed trajectory shape {trajectory_train_val.shape}"
            mse_train_val = np.mean((predicted_trajectory_train_val - trajectory_train_val) ** 2)
            predicted_trajectory_test = predicted_system.evaluate_trajectory(init_test, time_stamps_test)
            assert predicted_trajectory_test.shape == trajectory_test.shape, f"Predicted trajectory shape {predicted_trajectory_test.shape} does not match observed trajectory shape {trajectory_test.shape}"
            mse_test = np.mean((predicted_trajectory_test - trajectory_test) ** 2)
            nmse_test = np.mean((predicted_trajectory_test - trajectory_test) ** 2) / np.mean(trajectory_test ** 2)
        except Exception as e:
            logging.warning(f"Error evaluating system {predicted_system}: {e}")
        finally:
            complexity = predicted_system.complexity()
            system_perfs.append([complexity, mse_train_val, mse_test, nmse_test, str(predicted_system)])
            continue

    system_perfs = pd.DataFrame(system_perfs, columns=['complexity', 'mse_val', 'mse_test', 'nmse_test', 'system_str'])
    system_perfs = system_perfs.sort_values(by='mse_val')
    system_perfs.to_csv(save_dir / f'{problem["name"]}.csv', index=False)

def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--save_dir', type=Path, required=True)
    return parser.parse_args()

if __name__ == "__main__":
    args = parse_args()
    save_dir = args.save_dir
    save_dir.mkdir(parents=True, exist_ok=True)

    print("Available GPUs: ", torch.cuda.device_count())
    problems = get_equations()
    if not save_dir.exists():
        save_dir.mkdir(parents=True)
    for problem in problems:
        run_baseline(problem, save_dir)
