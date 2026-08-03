"""Quantum computing API — QUBO, annealing, hybrid optimization endpoints."""

import logging
from fastapi import APIRouter, Depends
from app.middleware.auth import get_current_user
from app.services.quantum.qubo import QUBOSolver
from app.services.quantum.annealing import AnnealingSolver
from app.services.quantum.hybrid import HybridSolver

logger = logging.getLogger(__name__)
router = APIRouter(prefix="/quantum", tags=["Quantum"])


@router.post("/portfolio")
async def quantum_portfolio(expected_returns: list[float], covariance: list[list[float]], gamma: float = 1.0, user=Depends(get_current_user)):
    qubo = QUBOSolver.portfolio_optimization(expected_returns, covariance, gamma)
    result = AnnealingSolver.solve_qubo(qubo["matrix"])
    result["problem"] = qubo
    return result


@router.post("/qubo/solve")
async def solve_qubo(Q: list[list[float]], num_reads: int = 10, use_dwave: bool = False, user=Depends(get_current_user)):
    return AnnealingSolver.solve_qubo(Q, num_reads=num_reads, use_dwave=use_dwave)


@router.post("/hybrid/vqe")
async def hybrid_vqe(hamiltonian: list[list[float]], n_layers: int = 2, max_iter: int = 100, user=Depends(get_current_user)):
    return HybridSolver.vqe_solve(hamiltonian, n_layers, max_iter)


@router.post("/hybrid/qaoa")
async def hybrid_qaoa(Q: list[list[float]], p_layers: int = 2, user=Depends(get_current_user)):
    return HybridSolver.qaoa_solve(Q, p_layers)


@router.get("/info")
async def quantum_info():
    return {
        "algorithms": ["QUBO", "Quantum Annealing", "VQE", "QAOA"],
        "backends": ["classical_simulator", "dwave_quantum_annealer"],
        "dwave_available": False,
        "problems": ["portfolio_optimization", "tsp", "risk_analysis", "option_pricing"],
    }
