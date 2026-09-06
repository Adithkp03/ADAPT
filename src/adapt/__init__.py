"""ADAPT Phase 2 — computational substrate.

Real tiny-model experiment engine. No fake computation: every prediction
comes from an actual fit / gradient update / state accumulation.
Evidence type of all outputs here: TOY_EXPERIMENT (our controlled
educational implementation), unless stated otherwise.
"""
from .tasks import generate_task, Task, FAMILIES, GENERATOR_VERSION
from .strategies import (
    AdaptationStrategy, FrozenBaseline, ContextICL,
    ParamTTA, RecurrentState, TTTState, make_strategy,
)
from .runner import run, run_with_protocol, sweep
from .telemetry import (
    l2_delta, regression_correct, exact_correct, grid_correct,
    accuracy_ci,
)

__all__ = [
    "generate_task", "Task", "FAMILIES", "GENERATOR_VERSION",
    "AdaptationStrategy", "FrozenBaseline", "ContextICL",
    "ParamTTA", "RecurrentState", "TTTState", "make_strategy",
    "l2_delta", "regression_correct", "exact_correct", "grid_correct",
    "accuracy_ci",
]
