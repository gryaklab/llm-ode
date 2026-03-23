"""
Adapted from:
- https://github.com/sdascoli/odeformer/blob/main/odeformer/odebench/strogatz_equations.py
- https://juliadynamics.github.io/PredefinedDynamicalSystems.jl/dev/#PredefinedDynamicalSystems.jl
"""

equations = [
{
    'eq': '(c_0 - x_0 / c_1) / c_2',
    'dim': 1,
    'consts': [[0.7, 1.2, 2.31]],
    'init': [[10.], [3.54]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_1 > 0, c_2 > 0',
    'eq_description': 'RC-circuit (charging capacitor)',
    'name': 'RC-circuit',
    'const_description': 'c_0: fixed voltage source, c_1: capacitance, c_2: resistance',
    'var_description': 'x_0: charge',
    'source': 'strogatz p.20'
},
{
    'eq': 'c_0 * x_0',
    'dim': 1,
    'consts': [[0.23]],
    'init': [[4.78], [0.87]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': '',
    'eq_description': 'Population growth (naive)',
    'name': 'Population growth naive',
    'const_description': 'c_0: growth rate',
    'var_description': 'x_0: population',
    'source': 'strogatz p.22'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1)',
    'dim': 1,
    'consts': [[0.79, 74.3]],
    'init': [[7.3], [21.]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_1 > 0',
    'eq_description': 'Population growth with carrying capacity',
    'name': 'Population growth carrying capacity',
    'const_description': 'c_0: growth rate, c_1: carrying capacity',
    'var_description': 'x_0: population',
    'source': 'strogatz p.22'
},
{
    'eq': '1 / (1 + exp(c_0 - x_0 / c_1)) - 0.5',
    'dim': 1,
    'consts': [[0.5, 0.96]],
    'init': [[0.8], [0.02]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_1 > 0',
    'eq_description': 'RC-circuit with non-linear resistor (charging capacitor)',
    'name': 'RC-circuit non-linear resistor',
    'const_description': 'c_0: fixed voltage source, c_1: capacitance',
    'var_description': 'x_0: charge',
    'source': 'strogatz p.38'
},
{
    'eq': 'c_0 - c_1 * x_0^2',
    'dim': 1,
    'consts': [[9.81, 0.0021175]],
    'init': [[0.5], [73.]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Velocity of a falling object with air resistance',
    'name': 'Velocity falling object',
    'const_description': 'c_0: gravitational acceleration, c_1: overall drag for human: 0.5 * C * rho * A / m, with drag coeff C=0.7, air density rho=1.21, cross-sectional area A=0.25, mass m=50',
    'var_description': 'x_0: velocity',
    'source': 'strogatz p.38'
},
{
    'eq': 'c_0 * x_0 - c_1 * x_0^2',
    'dim': 1,
    'consts': [[2.1, 0.5]],
    'init': [[0.13], [2.24]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Autocatalysis with one fixed abundant chemical',
    'name': 'Autocatalysis',
    'const_description': 'c_0: concentration of abundant chemical A times the rate constant of A + X -> 2 X, c_1: rate constant of A + X -> 2X',
    'var_description': 'x_0: concentration of chemical X',
    'source': 'strogatz p.39'
},
{
    'eq': 'c_0 * x_0 * log(c_1 * x_0)',
    'dim': 1,
    'consts': [[0.032, 2.29]],
    'init': [[1.73], [9.5]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Gompertz law for tumor growth',
    'name': 'Gompertz law tumor growth',
    'const_description': 'c_0: growth rate, c_1: tumor carrying capacity',
    'var_description': 'x_0: proportional to number of cells (tumor size)',
    'source': 'strogatz p.39'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1) * (x_0 / c_2 - 1)',
    'dim': 1,
    'consts': [[0.14, 130., 4.4]],
    'init': [[6.123], [2.1]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Logistic equation with Allee effect',
    'name': 'Logistic equation Allee effect',
    'const_description': 'c_0: growth rate, c_1: carrying capacity, c_2: Allee effect parameter',
    'var_description': 'x_0: population',
    'source': 'strogatz p.39'
},
{
    'eq': '(1 - x_0) * c_0 - x_0 * c_1',
    'dim': 1,
    'consts': [[0.32, 0.28]],
    'init': [[0.14], [0.55]],
    'init_constraints': '0 < x_0 < 1',
    'const_constraints': 'c_0 >= 0, c_1 >= 0',
    'eq_description': 'Language death model for two languages',
    'name': 'Language death model',
    'const_description': 'c_0: rate of language 1 speakers switching to language 2, c_1: rate of language 2 speakers switching to language 1',
    'var_description': 'x_0: proportion of population speaking language 1',
    'source': 'strogatz p.40'
},
{
    'eq': '(1 - x_0) * c_0 * x_0^c_1 - x_0 * (1 - c_0) * (1 - x_0)^c_1',
    'dim': 1,
    'consts': [[0.2, 1.2]],
    'init': [[0.83], [0.34]],
    'init_constraints': '0 < x_0 < 1',
    'const_constraints': '0 <= c_0 <= 1, c_1 > 1',
    'eq_description': 'Refined language death model for two languages',
    'name': 'Refined language death model',
    'const_description': 'c_0: perceived status of language 1, c_1: adjustable exponent',
    'var_description': 'x_0: proportion of population speaking language 1',
    'source': 'strogatz p.40'
},
{
    'eq': '- x_0^3',
    'dim': 1,
    'consts': [[]],
    'init': [[3.4], [1.6]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Naive critical slowing down (statistical mechanics)',
    'name': 'Naive critical slowing down',
    'const_description': '',
    'var_description': 'x_0: order parameter',
    'source': 'strogatz p.41'
},
{
    'eq': 'c_0 * x_0 - c_1 * x_0^2',
    'dim': 1,
    'consts': [[1.8, 0.1107]],
    'init': [[11.], [1.3]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Photons in a laser (simple)',
    'name': 'Photons in a laser',
    'const_description': 'c_0: G * N0 - k, for G: gain coefficient, N0: initial excited atoms, k: loss rate, c_1: alpha * G, for G: gain coefficient, alpha: rate of atoms dropping back to ground state',
    'var_description': 'x_0: number of photons',
    'source': 'strogatz p.55'
},
{
    'eq': 'c_0 * sin(x_0) * (c_1 * cos(x_0) - 1)',
    'dim': 1,
    'consts': [[0.0981, 9.7]],
    'init': [[3.1], [2.4]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Overdamped bead on a rotating hoop',
    'name': 'Overdamped bead',
    'const_description': 'c_0: m * g, for m: mass, g: gravitational acceleration, c_1: r * omega^2 / g, for r: radius, omega: angular velocity',
    'var_description': 'x_0: angle',
    'source': 'strogatz p.63'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1) - c_3 * x_0^2 / (c_2^2 + x_0^2)',
    'dim': 1,
    'consts': [[0.78, 81., 21.2, 0.9]],
    'init': [[2.76], [23.3]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Budworm outbreak model with predation',
    'name': 'Budworm outbreak model',
    'const_description': 'c_0: growth rate, c_1: carrying capacity, c_2: predation onset, c_3: predation limit',
    'var_description': 'x_0: population',
    'source': 'strogatz p.75'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1) - x_0^2 / (1 + x_0^2)',
    'dim': 1,
    'consts': [[0.4, 95.]],
    'init': [[44.3], [4.5]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Budworm outbreak with predation (dimensionless)',
    'name': 'Budworm outbreak predation',
    'const_description': 'c_0: growth rate (<0.5 for young forest, 1 for mature), c_1: carrying capacity (~300 for young forest)',
    'var_description': 'x_0: population',
    'source': 'strogatz p.76'
},
{
    'eq': 'c_0 * x_0 - c_1 * x_0^3 - c_2 * x_0^5',
    'dim': 1,
    'consts': [[0.1, -0.04, 0.001]],
    'init': [[0.94], [1.65]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Landau equation (typical time scale tau = 1)',
    'name': 'Landau equation',
    'const_description': 'c_0: small dimensionless parameter, c_1: constant, c_2: constant; c_1 > 0 for supercritical bifurcation; c_1 < 0 and c_2 > 0 for subcritical bifurcation',
    'var_description': 'x_0: order parameter',
    'source': 'strogatz p.87'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1) - c_2',
    'dim': 1,
    'consts': [[0.4, 100., 0.3]],
    'init': [[14.3], [34.2]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 >= 0',
    'eq_description': 'Logistic equation with harvesting/fishing',
    'name': 'Logistic equation harvesting',
    'const_description': 'c_0: growth rate, c_1: carrying capacity, c_2: harvesting rate',
    'var_description': 'x_0: population',
    'source': 'strogatz p.89'
},
{
    'eq': 'c_0 * x_0 * (1 - x_0 / c_1) - c_2 * x_0 / (c_3 + x_0)',
    'dim': 1,
    'consts': [[0.4, 100., 0.24, 50.]],
    'init': [[21.1], [44.1]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Improved logistic equation with harvesting/fishing',
    'name': 'Improved logistic equation harvesting',
    'const_description': 'c_0: growth rate, c_1: carrying capacity, c_2: harvesting rate, c_3: harvesting onset',
    'var_description': 'x_0: population',
    'source': 'strogatz p.90'
},
{
    'eq': 'x_0 * (1 - x_0) - c_0 * x_0 / (c_1 + x_0)',
    'dim': 1,
    'consts': [[0.08, 0.8]],
    'init': [[0.13], [0.03]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Improved logistic equation with harvesting/fishing (dimensionless)',
    'name': 'Improved logistic equation harvesting dimensionless',
    'const_description': 'c_0: harvesting rate, c_1: harvesting onset',
    'var_description': 'x_0: population',
    'source': 'strogatz p.90'
},
{
    'eq': 'c_0 - c_1 * x_0 + x_0^2 / (1 + x_0^2)',
    'dim': 1,
    'consts': [[0.1, 0.55]],
    'init': [[0.002], [0.25]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 >= 0, c_1 > 0',
    'eq_description': 'Autocatalytic gene switching (dimensionless)',
    'name': 'Autocatalytic gene switching',
    'const_description': 'c_0: basal production rate, c_1: degradation rate',
    'var_description': 'x_0: gene product',
    'source': 'strogatz p.91'
},
{
    'eq': 'c_0 - c_1 * x_0 - exp(-x_0)',
    'dim': 1,
    'consts': [[1.2, 0.2]],
    'init': [[0.], [0.8]],
    'init_constraints': 'x_0 >= 0',
    'const_constraints': 'c_0 >= 1, c_1 > 0',
    'eq_description': 'Dimensionally reduced SIR infection model for dead people (dimensionless)',
    'name': 'Dimensionally reduced SIR',
    'const_description': 'c_0: death rate, c_1: unknown parameter group',
    'var_description': 'x_0: dead people',
    'source': 'strogatz p.92'
},
{
    'eq': 'c_0 + c_1 * x_0^5 / (c_2 + x_0^5) - c_3 * x_0',
    'dim': 1,
    'consts': [[1.4, 0.4, 123., 0.89]],
    'init': [[3.1], [6.3]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Hysteretic activation of a protein expression (positive feedback, basal promoter expression)',
    'name': 'Protein expression',
    'const_description': 'c_0: basal transcription rate, c_1: maximum transcription rate, c_2: activation coefficient, c_3: decay rate',
    'var_description': 'x_0: protein concentration',
    'source': 'strogatz p.93'
},
{
    'eq': 'c_0 - sin(x_0)',
    'dim': 1,
    'consts': [[0.21]],
    'init': [[-2.74], [1.65]],
    'init_constraints': '-pi <= x_0 <= pi',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Overdamped pendulum with constant driving torque/fireflies/Josephson junction (dimensionless)',
    'name': 'Overdamped pendulum',
    'const_description': 'c_0: ratio of driving torque to maximum gravitational torque',
    'var_description': 'x_0: angle',
    'source': 'strogatz p.104'
},
{
    'eq': '''
        x_1 |
        - c_0 * x_0
    ''',
    'dim': 2,
    'consts': [[2.1]],
    'init': [[0.4, -0.03], [0.0, 0.2]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Harmonic oscillator without damping',
    'name': 'Harmonic oscillator',
    'const_description': 'c_0: spring constant to mass ratio',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.126'
},
{
    'eq': '''
        x_1 |
        - c_0 * x_0 - c_1 * x_1
    ''',
    'dim': 2,
    'consts': [[4.5, 0.43]],
    'init': [[0.12, 0.043], [0.0, -0.3]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Harmonic oscillator with damping',
    'name': 'Harmonic oscillator damping',
    'const_description': 'c_0: spring constant to mass ratio, c_1: damping coefficient to mass ratio',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.144'
},
{
    'eq': '''
        x_0 * (c_0 - x_0 - c_1 * x_1) |
        x_1 * (c_2 - x_0 - x_1)
    ''',
    'dim': 2,
    'consts': [[3., 2., 2.]],
    'init': [[5.0, 4.3], [2.3, 3.6]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Lotka-Volterra competition model (Strogatz version with sheep and rabbits)',
    'name': 'Lotka-Volterra competition',
    'const_description': 'c_0: growth rate of rabbits, c_1: death rate of rabbits due to sheep, c_2: growth rate of sheep',
    'var_description': 'x_0: rabbits, x_1: sheep',
    'source': 'strogatz p.157'
},
{
    'eq': '''
        x_0 * (c_0 - c_1 * x_1) |
        - x_1 * (c_2 - c_3 * x_0)
    ''',
    'dim': 2,
    'consts': [[1.84, 1.45, 3.0, 1.62]],
    'init': [[8.3, 3.4], [0.4, 0.65]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Lotka-Volterra simple (as on Wikipedia)',
    'name': 'Lotka-Volterra simple',
    'const_description': 'c_0: growth rate of prey without predators, c_1: killing rate of prey due to predators, c_2: death rate of predators without prey, c_3: growth rate of predators per prey',
    'var_description': 'x_0: prey, x_1: predators',
    'source': 'https://en.wikipedia.org/wiki/Lotka-Volterra_equations'
},
{
    'eq': '''
        x_1 |
        - c_0 * sin(x_0)
    ''',
    'dim': 2,
    'consts': [[0.9]],
    'init': [[-1.9, 0.], [0.3, 0.8]],
    'init_constraints': '-pi <= x_0 <= pi',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Pendulum without friction',
    'name': 'Pendulum without friction',
    'const_description': 'c_0: gravitational acceleration to length ratio',
    'var_description': 'x_0: angle, x_1: angular velocity',
    'source': 'strogatz p.169'
},
{
    'eq': '''
        c_0 * x_0 * x_1 |
        x_1^2 - x_0^2
    ''',
    'dim': 2,
    'consts': [[0.65]],
    'init': [[3.2, 1.4], [1.3, 0.2]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Dipole fixed point',
    'name': 'Dipole fixed point',
    'const_description': 'c_0: constant',
    'var_description': 'x_0: x, x_1: y',
    'source': 'strogatz p.181'
},
{
    'eq': '''
        x_0 * (x_1 - c_0 * x_0 * x_1) |
        x_1 * (x_0 - c_0 * x_0 * x_1)
    ''',
    'dim': 2,
    'consts': [[1.61]],
    'init': [[0.3, 0.04], [0.1, 0.21]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'RNA molecules catalyzing each others replication',
    'name': 'Catalyzing RNA molecules',
    'const_description': 'c_0: catalytic rate',
    'var_description': 'x_0: concentration of molecule 1, x_1: concentration of molecule 2',
    'source': 'strogatz p.187'
},
{
    'eq': '''
        - c_0 * x_0 * x_1 |
        c_0 * x_0 * x_1 - c_1 * x_1
    ''',
    'dim': 2,
    'consts': [[0.4, 0.314]],
    'init': [[7.2, 0.98], [20., 12.4]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'SIR infection model only for healthy and sick',
    'name': 'SIR infection',
    'const_description': 'c_0: recovery rate, c_1: infection rate',
    'var_description': 'x_0: healthy, x_1: sick',
    'source': 'strogatz p.188'
},
{
    'eq': '''
        x_1 |
        - c_0 * x_1 + x_0 - x_0^3
    ''',
    'dim': 2,
    'consts': [[0.18]],
    'init': [[-1.8, -1.8], [5.8, 0.]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Damped double well oscillator',
    'name': 'Damped double well oscillator',
    'const_description': 'c_0: damping coefficient',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.190'
},
{
    'eq': '''
        - sin(x_1) - c_0 * x_0^2 |
        x_0 - cos(x_1) / x_0
    ''',
    'dim': 2,
    'consts': [[0.08]],
    'init': [[5.0, 0.7], [9.81, -0.8]],
    'init_constraints': 'x_0 > 0',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Glider (dimensionless)',
    'name': 'Glider',
    'const_description': 'c_0: drag coefficient',
    'var_description': 'x_0: speed, x_1: angle to horizontal',
    'source': 'strogatz p.190'
},
{
    'eq': '''
        x_1 | sin(x_0) * (cos(x_0) - c_0)
    ''',
    'dim': 2,
    'consts': [[0.93]],
    'init': [[2.1, 0.], [-1.2, -0.2]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Frictionless bead on a rotating hoop (dimensionless)',
    'name': 'Frictionless bead',
    'const_description': 'c_0: gravitational acceleration over radius times omega^2',
    'var_description': 'x_0: angle, x_1: angular velocity',
    'source': 'strogatz p.191'
},
{
    'eq': '''
        cot(x_1) * cos(x_0) |
        sin(x_0) * (cos(x_1)^2 + c_0 * sin(x_1)^2)
    ''',
    'dim': 2,
    'consts': [[4.2]],
    'init': [[1.13, -0.3], [2.4, 1.7]],
    'init_constraints': '-pi < x_0 <= pi, -pi / 2 <= x_1 <= pi / 2',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Rotational dynamics of an object in a shear flow',
    'name': 'Rotational dynamics',
    'const_description': 'c_0: shape dependent parameter',
    'var_description': 'x_0: longitude (angle around z-axis), x_1: latitue (angle from north)',
    'source': 'strogatz p.194'
},
{
    'eq': '''
        x_1 |
        - sin(x_0) - x_1 - c_0 * cos(x_0) * x_1
    ''',
    'dim': 2,
    'consts': [[0.07]],
    'init': [[0.45, 0.9], [1.34, -0.8]],
    'init_constraints': '-pi < x_o < pi',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Pendulum with non-linear damping, no driving (dimensionless)',
    'name': 'Pendulum non-linear damping',
    'const_description': 'c_0: Damping coefficient',
    'var_description': 'x_0: angle, x_1: angular velocity',
    'source': 'strogatz p.195'
},
{
    'eq': '''
        x_1 |
        - x_0 - c_0 * (x_0^2 - 1) * x_1
    ''',
    'dim': 2,
    'consts': [[0.43]],
    'init': [[2.2, 0.], [0.1, 3.2]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Van der Pol oscillator (standard form)',
    'name': 'Van der Pol oscillator',
    'const_description': 'c_0: damping parameter for nonlinear damping term',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.200'
},
{
    'eq': '''
        c_0 * (x_1 - x_0^3 / 3 + x_0) |
        - x_0 / c_0
    ''',
    'dim': 2,
    'consts': [[3.37]],
    'init': [[0.7, 0.], [-1.1, -0.7]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Van der Pol oscillator (simplified form from Strogatz)',
    'name': 'Van der Pol oscillator simplified',
    'const_description': 'c_0: damping parameter for nonlinear damping term',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.214'
},
{
    'eq': '''
        - x_0 + c_0 * x_1 + x_0^2 * x_1 |
        c_1 - c_0 * x_0 - x_0^2 * x_1
    ''',
    'dim': 2,
    'consts': [[2.4, 0.07]],
    'init': [[0.4, 0.31], [0.2, -0.7]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Glycolytic oscillator, e.g., ADP and F6P in yeast (dimensionless)',
    'name': 'Glycolytic oscillator',
    'const_description': 'c_0: kinetic parameter, c_1: kinetic parameter',
    'var_description': 'x_0: concentration of ADP, x_1: concentration of F6P',
    'source': 'strogatz p.207'
},
{
    'eq': '''
        x_1 |
        - x_0 + c_0 * x_1 * (1 - x_0^2)
    ''',
    'dim': 2,
    'consts': [[0.886]],
    'init': [[0.63, -0.03], [0.2, 0.2]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Duffing equation (weakly non-linear oscillation)',
    'name': 'Duffing equation',
    'const_description': 'c_0: parameter for cubic nonlinearity',
    'var_description': 'x_0: position, x_1: velocity',
    'source': 'strogatz p.217'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) * (c_1 + x_0^2) - x_0 |
        c_2 - x_0
    ''',
    'dim': 2,
    'consts': [[15.3, 0.001, 0.3]],
    'init': [[0.8, 0.3], [0.02, 1.2]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 1, 0 < c_1 < 1, c_2 > 0, 8 * c_0 * c_1 < 1',
    'eq_description': 'Cell cycle model by Tyson for interaction between protein cdc2 and cyclin (dimensionless)',
    'name': 'Cell cycle model',
    'const_description': 'c_0: parameter >> 1, c_1: parameter << 1, c_2: adjustable parameter',
    'var_description': 'x_0: concentration of cdc2, x_1: concentration of cyclin',
    'source': 'strogatz p.238'
},
{
    'eq': '''
        c_0 - x_0 - c_1 * x_0 * x_1 / (1 + x_0^2) |
        c_2 * x_0 * (1 - x_1 / (1 + x_0^2))
    ''',
    'dim': 2,
    'consts': [[8.9, 4.0, 1.4]],
    'init': [[0.2, 0.35], [3.0, 7.8]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Reduced model for chlorine dioxide-iodine-malonic acid reaction (dimensionless)',
    'name': 'CDIMA reaction',
    'const_description': 'c_0: empirical rate parameter, c_1: fixed to 4 by strogatz, c_2: empirical rate parameter',
    'var_description': 'x_0: dimensionless I- concentration, x_1: dimensionless ClO2 concentration',
    'source': 'strogatz p.260'
},
{
    'eq': '''
        x_1 |
        c_0 - sin(x_0) - c_1 * x_1
    ''',
    'dim': 2,
    'consts': [[1.67, 0.64]],
    'init': [[1.47, -0.2], [-1.9, 0.03]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Driven pendulum with linear damping / Josephson junction (dimensionless)',
    'name': 'Driven pendulum linear damping',
    'const_description': 'c_0: driving force/current, c_1: damping parameter',
    'var_description': 'x_0: angle, x_1: angular velocity',
    'source': 'strogatz p.269'
},
{
    'eq': '''
        x_1 |
        c_0 - sin(x_0) - c_1 * x_1 * abs(x_1)
    ''',
    'dim': 2,
    'consts': [[1.67, 0.64]],
    'init': [[1.47, -0.2], [-1.9, 0.03]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Driven pendulum with quadratic damping (dimensionless)',
    'name': 'Driven pendulum quadratic damping',
    'const_description': 'c_0: driving torque, c_1: damping parameter',
    'var_description': 'x_0: angle, x_1: angular velocity',
    'source': 'strogatz p.300'
},
{
    'eq': '''
        c_0 * (1 - x_0) - x_0 * x_1^2 |
        x_0 * x_1^2 - c_1 * x_1
    ''',
    'dim': 2,
    'consts': [[0.5, 0.02]],
    'init': [[1.4, 0.2], [0.32, 0.64]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Isothermal autocatalytic reaction model by Gray and Scott 1985 (dimensionless)',
    'name': 'Gray-Scott model',
    'const_description': 'c_0: rate constant, c_1: rate constant',
    'var_description': 'x_0: concentration 1, x_1: concentration 2',
    'source': 'strogatz p.288'
},
{
    'eq': '''
        c_0 * sin(x_0 - x_1) - sin(x_0) |
        c_0 * sin(x_1 - x_0) - sin(x_1)
    ''',
    'dim': 2,
    'consts': [[0.33]],
    'init': [[0.54, -0.1], [0.43, 1.21]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0',
    'eq_description': 'Interacting bar magnets',
    'name': 'Interacting bar magnets',
    'const_description': 'c_0: coupling constant',
    'var_description': 'x_0: angle of magnet 1, x_1: angle of magnet 2',
    'source': 'strogatz p.289'
},
{
    'eq': '''
        - x_0 + 1 / (1 + exp(c_0 * x_1 - c_1)) |
        - x_1 + 1 / (1 + exp(c_0 * x_0 - c_1))
    ''',
    'dim': 2,
    'consts': [[4.89, 1.4]],
    'init': [[0.65, 0.59], [3.2, 10.3]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Binocular rivalry model (no oscillations)',
    'name': 'Binocular rivalry model',
    'const_description': 'c_0: strength of mutual antagonism, c_1: strength of input stimulus',
    'var_description': 'x_0: perception of left eye stimulus, x_1: perception of right eye stimulus',
    'source': 'strogatz p.290'
},
{
    'eq': '''
        c_0 - x_0 - x_0 * x_1 / (1 + c_1 * x_0^2) |
        c_2 - x_0 * x_1 / (1 + c_1 * x_0^2)
    ''',
    'dim': 2,
    'consts': [[18.3, 0.48, 11.23]],
    'init': [[0.1, 30.4], [13.2, 5.21]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Bacterial respiration model for nutrients and oxygen levels',
    'name': 'Bacterial respiration model',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter',
    'var_description': 'x_0: concentration of nutrients, x_1: concentration of oxygen',
    'source': 'strogatz p.293'
},
{
    'eq': '''
        1 - (c_0 + 1) * x_0 + c_1 * x_0^2 * x_1 |
        c_0 * x_0 - c_1 * x_0^2 * x_1
    ''',
    'dim': 2,
    'consts': [[3.03, 3.1]],
    'init': [[0.7, -1.4], [2.1, 1.3]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Brusselator: hypothetical chemical oscillation model (dimensionless)',
    'name': 'Brusselator',
    'const_description': 'c_0: parameter, c_1: parameter',
    'var_description': 'x_0: concentration of X, x_1: concentration of Y',
    'source': 'strogatz p.296'
},
{
    'eq': '''
        c_0 - x_0 + x_0^2 * x_1 |
        c_1 - x_0^2 * x_1
    ''',
    'dim': 2,
    'consts': [[0.24, 1.43]],
    'init': [[0.14, 0.6], [1.5, 0.9]],
    'init_constraints': 'x_0 > 0, x_1 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Chemical oscillator model by Schnackenberg 1979 (dimensionless)',
    'name': 'Schnackenberg model',
    'const_description': 'c_0: parameter, c_1: parameter',
    'var_description': 'x_0: concentration of X, x_1: concentration of Y',
    'source': 'strogatz p.296'
},
{
    'eq': '''
        c_0 + sin(x_1) * cos(x_0) |
        c_1 + sin(x_1) * cos(x_0)
    ''',
    'dim': 2,
    'consts': [[1.432, 0.972]],
    'init': [[2.2, 0.67], [0.03, -0.12]],
    'init_constraints': '-pi < x_0 < pi, -pi < x_1 < pi',
    'const_constraints': 'c_0 > 0, c_1 > 0',
    'eq_description': 'Oscillator death model by Ermentrout and Kopell 1990',
    'name': 'Oscillator death model',
    'const_description': 'c_0: driving torque 1, c_1: driving torque 2',
    'var_description': 'x_0: angle 1, x_1: angle 2',
    'source': 'strogatz p.301'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        c_1 * (x_0 * x_2 - x_1) |
        c_2 * (c_3 + 1 - x_2 - c_3 * x_0 * x_1)
    ''',
    'dim': 3,
    'consts': [[0.1, 0.21, 0.34, 3.1]],
    'init': [[1.3, 1.1, 0.89], [0.89, 1.3, 1.1]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Maxwell-Bloch equations (laser dynamics)',
    'name': 'Maxwell-Bloch equations',
    'const_description': 'c_0: decay rate in cavity, c_1: decay rate atomic polarization, c_2: decay rate population inversion, c_3: pumping energy parameter',
    'var_description': 'x_0: E, x_1: P, x_2: D',
    'source': 'strogatz p.82'
},
{
    'eq': '''
        c_0 - c_5 * x_1 * x_0 / (c_9 + x_0) - c_4 * x_0 |
        c_1 * x_2 * (c_8 + x_1) - c_2 * x_1 / (c_6 + x_1) - c_3 * x_0 * x_1 / (c_7 + x_1) |
        - c_1 * x_2 * (c_8 + x_1) + c_2 * x_1 / (c_6 + x_1) + c_3 * x_0 * x_1 / (c_7 + x_1)
    ''',
    'dim': 3,
    'consts': [[0.1, 0.6, 0.2, 7.95, 0.05, 0.4, 0.1, 2.0, 0.1, 0.1]],
    'init': [[0.005, 0.26, 2.15], [0.248, 0.0973, 0.0027]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0, c_4 > 0, c_5 > 0, c_6 > 0, c_7 > 0, c_8 > 0, c_9 > 0',
    'eq_description': 'Model for apoptosis (cell death)',
    'name': 'Apoptosis model',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: parameter, c_4: parameter, c_5: parameter, c_6: parameter, c_7: parameter, c_8: parameter, c_9: parameter',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'https://epubs.siam.org/doi/10.1137/20M1318043',
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        c_1 * x_0 - x_1 - x_0 * x_2 |
        x_0 * x_1 - c_2 * x_2
    ''',
    'dim': 3,
    'consts': [[5.1, 12., 1.67]],
    'init': [[2.3, 8.1, 12.4], [10., 20., 30.]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Lorenz equations in well-behaved periodic regime',
    'name': 'Lorenz equations periodic',
    'const_description': 'c_0: Prandtl number (sigma), c_1: Rayleigh number (r), c_2: unnamed parameter (b)',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'strogatz p.319'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        c_1 * x_0 - x_1 - x_0 * x_2 |
        x_0 * x_1 - c_2 * x_2
    ''',
    'dim': 3,
    'consts': [[10., 99.96, 8. / 3.]],
    'init': [[2.3, 8.1, 12.4], [10., 20., 30.]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Lorenz equations in complex periodic regime',
    'name': 'Lorenz equations complex periodic',
    'const_description': 'c_0: Prandtl number (sigma), c_1: Rayleigh number (r), c_2: unnamed parameter (b)',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'strogatz p.319'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        c_1 * x_0 - x_1 - x_0 * x_2 |
        x_0 * x_1 - c_2 * x_2
    ''',
    'dim': 3,
    'consts': [[10., 28., 8. / 3.]],
    'init': [[2.3, 8.1, 12.4], [10., 20., 30.]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'Lorenz equations standard parameters (chaotic)',
    'name': 'Lorenz equations chaotic',
    'const_description': 'c_0: Prandtl number (sigma), c_1: Rayleigh number (r), c_2: unnamed parameter (b)',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'strogatz p.319'
},
{
    'eq': '''
        c_3 * (- x_1 - x_2) |
        c_3 * (x_0  + c_0 * x_1) |
        c_3 * (c_1 + x_2 * (x_0 - c_2))
    ''',
    'dim': 3,
    'consts': [[-0.2, 0.2, 5.7, 5.]],
    'init': [[2.3, 1.1, 0.8], [-0.1, 4.1, -2.1]],
    'init_constraints': '',
    'const_constraints': 'c_1 > 0, c_2 > 0',
    'eq_description': 'Rössler attractor (stable fixed point)',
    'name': 'Rössler fixed point',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: just for time scaling',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'https://en.wikipedia.org/wiki/Rössler_attractor',
},
{
    'eq': '''
        c_3 * (- x_1 - x_2) |
        c_3 * (x_0  + c_0 * x_1) |
        c_3 * (c_1 + x_2 * (x_0 - c_2))
    ''',
    'dim': 3,
    'consts': [[0.1, 0.2, 5.7, 5.]],
    'init': [[2.3, 1.1, 0.8], [-0.1, 4.1, -2.1]],
    'init_constraints': '',
    'const_constraints': 'c_1 > 0, c_2 > 0',
    'eq_description': 'Rössler attractor (periodic)',
    'name': 'Rössler attractor periodic',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: just for time scaling',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'https://en.wikipedia.org/wiki/Rössler_attractor',
},
{
    'eq': '''
        c_3 * (- x_1 - x_2) |
        c_3 * (x_0  + c_0 * x_1) |
        c_3 * (c_1 + x_2 * (x_0 - c_2))
    ''',
    'dim': 3,
    'consts': [[0.2, 0.2, 5.7, 5.]],
    'init': [[2.3, 1.1, 0.8], [-0.1, 4.1, -2.1]],
    'init_constraints': '',
    'const_constraints': 'c_1 > 0, c_2 > 0',
    'eq_description': 'Rössler attractor (chaotic)',
    'name': 'Rössler attractor chaotic',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: just for time scaling',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'https://en.wikipedia.org/wiki/Rössler_attractor',
},
{
    'eq': '''
        x_0 * (x_2 - c_1) - c_3 * x_1 |
        c_3 * x_0 + x_1 * (x_2 - c_1) |
        c_2 + c_0 * x_2 - x_2^3 / 3. - (x_0^2 + x_1^2) * (1 + c_4 * x_2) + c_5 * x_2 * x_0^3
    ''',
    'dim': 3,
    'consts': [[0.95, 0.7, 0.65, 3.5, 0.25, 0.1]],
    'init': [[0.1, 0.05, 0.05], [-0.3, 0.2, 0.1]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0, c_4 > 0',
    'eq_description': 'Aizawa attractor (chaotic)',
    'name': 'Aizawa attractor',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: parameter, c_4: parameter',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'https://analogparadigm.com/downloads/alpaca_17.pdf',
},
{
    'eq': '''
        c_0 * x_0 - x_1 * x_2 |
        c_1 * x_1 + x_0 * x_2 |
        c_2 * x_2 + x_0 * x_1 / c_3
    ''',
    'dim': 3,
    'consts': [[5.0, -10.0, -3.8, 3.0]],
    'init': [ [15, -15, -15], [8, 14, -10],],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Chen-Lee attractor; system for gyro motion with feedback control of rigid body (chaotic)',
    'name': 'Chen-Lee attractor',
    'const_description': 'c_0: parameter, c_1: parameter, c_2: parameter, c_3: fixed constant; parameters relate to principal moments of inertia',
    'var_description': 'x_0: omega_x, x_1: omega_y, x_2: omega_z; variables are essentially angular velocities',
    'source': 'https://doi.org/10.1016/j.chaos.2003.12.034'
},
{
    'eq':
        '''
        c_0 * x_0 - x_1 * x_2 |
        -c_1 * x_1 + x_0 * x_2 |
        c_2 - x_2 + x_0 * x_1
        ''',
    'dim': 3,
    'consts': [[0.119, 0.1, 0.9]],
    'init': [[3, 0.5, 1.5], [1.0, 1.0, 0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Gissinger chaotic reversals applied to study the reversals of the magnetic field of the Earth',
    'name': 'Gissinger chaotic reversals',
    'var_description': 'x_0: Q, x_1: D, x_2: V',
    'source': 'C. Gissinger, Eur. Phys. J. B 85, 4, pp 1-12 (2012)'
},
{
    'eq': '''
        c_0*x_0 - c_1*x_1 + c_2*x_0*x_2 + c_3*x_2*(x_0*x_0 + x_1*x_1) |
        c_0*x_1 + c_1*x_0 + c_2*x_2*x_1 |
        c_4 - x_2^2 - c_5*(x_0^2 + x_1^2) - c_0*x_2^3
    ''',
    'dim': 3,
    'consts': [[0.4, 20.25, 3, 1.6, 1.7, 0.44]],
    'init': [[-0.55582369, 0.05181624, 0.37766104], [-0.1, 0.4, 1]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Nonlinear oscillator with 3 states',
    'name': 'Nonlinear oscillator with 3 states',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'Guckenheimer, John, and Philip Holmes (1983). Nonlinear oscillations, dynamical systems, and bifurcations of vector fields. Vol. 42. Springer Science & Business Media.'
},
{
    'eq': '''
        -c_0*x_0 - c_1*(x_1 + x_2) - x_1^2 |
        -c_0*x_1 - c_1*(x_0 + x_2) - x_2^2 |
        -c_0*x_2 - c_1*(x_1 + x_0) - x_0^2
    ''',
    'dim': 3,
    'consts': [[1.4, 4]],
    'init': [[-8.6807408,-2.4741399,0.070775762], [-2.1, 2, 0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Sprott chaotic system',
    'name': 'Sprott chaotic system',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'Sprott, Julien C (2010). Elegant chaos: algebraically simple chaotic flows. World Scientific, 2010.'
},
{
    'eq': '''
        x_1 - c_0*x_0^3 + c_1*x_0^2 + c_7 - x_2 |
        c_2 - c_3*x_0^2 - x_1 |
        c_4*(c_5*(x_0 - c_6) - x_2)
    ''',
    'dim': 3,
    'consts': [[1, 3, 1, 5, 0.1, 4, -8/5, 2]], # c0: a, c1: b, c2: c, c3: d, c4: r, c5: s, c6: x_r, c7: I (applied current)
    'init': [[-1, 0, 0], [-0.5, 0.2, -1]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Hindmarsh-Rose model of the bursting behavior of a neuron\'s membrane potential',
    'name': 'Hindmarsh-Rose model',
    'var_description': 'x_0: x, x_1: y, x_2: z', # x: membrane potential, y: sodium and potassium ionic currents, z: adaptation current
    'source': 'J. L. Hindmarsh and R. M. Rose (1984) "A model of neuronal bursting using three coupled first order differential equations", Proc. R. Soc. Lond. B 221, 87-102.'
},
{
    'eq': '''
        -x_1^2 - x_2^2 - c_2 * x_0 + c_2 * c_0 |
        x_0 * x_1 - x_1 - c_3 * x_0 * x_2 + c_1 |
        c_3 * x_0 * x_1 + x_0 * x_2 - x_2
    ''',
    'dim': 3,
    'consts': [[6.846, 1.287, 0.25, 4.0]], # c0: F, c1: G, c2: a, c3: b
    'init': [[0.1, 0.1, 0.1], [-0.1, 0.2, 0.4]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': "Lorenz-84's low order atmospheric general circulation model with multistability property in the phase space.",
    'name': 'Lorenz-84 system',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'J. G. Freire et al, Multistability, phase diagrams, and intransitivity in the Lorenz-84 low-order atmospheric circulation model, Chaos 18, 033121 (2008)'
},
{
    'eq': '''
        x_1 - x_0 |
        -x_0 * x_2 |
        x_0 * x_1 - c_0
    ''',
    'dim': 3,
    'consts': [[4.7]],
    'init': [[5, 2.1, 0.1], [-2, -1.2, 0.4]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Diffusionless Lorenz system (probably the simplest rotationally invariant chaotic flow)',
    'name': 'Diffusionless Lorenz system',
    'const_description': '',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'J. C. Sprott, Simplest Chaotic Flows with Involutional Symmetries, Int. Jour. Bifurcation and Chaos 24, 1450009 (2014)'
},
{
    'eq': '''
        x_1 |
        -x_0 - sign(x_2) * x_1 |
        x_1^2 - exp(-x_0^2)
    ''',
    'dim': 3,
    'consts': [[]],
    'init': [[0.1, 0.1, 0.1], [-1.1, 0.2, -4]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A three-dimensional chaotic system noteworthy because its strange attractor is multifractal with a fractal dimension approximately equal to 3.',
    'name': 'Sprott multifractal system',
    'const_description': '',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'Sprott, J. C. (2020). Do We Need More Chaos Examples? Chaos Theory and Applications, 2(2), 1-3.'
},
{
    'eq': '''
        x_1 |
        x_1 * x_2 - x_0 |
        1 - x_1^2
    ''',
    'dim': 3,
    'consts': [[]],
    'init': [[0.0, 0.1, 0.0], [1.0, -1.0, 0.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Three dimensional conservative continuous system, discovered in 1984 during investigations in thermodynamical chemistry by Nosé and Hoover',
    'name': 'Nosé-Hoover system',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': "Hoover, W. G. (1995). Remark on 'Some simple chaotic flows'. Physical Review E, 51(1), 759."
},
{
    'eq': '''
        -c_0 * x_0 + x_1 * x_2 |
        -c_0 * x_1 + x_0 * (x_2 - c_1) |
        1 - x_0 * x_1
    ''',
    'dim': 3,
    'consts': [[1.0, 1.0]], # c0: mu, c1: alpha
    'init': [[1.0, 0.0, 0.6], [-1.0, 0.0, -0.6]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': "Rikitake's dynamo is a system that tries to model the magnetic reversal events by means of a double-disk dynamo system.",
    'name': "Rikitake's dynamo",
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'T. Rikitake Math. Proc. Camb. Phil. Soc. 54, pp 89-105, (1958)'
},
{
    'eq': '''
        c_0 * x_0 + x_1 + x_1 * x_2 |
        -x_0 * x_2 + x_1 * x_2 |
        -x_2 - c_2 * x_0 * x_1 + c_1
    ''',
    'dim': 3,
    'consts': [[1.0, 1.0, 1.0]],
    'init': [[-2.8976045, 3.8877978, 3.07465], [1.3, -4.342, 9]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A system presenting robust chaos that varies from single wing to double wings to four wings.',
    'name': 'Li system',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'Li, Chunbiao, et al (2015). A novel four-wing strange attractor born in bistability. IEICE Electronics Express 12.4.'
},
{
    'eq': '''
        x_1 + c_0 * x_0 * x_1 + x_0 * x_2 |
        1 - 2 * x_0^2 + c_1 * x_1 * x_2 |
        c_2 * x_0 - x_0^2 - x_1^2
    ''',
    'dim': 3,
    'consts': [[2.0, 1.0, 1.0]],
    'init': [[1.0, 0.0, 0.0], [2.0, 0.0, 0.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'An interesting system where certain initial conditions lead to quasi-periodic motion on a 2-torus, while others lead to motion on a dissipative chaotic attractor.',
    'name': 'Sprott dissipative-conservative system',
    'const_description': 'c_0: a, c_1: b, c_2: c',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'J. C. Sprott. Physics Letters A, 378'
},
{
    'eq': '''
        c_0 * (x_1 - (c_2 * x_0 + 0.5*(c_1 - c_2)*(Abs(x_0 + 1) - Abs(x_0 - 1)))) |
        x_0 - x_1 + x_2 |
        -c_3 * x_1
    ''',
    'dim': 3,
    'consts': [[15.6, 8/7, 5/7, 25.58]],
    'init': [[0.7, 0.1, -0.2], [3.23, 0.1, -7.2]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Chua chaotic circuit',
    'name': 'Chua chaotic circuit',
    'var_description': 'x_0: x, x_1: y, x_2: z',
    'source': 'Chua, L. O., Komuro, M., and Matsumoto, T. (1986) The double scroll family, IEEE Transactions on Circuits and Systems, 33 : 1072-1118'
},
{
    'eq': '''
        - x_0 + 1 / (1 + exp(c_0 * x_2 + c_1 * x_1 - c_2)) |
        c_3 * (x_0 - x_1) |
        - x_2 + 1 / (1 + exp(c_0 * x_0 + c_1 * x_3 - c_2)) |
        c_3 * (x_2 - x_3)
    ''',
    'dim': 4,
    'consts': [[0.89, 0.4, 1.4, 1.0]],
    'init': [[2.25, -0.5, -1.13, 0.4], [0.342, -0.431, -0.86, 0.041]],
    'init_constraints': 'x_0 > 0, x_1 > 0, x_2 > 0, x_3 > 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0',
    'eq_description': 'Binocular rivalry model with adaptation (oscillations)',
    'name': 'Binocular rivalry adaptation',
    'const_description': 'c_0: strength of mutual antagonism, c_1: influence of adaptation, c_2: strength of input stimulus, c_3: time scale of adaptation',
    'var_description': 'x_0: perception of left eye stimulus, x_1: adaptation of left eye stimulus, x_2: perception of right eye stimulus, x_3: adaptation of right eye stimulus',
    'source': 'strogatz p.295'
},
{
    'eq': '''
        - c_1 * x_0 * x_2 |
        c_1 * x_0 * x_2 - c_0 * x_1 |
        c_0 * x_1 - c_2 * x_2 |
        c_2 * x_2
    ''',
    'dim': 4,
    'consts': [[0.47, 0.28, 0.3]],
    'init': [[0.6, 0.3, 0.09, 0.01], [0.4, 0.3, 0.25, 0.05]],
    'init_constraints': '0 < x_0 < 1, 0 < x_1 < 1, 0 < x_2 < 1, 0 < x_3 < 1, x_1 + x_2 + x_3 + x_4 = 1',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'SEIR infection model (proportions)',
    'name': 'SEIR infection',
    'const_description': 'c_0: transfer rate rate, c_1: transmission rate, c_2: recovery rate',
    'var_description': 'x_0: susceptible, x_1: exposed, x_2: infected, x_3: recovered',
    'source': 'https://de.wikipedia.org/wiki/SEIR-Modell'
},
{
    'eq': '''
        x_2 |
        x_3 |
        -x_0 - 2*x_0*x_1 |
        -x_1 - x_0^2 + x_1^2
    ''',
    'dim': 4,
    'consts': [[]],
    'init': [[0, -0.25, 0.42081, 0], [0.3, -0.2, 0.28, 0.01]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Hénon-Heiles system: a conservative dynamical system, introduced as a simplification of the motion of a star around a galactic center',
    'name': 'Hénon-Heiles',
    'var_description': 'x_0: x, x_1: y, x_2: p_x, x_3: p_y',
    'source': 'Hénon & Heiles, The Astronomical Journal 69, pp 73-79 (1964)'
},
{
    'eq': '''
        c_0*(x_1 - x_0) + x_3 |
        c_2*x_1 - x_0*x_2 |
        x_0*x_1 - c_1*x_2 |
        c_4*x_0 - c_3*x_1*x_2
    ''',
    'dim': 4,
    'consts': [[36.0, 3.0, 20.5, 0.1, 21.0]],
    'init': [[5.0, 8.0, 12.0, 21.0], [9.0, 8.0, 5.8, 11.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A hyperchaotic attractor obtained from chaotic Lu system',
    'name': 'Hyperchaotic Lu system (Bo-Cheng & Zhong)',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Bo-Cheng, B., & Zhong, L. (2008). A hyperchaotic attractor coined from chaotic Lü system. Chinese Physics Letters, 25(7), 2396.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        c_1 * x_0 + c_2 * x_1 - x_0 * x_2 + x_3 |
        -c_3 * x_2 + x_1 * x_1 |
        -c_4 * x_0
    ''',
    'dim': 4,
    'consts': [[27.5, 3.0, 19.3, 2.9, 3.3]],
    'init': [[1.0, 8.0, 20.0, 10.0], [2.0, 5.0, 15.0, 17.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Hyperchaotic system derived from a finance model',
    'name': 'Cai-Huang hyperchaotic finance system',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Cai, G., & Huang, J. (2007). A new finance chaotic attractor. International Journal of Nonlinear Science, 3(3), 213-220.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) + x_3 |
        x_0 * (c_1 - x_2) - x_1 |
        x_0 * x_1 - c_2 * x_2 |
        c_3 * x_3 - x_0 * x_2
    ''',
    'dim': 4,
    'consts': [[10.0, 28.0, 8.0 / 3.0, 1.3]],
    'init': [[0.1, 0.1, 0.1, 0.1], [-10.0, -6.0, 0.0, 10.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'An extension of the Lorenz system showchasing hyperchaos',
    'name': 'Hyperchaotic Lorenz system (Hussain-Gondal-Hussain)',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Hussain, I., Gondal, M. A., & Hussain, A. (2015). Construction of dynamical non-linear components based on lorenz system and symmetric group of permutations. 3D Research, 6, 1-6.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) + x_3 |
        x_0 * (c_1 - x_2) - x_1 |
        x_0 * x_1 - c_2 * x_2 |
        c_3 * x_3 - x_1 * x_2
    ''',
    'dim': 4,
    'consts': [[10.0, 28.0, 8.0 / 3.0, -1.0]],
    'init': [[-10.0, -6.0, 0.0, 10.0], [4.0, 0.2, 0.0, -1.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Hyperchaotic extension of the classical Lorenz system',
    'name': 'Hyperchaotic Lorenz system (Wang-Wang)',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Wang, X., & Wang, M. (2008). A hyperchaos generated from Lorenz system. Physica A: Statistical Mechanics and its Applications, 387(14), 3751-3758.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) + x_3 |
        c_2 * x_1 - x_0 * x_2 |
        x_0 * x_1 - c_1 * x_2 |
        c_3 * x_3 + x_0 * x_2
    ''',
    'dim': 4,
    'consts': [[36.0, 3.0, 20.0, 1.3]],
    'init': [[5.0, 8.0, 12.0, 21.0], [0.2, -0.2, 0.2, 0.1]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A system showcasing hyperchaos obtained from the Lu system via state feedback control.',
    'name': 'Hyperchaotic Lu system (Chen-Lu-Lü-Yu)',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Chen, A., Lu, J., Lü, J., & Yu, S. (2006). Generating hyperchaotic Lü attractor via state feedback control. Physica A: Statistical Mechanics and its Applications, 364, 103-110.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        -x_0 * x_2 + c_2 * x_1 + x_3 |
        x_0 * x_1 - c_1 * x_2 |
        -c_3 * (x_0 + x_1)
    ''',
    'dim': 4,
    'consts': [[36.0, 3.0, 20.0, 2.0]],
    'init': [[1.0, 1.0, 10.0, 1.0], [0.2, -0.2, -0.2, -0.1]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A system showcasing hyperchaos obtained from the Lü system.',
    'name': 'Hyperchaotic Pang system',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Pang, S., & Liu, Y. (2011). Journal of Computational and Applied Mathematics, 235(8), 2775-2789.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) + x_1 * x_2 |
        c_1 * (x_0 + x_1) - x_0 * x_2 |
        -c_2 * x_2 - c_4 * x_3 + x_0 * x_1 |
        -c_3 * x_3 + c_5 * x_2 + x_0 * x_1
    ''',
    'dim': 4,
    'consts': [[5.0, 2.4, 1.3, 0.8, 3.3, 3.0]],
    'init': [[1.0, 1.5, 2.0, 2.2], [0.1, -3.1, 0.2, -0.1]],
    'init_constraints': '',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0, c_3 > 0, c_4 > 0, c_5 > 0',
    'eq_description': 'A hyperchaotic dynamical system showcasing rich bifurcations in different directions.',
    'name': 'Hyperchaotic Qi system',
    'const_description': 'c_0: a, c_1: b, c_2: c, c_3: d, c_4: e, c_5: f',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Qi, G., van Wyk, M. A., van Wyk, B. J., & Chen, G. (2008). Physics Letters A, 372(2), 124-136.'
},
{
    'eq': '''
        -x_1 - x_2 |
        x_0 + c_0 * x_1 + x_3 |
        c_1 + x_0 * x_2 |
        -c_2 * x_2 + c_3 * x_3
    ''',
    'dim': 4,
    'consts': [[0.25, 3.0, 0.5, 0.05]],
    'init': [[-10.0, -6.0, 0.0, 10.0], [-0.2, -6, 0, 11]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'An extension of the Rössler system showcasing hyperchaos.',
    'name': 'Hyperchaotic Rössler system',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Rossler, O. (1979). An equation for hyperchaos. Physics Letters A, 71(2-3), 155-157.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) |
        -x_0 * x_2 + c_1 * x_0 + x_3 |
        c_4 * x_0^2 - c_2 * x_2 |
        -c_3 * x_0
    ''',
    'dim': 4,
    'consts': [[10.0, 40.0, 2.5, 10.6, 4.0]],
    'init': [[5.0, 1.0, 30.0, 1.0], [1.0, 1.0, 1.0, 1.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'An extension of the Wang system showcasing hyperchaos.',
    'name': 'Hyperchaotic Wang system',
    'const_description': '',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Wang, Z., Sun, Y., van Wyk, B. J., Qi, G., & van Wyk, M. A. (2009). A 3-D four-wing attractor and its analysis. Brazilian Journal of Physics, 39, 547-553.'
},
{
    'eq': '''
        c_0 * (x_1 - x_0) + x_3 |
        c_1 * x_0 + c_4 * x_0 * x_2 |
        -c_2 * x_2 - x_0 * x_1 |
        x_0 * x_2 - c_3 * x_1
    ''',
    'dim': 4,
    'consts': [[10.0, 40.0, 2.5, 2.0, 16.0]],
    'init': [[2.0, -1.0, -2.0, -10.0], [-1.0, 1.0, 1.0,- 1.0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Hyperchaotic Xu system',
    'name': 'Hyperchaotic Xu system',
    'const_description': '',
    'var_description': 'x_0: x, x_1: y, x_2: z, x_3: w',
    'source': 'Letellier, C., & Rossler, O. E. (2007). Hyperchaos. Scholarpedia, 2(8), 1936.'
},
{
    'eq': '''
        x_1 / (c_0 + c_1) |
        (x_3^2 / (c_0*x_0^3)) - c_1 * 9.80665 + c_0 * 9.80665 * cos(x_2) |
        x_3 / (c_0 * x_0^2) |
        -c_0 * 9.80665 * x_0 * sin(x_2)
    ''',
    'dim': 4,
    'consts': [[1.0, 2]],
    'init': [[0.113296,1.5707963267948966,0.10992,0.17747], [0.6, 2.9, -0.1, 0.1]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'A mechanical system consisting of two swinging weights connected by ropes and pulleys',
    'name': "Swinging Atwood's machine",
    'var_description': 'x_0: r, x_1: p_r, x_2: theta, x_3: p_theta',
    'source': 'Tufillaro, Nicholas B.; Abbott, Tyler A.; Griffiths, David J. (1984). Swinging Atwood’s Machine. American Journal of Physics. 52 (10): 895–903.'
},
{
    'eq': '''
        -c_0 * x_3 * x_0 + c_1 * x_1 - c_2 * x_1 * x_0 + c_3 * x_2 |
        c_0 * x_3 * x_0 - c_1 * x_1 - c_3 * x_1 * x_0 + c_2 * x_2 |
        c_2 * x_1 * x_0 - c_3 * x_2 |
        -c_0 * x_3 * x_0 + c_1 * x_1
    ''',
    'dim': 4,
    'consts': [[0.01, 0.08, 0.03, 0.03]],
    'init': [[30.0, 0.0, 0.0, 10.0], [0.01, 0.08, 0.03, 0.03]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Kinetics of the Diels-Alder cross-linking and retro-Diels-Alder (rDA) de-cross-linking reactions',
    'name': 'Polymer DA cross-linking and rDA de-cross-linking',
    'const_description': 'c_0: k1_f, c_1: k1_r, c_2: k2_f, c_3: k2_r',
    'var_description': 'x_0: F, x_1: FMM, x_2: FMMF, x_3: MM',
    'source': 'Polgar, L. M., et al. "Kinetics of cross-linking and de-cross-linking of EPM rubber with thermoreversible Diels-Alder chemistry." European Polymer Journal 90 (2017): 150-161.'
},
{
    'eq':
        '''
        x_2 |
        x_3 |
        (-c_0*(c_1 + c_2)*sin(x_0) +  c_2*c_4*((x_3)^2)*sin(x_1-x_0)     + c_2*c_0*sin(x_1)*cos(x_1-x_0)       + c_2*c_3*((x_2)^2*sin(x_1-x_0)*cos(x_1-x_0))) / (c_3*(c_1 + c_2 - c_2*cos(x_1-x_0)*cos(x_1-x_0))) |
        (-c_0*(c_1 + c_2)*sin(x_1) + -c_3*(c_1 + c_2)*x_2^2*sin(x_1-x_0) + (c_1+c_2)*c_0*sin(x_0)*cos(x_1-x_0) - c_2*c_4*((x_3)^2*sin(x_1-x_0)*cos(x_1-x_0))) / (c_4*(c_1 + c_2 - c_2*cos(x_1-x_0)*cos(x_1-x_0)))
        ''',
    'dim': 4,
    'consts': [[9.81, 1.2, 1.1, .5, 1.9]],  # c0=g (gravity), c1=m1 (mass of first pendulum), c2=m2 (mass of second pendulum), c3=l1 (length of first rod), c4=l2 (length of second rod)
    'init': [[0.5, 0.5, 0, 0], [0.1, 0.2, 0, 0]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Double pendulum dynamics',
    'name': 'Double Pendulum',
    'var_description': 'x_0: theta1, x_1: theta2, x_2: theta1_dot, x_3: theta2_dot',
    'source': 'https://en.wikipedia.org/wiki/Double_pendulum#Equations_of_motion'
},
{
    'eq': '''
        -c_0 * x_0 * x_1 + c_1 * x_2 + c_2 * x_2 |
        -c_0 * x_0 * x_1 + c_1 * x_2 |
        c_0 * x_0 * x_1 - (c_1 + c_2) * x_2 |
        c_2 * x_2
    ''',
    'dim': 4,
    'consts': [[0.1, 0.024, 0.5]],
    'init': [[1.3, 1.2, 0.1, 0.05], [0.1, 0.2, 0.3, 0.4]],
    'init_constraints': 'x_0 >= 0, x_1 >= 0, x_2 >= 0, x_3 >= 0',
    'const_constraints': 'c_0 > 0, c_1 > 0, c_2 > 0',
    'eq_description': 'A fundamental biochemical model describing the rate of enzymatic reactions by relating reaction rate to the concentration of a substrate.',
    'name': 'Enzyme kinetics (Michaelis-Menten)',
    'const_description': 'c_0: k1 (forward), c_1: k_1 (reverse), c_2: k2 (catalytic)',
    'var_description': 'x_0: E (Enzyme), x_1: S (Substrate), x_2: ES (Complex), x_3: P (Product)',
    'source': 'Leonor Michaelis and Maud Menten (1913)'
},
{
    'eq': '''
        x_1 |
        (-c_0 * (x_1 - x_3) - c_1 * (x_0 - x_2)) / c_2 |
        x_3 |
        (c_4 - c_0 * (x_3 - x_1) - c_1 * (x_2 - x_0)) / c_3
    ''',
    'dim': 4,
    'consts': [[0.4, 0.28, 3, 2.5, 0.5]],
    'init': [[-1, -2, -0.5, -0.5], [-0.1, 0.3, 0.3, -0.4]],
    'init_constraints': '',
    'const_constraints': '',
    'eq_description': 'Two-mass spring system with damping and external force.',
    'name': 'Two-mass spring system with damping and external force',
    'const_description': 'c_0: b, c_1: k, c_2: m_1, c_3: m_2, c_4: constnat external force',
    'var_description': 'x_0: v1, x_1: a1, x_2: v2, x_3: a2',
    'source': 'Behl, M., Principles of Modeling for CPS, lecture notes, University of Virginia, 2019'
},
]