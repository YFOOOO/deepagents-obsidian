"""SmartRouter skeleton for Obsidian Assistant V2.1.

Responsibilities:
- Build a lightweight keyword index of the Obsidian markdown knowledge base.
- Heuristically decide routing strategy: local_only | web_first | hybrid.
- Provide instrumentation hooks (counters) for later telemetry.

Notes:
- Actual semantic indexing / vector search not implemented in this skeleton.
- Coverage heuristic uses naive keyword frequency presence.
- Time sensitivity keywords list can be extended from configuration.
"""
from __future__ import annotations
from pathlib import Path
from typing import Set, Dict, Tuple
import re

DEFAULT_TIME_KEYWORDS = ["最新", "推荐", "现在", "今年", "2025", "2024", "update", "recent", "trend"]
STOPWORDS = {"的", "是", "在", "和", "了", "有", "就", "不", "the", "is", "a", "an", "to", "of"}

class SmartRouter:
    """Heuristic routing engine.

    Parameters:
        docs_path: Root path of Obsidian vault subset to index.
        time_keywords: List of words/phrases indicating need for fresh info.
        coverage_thresholds: Tuple (high, mid) for routing decision splits.
    """

    def __init__(
        self,
        docs_path: str,
        time_keywords=None,
        coverage_thresholds: Tuple[float, float] = (0.8, 0.4),
        max_files: int = 2000,
    ) -> None:
        self.docs_path = Path(docs_path)
        self.time_keywords = time_keywords or DEFAULT_TIME_KEYWORDS
        self.coverage_high, self.coverage_mid = coverage_thresholds
        self.max_files = max_files
        self._index: Set[str] = set()
        self._stats: Dict[str, int] = {"queries": 0, "local_only": 0, "web_first": 0, "hybrid": 0}

    # ------------------------------------------------------------------
    # Public API
    # ------------------------------------------------------------------
    def route(self, query: str) -> str:
        """Return routing strategy.
        local_only | web_first | hybrid
        """
        decision, coverage, time_sensitive = self.route_details(query)
        return decision

    def route_details(self, query: str):
        """Return (strategy, coverage_score, time_sensitive_flag)."""
        self._stats["queries"] += 1
        time_sensitive = self._is_time_sensitive(query)
        if time_sensitive:
            decision = "web_first"
            coverage = self._check_local_coverage(query)  # still compute for telemetry
        else:
            coverage = self._check_local_coverage(query)
            if coverage >= self.coverage_high:
                decision = "local_only"
            elif coverage >= self.coverage_mid:
                decision = "hybrid"
            else:
                decision = "web_first"
        self._stats[decision] += 1
        # cache last metrics for external access
        self.last_query = query
        self.last_coverage = coverage
        self.last_time_sensitive = time_sensitive
        self.last_decision = decision
        return decision, coverage, time_sensitive

    def stats(self) -> Dict[str, int]:
        return dict(self._stats)

    def ensure_index(self) -> None:
        if not self._index:
            self._index = self._build_local_index()

    # ------------------------------------------------------------------
    # Internal helpers
    # ------------------------------------------------------------------
    def _is_time_sensitive(self, query: str) -> bool:
        lowered = query.lower()
        return any(kw.lower() in lowered for kw in self.time_keywords)

    def _tokenize(self, text: str) -> Set[str]:
        words = re.findall(r"[\w\-]+", text.lower())
        return {w for w in words if w not in STOPWORDS and len(w) > 1}

    def _build_local_index(self) -> Set[str]:
        if not self.docs_path.exists():
            return set()
        collected: Set[str] = set()
        md_files = list(self.docs_path.rglob("*.md"))[: self.max_files]
        for f in md_files:
            try:
                content = f.read_text(encoding="utf-8", errors="ignore")
            except Exception:
                continue
            # Simple: include tokens from title (filename) and first 400 chars
            snippet = f.name + "\n" + content[:400]
            tokens = self._tokenize(snippet)
            collected.update(tokens)
        return collected

    def _check_local_coverage(self, query: str) -> float:
        self.ensure_index()
        if not self._index:
            return 0.0
        keywords = list(self._tokenize(query))
        if not keywords:
            return 0.0
        matched = sum(1 for k in keywords if k in self._index)
        return matched / len(keywords)

# Convenience factory (future: support config object)

def create_smart_router(docs_path: str) -> SmartRouter:
    return SmartRouter(docs_path=docs_path)

__all__ = ["SmartRouter", "create_smart_router"]
