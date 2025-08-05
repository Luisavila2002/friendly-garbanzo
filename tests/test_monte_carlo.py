from pathlib import Path
import sys

# Ensure the module under test is importable when tests are run directly
sys.path.append(str(Path(__file__).resolve().parents[1]))

from monte_carlo_risk import monte_carlo_var


def test_var_es_relationship():
    var, es = monte_carlo_var(num_sims=10000, seed=1)
    assert var >= 0
    assert es >= var


def test_deterministic_seed():
    var1, es1 = monte_carlo_var(num_sims=1000, seed=123)
    var2, es2 = monte_carlo_var(num_sims=1000, seed=123)
    assert var1 == var2
    assert es1 == es2
