from typing import List, Dict

import numpy as np
from data.equations import equations

def get_equations() -> List[Dict]:
    eqs = []
    for eq_id, item in enumerate(equations):
        eq_name = item['name'].lower().replace(' ', '_').replace('/', '_')
        equation = item['eq']
        for i, const in enumerate(item['consts'][0]):
            equation = equation.replace(f'c_{i}', str(const))
        init_train = np.array(item['init'][0])
        init_test = np.array(item['init'][1])
        eqs.append({
            'id': eq_id,
            'name': eq_name,
            'equation': equation,
            'init_train': init_train,
            'init_test': init_test,
        })
    return eqs
