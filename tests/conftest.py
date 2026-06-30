"""Shared pytest fixtures for lexograph tests."""

import os

import pytest
from hypothesis import HealthCheck, settings

from lexograph.datasets import load_demo_text

# Mutation testing (mutmut) runs the same property test from multiple forked
# workers, which trips Hypothesis's ``differing_executors`` health check. This
# env-gated profile suppresses that check (and the shared example database) only
# during mutation runs — the normal test suite is unaffected.
settings.register_profile(
    "mutation",
    suppress_health_check=[HealthCheck.differing_executors],
    database=None,
    deadline=None,
)
if os.environ.get("LEXOGRAPH_MUTATION"):
    settings.load_profile("mutation")


@pytest.fixture
def demo_text() -> str:
    """The bundled Pride and Prejudice demo text."""
    return load_demo_text()
