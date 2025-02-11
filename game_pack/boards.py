from game_pack.figures import *


class Move:

    def __init__(self, move_type, figure, new_row, new_col):
        self.m_type = move_type
        self.figure = figure
        self.new_row = new_row
        self.new_col = new_col
        self.old_row = figure.row
        self.old_col = figure.col


class Board:

    def __init__(self, pl_side):
        self.pl_side = pl_side
        self.cmp_side = OPPOSITE_SIDE[pl_side]
        self.pl_figures = []
        self.cmp_figures = []
        self.figures_dict = {self.pl_side: self.pl_figures, self.cmp_side: self.cmp_figures}
        self.kings_dict = {}
        if self.cmp_side == WHITE:
            self.cmp_king = King(0, 3, self.cmp_side, self)
            self.kings_dict[WHITE] = self.cmp_king
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 4, self.cmp_side, self))
        if self.cmp_side == BLACK:
            self.cmp_king = King(0, 4, self.cmp_side, self)
            self.kings_dict[BLACK] = self.cmp_king
            self.cmp_figures.append(self.cmp_king)
            self.cmp_figures.append(Queen(0, 3, self.cmp_side, self))
        self.cmp_figures.append(Rook(0, 0, self.cmp_side, self))
        self.cmp_figures.append(Rook(0, 7, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 1, self.cmp_side, self))
        self.cmp_figures.append(Knight(0, 6, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 2, self.cmp_side, self))
        self.cmp_figures.append(Bishop(0, 5, self.cmp_side, self))
        for i in range(0, 8):
            self.cmp_figures.append(Pawn(1, i, self.cmp_side, self))
        if self.pl_side == BLACK:
            self.pl_king = King(7, 3, self.pl_side, self)
            self.kings_dict[BLACK] = self.pl_king
            self.pl_figures.append(self.pl_king)
            self.pl_figures.append(Queen(7, 4, self.pl_side, self))

        if self.pl_side == WHITE:
            self.pl_king = King(7, 4, self.pl_side, self)
            self.kings_dict[WHITE] = self.pl_king
            self.pl_figures.append(self.pl_king)
            self.pl_figures.append(Queen(7, 3, self.pl_side, self))

        self.pl_figures.append(Rook(7, 0, self.pl_side, self))
        self.pl_figures.append(Rook(7, 7, self.pl_side, self))
        self.pl_figures.append(Knight(7, 1, self.pl_side, self))
        self.pl_figures.append(Knight(7, 6, self.pl_side, self))
        self.pl_figures.append(Bishop(7, 2, self.pl_side, self))
        self.pl_figures.append(Bishop(7, 5, self.pl_side, self))

        for i in range(0, 8):
            self.pl_figures.append(Pawn(6, i, self.pl_side, self))

        self.cells = []
        for i in range(0, 8):
            self.cells.append([None] * 8)
        for figure in (self.cmp_figures + self.pl_figures):
            self.cells[figure.row][figure.col] = figure

        self.move_list = []
        self.values_figure = {
            Pawn: 100,
            Knight: 300,
            Bishop: 300,
            Rook: 500,
            Queen: 900,
            King: 9000
        }

        self.pos_pl_king = [
            [25, 25, 21, 15, 15, 21, 25, 25],
            [21, 21, 17, 13, 13, 17, 21, 21],
            [13, 13, 5, 5, 5, 5, 13, 13],
            [9, 5, 0, 0, 0, 0, 5, 9],
            [9, 5, 0, 0, 0, 0, 5, 9],
            [13, 13, 5, 5, 5, 5, 13, 13],
            [21, 21, 17, 13, 13, 17, 21, 21],
            [25, 25, 21, 15, 15, 21, 25, 25]
        ]

        self.pos_pl_queen = [
            [20, 25, 25, 30, 30, 25, 25, 20],
            [17, 20, 25, 27, 27, 25, 20, 17],
            [15, 18, 20, 25, 25, 20, 18, 15],
            [12, 15, 19, 21, 21, 19, 15, 12],
            [11, 15, 19, 21, 21, 19, 15, 11],
            [10, 15, 17, 19, 19, 17, 15, 10],
            [8, 12, 15, 15, 15, 15, 12, 8],
            [7, 10, 15, 20, 20, 15, 10, 7]
        ]

        self.pos_pl_rook = [
            [20, 25, 25, 30, 30, 25, 25, 20],
            [17, 20, 25, 27, 27, 25, 20, 17],
            [15, 18, 20, 25, 25, 20, 18, 15],
            [12, 15, 19, 21, 21, 19, 15, 12],
            [11, 15, 19, 21, 21, 19, 15, 11],
            [10, 15, 17, 19, 19, 17, 15, 10],
            [8, 12, 15, 15, 15, 15, 12, 8],
            [7, 10, 15, 20, 20, 15, 10, 7]
        ]

        self.pos_pl_bishop = [
            [14, 14, 14, 14, 14, 14, 14, 14],
            [14, 22, 18, 18, 18, 18, 22, 14],
            [14, 18, 22, 22, 22, 22, 18, 14],
            [14, 18, 22, 25, 25, 22, 18, 14],
            [14, 18, 22, 25, 25, 22, 18, 14],
            [14, 18, 22, 22, 22, 22, 18, 14],
            [14, 22, 18, 18, 18, 18, 22, 14],
            [14, 14, 14, 14, 14, 14, 14, 14]
        ]

        self.pos_pl_knight = [
            [0, 4, 8, 10, 10, 8, 4, 0],
            [4, 8, 16, 20, 20, 16, 8, 4],
            [8, 16, 24, 28, 28, 24, 16, 8],
            [10, 20, 28, 32, 32, 28, 20, 10],
            [10, 20, 28, 32, 32, 28, 20, 10],
            [8, 16, 24, 28, 28, 24, 16, 8],
            [4, 8, 16, 20, 20, 16, 8, 4],
            [0, 4, 8, 10, 10, 8, 4, 0]
        ]

        self.pos_pl_pawn = [
            [20, 20, 28, 35, 35, 28, 20, 20],
            [25, 25, 28, 32, 32, 28, 25, 25],
            [15, 18, 25, 32, 32, 25, 18, 15],
            [8, 12, 16, 24, 24, 16, 12, 8],
            [6, 8, 12, 16, 16, 12, 8, 6],
            [6, 8, 8, 12, 12, 8, 8, 6],
            [4, 4, 4, 6, 6, 4, 4, 4],
            [0, 0, 0, 0, 0, 0, 0, 0]
        ]

        def create_cmp_pos_table(source_table):
            result = []
            for line in reversed(source_table):
                result.append(line)
            return result

        self.pos_cmp_king = create_cmp_pos_table(self.pos_pl_king)
        self.pos_cmp_queen = create_cmp_pos_table(self.pos_pl_queen)
        self.pos_cmp_rook = create_cmp_pos_table(self.pos_pl_rook)
        self.pos_cmp_bishop = create_cmp_pos_table(self.pos_pl_bishop)
        self.pos_cmp_knight = create_cmp_pos_table(self.pos_pl_knight)
        self.pos_cmp_pawn = create_cmp_pos_table(self.pos_pl_pawn)

        self.pos_pl_dict = {}
        self.pos_pl_dict[Pawn] = self.pos_pl_pawn
        self.pos_pl_dict[Knight] = self.pos_pl_knight
        self.pos_pl_dict[Bishop] = self.pos_pl_bishop
        self.pos_pl_dict[Rook] = self.pos_pl_rook
        self.pos_pl_dict[Queen] = self.pos_pl_queen
        self.pos_pl_dict[King] = self.pos_pl_king

        self.pos_cmp_dict = {}
        self.pos_cmp_dict[Pawn] = self.pos_cmp_pawn
        self.pos_cmp_dict[Knight] = self.pos_cmp_knight
        self.pos_cmp_dict[Bishop] = self.pos_cmp_bishop
        self.pos_cmp_dict[Rook] = self.pos_cmp_rook
        self.pos_cmp_dict[Queen] = self.pos_cmp_queen
        self.pos_cmp_dict[King] = self.pos_cmp_king

    def position_evaluation(self):

        def get_evals(side):
            work_list = self.figures_dict[side]
            king = self.kings_dict[side]
            value_eval = 0
            pos_eval = 0
            actions_eval = 0
            for figure in work_list:
                if figure.is_drop:
                    continue
                figure_type = type(figure)
                value_eval += self.values_figure[figure_type]
                pos_eval += self.pos_cmp_dict[figure_type][figure.row][figure.col] * 5
                if figure_type == King:
                    continue
                if figure_type == Pawn:
                    actions = figure.get_actions(PAWN_TAKES)
                else:
                    actions = figure.get_actions()
                for row, col in actions:
                    figure_on_action = self.get_figure(row, col)
                    if figure_on_action is None:
                        continue
                    if figure_on_action is king:
                        continue
                    figure_on_action_type = type(figure_on_action)
                    actions_eval += self.values_figure[figure_on_action_type] // 40
            return value_eval + pos_eval + actions_eval
        return get_evals(self.cmp_side) - get_evals(self.pl_side)

    def get_moves_count(self):
        return len(self.move_list)

    def get_figures_count(self):
        count = 0
        for figure in (self.pl_figures + self.cmp_figures):
            if not figure.is_drop:
                count += 1
        return count

    def get_all_avl_moves(self, side):
        work_list = self.figures_dict[side]

        result = []
        for figure in work_list:
            if figure.is_drop:
                continue
            avl_moves = self.get_avl_moves_for_figure(figure)
            result += avl_moves

        result.sort(key=key_func_for_moves)

        return result

    def get_avl_moves_for_figure(self, figure):
        moves = []

        figure_type = type(figure)
        if figure_type == Pawn:
            actions = figure.get_actions(PAWN_MOVES)
            for new_row, new_col in actions:
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_normal_move(figure, new_row, new_col))

            actions = figure.get_actions(PAWN_TAKES)
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    continue
                if drop_figure.side == figure.side:
                    continue
                if new_row == 0 or new_row == 7:
                    moves.append(self.create_conversion_move(figure, new_row, new_col))
                else:
                    moves.append(self.create_take_move(figure, new_row, new_col))
            if self.get_moves_count() > 0:
                last_move = self.move_list[-1]
                if type(last_move.figure) == Pawn and last_move.figure.side != figure.side:
                    r0 = min(last_move.new_row, last_move.old_row)
                    r2 = max(last_move.new_row, last_move.old_row)
                    if (r2 - r0) == 2:
                        c = last_move.new_col
                        for r1, c1 in actions:
                            if r0 < r1 < r2 and c1 == c:
                                moves.append(self.create_passed_take_move(figure, r1, c1, last_move.figure))

        if figure_type == King:
            if not self.was_move(figure):
                if not self.is_strike_cell(figure.row, figure.col, OPPOSITE_SIDE[figure.side]):

                    l_rook = self.get_figure(figure.row, 0)
                    if type(l_rook) == Rook:
                        if not self.was_move(l_rook):
                            cell_list = [(figure.row, 1), (figure.row, 2)]
                            if figure.col == 4:
                                cell_list.append((figure.row, 3))
                            allowed_cells_flag = True
                            for row_cell, col_cell in cell_list:
                                figure_on_cell = self.get_figure(row_cell, col_cell)
                                if figure_on_cell is not None or self.is_strike_cell(row_cell, col_cell,
                                                                                     OPPOSITE_SIDE[figure.side]):
                                    allowed_cells_flag = False
                                    break
                            if allowed_cells_flag:
                                moves.append(
                                    self.create_castling_move(figure, figure.row, figure.col - 2, l_rook, figure.row,
                                                              figure.col - 1))

                    r_rook = self.get_figure(figure.row, 7)
                    if type(r_rook) == Rook:
                        if not self.was_move(r_rook):
                            cell_list = [(figure.row, 6), (figure.row, 5)]
                            if figure.col == 3:
                                cell_list.append((figure.row, 4))
                            allowed_cells_flag = True
                            for row_cell, col_cell in cell_list:
                                figure_on_cell = self.get_figure(row_cell, col_cell)
                                if figure_on_cell is not None or self.is_strike_cell(row_cell, col_cell,
                                                                                     OPPOSITE_SIDE[figure.side]):
                                    allowed_cells_flag = False
                                    break
                            if allowed_cells_flag:
                                moves.append(
                                    self.create_castling_move(figure, figure.row, figure.col + 2, r_rook, figure.row,
                                                              figure.col + 1))

        if figure_type != Pawn:
            actions = figure.get_actions()
            for new_row, new_col in actions:
                drop_figure = self.get_figure(new_row, new_col)
                if drop_figure is None:
                    moves.append(self.create_normal_move(figure, new_row, new_col))
                    continue
                if drop_figure.side != figure.side:
                    moves.append(self.create_take_move(figure, new_row, new_col))

        avl_moves = []
        king = self.kings_dict[figure.side]
        for move in moves:
            if move.m_type == CONVERSION:
                move.new_figure = Queen(move.new_row, move.new_col, figure.side, self)
            self.apply_move(move)
            if not self.is_strike_figure(king):
                avl_moves.append(move)
            self.cancel_move()
            if move.m_type == CONVERSION:
                move.new_figure = None
        moves = avl_moves
        return moves

    @staticmethod
    def create_normal_move(figure, new_row, new_col):
        move = Move(NORMAL_MOVE, figure, new_row, new_col)
        return move
    def create_take_move(self, figure, new_row, new_col):
        move = Move(TAKE_MOVE, figure, new_row, new_col)
        move.drop_figure = self.get_figure(new_row, new_col)
        return move

    def create_conversion_move(self, figure, new_row, new_col):
        move = Move(CONVERSION, figure, new_row, new_col)
        move.drop_figure = self.get_figure(new_row, new_col)
        move.new_figure = None
        return move

    @staticmethod
    def create_passed_take_move(figure, new_row, new_col, drop_figure):
        move = Move(PASSED_TAKE, figure, new_row, new_col)
        move.drop_figure = drop_figure
        return move

    @staticmethod
    def create_castling_move(figure, new_row_figure, new_col_figure, rook, new_row_rook, new_col_rook):
        move = Move(CASTLING, figure, new_row_figure, new_col_figure)

        move.rook = rook
        move.old_row_rook = rook.row
        move.old_col_rook = rook.col
        move.new_row_rook = new_row_rook
        move.new_col_rook = new_col_rook

        return move

    def apply_move(self, move):
        self.move_list.append(move)

        if move.m_type == NORMAL_MOVE:
            move.figure.set_pos(move.new_row, move.new_col)
            self.cells[move.old_row][move.old_col] = None
            self.cells[move.new_row][move.new_col] = move.figure
            return

        if move.m_type == TAKE_MOVE or move.m_type == PASSED_TAKE:
            move.figure.set_pos(move.new_row, move.new_col)
            move.drop_figure.is_drop = True
            self.cells[move.drop_figure.row][move.drop_figure.col] = None
            self.cells[move.old_row][move.old_col] = None
            self.cells[move.new_row][move.new_col] = move.figure
            return

        if move.m_type == CONVERSION:
            move.figure.set_pos(move.new_row, move.new_col)
            move.figure.is_drop = True
            if move.drop_figure is not None:
                move.drop_figure.is_drop = True
            self.figures_dict[move.new_figure.side].append(move.new_figure)
            self.cells[move.old_row][move.old_col] = None
            self.cells[move.new_figure.row][move.new_figure.col] = move.new_figure

        if move.m_type == CASTLING:
            move.figure.set_pos(move.new_row, move.new_col)
            move.rook.set_pos(move.new_row_rook, move.new_col_rook)
            self.cells[move.old_row][move.old_col] = None
            self.cells[move.new_row][move.new_col] = move.figure
            self.cells[move.old_row_rook][move.old_col_rook] = None
            self.cells[move.new_row_rook][move.new_col_rook] = move.rook
            return

    def cancel_move(self):
        if self.get_moves_count() == 0:
            return
        last_move = self.move_list.pop(-1)
        if last_move.m_type == NORMAL_MOVE:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            # Перемещаем фигуру на старое место
            self.cells[last_move.new_row][last_move.new_col] = None
            self.cells[last_move.old_row][last_move.old_col] = last_move.figure
            return

        if last_move.m_type == TAKE_MOVE or last_move.m_type == PASSED_TAKE:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.drop_figure.is_drop = False
            self.cells[last_move.new_row][last_move.new_col] = None
            self.cells[last_move.old_row][last_move.old_col] = last_move.figure
            self.cells[last_move.drop_figure.row][last_move.drop_figure.col] = last_move.drop_figure
            return

        if last_move.m_type == CONVERSION:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.figure.is_drop = False
            if last_move.drop_figure is not None:
                last_move.drop_figure.is_drop = False
            work_list = self.figures_dict[last_move.new_figure.side]
            work_list.remove(last_move.new_figure)
            self.cells[last_move.new_row][last_move.new_col] = None
            self.cells[last_move.old_row][last_move.old_col] = last_move.figure
            if last_move.drop_figure is not None:
                self.cells[last_move.drop_figure.row][last_move.drop_figure.col] = last_move.drop_figure
            return

        if last_move.m_type == CASTLING:
            last_move.figure.set_pos(last_move.old_row, last_move.old_col)
            last_move.rook.set_pos(last_move.old_row_rook, last_move.old_col_rook)
            self.cells[last_move.new_row][last_move.new_col] = None
            self.cells[last_move.old_row][last_move.old_col] = last_move.figure
            self.cells[last_move.new_row_rook][last_move.new_col_rook] = None
            self.cells[last_move.old_row_rook][last_move.old_col_rook] = last_move.rook
            return
    def is_strike_cell(self, row, col, side):
        work_list = self.figures_dict[side]
        for figure in work_list:
            if figure.is_drop:
                continue
            figure_type = type(figure)
            if figure_type == Pawn:
                actions = figure.get_actions(PAWN_TAKES)
            else:
                actions = figure.get_actions()
            for r, c in actions:
                if r == row and c == col:
                    return True

        return False
    def is_strike_figure(self, figure):
        return self.is_strike_cell(figure.row, figure.col, OPPOSITE_SIDE[figure.side])

    def was_move(self, figure):
        for move in self.move_list:
            if figure == move.figure:
                return True
        return False

    def get_figure(self, r, c):
        return self.cells[r][c]


class SelectorBoard:

    def __init__(self, side, main_board):
        self.queen = Queen(3, 3, side, main_board)
        self.rook = Rook(3, 4, side, main_board)
        self.bishop = Bishop(4, 3, side, main_board)
        self.knight = Knight(4, 4, side, main_board)

    def get_figure(self, r, c):
        if r == 3 and c == 3:
            return self.queen
        if r == 3 and c == 4:
            return self.rook
        if r == 4 and c == 3:
            return self.bishop
        if r == 4 and c == 4:
            return self.knight
