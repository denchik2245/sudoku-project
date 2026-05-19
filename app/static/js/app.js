let currentGameId = null;
let currentBoard = [];
let initialBoard = [];
let selectedRow = null;
let selectedCol = null;
let activeModal = null;
let lastFocusedElement = null;

const boardElement = document.getElementById("sudoku-board");
const boardEmptyStateElement = document.getElementById("board-empty-state");
const selectedCellElement = document.getElementById("selected-cell");
const messageBoxElement = document.getElementById("message-box");

const difficultyElement = document.getElementById("difficulty");
const newGameButton = document.getElementById("new-game-btn");
const checkButton = document.getElementById("check-btn");
const solveButton = document.getElementById("solve-btn");
const checkCellButton = document.getElementById("check-cell-btn");

function setMessage(message) {
    if (messageBoxElement) {
        messageBoxElement.textContent = message;
    }
}

function setSelectedCell(row, col) {
    if (!selectedCellElement) {
        return;
    }

    if (row === null || col === null) {
        selectedCellElement.textContent = "—";
        return;
    }

    selectedCellElement.textContent = `строка ${row + 1}, столбец ${col + 1}`;
}

function clearCellHighlights() {
    const cells = document.querySelectorAll(".cell");

    cells.forEach((cell) => {
        cell.classList.remove("selected", "correct", "wrong");
    });
}

function updateBoardVisibility(hasBoard) {
    if (boardElement) {
        boardElement.hidden = !hasBoard;
    }

    if (boardEmptyStateElement) {
        boardEmptyStateElement.hidden = hasBoard;
    }
}

function highlightSelectedCell() {
    clearCellHighlights();

    if (selectedRow === null || selectedCol === null) {
        return;
    }

    const selectedInput = document.querySelector(
        `.cell[data-row="${selectedRow}"][data-col="${selectedCol}"]`
    );

    if (selectedInput) {
        selectedInput.classList.add("selected");
    }
}

function renderBoard(board, fixedBoard) {
    if (!boardElement) {
        return;
    }

    updateBoardVisibility(true);
    boardElement.innerHTML = "";

    for (let row = 0; row < 9; row++) {
        for (let col = 0; col < 9; col++) {
            const input = document.createElement("input");
            input.type = "text";
            input.inputMode = "numeric";
            input.maxLength = 1;
            input.classList.add("cell");
            input.dataset.row = row;
            input.dataset.col = col;
            input.setAttribute("aria-label", `Клетка ${row + 1}:${col + 1}`);

            if ((col + 1) % 3 === 0 && col !== 8) {
                input.classList.add("border-right-bold");
            }

            if ((row + 1) % 3 === 0 && row !== 8) {
                input.classList.add("border-bottom-bold");
            }

            const value = board[row][col];
            const fixedValue = fixedBoard[row][col];

            if (value !== 0) {
                input.value = String(value);
            }

            if (fixedValue !== 0) {
                input.disabled = true;
                input.classList.add("fixed");
            } else {
                input.classList.add("editable");

                const selectCell = () => {
                    selectedRow = row;
                    selectedCol = col;
                    setSelectedCell(row, col);
                    highlightSelectedCell();
                };

                input.addEventListener("focus", selectCell);
                input.addEventListener("click", selectCell);

                input.addEventListener("input", (event) => {
                    const rawValue = event.target.value.trim();

                    selectCell();

                    if (rawValue === "") {
                        currentBoard[row][col] = 0;
                        return;
                    }

                    const numValue = Number(rawValue);

                    if (!Number.isInteger(numValue) || numValue < 1 || numValue > 9) {
                        event.target.value = "";
                        currentBoard[row][col] = 0;
                        setMessage("Введите число от 1 до 9");
                        return;
                    }

                    currentBoard[row][col] = numValue;
                });

                input.addEventListener("change", async (event) => {
                    const rawValue = event.target.value.trim();

                    selectCell();

                    if (rawValue === "") {
                        await sendMove(row, col, 0);
                        return;
                    }

                    const numValue = Number(rawValue);

                    if (!Number.isInteger(numValue) || numValue < 1 || numValue > 9) {
                        event.target.value = "";
                        currentBoard[row][col] = 0;
                        setMessage("Введите число от 1 до 9");
                        return;
                    }

                    await sendMove(row, col, numValue);
                });
            }

            boardElement.appendChild(input);
        }
    }

    highlightSelectedCell();
}

async function createNewGame() {
    try {
        const difficulty = difficultyElement.value;

        const response = await fetch("/api/v1/games", {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ difficulty })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Не удалось создать игру");
        }

        currentGameId = data.id;
        currentBoard = data.current_board;
        initialBoard = data.initial_board;
        selectedRow = null;
        selectedCol = null;

        setSelectedCell(null, null);
        setMessage(`Создана новая игра. Сложность: ${translateDifficulty(data.difficulty)}`);

        renderBoard(currentBoard, initialBoard);
    } catch (error) {
        setMessage(error.message);
    }
}

async function sendMove(row, col, value) {
    if (!currentGameId) {
        setMessage("Сначала создайте игру");
        return;
    }

    try {
        const response = await fetch(`/api/v1/games/${currentGameId}/move`, {
            method: "POST",
            headers: {
                "Content-Type": "application/json"
            },
            body: JSON.stringify({ row, col, value })
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Не удалось выполнить ход");
        }

        currentBoard = data.current_board;
        renderBoard(currentBoard, initialBoard);

        setMessage(data.message);
    } catch (error) {
        setMessage(error.message);
        renderBoard(currentBoard, initialBoard);
    }
}

async function checkGame() {
    if (!currentGameId) {
        setMessage("Сначала создайте игру");
        return;
    }

    try {
        const response = await fetch(`/api/v1/games/${currentGameId}/check`);
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Не удалось проверить игру");
        }

        currentBoard = data.current_board;
        renderBoard(currentBoard, initialBoard);

        setMessage(data.message);
    } catch (error) {
        setMessage(error.message);
    }
}

async function solveGame() {
    if (!currentGameId) {
        setMessage("Сначала создайте игру");
        return;
    }

    try {
        const response = await fetch(`/api/v1/games/${currentGameId}/solve`, {
            method: "POST"
        });

        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Не удалось решить игру");
        }

        currentBoard = data.current_board;
        initialBoard = data.initial_board;

        renderBoard(currentBoard, initialBoard);
        setMessage("Судоку решено");
    } catch (error) {
        setMessage(error.message);
    }
}

async function checkSelectedCell() {
    if (!currentGameId) {
        setMessage("Сначала создайте игру");
        return;
    }

    if (selectedRow === null || selectedCol === null) {
        setMessage("Сначала выберите клетку, которую хотите проверить");
        return;
    }

    try {
        const response = await fetch(
            `/api/v1/games/${currentGameId}/check-cell?row=${selectedRow}&col=${selectedCol}`
        );
        const data = await response.json();

        if (!response.ok) {
            throw new Error(data.detail || "Не удалось проверить клетку");
        }

        highlightSelectedCell();

        const selectedInput = document.querySelector(
            `.cell[data-row="${selectedRow}"][data-col="${selectedCol}"]`
        );

        if (selectedInput && data.checked) {
            selectedInput.classList.remove("correct", "wrong");
            selectedInput.classList.add(data.is_correct ? "correct" : "wrong");
        }

        setMessage(data.message);
    } catch (error) {
        setMessage(error.message);
    }
}

function translateDifficulty(value) {
    if (value === "easy") return "лёгкая";
    if (value === "medium") return "средняя";
    if (value === "hard") return "сложная";
    return value;
}

function openModal(modal) {
    if (!modal) {
        return;
    }

    lastFocusedElement = document.activeElement;
    activeModal = modal;
    modal.hidden = false;
    document.body.style.overflow = "hidden";

    const closeButton = modal.querySelector(".modal-close");

    if (closeButton) {
        closeButton.focus();
    }
}

function closeModal(modal = activeModal) {
    if (!modal) {
        return;
    }

    modal.hidden = true;
    document.body.style.overflow = "";
    activeModal = null;

    if (lastFocusedElement instanceof HTMLElement) {
        lastFocusedElement.focus();
    }
}

document.querySelectorAll("[data-modal-target]").forEach((button) => {
    button.addEventListener("click", () => {
        const modal = document.getElementById(button.dataset.modalTarget);
        openModal(modal);
    });
});

document.querySelectorAll("[data-modal-close]").forEach((element) => {
    element.addEventListener("click", () => closeModal(element.closest(".modal")));
});

document.addEventListener("keydown", (event) => {
    if (event.key === "Escape" && activeModal) {
        closeModal(activeModal);
    }
});

if (newGameButton) {
    newGameButton.addEventListener("click", createNewGame);
}

if (checkButton) {
    checkButton.addEventListener("click", checkGame);
}

if (solveButton) {
    solveButton.addEventListener("click", solveGame);
}

if (checkCellButton) {
    checkCellButton.addEventListener("click", checkSelectedCell);
}

updateBoardVisibility(false);
