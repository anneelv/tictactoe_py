import pygame
import sys
from pygame.locals import *
import random

# .init() to start the game environment
pygame.init()
pygame.font.init()

window_size = (450, 500)
cell_size = 150

screen = pygame.display.set_mode(window_size)
pygame.display.set_caption("Tic Tac Toe")

class TicTacToe():

    # Initializing game environment
    def __init__(self, table_size):
        self.table_size = table_size
        self.cell_size = table_size // 3
        self.table_space = 20 # padding from the edges of the game window
        self.table = [] # Represent the game board
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")

        self.player = "X"
        self.winner = None
        self.taking_move = True
        self.running = True

        self.background_color = (0, 155, 255)
        self.table_color = (50, 50, 50)
        self.line_color = (190, 0 ,10)
        self.instruction_color = (17, 53, 165)
        self.game_over_bg_color = (47, 98, 162)
        self.game_over_color = (255, 179, 1)
        self.font = pygame.font.SysFont("Courier New", 35)
        self.FPS = pygame.time.Clock()

    # Drawing the table for the game
    def _draw_table(self):
        tb_space_point = (self.table_space, self.table_size - self.table_space)
        cell_space_point = (self.cell_size, self.cell_size * 2)
        # tb_space_point[0] to give padding on the left and top side of the table
        # tb_space_point[1] to give padding on the right and bottom side of the table
        r1 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[0]], [tb_space_point[1], cell_space_point[0]], 8)
        c1 = pygame.draw.line(screen, self.table_color, [cell_space_point[0], tb_space_point [0]], [cell_space_point[0], tb_space_point [1]], 8)
        r2 = pygame.draw.line(screen, self.table_color, [tb_space_point[0], cell_space_point[1]], [tb_space_point[1], cell_space_point[1]], 8)
        c2 = pygame.draw.line(screen, self.table_color, [cell_space_point[1], tb_space_point [0]], [cell_space_point[1], tb_space_point [1]], 8)

    # Changing player
    def _change_player(self):
        self.player = "O" if self.player == "X" else "X"

    # Handling user clicks
    def _move(self, pos):
        try:
             # pos represent the position of user click on the board
            x, y = pos[0] // self.cell_size, pos[1] // self.cell_size
            if self.table[x][y] == "-":
                self.table[x][y] = self.player # Change the value from "-" to the player mark
                self._draw_char(x,y,self.player)
                self._game_check()
                self._change_player()
        except:
            print("Click inside the table only")

    # Draw image to represent the action of the player
    def _draw_char(self, x, y, player):
        if self.player == "O":
            img = pygame.image.load("images_3t/Tc-O.png")
        elif self.player == "X":
            img = pygame.image.load("images_3t/Tc-X.png")
        # resizing the image size to fit the table space
        img = pygame.transform.scale(img, (self.cell_size, self.cell_size))
        # blit = draw to the window
        screen.blit(img, (x * self.cell_size, y * self.cell_size, self.cell_size, self.cell_size))

    # Game messages
    def _message(self):
        if self.winner is not None:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35)) # numbers are coordinates indicating the location and size of the area
            msg = self.font.render(f'{self.winner} WINS!!', True, self.game_over_color)
            screen.blit(msg,(144,445)) # the numbers are the coordinate to print the message
        elif not self.taking_move:
            screen.fill(self.game_over_bg_color, (130, 445, 193, 35))
            instructions = self.font.render('DRAW!!', True, self.game_over_color)
            screen.blit(instructions, (165, 445))
        else:
            screen.fill(self.game_over_bg_color, (135, 445, 188, 35))
            instructions = self.font.render(f'{self.player} to move', True, self.instruction_color)
            screen.blit(instructions, (135, 445))

    # Checking the winner of the game
    def _game_check(self):
        # vertical check
        for x_index, col in enumerate(self.table):
            win = True
            pattern_list = []
            for y_index, content in enumerate(col):
                if content != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((x_index, y_index))

            if win == True:
                self._pattern_strike(pattern_list[0], pattern_list[-1],"ver")
                self.winner = self.player
                self.taking_move = False
                self._message()
                self._draw_reset()
                self._move(self.event.pos)
                break

        # horizontal check
        for row in range(len(self.table)):
            win = True
            pattern_list = []
            for col in range(len(self.table)):
                if self.table[col][row] != self.player:
                    win = False
                    break
                else:
                    pattern_list.append((col, row))
            if win == True:
                self._pattern_strike(pattern_list[0],pattern_list[-1],"hor")
                self.winner = self.player
                self.taking_move = False
                self._message()
                self._draw_reset()
                self._move(self.event.pos)
                break

        # left diagonal check
        for index, row in enumerate(self.table):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self._pattern_strike((0,0), (2,2), "left-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()
            self._draw_reset()
            self._move(self.event.pos)

        # right diagonal check
        for index, row in enumerate(self.table[::-1]):
            win = True
            if row[index] != self.player:
                win = False
                break
        if win == True:
            self._pattern_strike((2,0),(0,2),"right-diag")
            self.winner = self.player
            self.taking_move = False
            self._message()
            self._draw_reset()
            self._move(self.event.pos)

        # check blank table cells
        blank_cells = 0
        for row in self.table:
            for cell in row:
                if cell == "-":
                    blank_cells += 1
        if blank_cells == 0:
            self.taking_move = False
            self._message()
            self._draw_reset()
            self._move(self.event.pos)

    # Highlighting the winning pattern
    def _pattern_strike(self, start_point, end_point, line_type):
        # get the middle calue of the cell
        mid_val = self.cell_size // 2

        # for vertical winning pattern
        if line_type == "ver":
            start_x, start_y = start_point[0] * self.cell_size + mid_val, self.table_space
            end_x, end_y = end_point[0] * self.cell_size + mid_val, self.table_size - self.table_space

            # for the horizontal winning pattern
        elif line_type == "hor":
            start_x, start_y = self.table_space, start_point[-1] * self.cell_size + mid_val
            end_x, end_y = self.table_size - self.table_space, end_point[-1] * self.cell_size + mid_val

        # for the diagonal winning pattern from top-left to bottom right
        elif line_type == "left-diag":
            start_x, start_y = self.table_space, self.table_space
            end_x, end_y = self.table_size - self.table_space, self.table_size - self.table_space

        # for the diagonal winning pattern from top-right to bottom-left
        elif line_type == "right-diag":
            start_x, start_y = self.table_size - self.table_space, self.table_space
            end_x, end_y = self.table_space, self.table_size - self.table_space

        # draws the line strike
        line_strike = pygame.draw.line(screen, self.line_color, [start_x, start_y], [end_x, end_y], 8)

    # random function for machine player
    def _random(self, bot):
        # Continue choosing random value as long as taking_move condition is True for the machine
        while self.taking_move:
            if self.player != bot:
                break

            # randomizing target cell to fill in
            x = random.randint(0, 2)
            y = random.randint(0, 2)

            if self.table[x][y] == "-":
                self.table[x][y] = self.player  # Change the value from "-" to the player mark
                self._draw_char(x, y, self.player)
                self._game_check()
                self._change_player()
                break

    def _draw_arr(self, arr_pos):
        arr_img = pygame.image.load("images_3t/arrow.png")
        arr_img = pygame.transform.scale(arr_img, (20, 20))
        screen.blit(arr_img, arr_pos)
        pygame.display.update()

    # First screen when the game is launched
    def _start_screen(self):
        screen.fill(self.background_color)

        # TITLE
        start_font = pygame.font.SysFont("Courier New", 40)
        title_text = start_font.render("Tic Tac Toe", True, (255, 255, 255))
        screen.blit(title_text, (window_size[0] // 2 - title_text.get_width() // 2, 100))

        # PYTHON IMAGE
        pyt_img = pygame.image.load("images_3t/python.png")
        pyt_img = pygame.transform.scale(pyt_img, (50, 30))
        screen.blit(pyt_img, (window_size[0] // 2 - title_text.get_width() // 2 - 25, 125))

        # TIC TAC TOE IMAGE
        tic_img = pygame.image.load("images_3t/tictactoe.png")
        tic_img = pygame.transform.scale(tic_img, (80, 80))
        screen.blit(tic_img, (window_size[0] // 2 - 40, 180))

        # GAME MODE OPTION
        options_font = pygame.font.SysFont("Courier New", 20)
        option1_text = options_font.render("1. Play against another player", True, (255, 255, 255))
        option2_text = options_font.render("2. Play against computer", True, (255, 255, 255))
        screen.blit(option1_text, (window_size[0] // 2 - option1_text.get_width() // 2, 325))
        screen.blit(option2_text, (window_size[0] // 2 - option2_text.get_width() // 2, 375))
        arr_pos = (window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323)

        pygame.display.flip()
        self._draw_arr(arr_pos)

        game_modes = ["2P", "1P"]
        selected_mode = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "2P"
                    elif event.key == pygame.K_2:
                        return "1P"
                    elif event.key == pygame.K_UP:
                        selected_mode = 0
                        pygame.draw.rect(screen, self.background_color, pygame.Rect((window_size[0] // 2 - option2_text.get_width() // 2 - 20, 373), (20,20)))
                        arr_pos = (window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323)
                        self._draw_arr(arr_pos)
                    elif event.key == pygame.K_DOWN:
                        selected_mode = 1
                        pygame.draw.rect(screen, self.background_color,
                        pygame.Rect((window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323),(20, 20)))
                        arr_pos = (window_size[0] // 2 - option2_text.get_width() // 2 - 20, 373)
                        self._draw_arr(arr_pos)
                    elif event.key == pygame.K_RETURN:
                        chosen_mode = game_modes[selected_mode]
                        return chosen_mode

    def _second_screen(self):
        screen.fill(self.background_color)
        # TITLE
        start_font = pygame.font.SysFont("Courier New", 40)
        title_text = start_font.render("Tic Tac Toe", True, (255, 255, 255))
        screen.blit(title_text, (window_size[0] // 2 - title_text.get_width() // 2, 100))

        # PYTHON IMAGE
        pyt_img = pygame.image.load("images_3t/python.png")
        pyt_img = pygame.transform.scale(pyt_img, (50, 30))
        screen.blit(pyt_img, (window_size[0] // 2 - title_text.get_width() // 2 - 25, 125))

        # TIC TAC TOE IMAGE
        tic_img = pygame.image.load("images_3t/tictactoe.png")
        tic_img = pygame.transform.scale(tic_img, (80, 80))
        screen.blit(tic_img, (window_size[0] // 2 - 40, 180))

        # GAME MODE OPTION
        options_font = pygame.font.SysFont("Courier New", 20)
        option1_text = options_font.render("1. Play first as X", True, (255, 255, 255))
        option2_text = options_font.render("2. Play second as O", True, (255, 255, 255))
        screen.blit(option1_text, (window_size[0] // 2 - option1_text.get_width() // 2, 325))
        screen.blit(option2_text, (window_size[0] // 2 - option2_text.get_width() // 2, 375))
        arr_pos = (window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323)

        pygame.display.flip()
        self._draw_arr(arr_pos)

        turn_modes = ["first", "second"]
        selected_turn = 0
        while self.running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    sys.exit()

                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        return "first"
                    elif event.key == pygame.K_2:
                        return "second"
                    elif event.key == pygame.K_UP:
                        selected_turn = 0
                        pygame.draw.rect(screen, self.background_color, pygame.Rect((window_size[0] // 2 - option2_text.get_width() // 2 - 20, 373), (20,20)))
                        arr_pos = (window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323)
                        self._draw_arr(arr_pos)
                    elif event.key == pygame.K_DOWN:
                        selected_turn = 1
                        pygame.draw.rect(screen, self.background_color,
                        pygame.Rect((window_size[0] // 2 - option1_text.get_width() // 2 - 20, 323),(20, 20)))
                        arr_pos = (window_size[0] // 2 - option2_text.get_width() // 2 - 20, 373)
                        self._draw_arr(arr_pos)
                    elif event.key == pygame.K_RETURN:
                        chosen_turn = turn_modes[selected_turn]
                        return chosen_turn

    def _play_2p(self):
        while self.running:
            self._message()
            for self.event in pygame.event.get():
                if self.event.type == pygame.QUIT:
                    sys.exit()

                # listen to mouse click event
                if self.event.type == pygame.MOUSEBUTTONDOWN:
                    if self.taking_move:
                        self._move(self.event.pos)

                # listen whether user click somewhere around the reset button or not
                if self.taking_move == False:
                    if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == pygame.BUTTON_LEFT:
                        mouse_x, mouse_y = self.event.pos[0], self.event.pos[1]
                        mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
                        # Check for mouse click inside _reset_button_rect
                        if mouse_rect.colliderect(self.reset_button_rect):
                            self._reset_game()

            # To update the content of the display
            pygame.display.flip()
            self.FPS.tick(60)

    def _play_1p(self, game_turn):
        while self.running:
            self._message()

            if game_turn == "first":
                bot = "O"
                for self.event in pygame.event.get():
                    if self.event.type == pygame.QUIT:
                        sys.exit()

                    # listen to mouse click event
                    if self.event.type == pygame.MOUSEBUTTONDOWN:
                        if self.taking_move:
                            self._move(self.event.pos)
                            self._random(bot)

                        # listen whether user click somewhere around the reset button or not
                        if self.taking_move == False:
                            if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == pygame.BUTTON_LEFT:
                                mouse_x, mouse_y = self.event.pos[0], self.event.pos[1]
                                mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
                                # Check for mouse click inside _reset_button_rect
                                if mouse_rect.colliderect(self.reset_button_rect):
                                    self._reset_game()

            elif game_turn == "second":
                bot = "X"
                self._random(bot)
                for self.event in pygame.event.get():
                    if self.event.type == pygame.QUIT:
                        sys.exit()

                    # listen to mouse click event
                    if self.event.type == pygame.MOUSEBUTTONDOWN:
                        if self.taking_move:
                            self._move(self.event.pos)
                            self._random(bot)

                    # listen whether user click somewhere around the reset button or not
                    if self.taking_move == False:
                        if self.event.type == pygame.MOUSEBUTTONDOWN and self.event.button == pygame.BUTTON_LEFT:
                            mouse_x, mouse_y = self.event.pos[0], self.event.pos[1]
                            mouse_rect = pygame.Rect(mouse_x, mouse_y, 1, 1)
                            # Check for mouse click inside _reset_button_rect
                            if mouse_rect.colliderect(self.reset_button_rect):
                                self._reset_game()

            # To update the content of the display
            pygame.display.flip()
            self.FPS.tick(60)

    # Resetting the game condition
    def _reset_game(self):
        self.table = []
        for col in range(3):
            self.table.append([])
            for row in range(3):
                self.table[col].append("-")

        self.player = "X"
        self.winner = None
        self.taking_move = True
        screen.fill(self.background_color)
        self._draw_table()
        self._message()

    # Create reset button
    def _draw_reset(self):
        self.reset_button_text = self.font.render("Reset", True, (255, 255, 255))
        self.reset_button_rect = self.reset_button_text.get_rect(center=(window_size[0] // 2, window_size[1] //2))
        pygame.draw.rect(screen, self.game_over_bg_color, self.reset_button_rect)
        screen.blit(self.reset_button_text, self.reset_button_rect)
        pygame.display.flip()

    # Updating the game display, process user input events, and regulate the frame rate
    def main(self):
        while self.taking_move == True:
            game_mode = self._start_screen()

            if game_mode == "2P":
                screen.fill(self.background_color)
                self._draw_table()
                self._play_2p()
            elif game_mode == "1P":
                game_turn = self._second_screen()
                screen.fill(self.background_color)
                self._draw_table()
                self._play_1p(game_turn)

if __name__ == "__main__":
    g = TicTacToe(window_size[0])
    g.main()
