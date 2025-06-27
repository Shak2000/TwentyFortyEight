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
async def start_new_game(height=4, width=4, win=2048):
    game.board = Board(height, width, win)
    game.ai = AI(game.board)
    game.board.spawn()
    game.board.spawn()


@app.post("/restart_game")
async def restart_game():
    game.restart_game()


@app.post("/make_user_move")
async def make_user_move():
    game.make_user_move()


@app.post("/make_ai_move")
async def make_ai_move():
    game.make_ai_move()


@app.post("/undo")
async def undo():
    game.board.undo()
