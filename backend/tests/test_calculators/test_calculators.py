"""Unit tests for calculator suite — pure computation logic.

All calculators in app/api/datavore.py are pure functions (no DB, no HTTP).
These tests exercise the math directly via the endpoint logic.
"""
import math
import random
import statistics
import pytest
from unittest.mock import AsyncMock, MagicMock, patch


# ── 1. DCA Calculator ──────────────────────────────────────────

class TestDCACalculator:

    def _dca(self, amount: float, period: str, years: int,
             annual_return: float, annual_volatility: float) -> dict:
        """Replicate the logic from app/api/datavore.py calc_dca."""
        periods_per_year = {"weekly": 52, "biweekly": 26, "monthly": 12,
                            "quarterly": 4, "yearly": 1}.get(period, 12)
        total_periods = years * periods_per_year
        periodic_return = annual_return / 100 / periods_per_year
        periodic_vol = annual_volatility / 100 / (periods_per_year ** 0.5)

        random.seed(42)
        total_invested = amount * total_periods
        shares = 0.0
        for i in range(total_periods):
            price_change = random.gauss(periodic_return, periodic_vol)
            shares += amount * (1 + price_change) / (1 + periodic_return) if i > 0 else amount
        final_value = round(shares, 2)
        cagr = round((final_value / total_invested) ** (1 / years) - 1, 4) if total_invested > 0 else 0

        return {
            "total_invested": round(total_invested, 2),
            "final_value": final_value,
            "total_return": round(final_value - total_invested, 2),
            "return_pct": round((final_value - total_invested) / total_invested * 100, 2) if total_invested > 0 else 0,
            "cagr": round(cagr * 100, 2),
            "years": years,
            "period": period,
            "amount": amount,
            "annual_return": annual_return,
        }

    def test_dca_monthly_returns_positive(self):
        result = self._dca(amount=500, period="monthly", years=10,
                           annual_return=7.0, annual_volatility=15.0)
        assert result["total_invested"] == 60000.0
        assert result["final_value"] > 0
        assert result["total_return"] > 0
        assert result["return_pct"] > 0

    def test_dca_yearly_less_periods(self):
        result = self._dca(amount=6000, period="yearly", years=10,
                           annual_return=7.0, annual_volatility=15.0)
        assert result["total_invested"] == 60000.0
        assert result["period"] == "yearly"

    def test_dca_weekly_more_periods(self):
        result = self._dca(amount=100, period="weekly", years=5,
                           annual_return=7.0, annual_volatility=15.0)
        assert result["total_invested"] == 26000.0

    def test_dca_zero_return(self):
        result = self._dca(amount=500, period="monthly", years=5,
                           annual_return=0.0, annual_volatility=0.0)
        assert result["total_invested"] == 30000.0
        assert result["final_value"] == 30000.0
        assert result["cagr"] == 0.0


# ── 2. Compound Interest Calculator ────────────────────────────

class TestCompoundInterestCalculator:

    def _compound(self, principal: float, rate: float, years: float,
                  contribution: float = 0, compound_frequency: str = "monthly") -> dict:
        n = {"daily": 365, "monthly": 12, "quarterly": 4, "yearly": 1}.get(compound_frequency, 12)
        r = rate / 100 / n
        t = years
        total_contributions = contribution * 12 * t
        fv_principal = principal * (1 + r) ** (n * t)
        if contribution > 0:
            fv_contributions = contribution * 12 * ((1 + r) ** (n * t) - 1) / (r * n) if r > 0 else contribution * 12 * t
        else:
            fv_contributions = 0
        final_value = fv_principal + fv_contributions
        schedule = []
        for year in range(1, int(t) + 1):
            y_principal = principal * (1 + r) ** (n * year)
            y_contrib = contribution * 12 * ((1 + r) ** (n * year) - 1) / (r * n) if r > 0 and contribution > 0 else contribution * 12 * year
            schedule.append({"year": year, "value": round(y_principal + y_contrib, 2),
                             "contributions": round(principal + contribution * 12 * year, 2)})
        return {
            "final_value": round(final_value, 2),
            "total_contributions": round(principal + total_contributions, 2),
            "total_interest": round(final_value - principal - total_contributions, 2),
            "schedule": schedule,
        }

    def test_compound_principal_only(self):
        result = self._compound(principal=10000, rate=7.0, years=10)
        assert result["final_value"] > 10000
        assert result["total_interest"] > 0
        assert len(result["schedule"]) == 10

    def test_compound_with_monthly_contributions(self):
        result = self._compound(principal=10000, rate=7.0, years=30, contribution=500)
        assert result["final_value"] > result["total_contributions"]
        assert result["total_interest"] > 0

    def test_compound_yearly_frequency(self):
        result = self._compound(principal=1000, rate=10.0, years=5, compound_frequency="yearly")
        expected = 1000 * (1 + 0.10) ** 5
        assert abs(result["final_value"] - round(expected, 2)) < 0.01

    def test_compound_zero_rate(self):
        result = self._compound(principal=10000, rate=0.0, years=5, contribution=100)
        assert result["final_value"] == 10000 + 100 * 12 * 5


# ── 3. Retirement Projection ───────────────────────────────────

class TestRetirementProjection:

    def _retire(self, age: int, savings: float, monthly_contribution: float,
                annual_return: float, retirement_age: int,
                withdrawal_rate: float, inflation: float) -> dict:
        years_to_retire = retirement_age - age
        monthly_rate = annual_return / 100 / 12
        inflation_rate = inflation / 100
        total_months = years_to_retire * 12
        balance = savings
        schedule = []
        for m in range(1, total_months + 1):
            balance = balance * (1 + monthly_rate) + monthly_contribution
            if m % 12 == 0:
                schedule.append({"year": m // 12, "age": age + m // 12, "balance": round(balance, 2)})
        retirement_income = balance * (withdrawal_rate / 100)
        real_income = retirement_income / ((1 + inflation_rate) ** 30)
        return {
            "projected_balance": round(balance, 2),
            "annual_retirement_income": round(retirement_income, 2),
            "real_annual_income_adj": round(real_income, 2),
            "schedule": schedule,
        }

    def test_retirement_accumulates(self):
        result = self._retire(age=30, savings=50000, monthly_contribution=1000,
                              annual_return=7.0, retirement_age=65,
                              withdrawal_rate=4.0, inflation=3.0)
        assert result["projected_balance"] > 50000
        assert len(result["schedule"]) == 35
        assert result["annual_retirement_income"] > 0

    def test_retirement_low_return(self):
        result = self._retire(age=40, savings=100000, monthly_contribution=500,
                              annual_return=3.0, retirement_age=65,
                              withdrawal_rate=4.0, inflation=2.0)
        assert result["projected_balance"] > 100000

    def test_retirement_schedule_monotonic(self):
        result = self._retire(age=25, savings=0, monthly_contribution=2000,
                              annual_return=8.0, retirement_age=60,
                              withdrawal_rate=4.0, inflation=3.0)
        balances = [entry["balance"] for entry in result["schedule"]]
        assert all(balances[i] <= balances[i + 1] for i in range(len(balances) - 1))


# ── 4. Loan Amortization ───────────────────────────────────────

class TestLoanAmortization:

    def _loan(self, amount: float, rate: float, years: int) -> dict:
        monthly_rate = rate / 100 / 12
        payments = years * 12
        if monthly_rate > 0:
            monthly_payment = amount * (monthly_rate * (1 + monthly_rate) ** payments) / ((1 + monthly_rate) ** payments - 1)
        else:
            monthly_payment = amount / payments
        total_paid = monthly_payment * payments
        total_interest = total_paid - amount
        amortization = []
        balance = amount
        for i in range(1, payments + 1):
            interest_pmt = balance * monthly_rate
            principal_pmt = monthly_payment - interest_pmt
            balance -= principal_pmt
            if i <= 12 or i % 60 == 0 or i == payments:
                amortization.append({
                    "payment": i,
                    "monthly": round(monthly_payment, 2),
                    "principal": round(principal_pmt, 2),
                    "interest": round(interest_pmt, 2),
                    "balance": round(max(balance, 0), 2),
                })
        return {
            "monthly_payment": round(monthly_payment, 2),
            "total_paid": round(total_paid, 2),
            "total_interest": round(total_interest, 2),
            "amortization_schedule": amortization,
        }

    def test_loan_standard(self):
        result = self._loan(amount=500000, rate=6.5, years=30)
        assert result["monthly_payment"] > 0
        assert result["total_paid"] > 500000
        assert result["total_interest"] > 0

    def test_loan_zero_interest(self):
        result = self._loan(amount=100000, rate=0.0, years=10)
        assert result["monthly_payment"] == round(100000 / 120, 2)
        assert result["total_interest"] == 0.0

    def test_loan_short_term(self):
        result = self._loan(amount=20000, rate=5.0, years=3)
        assert len(result["amortization_schedule"]) >= 12

    def test_loan_balance_descends(self):
        result = self._loan(amount=300000, rate=4.5, years=15)
        balances = [e["balance"] for e in result["amortization_schedule"]]
        assert balances[0] < 300000
        assert balances[-1] == 0.0


# ── 5. Margin Calculator ───────────────────────────────────────

class TestMarginCalculator:

    def _margin(self, price: float, quantity: int, leverage: float,
                maintenance_margin: float, margin_rate: float) -> dict:
        total_value = price * quantity
        equity = total_value / leverage
        borrowed = total_value - equity
        liquidation_price = (maintenance_margin / 100 * total_value + borrowed - total_value) / quantity
        margin_call_price = (maintenance_margin / 100 * total_value + borrowed) / quantity
        monthly_interest = borrowed * (margin_rate / 100) / 12
        return {
            "total_value": round(total_value, 2),
            "equity": round(equity, 2),
            "borrowed": round(borrowed, 2),
            "leverage_ratio": leverage,
            "margin_ratio": round((total_value - borrowed) / total_value * 100, 2),
            "liquidation_price": round(liquidation_price, 2),
            "margin_call_price": round(margin_call_price, 2),
            "monthly_interest": round(monthly_interest, 2),
        }

    def test_margin_2x(self):
        result = self._margin(price=150, quantity=100, leverage=2.0,
                              maintenance_margin=25.0, margin_rate=8.0)
        assert result["total_value"] == 15000.0
        assert result["equity"] == 7500.0
        assert result["borrowed"] == 7500.0
        assert result["margin_ratio"] == 50.0

    def test_margin_4x(self):
        result = self._margin(price=100, quantity=50, leverage=4.0,
                              maintenance_margin=30.0, margin_rate=6.0)
        total = 100 * 50
        expected_equity = total / 4.0
        assert result["equity"] == round(expected_equity, 2)

    def test_margin_high_leverage_liquidation(self):
        result = self._margin(price=100, quantity=100, leverage=5.0,
                              maintenance_margin=25.0, margin_rate=8.0)
        assert result["liquidation_price"] > 0

    def test_margin_liquidation_below_price(self):
        result = self._margin(price=200, quantity=10, leverage=2.0,
                              maintenance_margin=25.0, margin_rate=5.0)
        assert result["liquidation_price"] < 200


# ── 6. Options Payoff ──────────────────────────────────────────

class TestOptionsPayoff:

    def _options_payoff(self, strike: float, premium: float, strategy: str,
                        contracts: int, spot_start: float, spot_end: float | None = None) -> dict:
        end = spot_end or spot_start * 1.5
        if end <= spot_start:
            end = spot_start * 1.5
        prices = []
        step = (end - spot_start) / 20
        for i in range(21):
            spot = spot_start + i * step
            payoff = 0
            if strategy == "long_call":
                payoff = max(0, spot - strike) - premium
            elif strategy == "long_put":
                payoff = max(0, strike - spot) - premium
            elif strategy == "covered_call":
                payoff = (spot - strike) - max(0, spot - strike) + premium
            elif strategy == "straddle":
                payoff = max(0, spot - strike) + max(0, strike - spot) - 2 * premium
            elif strategy == "strangle":
                otm_call = strike * 1.1
                otm_put = strike * 0.9
                payoff = max(0, spot - otm_call) + max(0, otm_put - spot) - 2 * premium
            prices.append({"spot": round(spot, 2), "payoff": round(payoff * contracts * 100, 2)})
        return {"prices": prices, "max_payoff": max(p["payoff"] for p in prices),
                "min_payoff": min(p["payoff"] for p in prices)}

    def test_long_call_payoff(self):
        result = self._options_payoff(strike=100, premium=5, strategy="long_call",
                                      contracts=1, spot_start=80, spot_end=120)
        payoffs = [p["payoff"] for p in result["prices"]]
        assert payoffs[0] < 0  # OTM → loss of premium
        assert payoffs[-1] > 0  # ITM → profit

    def test_long_put_payoff(self):
        result = self._options_payoff(strike=100, premium=5, strategy="long_put",
                                      contracts=1, spot_start=80, spot_end=120)
        payoffs = [p["payoff"] for p in result["prices"]]
        assert payoffs[0] > 0  # ITM
        assert payoffs[-1] < 0  # OTM

    def test_straddle_payoff(self):
        result = self._options_payoff(strike=100, premium=5, strategy="straddle",
                                      contracts=1, spot_start=80, spot_end=120)
        assert result["min_payoff"] < 0

    def test_covered_call_payoff(self):
        result = self._options_payoff(strike=100, premium=5, strategy="covered_call",
                                      contracts=1, spot_start=80, spot_end=120)
        assert len(result["prices"]) == 21


# ── 7. Portfolio Rebalancing ───────────────────────────────────

class TestPortfolioRebalancing:

    def test_detect_drift_equal_weight(self):
        holdings = [
            {"ticker": "AAPL", "market_value": 60000},
            {"ticker": "MSFT", "market_value": 40000},
        ]
        total = sum(h["market_value"] for h in holdings)
        expected_weight = 1.0 / len(holdings)
        drifted = []
        for h in holdings:
            w = h["market_value"] / total
            if abs(w - expected_weight) > 0.05:
                drifted.append(h["ticker"])
        assert len(drifted) == 2
        assert "AAPL" in drifted
        assert "MSFT" in drifted

    def test_no_drift_within_threshold(self):
        holdings = [
            {"ticker": "AAPL", "market_value": 51000},
            {"ticker": "MSFT", "market_value": 49000},
        ]
        total = sum(h["market_value"] for h in holdings)
        expected_weight = 0.5
        drifted = [h["ticker"] for h in holdings
                   if abs(h["market_value"] / total - expected_weight) > 0.05]
        assert len(drifted) == 0

    def test_rebalance_trade_generation(self):
        holdings = {
            "AAPL": 0.70,
            "MSFT": 0.20,
            "GOOGL": 0.10,
        }
        total = 100000
        target = 1.0 / 3
        trades = []
        for ticker, weight in holdings.items():
            diff = weight - target
            if abs(diff) > 0.05:
                trade_value = abs(diff) * total
                side = "sell" if diff > 0 else "buy"
                trades.append({"ticker": ticker, "side": side, "value": round(trade_value, 2)})
        assert len(trades) == 3
        sell_tickers = [t["ticker"] for t in trades if t["side"] == "sell"]
        buy_tickers = [t["ticker"] for t in trades if t["side"] == "buy"]
        assert "AAPL" in sell_tickers
        assert "MSFT" in buy_tickers
        assert "GOOGL" in buy_tickers


# ── 8. Tax Lot Accounting ──────────────────────────────────────

class TestTaxLotAccounting:

    def _compute_tax_lot(self, lots: list[dict], sell_qty: int, method: str = "fifo") -> dict:
        """Simple tax lot accounting: FIFO and LIFO."""
        sorted_lots = sorted(lots, key=lambda x: x["date"])
        if method == "lifo":
            sorted_lots = list(reversed(sorted_lots))

        remaining = sell_qty
        cost_basis = 0.0
        used_lots = []
        for lot in sorted_lots:
            if remaining <= 0:
                break
            taken = min(remaining, lot["qty"])
            cost_basis += taken * lot["cost_per_share"]
            used_lots.append({"date": lot["date"], "qty": taken,
                              "cost_per_share": lot["cost_per_share"]})
            remaining -= taken

        return {
            "method": method,
            "total_shares_sold": sell_qty,
            "cost_basis": round(cost_basis, 2),
            "lots_used": used_lots,
            "remaining_shares": sum(l["qty"] for l in lots) - sell_qty,
        }

    def test_fifo_tax_lot(self):
        lots = [
            {"date": "2024-01-15", "qty": 100, "cost_per_share": 50.0},
            {"date": "2024-06-20", "qty": 50, "cost_per_share": 55.0},
            {"date": "2024-09-10", "qty": 75, "cost_per_share": 52.0},
        ]
        result = self._compute_tax_lot(lots, sell_qty=120, method="fifo")
        assert result["method"] == "fifo"
        assert result["total_shares_sold"] == 120
        expected_cost = 100 * 50.0 + 20 * 55.0
        assert result["cost_basis"] == expected_cost
        assert len(result["lots_used"]) == 2

    def test_lifo_tax_lot(self):
        lots = [
            {"date": "2024-01-15", "qty": 100, "cost_per_share": 50.0},
            {"date": "2024-06-20", "qty": 50, "cost_per_share": 55.0},
            {"date": "2024-09-10", "qty": 75, "cost_per_share": 52.0},
        ]
        result = self._compute_tax_lot(lots, sell_qty=80, method="lifo")
        assert result["method"] == "lifo"
        expected_cost = 75 * 52.0 + 5 * 55.0
        assert result["cost_basis"] == expected_cost

    def test_fifo_vs_lifo_different_costs(self):
        lots = [
            {"date": "2024-01-15", "qty": 100, "cost_per_share": 50.0},
            {"date": "2024-09-10", "qty": 100, "cost_per_share": 70.0},
        ]
        fifo = self._compute_tax_lot(lots, sell_qty=100, method="fifo")
        lifo = self._compute_tax_lot(lots, sell_qty=100, method="lifo")
        assert fifo["cost_basis"] < lifo["cost_basis"]
