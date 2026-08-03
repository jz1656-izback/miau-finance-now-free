from pydantic import BaseModel, Field
from typing import Any, Optional
from decimal import Decimal


class StrategyParamDef(BaseModel):
    name: str
    type: str
    default: Any = None
    min: Optional[float] = None
    max: Optional[float] = None
    description: str = ""


class StrategyConfig(BaseModel):
    strategy_name: str = Field(..., description="Strategy identifier")
    params: dict[str, Any] = Field(default_factory=dict)

    def validate_params(self) -> dict[str, Any]:
        from app.services.strategies.registry import list_strategies
        for s in list_strategies():
            if s["name"] == self.strategy_name:
                validated = {}
                for p in s["params"]:
                    name = p["name"]
                    raw = self.params.get(name, p["default"])
                    if p["type"] == "int":
                        val = int(raw)
                        if p.get("min") is not None and val < p["min"]:
                            raise ValueError(f"{name}: {val} < min {p['min']}")
                        if p.get("max") is not None and val > p["max"]:
                            raise ValueError(f"{name}: {val} > max {p['max']}")
                        validated[name] = val
                    elif p["type"] == "float":
                        val = float(raw)
                        if p.get("min") is not None and val < p["min"]:
                            raise ValueError(f"{name}: {val} < min {p['min']}")
                        if p.get("max") is not None and val > p["max"]:
                            raise ValueError(f"{name}: {val} > max {p['max']}")
                        validated[name] = val
                    else:
                        validated[name] = raw
                return validated
        raise ValueError(f"Unknown strategy: {self.strategy_name}")


class BacktestRequest(BaseModel):
    strategy_name: str
    ticker: str
    period: str = "1y"
    params: dict[str, Any] = Field(default_factory=dict)
    initial_capital: Decimal = Field(default=Decimal("100000"), gt=0)
