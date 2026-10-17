"""Rate limit configuration for the service."""

from vendor.ratelib.limits import TIER_TABLE, resolve

DEFAULT_WINDOW_SECONDS = 60


def get_limit(tier):
    """Return the request ceiling for a tier."""
    return resolve(TIER_TABLE, tier)
