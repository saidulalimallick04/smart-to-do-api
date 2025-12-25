import pytest

@pytest.mark.anyio
async def test_create_task(async_client):
    # Login first
    login_response = await async_client.post(
        "/api/v1/auth/login",
        data={"username": "test@example.com", "password": "testpassword"}
    )
    token = login_response.json()["access_token"]
    headers = {"Authorization": f"Bearer {token}"}
    
    # Create Task
    response = await async_client.post(
        "/api/v1/tasks/",
        json={"title": "Buy groceries", "tags": ["home"]},
        headers=headers
    )
    assert response.status_code == 200
    data = response.json()
    assert data["title"] == "Buy groceries"
    assert "shopping" in data["tags"] # Smart logic check
    
    # Verify persistence
    response = await async_client.get("/api/v1/tasks/", headers=headers)
    assert response.status_code == 200
    assert len(response.json()) > 0
