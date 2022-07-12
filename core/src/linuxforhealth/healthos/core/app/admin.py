"""
admin.py

Implements /admin endpoints used to manage core service tasks
"""

from fastapi.routing import APIRouter

router = APIRouter(prefix="/admin")


@router.get("")
async def list_tasks():
    """Lists the tasks registered with the core service"""
    return {"status": "ok"}
