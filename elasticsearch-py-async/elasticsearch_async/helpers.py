import asyncio

ensure_future = getattr(asyncio, 'ensure_future', asyncio.async)
