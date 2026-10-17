"""ratelib.limits -- tier table helpers.

Vendored from the upstream `ratelib` package, version 2.3.1.
"""

TIER_TABLE = {"free": 15, "pro": 100, "ultra": 300}


def resolve(table, tier, default=100):
    """Look up a tier in the table, falling back to a default ceiling."""
    return table.get(tier, default)
