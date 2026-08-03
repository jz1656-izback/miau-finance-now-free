"""QUBO formulation for finance problems."""

from typing import Optional


class QUBOSolver:
    @staticmethod
    def portfolio_optimization(expected_returns, covariance, gamma=1.0, n_assets=None):
        n = n_assets or len(expected_returns)
        Q = [[0.0] * n for _ in range(n)]
        for i in range(n):
            for j in range(n):
                Q[i][j] = gamma * covariance[i][j] - (expected_returns[i] if i == j else 0)
        return {"matrix": Q, "n_variables": n, "problem_type": "portfolio", "gamma": gamma}

    @staticmethod
    def solve_classical(Q, n_iterations=1000):
        import random
        n = len(Q)
        best_x = best_energy = None
        for _ in range(n_iterations):
            x = [random.randint(0, 1) for _ in range(n)]
            energy = sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            improved = True
            while improved:
                improved = False
                for i in range(n):
                    x[i] = 1 - x[i]
                    new_e = sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
                    if new_e < energy:
                        energy = new_e
                        improved = True
                    else:
                        x[i] = 1 - x[i]
            if best_energy is None or energy < best_energy:
                best_energy = energy
                best_x = x[:]
        return {"solution": best_x, "energy": round(best_energy, 4), "n_variables": n}
