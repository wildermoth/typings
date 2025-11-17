"""Type stubs for google.cloud.datastore.query_profile"""

from __future__ import annotations

from typing import Any, Dict, List
from dataclasses import dataclass
import datetime

@dataclass(frozen=True)
class ExplainOptions:
    """Class used to configure query profiling on a query."""

    analyze: bool = ...

    def _to_dict(self) -> Dict[str, bool]: ...

@dataclass(frozen=True)
class PlanSummary:
    """Contains planning phase information about a query."""

    indexes_used: List[Dict[str, Any]]

@dataclass(frozen=True)
class ExecutionStats:
    """Execution phase information about a query."""

    results_returned: int
    execution_duration: datetime.timedelta
    read_operations: int
    debug_stats: Dict[str, Any]

@dataclass(frozen=True)
class ExplainMetrics:
    """ExplainMetrics contains information about the planning and execution of a query."""

    plan_summary: PlanSummary

    @staticmethod
    def _from_pb(metrics_pb: Any) -> ExplainMetrics: ...

    @property
    def execution_stats(self) -> ExecutionStats: ...

@dataclass(frozen=True)
class _ExplainAnalyzeMetrics(ExplainMetrics):
    """Subclass of ExplainMetrics that includes execution_stats."""

    plan_summary: PlanSummary
    _execution_stats: ExecutionStats

    @property
    def execution_stats(self) -> ExecutionStats: ...

class QueryExplainError(Exception):
    """Error returned when there is a problem accessing query profiling information."""
    ...
