import numpy as np

from llmode.program import Program
from llmode.system import System

def make_mock_program(system: str, score: np.ndarray):
    return Program(system=System(system), score=score)