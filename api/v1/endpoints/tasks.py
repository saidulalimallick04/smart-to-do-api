from typing import List, Annotated
from fastapi import APIRouter, Depends, HTTPException, status
from beanie import PydanticObjectId

from models.task import Task
from models.user import User
from schemas.task import TaskCreate, TaskUpdate, TaskOut
from api.deps import get_current_user
from core.utils import enhance_task_context

router = APIRouter()

@router.post("/", response_model=TaskOut)
async def create_task(
    task_in: TaskCreate,
    current_user: User = Depends(get_current_user)
):
    # Smart Logic: Infer priority and tags if not provided or to enhance
    inferred_priority, inferred_tags = enhance_task_context(task_in.title, task_in.description or "", task_in.tags)
    
    # If user didn't specify priority, use inferred. If they did, keep theirs.
    # Same for tags: merge them.
    final_priority = task_in.priority if task_in.priority != "medium" else inferred_priority
    final_tags = list(set(task_in.tags + inferred_tags))
    
    task = Task(
        **task_in.model_dump(exclude={"priority", "tags"}),
        priority=final_priority,
        tags=final_tags,
        owner=current_user
    )
    await task.insert()
    return task

@router.get("/", response_model=List[TaskOut])
async def read_tasks(
    current_user: User = Depends(get_current_user),
    skip: int = 0,
    limit: int = 100,
    priority: str = None,
    is_completed: bool = None
):
    query = [Task.owner.id == current_user.id]
    if priority:
        query.append(Task.priority == priority)
    if is_completed is not None:
        query.append(Task.is_completed == is_completed)
        
    tasks = await Task.find(*query).skip(skip).limit(limit).to_list()
    return tasks

@router.get("/{task_id}", response_model=TaskOut)
async def read_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    # Retrieve task and ensure ownership
    task = await Task.find_one(Task.id == PydanticObjectId(task_id), Task.owner.id == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task

@router.put("/{task_id}", response_model=TaskOut)
async def update_task(
    task_id: str,
    task_in: TaskUpdate,
    current_user: User = Depends(get_current_user)
):
    task = await Task.find_one(Task.id == PydanticObjectId(task_id), Task.owner.id == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    update_data = task_in.model_dump(exclude_unset=True)
    await task.set(update_data)
    return task

@router.delete("/{task_id}")
async def delete_task(
    task_id: str,
    current_user: User = Depends(get_current_user)
):
    task = await Task.find_one(Task.id == PydanticObjectId(task_id), Task.owner.id == current_user.id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    
    await task.delete()
    return {
        "message": "Task deleted successfully"
    }
