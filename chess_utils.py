import chess


board = chess.Board()


def get_piece_css_class(square_name: str) -> str:
    square_index = chess.parse_square(square_name)
    piece = board.piece_at(chess.Square(square_index))
    if piece is not None:
        piece_name = {
            chess.BISHOP: 'bishop',
            chess.KING: 'king',
            chess.KNIGHT: 'knight',
            chess.PAWN: 'pawn',
            chess.QUEEN: 'queen',
            chess.ROOK: 'rook',
        }.get(piece.piece_type)
        style = 'solid' if piece.color == chess.BLACK else 'regular'
        icon_css_class = f'fa-{style} fa-chess-{piece_name} fa-2xl'
    else:
        icon_css_class = ""
    return {
            'icon_css_class': icon_css_class,
            'div_css_class': 'darksquare' if (square_index // 8 + square_index % 8) % 2 == 0 else 'lightsquare'
        }


def process_move(move_uci: str):
    move = chess.Move.from_uci(move_uci)
    if move in board.legal_moves:
        board.push(move)
        if board.is_checkmate():
            return 'checkmate'
        elif board.is_stalemate():
            return 'stalemate'
        else:
            return 'accepted'
    

def reset_board():
    global board
    board.reset()
    
