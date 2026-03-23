# import sys
# sys.setrecursionlimit(500)

import argparse
from typing import List
import logging
from pathlib import Path
from typing import Dict

from llmode.llm import Llm
from llmode.llmode import LlmOde
from data.dataset import get_equations


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument('--iters', type=int, default=200)
    parser.add_argument('--n_islands', type=int, default=4)
    parser.add_argument('--island_size', type=int, default=2)
    parser.add_argument('--k', type=int, default=8)
    parser.add_argument('--b', type=int, default=3)
    parser.add_argument('--results_dir', type=Path, required=True)
    parser.add_argument('--problem', type=str, required=True)
    parser.add_argument('--iters_per_refine', type=int, default=5)
    parser.add_argument('--save_iterations', type=int, nargs='+', default=None)
    parser.add_argument('--num_mixing', type=int, default=2)

    parser.add_argument('--openai_api_key', type=str, default='EMPTY')
    parser.add_argument('--openai_api_base', type=str, default='http://localhost:8000/v1')
    return parser.parse_args()

def run_experiment(args: Dict, problem: Dict, llm: Llm):
    config = {
        'n_islands': args.n_islands,
        'island_size': args.island_size,
        'k': args.k,
        'b': args.b,
        'iters_per_refine': args.iters_per_refine,
        'num_mixing': args.num_mixing,
    }
    llm_ode = LlmOde(llm=llm,
                     problem=problem,
                     results_dir=args.results_dir,
                     config=config)
    llm_ode.train(n_iterations=args.iters, save_iterations=args.save_iterations)


if __name__ == "__main__":
    args = parse_args()
    if not args.results_dir.exists():
        args.results_dir.mkdir(parents=True)

    # Configure logging with the logfile name from args
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s %(levelname)s %(message)s',
        handlers=[
            logging.FileHandler(args.results_dir / f'llm_ode.log'),
        ]
    )

    problems = get_equations()
    if args.problem == 'all':
        problems = problems
    else:
        problem_names = [x.strip().lower().replace(' ', '_').replace('/', '_') for x in args.problem.split(',')]
        problems = [p for p in problems if p['name'] in problem_names]

    llm = Llm(args.openai_api_key, args.openai_api_base)

    print("Problems:")
    for i, problem in enumerate(problems):
        print(f" {i+1}. {problem['name']}")
    for problem in problems:
        logging.info(f"Running experiment for problem {problem['id']}: {problem['name']}")
        try:
            run_experiment(args, problem, llm)
        except Exception as e:
            print(e)
            logging.error(f"Error running experiment for problem {problem['id']}: {problem['name']}: {e}")
