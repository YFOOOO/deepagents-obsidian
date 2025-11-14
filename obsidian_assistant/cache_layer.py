"""Caching & Compression skeleton for Obsidian Assistant.

Goals:
    - Reduce repeated token usage for identical / near-identical queries.
    - Provide hooks for semantic similarity, future embedding integration.
    - Provide lightweight result compression for verbose web search results.

Components:
    SimpleQueryCache: exact-match cache with optional disk persistence.
    SemanticStub: placeholder for semantic similarity future extension.
    TextCompressor: naive length & line-based compressor (ratio metadata).

Usage (skeleton):
    from cache_layer import SimpleQueryCache, TextCompressor
    cache = SimpleQueryCache(max_items=256)
    compressor = TextCompressor(max_chars=2000)

    cached = cache.get(query)
    if cached: return cached
    result = run_model(...)
    compressed = compressor.maybe_compress(result['answer'])
    cache.set(query, compressed_result)

Design Notes:
    - Disk persistence is JSON lines; one entry per line for append-only simplicity.
    - For thread-safety (future), can introduce a lock; omitted here.
    - Semantic layer left as stub: score(query, cached_query) -> float.
"""
from __future__ import annotations
import json
import time
from pathlib import Path
from typing import Dict, Any, Optional, List

class SimpleQueryCache:
    def __init__(self, max_items: int = 512, persist_path: Optional[str] = None):
        self.max_items = max_items
        self.persist_path = Path(persist_path) if persist_path else None
        self._store: Dict[str, Dict[str, Any]] = {}
        if self.persist_path and self.persist_path.exists():
            try:
                for line in self.persist_path.read_text(encoding='utf-8').splitlines():
                    if not line.strip():
                        continue
                    obj = json.loads(line)
                    key = obj.get('query')
                    if key:
                        self._store[key] = obj
            except Exception:
                pass

    def normalize(self, query: str) -> str:
        return query.strip().lower()

    def get(self, query: str) -> Optional[Dict[str, Any]]:
        return self._store.get(self.normalize(query))

    def set(self, query: str, result: Dict[str, Any]):
        key = self.normalize(query)
        entry = {
            'query': key,
            'cached_at': time.time(),
            'result': result,
        }
        self._store[key] = entry
        # Eviction: simple FIFO based on insertion order
        if len(self._store) > self.max_items:
            # remove oldest
            oldest_key = sorted(self._store.items(), key=lambda kv: kv[1]['cached_at'])[0][0]
            self._store.pop(oldest_key, None)
        if self.persist_path:
            try:
                with self.persist_path.open('a', encoding='utf-8') as f:
                    f.write(json.dumps(entry, ensure_ascii=False) + '\n')
            except Exception:
                pass

    def stats(self) -> Dict[str, Any]:
        return {
            'items': len(self._store),
            'max_items': self.max_items,
            'persist': bool(self.persist_path),
        }

class SemanticStub:
    """Placeholder for future semantic similarity (embedding based)."""
    def score(self, query: str, other: str) -> float:
        # naive token overlap ratio
        q_tokens = set(query.lower().split())
        o_tokens = set(other.lower().split())
        inter = len(q_tokens & o_tokens)
        union = len(q_tokens | o_tokens) or 1
        return inter / union

class TextCompressor:
    def __init__(self, max_chars: int = 4000, trim_ratio: float = 0.6):
        self.max_chars = max_chars
        self.trim_ratio = trim_ratio

    def maybe_compress(self, text: Optional[str]) -> Dict[str, Any]:
        if not text:
            return {'compressed': text, 'original_length': 0, 'compressed_length': 0, 'ratio': 0.0, 'applied': False}
        original_length = len(text)
        applied = False
        compressed_text = text
        if original_length > self.max_chars:
            target = int(self.max_chars * self.trim_ratio)
            compressed_text = text[:target] + '\n...[内容已截断，后续压缩器可提供摘要]'
            applied = True
        return {
            'compressed': compressed_text,
            'original_length': original_length,
            'compressed_length': len(compressed_text),
            'ratio': (len(compressed_text) / original_length) if original_length else 1.0,
            'applied': applied,
        }

__all__ = [
    'SimpleQueryCache',
    'SemanticStub',
    'TextCompressor'
]
