import math
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text


def _z_test_p_value(control_rate: float, variant_rate: float,
                    control_n: int, variant_n: int) -> float:
    if control_n == 0 or variant_n == 0:
        return 0
    p_pool = (control_rate * control_n + variant_rate * variant_n) / (control_n + variant_n)
    se = math.sqrt(p_pool * (1 - p_pool) * (1 / control_n + 1 / variant_n))
    if se == 0:
        return 0
    z = (variant_rate - control_rate) / se
    return 0.5 * (1 + math.erf(abs(z) / math.sqrt(2)))


async def create_experiment(db: AsyncSession, name: str, page: str,
                            description: str | None = None,
                            metric: str = "conversion_rate",
                            min_sample_size: int = 1000,
                            created_by: str | None = None) -> dict:
    row = await db.execute(text("""
        INSERT INTO experiments (name, page, description, metric, min_sample_size, created_by)
        VALUES (:name, :page, :description, :metric, :min_sample_size, :created_by)
        RETURNING id, name, page, description, metric, min_sample_size, status, created_at, created_by
    """), {"name": name, "page": page, "description": description,
           "metric": metric, "min_sample_size": min_sample_size, "created_by": created_by})
    await db.commit()
    return dict(row.mappings().first())


async def list_experiments(db: AsyncSession) -> list[dict]:
    rows = await db.execute(text("""
        SELECT e.id, e.name, e.page, e.description, e.metric, e.min_sample_size,
               e.status, e.created_at, e.created_by,
               COALESCE(json_agg(json_build_object(
                   'id', ev.id, 'name', ev.name, 'is_control', ev.is_control,
                   'traffic_pct', ev.traffic_pct, 'participants', ev.participants,
                   'conversions', ev.conversions, 'conversion_rate', ev.conversion_rate,
                   'improvement', ev.improvement, 'is_winner', ev.is_winner,
                   'confidence', ev.confidence
               ) ORDER BY ev.id) FILTER (WHERE ev.id IS NOT NULL), '[]') AS variants,
               COALESCE(SUM(ev.participants), 0) AS total_participants
        FROM experiments e
        LEFT JOIN experiment_variants ev ON ev.experiment_id = e.id
        GROUP BY e.id ORDER BY e.created_at DESC
    """))
    return [dict(r._mapping) for r in rows]


async def get_experiment_results(db: AsyncSession, experiment_id: str) -> dict:
    exp = await db.execute(text("""
        SELECT id, name, page, description, metric, min_sample_size, status
        FROM experiments WHERE id = :id
    """), {"id": experiment_id})
    experiment = dict(exp.mappings().first() or {})
    if not experiment:
        return {"experiment": {}, "results": []}

    rows = await db.execute(text("""
        SELECT id, name, is_control, traffic_pct, participants, conversions,
               conversion_rate, improvement, is_winner, confidence
        FROM experiment_variants WHERE experiment_id = :eid ORDER BY id
    """), {"eid": experiment_id})
    variants = [dict(r._mapping) for r in rows]

    control = next((v for v in variants if v["is_control"]), None)
    if control and control["participants"] > 0:
        for v in variants:
            if v["is_control"]:
                v["improvement"] = None
                v["confidence"] = None
            else:
                v["improvement"] = ((v["conversion_rate"] - control["conversion_rate"]) / control["conversion_rate"]) * 100 if control["conversion_rate"] > 0 else 0
                v["confidence"] = round(_z_test_p_value(
                    control["conversion_rate"] / 100, v["conversion_rate"] / 100,
                    control["participants"], v["participants"]
                ) * 100, 1)

    return {"experiment": experiment, "results": variants}


async def create_variant(db: AsyncSession, experiment_id: str, name: str,
                         is_control: bool = False, traffic_pct: float = 50.0,
                         description: str | None = None) -> dict:
    row = await db.execute(text("""
        INSERT INTO experiment_variants (experiment_id, name, is_control, traffic_pct, description)
        VALUES (:eid, :name, :is_control, :traffic_pct, :desc)
        RETURNING id, name, is_control, traffic_pct, participants, conversions, conversion_rate
    """), {"eid": experiment_id, "name": name, "is_control": is_control,
           "traffic_pct": traffic_pct, "desc": description})
    await db.commit()
    return dict(row.mappings().first())
