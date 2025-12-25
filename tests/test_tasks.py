import pytest

# 1. Test Create Task
@pytest.mark.anyio
async def test_create_task(authed_client):
    response = await authed_client.post(
        "/api/v1/tasks/",
        json={"title": "Granular Task", "description": "Testing Create", "tags": ["test"]}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Granular Task"
    # Store ID on the client instance to share across tests (hacky but effective for sequential flows)
    authed_client.task_id = data["id"]

# 2. Test Get All Tasks
@pytest.mark.anyio
async def test_get_all_tasks(authed_client):
    response = await authed_client.get("/api/v1/tasks/")
    assert response.status_code == 200
    tasks = response.json()
    assert len(tasks) > 0
    # Ensure our task is in the list
    assert any(t["title"] == "Granular Task" for t in tasks)

# 3. Test Update Task
@pytest.mark.anyio
async def test_update_task(authed_client):
    # Ensure task_id is available from creating step, or create one if running standalone
    if not hasattr(authed_client, "task_id"):
         res = await authed_client.post("/api/v1/tasks/", json={"title": "Temp", "priority": "low"})
         authed_client.task_id = res.json()["id"]

    task_id = authed_client.task_id
    response = await authed_client.put(
        f"/api/v1/tasks/{task_id}",
        json={"title": "Updated Granular Task", "is_completed": True}
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Updated Granular Task"
    assert data["is_completed"] is True

# 4. Test Delete Task
@pytest.mark.anyio
async def test_delete_task(authed_client):
    if not hasattr(authed_client, "task_id"):
         res = await authed_client.post("/api/v1/tasks/", json={"title": "Temp Delete", "priority": "low"})
         authed_client.task_id = res.json()["id"]

    task_id = authed_client.task_id
    response = await authed_client.delete(f"/api/v1/tasks/{task_id}")
    assert response.status_code == 200

    # Verify 404
    get_res = await authed_client.get(f"/api/v1/tasks/{task_id}")
    assert get_res.status_code == 404
