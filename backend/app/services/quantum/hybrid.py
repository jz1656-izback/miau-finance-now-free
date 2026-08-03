"""Hybrid quantum-classical algorithms."""

import logging
import random
import math

logger = logging.getLogger(__name__)


class HybridSolver:
    @staticmethod
    def vqe_solve(hamiltonian, n_layers=2, max_iter=100):
        n = len(hamiltonian)
        params = [random.uniform(-math.pi, math.pi) for _ in range(n_layers * n)]

        def energy(theta):
            e = 0.0
            for i in range(n):
                angle = sum(theta[k * n + i] for k in range(n_layers))
                e += hamiltonian[i][i] * math.cos(angle) ** 2
                for j in range(n):
                    if i != j:
                        e += hamiltonian[i][j] * math.sin(theta[i]) * math.cos(theta[j])
            return e

        lr = 0.01
        for _ in range(max_iter):
            grad = [0.0] * len(params)
            eps = 1e-4
            for idx in range(len(params)):
                p_plus, p_minus = list(params), list(params)
                p_plus[idx] += eps
                p_minus[idx] -= eps
                grad[idx] = (energy(p_plus) - energy(p_minus)) / (2 * eps)
            for idx in range(len(params)):
                params[idx] -= lr * grad[idx]
        return {"optimal_energy": round(float(energy(params)), 6), "n_parameters": len(params), "solver": "vqe"}

    @staticmethod
    def qaoa_solve(Q, p_layers=2):
        n = len(Q)
        opt_val = float("inf")
        opt_x = None
        for _ in range(50):
            x = [random.randint(0, 1) for _ in range(n)]
            for _ in range(p_layers):
                for i in range(n):
                    angle = sum(Q[i][j] * x[j] for j in range(n))
                    if random.random() < abs(math.sin(angle)):
                        x[i] = 1 - x[i]
            val = sum(Q[i][j] * x[i] * x[j] for i in range(n) for j in range(n))
            if val < opt_val:
                opt_val = val
                opt_x = x[:]
        return {"optimal_value": round(float(opt_val), 4), "solution": opt_x, "solver": "qaoa"}
