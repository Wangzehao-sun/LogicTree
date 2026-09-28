"""LogicTree: synthetic logical-reasoning data generation."""

from .core import (
    DEFAULT_STEP_COUNTS,
    LogicTree,
    LogicTreeNode,
    gen_multi_step_data,
    gen_multi_step_fol_data,
    generate_dataset,
    process_data,
)

__all__ = [
    "DEFAULT_STEP_COUNTS",
    "LogicTree",
    "LogicTreeNode",
    "gen_multi_step_data",
    "gen_multi_step_fol_data",
    "generate_dataset",
    "process_data",
]

__version__ = "0.1.0"
