from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_create_and_get_game() -> None:
    create_response = client.post(
        "/api/v1/games",
        json={"difficulty": "easy"},
    )
    assert create_response.status_code == 200

    created_game = create_response.json()
    game_id = created_game["id"]

    assert created_game["difficulty"] == "easy"
    assert "solution" not in created_game

    get_response = client.get(f"/api/v1/games/{game_id}")
    assert get_response.status_code == 200

    game_data = get_response.json()
    assert game_data["id"] == game_id
    assert len(game_data["current_board"]) == 9
    assert len(game_data["initial_board"]) == 9


def test_check_game() -> None:
    create_response = client.post(
        "/api/v1/games",
        json={"difficulty": "easy"},
    )
    assert create_response.status_code == 200
    game_id = create_response.json()["id"]

    check_response = client.get(f"/api/v1/games/{game_id}/check")
    assert check_response.status_code == 200

    data = check_response.json()
    assert "valid" in data
    assert "solved" in data
    assert "status" in data
    assert "current_board" in data


def test_solve_game() -> None:
    create_response = client.post(
        "/api/v1/games",
        json={"difficulty": "easy"},
    )
    assert create_response.status_code == 200
    game_id = create_response.json()["id"]

    solve_response = client.post(f"/api/v1/games/{game_id}/solve")
    assert solve_response.status_code == 200

    data = solve_response.json()
    assert data["id"] == game_id
    assert data["status"] == "solved"
    assert len(data["current_board"]) == 9