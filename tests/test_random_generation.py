import numpy as np
from python_anesthesia_simulator import simulator

# %% Initialization patient
ts = 5
age, height, weight, gender = 74, 164, 88, 1
np.random.seed(42)
george_nominal = simulator.Patient(
    [age, height, weight, gender],
    ts=ts,
)
george_random = simulator.Patient(
    [age, height, weight, gender],
    ts=ts,
    random_PK=True,
    random_PD=True,
)

# %% run a simple simulation
N_simu = int(60 * 60/ts)

uP, uR, uN = 0.15, 0.1, 2


for index in range(N_simu):
    george_nominal.one_step(
        u_propo=uP,
        u_remi=uR,
        u_nore=uN,
    )
    george_random.one_step(
        u_propo=uP,
        u_remi=uR,
        u_nore=uN,
    )


# %% Test function

def test_different_output():
    """Ensure that the random patient have different output than the nominal"""
    assert not np.allclose(george_nominal.dataframe['BIS'], george_random.dataframe['BIS'])
    assert not np.allclose(george_nominal.dataframe['MAP'], george_random.dataframe['MAP'])
    assert not np.allclose(george_nominal.dataframe['CO'], george_random.dataframe['CO'])
    assert not np.allclose(george_nominal.dataframe['TOL'], george_random.dataframe['TOL'])


def test_acceptable_random_output():
    """Ensure the physical feasibility of the output generated by the random patient."""
    assert np.all(george_random.dataframe['BIS'] <= 100)
    assert np.all(george_random.dataframe['BIS'] >= 0)
    assert np.all(george_random.dataframe['TOL'] <= 1)
    assert np.all(george_random.dataframe['TOL'] >= 0)
    assert np.all(george_random.dataframe['MAP'] <= 200)
    assert np.all(george_random.dataframe['MAP'] >= 0)
    assert np.all(george_random.dataframe['CO'] <= 20)
    assert np.all(george_random.dataframe['CO'] >= 0)
