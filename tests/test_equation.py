import sympy as sp
import numpy as np

from llmode.equation import Equation

np.random.seed(0)


def test_equation_init():
    X = np.linspace(0, 1, 10).reshape(-1, 1)
    y = 10*X + 2
    equation = Equation("C*x_0 + C", all_variables=["x_0"])
    assert equation.equation == sp.sympify("c_0*x_0 + c_1")
    assert equation.all_variables == ["x_0"]
    assert equation.variables == ["x_0"]
    assert equation.state_indice == [0]
    equation.optimize_coefficients(X, y)
    constants = equation.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [2, 10])


def test_equation_two_variables():
    X = np.random.rand(100, 2)
    y0 = 1.23*np.sin(X[:, 0])*np.log(X[:, 1])
    y1 = -9.23*X[:, 0]**2.34

    y = np.column_stack([y0, y1])
    eq1 = Equation("C*sin(x_0) * log(x_1)", all_variables=["x_0", "x_1"])
    eq2 = Equation("C*x_0**C", all_variables=["x_0", "x_1"])

    eq1.optimize_coefficients(X, y[:, 0])
    eq2.optimize_coefficients(X, y[:, 1])
    eq1(X)
    constants = eq1.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [1.23])
    constants = eq2.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [-9.23, 2.34], atol=1e-2)

def test_equation_three_variables():
    X = np.random.rand(100, 3)
    y0 = 1.23*np.sin(X[:, 1])
    y1 = (-9.23*X[:, 1]) / (X[:, 2] + 2.34)
    y2 = 8.23*np.sin(X[:, 2])

    y = np.column_stack([y0, y1, y2])
    eq1 = Equation("C*sin(x_1)", all_variables=["x_0", "x_1", "x_2"])
    eq2 = Equation("(C * x_1) / (x_2 + C)", all_variables=["x_0", "x_1", "x_2"])
    eq3 = Equation("C*sin(x_2)", all_variables=["x_0", "x_1", "x_2"])

    eq1.optimize_coefficients(X, y[:, 0])
    eq2.optimize_coefficients(X, y[:, 1])
    eq3.optimize_coefficients(X, y[:, 2])

    constants = eq1.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [1.23])

    constants = eq2.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [-9.23, -1, 2.34], atol=1e-2) # -1 is from the division

    constants = eq3.equation.atoms(sp.Number)
    assert np.allclose(sorted(constants), [8.23])

    y_pred = np.column_stack([eq1(X), eq2(X), eq3(X)])
    assert np.allclose(y, y_pred)

def test_equation_skeleton():
    eq1 = Equation("C*sin(x_0) * log(x_1**C)", all_variables=["x_0", "x_1"])
    eq2 = Equation("1.3*sin(x_0) * log(x_1**98)", all_variables=["x_0", "x_1"])
    assert eq1.get_skeleton() == eq2.get_skeleton()
    assert eq1 == eq2
