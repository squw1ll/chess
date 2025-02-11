FPS = 5

WHITE = 'white'
BLACK = 'black'

OPPOSITE_SIDE = {WHITE: BLACK, BLACK: WHITE}

# Ширина/высота одной клетки 
CELL_SIZE = 65


# Цвета для белых и черных клеток
WHITE_CELL_COLOR = (238, 238, 210)
BLACK_CELL_COLOR = (118, 150, 86)

# Цвет текста для сообщений
MSG_COLOR = (255, 10, 10)

SELECTED_CELL_COLOR = (120, 120, 255)

# Цвет грока если он под шахом
KING_ON_SHAH_COLOR = (255, 0, 0)

# доступной для хода
AVL_MOVE_CELL_COLOR = (255, 120, 120)

PAWN_MOVES = 'pawn_moves'
PAWN_TAKES = 'pawn_takes'

# Типы ходов
NORMAL_MOVE = 'normal_move'  # Обычный ход
TAKE_MOVE = 'take_move'      # Ход-взятие
CASTLING = 'castling'        # Рокировка
CONVERSION = 'conversion'    # Превращение пешки в другую фигуру
PASSED_TAKE = 'passed_take'  # Взятие на проходе

# Приоритеты ходов
priority_list = [TAKE_MOVE, CONVERSION, PASSED_TAKE, CASTLING, NORMAL_MOVE]


def key_func_for_moves(move):
    return priority_list.index(move.m_type, 0, 5)
MAT = 'mat'
PAT = 'pat'  
