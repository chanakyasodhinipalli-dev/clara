from __future__ import annotations
import asyncio
from typing import Iterable, Awaitable, List, TypeVar

T = TypeVar("T")

async def gather_limited(coros: Iterable[Awaitable[T]], limit: int = 8) -> List[T]:
    semaphore = asyncio.Semaphore(limit)
    results: List[T] = []
    async def _runner(coro: Awaitable[T]) -> None:
        async with semaphore:
            results.append(await coro)
    await asyncio.gather(*[_runner(c) for c in coros])
    return results
