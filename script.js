class Game2048 {
    constructor() {
        this.board = null;
        this.gameSettings = { height: 4, width: 4, win: 2048 };
        this.gameActive = false;
        this.initializeElements();
        this.setupEventListeners();
        this.showSetupModal();
    }

    initializeElements() {
        // Modals
        this.setupModal = document.getElementById('setup-modal');
        this.gameOverModal = document.getElementById('game-over-modal');

        // Setup form elements
        this.heightInput = document.getElementById('height');
        this.widthInput = document.getElementById('width');
        this.winTileSelect = document.getElementById('win-tile');
        this.startGameBtn = document.getElementById('start-game-btn');

        // Game elements
        this.gameBoard = document.getElementById('game-board');
        this.gameControls = document.getElementById('game-controls');
        this.targetTile = document.getElementById('target-tile');
        this.boardSize = document.getElementById('board-size');

        // Control buttons
        this.moveButtons = document.querySelectorAll('.move-btn');
        this.aiMoveBtn = document.getElementById('ai-move-btn');
        this.aiThinking = document.getElementById('ai-thinking');
        this.undoGameBtn = document.getElementById('undo-game-btn');
        this.restartGameBtn = document.getElementById('restart-game-btn');
        this.newGameSetupBtn = document.getElementById('new-game-setup-btn');

        // Game over modal buttons
        this.undoBtn = document.getElementById('undo-btn');
        this.restartBtn = document.getElementById('restart-btn');
        this.newGameBtn = document.getElementById('new-game-btn');

        // Status message
        this.statusMessage = document.getElementById('status-message');
    }

    setupEventListeners() {
        // Setup modal
        this.startGameBtn.addEventListener('click', () => this.startNewGame());

        // Move buttons
        this.moveButtons.forEach(btn => {
            btn.addEventListener('click', (e) => {
                const direction = e.target.dataset.direction;
                this.makeUserMove(direction);
            });
        });

        // AI and game controls
        this.aiMoveBtn.addEventListener('click', () => this.makeAIMove());
        this.undoGameBtn.addEventListener('click', () => this.undoMove());
        this.restartGameBtn.addEventListener('click', () => this.restartGame());
        this.newGameSetupBtn.addEventListener('click', () => this.showSetupModal());

        // Game over modal buttons
        this.undoBtn.addEventListener('click', () => this.undoFromGameOver());
        this.restartBtn.addEventListener('click', () => this.restartFromGameOver());
        this.newGameBtn.addEventListener('click', () => this.newGameFromGameOver());

        // Keyboard controls
        document.addEventListener('keydown', (e) => this.handleKeyPress(e));

        // Prevent modal close on outside click for setup
        this.setupModal.addEventListener('click', (e) => {
            if (e.target === this.setupModal) {
                e.preventDefault();
            }
        });
    }

    handleKeyPress(e) {
        if (!this.gameActive) return;

        const keyMap = {
            'ArrowUp': 'Up',
            'ArrowDown': 'Down',
            'ArrowLeft': 'Left',
            'ArrowRight': 'Right',
            'w': 'Up',
            'a': 'Left',
            's': 'Down',
            'd': 'Right',
            'W': 'Up',
            'A': 'Left',
            'S': 'Down',
            'D': 'Right'
        };

        const direction = keyMap[e.key];
        if (direction) {
            e.preventDefault();
            this.makeUserMove(direction);
        }
    }

    showSetupModal() {
        this.setupModal.classList.remove('hidden');
        this.gameControls.classList.add('hidden');
        this.gameBoard.classList.add('hidden');
    }

    hideSetupModal() {
        this.setupModal.classList.add('hidden');
    }

    showGameOverModal(isWin) {
        const title = document.getElementById('game-over-title');
        const message = document.getElementById('game-over-message');

        if (isWin) {
            title.textContent = '🎉 Congratulations!';
            message.textContent = `You reached the ${this.gameSettings.win} tile!`;
        } else {
            title.textContent = '💀 Game Over';
            message.textContent = 'No more moves possible!';
        }

        this.gameOverModal.classList.remove('hidden');
        this.gameActive = false;
    }

    hideGameOverModal() {
        this.gameOverModal.classList.add('hidden');
        this.gameActive = true;
    }

    async startNewGame() {
        try {
            const height = parseInt(this.heightInput.value);
            const width = parseInt(this.widthInput.value);
            const win = parseInt(this.winTileSelect.value);

            if (height < 2 || width < 2) {
                this.showStatus('Height and width must be at least 2!', 'error');
                return;
            }

            this.gameSettings = { height, width, win };

            const response = await fetch('/start_new_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(this.gameSettings)
            });

            if (response.ok) {
                this.hideSetupModal();
                this.updateGameInfo();
                this.createBoard();
                this.gameControls.classList.remove('hidden');
                this.gameBoard.classList.remove('hidden');
                this.gameActive = true;
                await this.updateBoard();
                this.showStatus('New game started!', 'success');
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to start game');
            }
        } catch (error) {
            this.showStatus('Error starting game', 'error');
            console.error(error);
        }
    }

    async restartGame() {
        try {
            const response = await fetch('/restart_game', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            if (response.ok) {
                this.gameActive = true;
                await this.updateBoard();
                this.showStatus('Game restarted!', 'success');
            } else {
                const errorData = await response.json();
                throw new Error(errorData.message || 'Failed to restart game');
            }
        } catch (error) {
            this.showStatus('Error restarting game', 'error');
            console.error(error);
        }
    }

    async makeUserMove(direction) {
        if (!this.gameActive) return;

        try {
            const response = await fetch('/make_user_move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify({ direction })
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                await this.updateBoard();
                await this.checkGameState();
            } else {
                this.showStatus(result.message || 'That move is not possible!', 'error');
            }
        } catch (error) {
            this.showStatus('Error making move', 'error');
            console.error(error);
        }
    }

    async makeAIMove() {
        if (!this.gameActive) return;

        this.aiMoveBtn.disabled = true;
        this.aiThinking.classList.remove('hidden');

        try {
            const response = await fetch('/make_ai_move', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                await this.updateBoard();
                await this.checkGameState();
                this.showStatus(result.message || 'AI made a move!', 'info');
            } else {
                this.showStatus(result.message || 'No moves available for AI!', 'error');
            }
        } catch (error) {
            this.showStatus('Error making AI move', 'error');
            console.error(error);
        } finally {
            this.aiMoveBtn.disabled = false;
            this.aiThinking.classList.add('hidden');
        }
    }

    async undoMove() {
        if (!this.gameActive) return;

        try {
            const response = await fetch('/undo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                await this.updateBoard();
                this.showStatus(result.message || 'Move undone!', 'success');
            } else {
                this.showStatus(result.message || 'No moves to undo!', 'error');
            }
        } catch (error) {
            this.showStatus('Error undoing move', 'error');
            console.error(error);
        }
    }

    async undoFromGameOver() {
        try {
            const response = await fetch('/undo', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' }
            });

            const result = await response.json();

            if (response.ok && result.status === 'success') {
                this.hideGameOverModal();
                await this.updateBoard();
                this.showStatus(result.message || 'Move undone!', 'success');
            } else {
                this.showStatus(result.message || 'No moves to undo!', 'error');
            }
        } catch (error) {
            this.showStatus('Error undoing move', 'error');
            console.error(error);
        }
    }

    async restartFromGameOver() {
        this.hideGameOverModal();
        await this.restartGame();
    }

    newGameFromGameOver() {
        this.hideGameOverModal();
        this.showSetupModal();
    }

    updateGameInfo() {
        this.targetTile.textContent = this.gameSettings.win.toLocaleString();
        this.boardSize.textContent = `${this.gameSettings.width}×${this.gameSettings.height}`;
    }

    createBoard() {
        this.gameBoard.innerHTML = '';
        this.gameBoard.style.display = 'grid';
        this.gameBoard.style.gridTemplateColumns = `repeat(${this.gameSettings.width}, 1fr)`;
        this.gameBoard.style.gridTemplateRows = `repeat(${this.gameSettings.height}, 1fr)`;

        // Calculate cell size based on board dimensions
        const maxBoardSize = Math.min(400, window.innerWidth - 100);
        const cellSize = Math.floor(maxBoardSize / Math.max(this.gameSettings.width, this.gameSettings.height)) - 4;

        for (let i = 0; i < this.gameSettings.height; i++) {
            for (let j = 0; j < this.gameSettings.width; j++) {
                const cell = document.createElement('div');
                cell.className = 'board-cell';
                cell.style.width = `${cellSize}px`;
                cell.style.height = `${cellSize}px`;
                cell.dataset.row = i;
                cell.dataset.col = j;
                this.gameBoard.appendChild(cell);
            }
        }
    }

    async updateBoard() {
        try {
            const response = await fetch('/get_board_state');
            if (!response.ok) {
                throw new Error('Failed to get board state');
            }

            const boardState = await response.json();
            this.board = boardState.board;

            const cells = this.gameBoard.querySelectorAll('.board-cell');
            cells.forEach(cell => {
                const row = parseInt(cell.dataset.row);
                const col = parseInt(cell.dataset.col);
                const value = this.board[row][col];

                // Clear previous tile classes
                cell.className = 'board-cell';
                cell.textContent = '';

                if (value > 0) {
                    cell.classList.add(`tile-${value}`);
                    cell.textContent = value.toLocaleString();
                }
            });
        } catch (error) {
            console.error('Error updating board:', error);
            this.showStatus('Error updating board display', 'error');
        }
    }

    async checkGameState() {
        try {
            const response = await fetch('/get_game_state');
            if (!response.ok) {
                throw new Error('Failed to get game state');
            }

            const gameState = await response.json();

            if (gameState.is_win) {
                this.showGameOverModal(true);
            } else if (gameState.is_gameover) {
                this.showGameOverModal(false);
            }
        } catch (error) {
            console.error('Error checking game state:', error);
        }
    }

    showStatus(message, type = 'info') {
        this.statusMessage.textContent = message;
        this.statusMessage.className = `status-message ${type} show`;

        setTimeout(() => {
            this.statusMessage.classList.remove('show');
        }, 3000);
    }
}

// Initialize the game when the page loads
document.addEventListener('DOMContentLoaded', () => {
    new Game2048();
});
