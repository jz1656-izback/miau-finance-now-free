import pytest
from httpx import AsyncClient
from unittest.mock import AsyncMock, MagicMock
from uuid import uuid4

_USER_ID = str(uuid4())
_TEAM_ID = str(uuid4())
_OTHER_USER_ID = str(uuid4())

_TEAM_ROW = {
    "id": _TEAM_ID,
    "name": "Test Team",
    "description": "A test team",
    "owner_id": _USER_ID,
    "created_at": "2025-01-01T00:00:00",
    "owner_username": "testuser",
}

_MEMBER_ROW = {
    "id": str(uuid4()),
    "team_id": _TEAM_ID,
    "user_id": str(uuid4()),
    "role": "member",
    "username": "member1",
}


@pytest.fixture
def mock_teams_db():
    from app.main import app
    from app.database import get_db
    from app.api import teams as teams_api

    mock_session = MagicMock()
    mock_session.execute = AsyncMock()
    mock_session.commit = AsyncMock()

    state = {"team_found": True, "is_owner": True, "member_found": True, "rows_affected": 1}

    async def mock_exec(*args, **kwargs):
        sql = str(args[0]) if args else ""
        result = MagicMock()
        result.rowcount = state["rows_affected"]

        if "SELECT id, username, email, role FROM users" in sql:
            result.mappings.return_value.first.return_value = {
                "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
            }
        elif "INSERT INTO teams" in sql and "RETURNING" in sql:
            result.mappings.return_value.first.return_value = _TEAM_ROW
        elif "INSERT INTO team_members" in sql and "RETURNING" in sql:
            result.mappings.return_value.first.return_value = _MEMBER_ROW
        elif "SELECT owner_id FROM teams" in sql:
            if state["team_found"]:
                result.mappings.return_value.first.return_value = {"owner_id": _USER_ID if state["is_owner"] else _OTHER_USER_ID}
            else:
                result.mappings.return_value.first.return_value = None
                result.mappings.return_value.all.return_value = []
                return result
        elif "FROM teams t LEFT JOIN team_members" in sql or "COUNT(DISTINCT t.id)" in sql:
            result.mappings.return_value.all.return_value = [_TEAM_ROW]
            result.scalar.return_value = 1
        elif "SELECT t.*, u.username as owner_username" in sql:
            if state["team_found"]:
                result.mappings.return_value.first.return_value = {**_TEAM_ROW, "owner_username": "testuser"}
            else:
                result.mappings.return_value.first.return_value = None
        elif "FROM team_members tm" in sql:
            result.mappings.return_value.all.return_value = [_MEMBER_ROW]
        elif "UPDATE teams SET" in sql and "RETURNING" in sql:
            result.mappings.return_value.first.return_value = _TEAM_ROW
        elif "DELETE FROM teams" in sql:
            result.rowcount = 1 if state["team_found"] else 0
        elif "DELETE FROM team_members" in sql:
            result.rowcount = 1 if state["member_found"] else 0
            result.mappings.return_value.all.return_value = []
        else:
            result.mappings.return_value.first.return_value = None
            result.mappings.return_value.all.return_value = []

        return result

    mock_session.execute.side_effect = mock_exec
    app.dependency_overrides[get_db] = lambda: mock_session
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }
    yield state
    app.dependency_overrides.pop(get_db, None)
    app.dependency_overrides.pop(teams_api.get_current_user_db, None)


@pytest.mark.anyio
async def test_create_team(client: AsyncClient, mock_teams_db):
    resp = await client.post("/api/v1/teams", params={"name": "Test Team", "description": "A test team"})
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Team"
    assert data["description"] == "A test team"


@pytest.mark.anyio
async def test_create_team_no_description(client: AsyncClient, mock_teams_db):
    resp = await client.post("/api/v1/teams", params={"name": "Minimal Team"})
    assert resp.status_code == 200
    assert resp.json()["name"] == "Minimal Team"


@pytest.mark.anyio
async def test_create_team_missing_name(client: AsyncClient, mock_teams_db):
    resp = await client.post("/api/v1/teams")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_teams(client: AsyncClient, mock_teams_db):
    resp = await client.get("/api/v1/teams")
    assert resp.status_code == 200
    data = resp.json()
    assert "items" in data
    assert "total" in data
    assert "page" in data
    assert "per_page" in data
    assert len(data["items"]) == 1


@pytest.mark.anyio
async def test_list_teams_paginated(client: AsyncClient, mock_teams_db):
    resp = await client.get("/api/v1/teams?page=1&per_page=10")
    assert resp.status_code == 200
    assert resp.json()["page"] == 1
    assert resp.json()["per_page"] == 10


@pytest.mark.anyio
async def test_list_teams_invalid_page(client: AsyncClient, mock_teams_db):
    resp = await client.get("/api/v1/teams?page=0")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_list_teams_invalid_per_page(client: AsyncClient, mock_teams_db):
    resp = await client.get("/api/v1/teams?per_page=200")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_get_team(client: AsyncClient, mock_teams_db):
    resp = await client.get(f"/api/v1/teams/{_TEAM_ID}")
    assert resp.status_code == 200
    data = resp.json()
    assert data["name"] == "Test Team"
    assert "members" in data


@pytest.mark.anyio
async def test_get_team_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["team_found"] = False
    resp = await client.get(f"/api/v1/teams/{uuid4()}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_get_team_invalid_id(client: AsyncClient, mock_teams_db):
    resp = await client.get("/api/v1/teams/not-a-uuid")
    assert resp.status_code == 422


@pytest.mark.anyio
async def test_update_team(client: AsyncClient, mock_teams_db):
    resp = await client.put(f"/api/v1/teams/{_TEAM_ID}", params={"name": "Updated Team"})
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_update_team_no_fields(client: AsyncClient, mock_teams_db):
    resp = await client.put(f"/api/v1/teams/{_TEAM_ID}")
    assert resp.status_code == 400
    assert "No fields to update" in resp.text


@pytest.mark.anyio
async def test_update_team_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["team_found"] = False
    resp = await client.put(f"/api/v1/teams/{uuid4()}", params={"name": "Nope"})
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_update_team_unauthorized(client: AsyncClient, mock_teams_db):
    mock_teams_db["is_owner"] = False
    resp = await client.put(f"/api/v1/teams/{_TEAM_ID}", params={"name": "Hacked"})
    assert resp.status_code == 403


@pytest.mark.anyio
async def test_delete_team(client: AsyncClient, mock_teams_db):
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}")
    assert resp.status_code == 200
    assert resp.json()["message"] == "Team deleted"


@pytest.mark.anyio
async def test_delete_team_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["team_found"] = False
    resp = await client.delete(f"/api/v1/teams/{uuid4()}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_delete_team_not_owner_not_admin(client: AsyncClient, mock_teams_db):
    from app.main import app
    from app.api import teams as teams_api

    mock_teams_db["is_owner"] = False
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _OTHER_USER_ID, "username": "other", "email": "o@t.com", "role": "user",
    }
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}")
    assert resp.status_code == 403
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }


@pytest.mark.anyio
async def test_delete_team_as_admin(client: AsyncClient, mock_teams_db):
    from app.main import app
    from app.api import teams as teams_api

    mock_teams_db["is_owner"] = False
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _OTHER_USER_ID, "username": "admin", "email": "a@t.com", "role": "admin",
    }
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}")
    assert resp.status_code == 200
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }


@pytest.mark.anyio
async def test_add_team_member(client: AsyncClient, mock_teams_db):
    resp = await client.post(
        f"/api/v1/teams/{_TEAM_ID}/members",
        params={"user_id": str(uuid4()), "role": "member"},
    )
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_add_team_member_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["team_found"] = False
    resp = await client.post(
        f"/api/v1/teams/{uuid4()}/members",
        params={"user_id": str(uuid4())},
    )
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_add_team_member_unauthorized(client: AsyncClient, mock_teams_db):
    from app.main import app
    from app.api import teams as teams_api

    mock_teams_db["is_owner"] = False
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _OTHER_USER_ID, "username": "other", "email": "o@t.com", "role": "user",
    }
    resp = await client.post(
        f"/api/v1/teams/{_TEAM_ID}/members",
        params={"user_id": str(uuid4())},
    )
    assert resp.status_code == 403
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }


@pytest.mark.anyio
async def test_remove_team_member(client: AsyncClient, mock_teams_db):
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}/members/{uuid4()}")
    assert resp.status_code == 200


@pytest.mark.anyio
async def test_remove_team_member_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["team_found"] = False
    resp = await client.delete(f"/api/v1/teams/{uuid4()}/members/{uuid4()}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_remove_team_member_user_not_found(client: AsyncClient, mock_teams_db):
    mock_teams_db["member_found"] = False
    mock_teams_db["rows_affected"] = 0
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}/members/{uuid4()}")
    assert resp.status_code == 404


@pytest.mark.anyio
async def test_remove_team_member_unauthorized(client: AsyncClient, mock_teams_db):
    from app.main import app
    from app.api import teams as teams_api

    mock_teams_db["is_owner"] = False
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _OTHER_USER_ID, "username": "other", "email": "o@t.com", "role": "user",
    }
    resp = await client.delete(f"/api/v1/teams/{_TEAM_ID}/members/{uuid4()}")
    assert resp.status_code == 403
    app.dependency_overrides[teams_api.get_current_user_db] = lambda: {
        "id": _USER_ID, "username": "testuser", "email": "test@test.com", "role": "user",
    }
