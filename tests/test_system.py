import numpy as np
import pytest
import sympy as sp
from findiff import Diff


from llmode.system import System, make_random_system
from tests.utils import make_mock_program

def test_system_init():
    system = System("x_0 | x_1 | x_2")
    assert system.N == 3
    assert system.var_symbols == [sp.symbols(f"x_{i}") for i in range(3)]
    assert system.equations == [sp.sympify(f"x_{i}") for i in range(3)]

def test_1d_system():
    system = System("2 * x_0")
    assert system.N == 1

    t = np.linspace(0, 1, 100)
    trajectory = system.evaluate_trajectory(np.array([2]), t)
    assert trajectory.shape == (100, 1)

def test_system_optimize_coefficients_1():
    '''
    x(t) = exp(t)
    x(t)' = x(t)
    '''
    system = System("c_0 * x_0")

    t = np.linspace(0, 1, 100).reshape(-1, 1)
    trajectory = np.exp(t)
    derivative = np.exp(t)
    system.optimize_coefficients(trajectory, derivative)

    t = np.linspace(1, 2, 100).reshape(-1, 1)
    trajectory = np.exp(t)
    true_derivative = np.exp(t)
    diff = system.evaluate_derivative(trajectory) - true_derivative
    assert np.all(diff < 1e-4)

def test_system_optimize_coefficients_2():

    '''
    x(t) = exp(t)
    x(t)' = 3.14 *x(t)
    '''
    system = System("c_0 * x_0")

    t = np.linspace(0, 1, 100).reshape(-1, 1)
    trajectory = np.exp(t)
    derivative = 3.14 * np.exp(t)
    system.optimize_coefficients(trajectory, derivative)

    t = np.linspace(1, 2, 100).reshape(-1, 1)
    trajectory = np.exp(t)
    true_derivative = 3.14 * np.exp(t)
    diff = system.evaluate_derivative(trajectory) - true_derivative
    assert np.all(diff < 1e-6)

def test_system_optimize_coefficients_two_equations_1():
    '''
    x0(t) = 4 * sin(t)
    x1(t) = 10 * cos(t)

    x0(t)' = 4 * cos(t) = 0.4 * x1(t)
    x1(t)' = -10 * sin(t) = -2.5 * x0(t)
    '''
    system = System("c_0 * x_1 | c_1 * x_0")

    t = np.linspace(0, 1, 5)
    trajectory = np.array([4 * np.sin(t), 10 * np.cos(t)]).T
    derivative = np.array([4 * np.cos(t), -10 * np.sin(t)]).T

    system.optimize_coefficients(trajectory, derivative)

    t = np.linspace(1, 2, 5)
    trajectory = np.array([4 * np.sin(t), 10 * np.cos(t)]).T
    true_derivative = np.array([4 * np.cos(t), -10 * np.sin(t)]).T
    diff = system.evaluate_derivative(trajectory) - true_derivative
    assert np.all(diff < 1e-6)

def test_system_optimize_coefficients_two_equations_2():
    '''
    x0(t) = 4 * sin(t)
    x1(t) = 10 * cos(t)

    x0(t)' = 4 * cos(t) = 0.4 * x1(t)
    x1(t)' = -10 * sin(t) = -2.5 * x0(t)
    '''
    system = System("c_0 * x_0 + c_1 * x_1 | c_2 * x_0 + c_3 * x_1")

    t = np.linspace(0, 1, 5)
    trajectory = np.array([4 * np.sin(t), 10 * np.cos(t)]).T
    derivative = np.array([4 * np.cos(t), -10 * np.sin(t)]).T

    system.optimize_coefficients(trajectory, derivative)

    t = np.linspace(1, 2, 5)
    trajectory = np.array([4 * np.sin(t), 10 * np.cos(t)]).T
    true_derivative = np.array([4 * np.cos(t), -10 * np.sin(t)]).T
    diff = system.evaluate_derivative(trajectory) - true_derivative
    assert np.all(diff < 1e-6)

def test_system_optimize_coefficients_one_equation_nested_1():
    '''
    x0(t) = 1/(1 + exp(2- x0(t)/3))
    '''
    true_system = System("1/(1 + exp(2 - x_0/3))")
    t = np.linspace(0, 10, 1000)
    trajectory = true_system.evaluate_trajectory(np.array([1]), t)

    system = System("1/(1 + exp(c_0 - x_0/c_1))")
    derivative = Diff(0, t[1] - t[0])(trajectory)
    system.optimize_coefficients(trajectory, derivative)

    t_test = np.linspace(10, 20, 1000)
    trajectory_test = true_system.evaluate_trajectory(trajectory[-1], t_test)
    derivative = Diff(0, t_test[1] - t_test[0])(trajectory_test)
    diff = system.evaluate_derivative(trajectory_test) - derivative
    assert np.all(diff < 1e-3)

def test_system_optimize_coefficients_one_equation_nested_2():
    '''
    x0(t) = 0.5/(4 + exp(2- x0(t)/3))
    '''
    true_system = System("0.5/(4 + exp(2 - x_0/3))")
    t = np.linspace(0, 10, 1000)
    trajectory = true_system.evaluate_trajectory(np.array([1]), t)

    system = System("c_0/(c_1 + exp(c_2 - x_0/c_3))")
    derivative = Diff(0, t[1] - t[0])(trajectory)

    system.optimize_coefficients(trajectory, derivative)

    t_test = np.linspace(10, 20, 1000)
    trajectory_test = true_system.evaluate_trajectory(np.array([1]), t_test)
    derivative = Diff(0, t_test[1] - t_test[0])(trajectory_test)
    diff = system.evaluate_derivative(trajectory_test) - derivative
    assert np.all(diff < 1e-2)


def test_system_optimize_coefficients_three_equations():

    '''
    x0(t) = 2 * sin(x1(t)) + x2(t)**2
    x1(t) = 0.5 * cos(x2(t))
    x2(t) = 0.5 * sin(x1(t))
    '''
    true_system = System("2 * sin(x_1) + x_2^2 | 0.5 * cos(x_2) | 0.5 * sin(x_1)")
    t = np.linspace(0, 10, 1000)
    trajectory = true_system.evaluate_trajectory(np.array([1, 1, 1]), t)

    system = System("c_0 * sin(x_1) + x_2^2 | c_1 * cos(x_2) | c_2 * sin(x_1)")
    derivative = Diff(0, t[1] - t[0])(trajectory)

    system.optimize_coefficients(trajectory, derivative)

    t_test = np.linspace(10, 20, 1000)
    trajectory_test = true_system.evaluate_trajectory(trajectory[-1], t_test)
    derivative = Diff(0, t_test[1] - t_test[0])(trajectory_test)
    diff = system.evaluate_derivative(trajectory_test) - derivative
    assert np.all(diff < 0.02)

def test_system_get_skeleton():
    system = System("c_0*x_0 | c_1*x_1")
    assert system.get_skeleton() == "C*x_0 | C*x_1"

    system = System("3.1*x_0 | 3.14*x_1 | -0.1415*x_2")
    assert system.get_skeleton() == "C*x_0 | C*x_1 | C*x_2"

    system = System("3.1*x_0 | 3.14*x_1 | cos(3.1415*x_2) | 3.14159*x_3")
    assert system.get_skeleton() == "C*x_0 | C*x_1 | cos(C*x_2) | C*x_3"


    '''
    x0(t) = 4 * sin(t)
    x1(t) = 10 * cos(t)

    x0(t)' = 4 * cos(t) = 0.4 * x1(t)
    x1(t)' = -10 * sin(t) = -2.5 * x0(t)
    '''
    system = System("C * x_1 | C * x_0")

    t = np.linspace(0, 1, 5)
    trajectory = np.array([4 * np.sin(t), 10 * np.cos(t)]).T
    derivative = np.array([4 * np.cos(t), -10 * np.sin(t)]).T

    system.optimize_coefficients(trajectory, derivative)
    assert system.get_skeleton() == "C*x_1 | C*x_0"
