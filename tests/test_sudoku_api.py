from fastapi.testclient import TestClient

from app.main import app

client = TestClient(app)


def test_validate_sudoku() -> None:
    payload = {
        "board": [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
    }

    response = client.post("/api/v1/sudoku/validate", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["valid"] is True
    assert data["message"] == "Board is valid"


def test_solve_sudoku() -> None:
    payload = {
        "board": [
            [5, 3, 0, 0, 7, 0, 0, 0, 0],
            [6, 0, 0, 1, 9, 5, 0, 0, 0],
            [0, 9, 8, 0, 0, 0, 0, 6, 0],
            [8, 0, 0, 0, 6, 0, 0, 0, 3],
            [4, 0, 0, 8, 0, 3, 0, 0, 1],
            [7, 0, 0, 0, 2, 0, 0, 0, 6],
            [0, 6, 0, 0, 0, 0, 2, 8, 0],
            [0, 0, 0, 4, 1, 9, 0, 0, 5],
            [0, 0, 0, 0, 8, 0, 0, 7, 9],
        ]
    }

    response = client.post("/api/v1/sudoku/solve", json=payload)
    assert response.status_code == 200

    data = response.json()
    assert data["solved"] is True
    assert data["solution"] is not None
    assert len(data["solution"]) == 9
    assert len(data["solution"][0]) == 9


def test_generate_sudoku() -> None:
    response = client.post(
        "/api/v1/sudoku/generate",
        json={"difficulty": "easy"},
    )
    assert response.status_code == 200

    data = response.json()
    assert data["difficulty"] == "easy"
    assert len(data["puzzle"]) == 9
    assert len(data["solution"]) == 9
