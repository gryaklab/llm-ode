from typing import List

import numpy as np

from llmode.program import Program, make_random_program


class Island:
    '''
    An island is a population of programs that are evolved together.
    '''
    def __init__(self, island_size: int, X: np.ndarray, y: np.ndarray):
        self.island_size = island_size
        self.programs = []
        while len(self.programs) < island_size:
            program = make_random_program(X, y)
            self.add_program(program)

    def replace_programs(self, old_programs: List[Program], new_programs: List[Program]):
        for i, old_program in enumerate(old_programs):
            self.programs[self.programs.index(old_program)] = new_programs[i]

    def add_program(self, program: Program):
        if program.score is None or np.isnan(program.score) or np.isinf(program.score):
            raise ValueError("Invalid program score: " + str(program.score) + " for program: " + str(program))
        self.add_programs([program])

    def add_programs(self, new_programs: List[Program]):
        new_programs = [p for p in new_programs if p not in self.programs]
        self.programs.extend(new_programs)

    def sample_programs(self, n_samples: int) -> List[Program]:
        n_samples = min(n_samples, len(self.programs))
        probs = np.array([-p.score for p in self.programs])
        probs = np.clip(probs, -10, 10)
        probs = np.exp(probs) / np.sum(np.exp(probs))
        if np.any(np.isnan(probs)) or np.any(np.isinf(probs)):
            raise ValueError("Invalid probabilities. Original probs: " + str([-p.score for p in self.programs]))
        samples = np.random.choice(self.programs, n_samples, replace=False, p=probs)
        samples = sorted(samples, key=lambda p: p.score, reverse=True)
        return samples

    def get_programs(self) -> List[Program]:
        return self.programs

    def trim_programs_(self, fraction: float = 0.5):
        """Trim the programs to keep only the top fraction of the programs"""
        programs = sorted(self.programs, key=lambda p: p.score)
        self.programs = programs[:int(len(programs) * fraction)]
