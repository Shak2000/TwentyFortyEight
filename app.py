from fastapi import FastAPI
from fastapi.responses import FileResponse
from pydantic import BaseModel

from main import Board, AI, Game

game = Game()
app = FastAPI()


class BoardConfig(BaseModel):
    height: int
    width: int
    win: int


class MoveRequest(BaseModel):
    direction: str


@app.get("/")
async def get_ui():
    return FileResponse("index.html")


@app.get("/styles.css")
async def get_styles():
    return FileResponse("styles.css")


@app.get("/script.js")
async def get_script():
    return FileResponse("script.js")


@app.post("/start_new_game")
async def start_new_game(config: BoardConfig):
    game.board = Board(config.height, config.width, config.win)
    game.ai = AI(game.board)
    game.board.spawn()
    game.board.spawn()
    return {"status": "success", "message": "Game started"}


@app.post("/restart_game")
async def restart_game():
    if game.board:
        height, width, win = game.board.height, game.board.width, game.board.win
        game.board = Board(height, width, win)
        game.ai = AI(game.board)
        game.board.spawn()
        game.board.spawn()
        return {"status": "success", "message": "Game restarted"}
    return {"status": "error", "message": "No game to restart"}


@app.post("/make_user_move")
async def make_user_move(move: MoveRequest):
    if game.board and game.board.move_is_possible(move.direction):
        game.board.move(move.direction)
        game.board.spawn()
        return {"status": "success", "message": f"Moved {move.direction}"}
    return {"status": "error", "message": "Move not possible"}


@app.post("/make_ai_move")
async def make_ai_move():
    if game.board and game.ai:
        best_move = game.ai.get_best_move()
        if best_move:
            game.board.move(best_move)
            game.board.spawn()
            return {"status": "success", "message": f"AI moved {best_move}"}
    return {"status": "error", "message": "No AI move available"}


@app.post("/undo")
async def undo():
    if game.board and game.board.undo():
        return {"status": "success", "message": "Move undone"}
    return {"status": "error", "message": "No moves to undo"}


@app.get("/get_board_state")
async def get_board_state():
    if game.board:
        return {
            "board": game.board.board,
            "height": game.board.height,
            "width": game.board.width,
            "win": game.board.win
        }
    return {"board": [], "height": 0, "width": 0, "win": 0}


@app.get("/get_game_state")
async def get_game_state():
    if game.board:
        return {
            "is_win": game.board.is_win(),
            "is_gameover": game.board.is_gameover()
        }
    return {"is_win": False, "is_gameover": False}
