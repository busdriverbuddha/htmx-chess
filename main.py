from fastapi import FastAPI, Request, Query
from fastapi.responses import HTMLResponse, JSONResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from pydantic import BaseModel

from chess_utils import get_piece_css_class, process_move, reset_board

app = FastAPI()

app.mount("/static", StaticFiles(directory="static"), name="static")


templates = Jinja2Templates(directory="templates")
messages = list()

class Move(BaseModel):
    uci: str


@app.get("/", response_class=HTMLResponse)
async def base(request: Request):
    return templates.TemplateResponse(
        request=request, name="base.html"
        )
    
    
@app.get("/_board/")
async def _board(request: Request, reset: bool = Query(False)):
    if reset:
        reset_board()
        global messages
        messages = list()
        
    squares = {}
    rows = range(8, 0, -1)
    columns = list('abcdefgh')
    
    for row in rows:
        squares[row] = {}
        for column in columns:
            squares[row][column] = get_piece_css_class(f"{column}{row}")

    return templates.TemplateResponse(
        request=request, name="_board.html", 
        context={
            'rows': rows,
            'columns': columns,
            'squares': squares,
        }
    ) 
    
    
@app.get("/_messagebox/", response_class=HTMLResponse)
async def base(request: Request):
    global messages
    return templates.TemplateResponse(
        request=request, name="_messagebox.html", context={'messages': messages}
        )
    

@app.post("/move/", response_class=JSONResponse)
def move(move: Move):
    accepted = True
    result = process_move(move.uci)
    match result:
        case 'checkmate':
            messages.append('Checkmate.')
        case 'stalemate':
            messages.append('Stalemate.')
        case 'accepted':
            pass
        case _:
            accepted = False
        
    return JSONResponse({'accepted': accepted})