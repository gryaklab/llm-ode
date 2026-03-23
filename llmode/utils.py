import re
from typing import List

import numpy as np
import pandas as pd

def refine_generated_hypothesis(hypothesis: str) -> str:
    hypothesis = re.sub(r'(C[_]*[\d]+)', 'C', hypothesis)
    return hypothesis


def compute_pareto_frontier(df: pd.DataFrame, columns: List[str]) -> pd.DataFrame:
    '''
    Compute the Pareto frontier of a DataFrame assuming that we want to minimize two columns.
    Args:
        df: DataFrame
        columns: columns to compute the Pareto frontier of
    '''
    assert len(columns) == 2, "We only support computing the Pareto frontier of two columns"
    df = df.dropna(subset=columns)

    c1, c2 = columns
    data = df[[c1, c2]].copy()

    # Convert to maximize
    data[c1] = -data[c1]
    data[c2] = -data[c2]

    # Sort by first metric descending
    order = data[c1].sort_values(ascending=False).index
    data = data.loc[order]

    pareto_idx = []
    best_m2 = -np.inf

    for idx, row in data.iterrows():
        if row[c2] > best_m2:
            pareto_idx.append(idx)
            best_m2 = row[c2]

    return df.loc[pareto_idx]

if __name__ == "__main__":
    generated_hypothesis = [
        "C1*x_0 + C2*x_1",
        "C1*sin(x_0) + C2*cos(x_1)",
        "C1*sqrt(x_0) + C2*x_1",
        "C_1*sqrt(x_0) + C_2*x_1",
    ]
    for hypothesis in generated_hypothesis:
        refined_hypothesis = refine_generated_hypothesis(hypothesis)
        print(hypothesis, '->', refined_hypothesis)