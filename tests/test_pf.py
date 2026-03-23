import pandas as pd

from llmode.utils import compute_pareto_frontier

def test_compute_pareto_frontier_1():
    df = pd.DataFrame({
        'm1': [1, 2, 3, 4, 5],
        'm2': [5, 4, 3, 2, 1],
        'm3': ['a', 'b', 'c', 'd', 'e'],
    })
    pareto_front = compute_pareto_frontier(df, ['m1', 'm2'])
    assert pareto_front.equals(df)

def test_compute_pareto_frontier_2():
    df = pd.DataFrame({
        'm1': [1, 2, 3, 4, 5],
        'm2': [5, 5, 5, 5, 5],
        'm3': ['a', 'b', 'c', 'd', 'e'],
    })
    pareto_front = compute_pareto_frontier(df, ['m1', 'm2'])
    assert pareto_front.equals(pd.DataFrame({
        'm1': [1],
        'm2': [5],
        'm3': ['a'],
    }))

def test_compute_pareto_frontier_3():
    df = pd.DataFrame({
        'm1': [2, 1, 3, 4, 3],
        'm2': [5, 5, 4, 5, 4],
        'm3': ['a', 'b', 'c', 'd', 'e'],
    })
    pareto_front = compute_pareto_frontier(df, ['m1', 'm2'])
    expected_pareto_front = pd.DataFrame({
        'm1': [1, 3],
        'm2': [5, 4],
        'm3': ['b', 'c'],
    }, index=[1, 2])
    assert pareto_front.equals(expected_pareto_front), f"Pareto front is not correct: {pareto_front}"