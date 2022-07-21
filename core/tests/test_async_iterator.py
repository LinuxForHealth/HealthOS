"""
test_async_iterator.py

Tests the AsyncIterator test support class
"""
import pytest

from .support import AsyncIterator


@pytest.mark.asyncio
async def test_async_iterator():
    """Validates that the AsyncIterator, used for async test case mock objects works correctly"""
    items = ["red", "blue", "green"]
    a = AsyncIterator(items)

    actual_items = []
    async for i in a:
        actual_items.append(i)

    assert items == actual_items

    with pytest.raises(StopAsyncIteration):
        await a.__anext__()
