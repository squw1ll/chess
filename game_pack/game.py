from game_pack.boards import *
from game_pack.ai import *

surface = None
#поле
board = None
# выбранная фигура 
selected_figure = None
# дсотупные ходы
avl_moves = []
#Сам ход
selected_move = None
# Шах
shah_flag = False
# Сообщение о победе или поражении 
msg = None


def start(player_side):
    global surface, board, selected_figure, avl_moves, selected_move, mode, shah_flag, msg
    pygame.init()
    pygame.display.set_caption('Chess @squw1ll') 
    surface = pygame.display.set_mode((CELL_SIZE * 8, CELL_SIZE * 8), pygame.NOFRAME)
    clock = pygame.time.Clock()

    # белый или черный цвет
    computer_side = OPPOSITE_SIDE[player_side]

    # Белые первые
    if computer_side == WHITE:
        mode = 'mode_5'
    else:
        mode = 'mode_1'

    main_board = Board(player_side)
    board = main_board

    # Нейросеть
    ai = Ai(computer_side, main_board)

    while True:
        # Обрабатываем события
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button != 1:
                    continue

                if mode == 'mode_1':
                    selected_figure = get_mouse_selected_figure(event, player_side)
                    if selected_figure is not None:
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                        if avl_moves:
                            mode = 'mode_2'
                            continue

                if mode == 'mode_2':
                    selected_row, selected_col = get_mouse_selected_cell(event)
                    selected_move = None
                    for move in avl_moves:
                        if selected_row == move.new_row and selected_col == move.new_col:
                            selected_move = move
                            break

                    if selected_move is not None:
                        if selected_move.m_type == CONVERSION:
                            selected_figure = None
                            avl_moves = []
                            board = SelectorBoard(player_side, main_board)
                            mode = 'mode_3'
                            continue
                        mode = 'mode_4'
                        continue

                    new_selected_figure = get_mouse_selected_figure(event, player_side)
                    if new_selected_figure is not None:
                        selected_figure = new_selected_figure
                        avl_moves = board.get_avl_moves_for_figure(selected_figure)
                    continue

                if mode == 'mode_3':
                    selected_figure = get_mouse_selected_figure(event, player_side)
                    if selected_figure is not None:
                        selected_figure.set_pos(selected_move.new_row, selected_move.new_col)
                        selected_move.new_figure = selected_figure
                        board = main_board
                        mode = 'mode_4'
                        continue

                if mode == 'mode_6':
                    exit()


        if mode == 'mode_4':
            board.apply_move(selected_move)
            selected_figure = None
            selected_move = None
            avl_moves = []

            shah_flag = False

            game_over = check_game_over(computer_side)
            if game_over == MAT:
                msg = 'You  win!!'
                mode = 'mode_6'
                continue
            if game_over == PAT:
                msg = 'draw'
                mode = 'mode_6'
                continue

            mode = 'mode_5'
            repaint()


        if mode == 'mode_5':
            move = ai.get_next_move()
            board.apply_move(move)
            selected_figure = None
            selected_move = None
            avl_moves = []

            if board.is_strike_figure(board.pl_king):
                shah_flag = True


            game_over = check_game_over(player_side)
            if game_over == MAT:
                msg = 'You lose...'
                mode = 'mode_6'
                continue
            if game_over == PAT:
                msg = 'Draw'
                mode = 'mode_6'
                continue

            mode = 'mode_1'

        repaint()
        clock.tick(FPS)



def check_game_over(side):
    king = board.kings_dict[side]
    sh_flag = board.is_strike_figure(king)
    avl_flag = (len(board.get_all_avl_moves(side)) == 0)
    if avl_flag and sh_flag:
        return MAT
    if avl_flag and not sh_flag:
        return PAT
    return None


def repaint():
    draw_cells()
    draw_select_cell()
    draw_avl_moves()
    draw_shah_cell()
    draw_figures()
    draw_msg()
    pygame.display.update()


def draw_cells():
    for r in range(0, 8):
        for c in range(0, 8):
            if (r + c) % 2 == 0:
                color = WHITE_CELL_COLOR
            else:
                color = BLACK_CELL_COLOR
            pygame.draw.rect(surface, color, (c * CELL_SIZE, r * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_figures():
    for row in range(0, 8):
        for col in range(0, 8):
            figure = board.get_figure(row, col)
            if figure is None:
                continue
            surface.blit(figure.image, figure.rect)

def draw_select_cell():
    if selected_figure:
        pygame.draw.rect(surface, SELECTED_CELL_COLOR,
                         (selected_figure.col * CELL_SIZE, selected_figure.row * CELL_SIZE, CELL_SIZE, CELL_SIZE))


def draw_avl_moves():
    for move in avl_moves:
        row_move = move.new_row
        col_move = move.new_col
        pygame.draw.rect(surface, AVL_MOVE_CELL_COLOR,
                         (col_move * CELL_SIZE + 4, row_move * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))
    pass


def draw_shah_cell():
    if shah_flag:
        row = board.pl_king.row
        col = board.pl_king.col
        pygame.draw.rect(surface, KING_ON_SHAH_COLOR,
                         (col * CELL_SIZE + 4, row * CELL_SIZE + 4, CELL_SIZE - 8, CELL_SIZE - 8))


def draw_msg():
    if not msg:
        return
    font = pygame.font.Font(None, 56)
    msg_surface = font.render(msg, 1, MSG_COLOR)
    x_pos = CELL_SIZE * 4 - msg_surface.get_width() // 2
    y_pos = CELL_SIZE * 4 - msg_surface.get_height() // 2
    msg_rect = msg_surface.get_rect(topleft=(x_pos, y_pos))

    surface.blit(msg_surface, msg_rect)



def get_mouse_selected_cell(mouse_event):
    c = mouse_event.pos[0] // CELL_SIZE
    r = mouse_event.pos[1] // CELL_SIZE
    return r, c


def get_mouse_selected_figure(mouse_event, side=None):
    selected_row, selected_col = get_mouse_selected_cell(mouse_event)
    figure = board.get_figure(selected_row, selected_col)
    if side is not None and figure is not None:
        if figure.side != side:
            return None
    return figure
