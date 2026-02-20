async def test_create_user(async_client):
    response = await async_client.post("/api/v1/users/", json={
        "username"  : "cactu",
        "email"     : "test@gmail.com",
        "first_name": "Yhon",
        "last_name" : "Vivas",
        "role"      : "admin",
        "active"    : True,
    })
    assert response.status_code == 200
    assert response.json()["username"] == "cactu"
    assert response.json()["email"] == "test@gmail.com"
    assert response.json()["first_name"] == "Yhon"
    assert response.json()["last_name"] == "Vivas"
    assert response.json()["role"] == "admin"
    assert response.json()["active"] == True

async def test_create_user_with_email_duplicate(async_client):
    response = await async_client.post("/api/v1/users/", json={
        "username": "cactu",
        "email": "test@gmail.com",
        "first_name": "Yhon",
        "last_name": "Vivas",
        "role": "admin",
        "active": True,
    })
    assert response.status_code == 200
    assert response.json()["username"] == "cactu"
    assert response.json()["email"] == "test@gmail.com"
    assert response.json()["first_name"] == "Yhon"
    assert response.json()["last_name"] == "Vivas"
    assert response.json()["role"] == "admin"
    assert response.json()["active"] == True
    newResponse = await async_client.post("/api/v1/users/", json={
        "username": "cactu",
        "email": "test@gmail.com",
        "first_name": "Yhon",
        "last_name": "Vivas",
        "role": "admin",
        "active": True,
    })
    assert newResponse.status_code == 409

async def test_get_users(async_client):
    response = await async_client.get("/api/v1/users/")
    assert response.status_code == 200

async def test_get_user_by_id(async_client):
    create_response = await async_client.post("/api/v1/users/", json={
        "username": "cactu",
        "email": "test@gmail.com",
        "first_name": "Yhon",
        "last_name": "Vivas",
        "role": "admin",
        "active": True,
    })
    user_id = create_response.json()["id"]

    response = await async_client.get(f"/api/v1/users/{user_id}")
    assert response.status_code == 200
    assert response.json()["id"] == user_id

async def test_update_user(async_client):
    create_response = await async_client.post("/api/v1/users/", json={
        "username": "cactu",
        "email": "test@gmail.com",
        "first_name": "Yhon",
        "last_name": "Vivas",
        "role": "admin",
        "active": True,
    })
    user_id = create_response.json()["id"]

    response = await async_client.put(f"/api/v1/users/{user_id}", json={
        "first_name": "Yhon Updated"
    })
    assert response.status_code == 200
    assert response.json()["first_name"] == "Yhon Updated"

async def test_delete_user(async_client):
    create_response = await async_client.post("/api/v1/users/", json={
        "username": "cactu",
        "email": "test@gmail.com",
        "first_name": "Yhon",
        "last_name": "Vivas",
        "role": "admin",
        "active": True,
    })
    user_id = create_response.json()["id"]

    response = await async_client.delete(f"/api/v1/users/{user_id}")
    assert response.status_code == 204

async def test_delete_user_not_found(async_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.delete(f"/api/v1/users/{fake_id}")
    assert response.status_code == 404

async def test_get_user_not_found(async_client):
    fake_id = "00000000-0000-0000-0000-000000000000"
    response = await async_client.delete(f"/api/v1/users/{fake_id}")
    assert response.status_code == 404