# -*- coding: utf-8 -*-
"""
Created on Sat Nov 04 17:08:12 2017

@author: tyler
"""
import pygame
from Agent import convert_to_position, Agent
from Board import GameBoard

import numpy as np
import copy


red = (255, 0, 0)
yellow = (255, 255, 0)
black = (0, 0, 0)
white = (255, 255, 255)
blue = (0, 0, 255)
green = (0, 255, 0)

class GUI:
    def __init__(self, width, height, rows, columns, game_board, player1, player2):
        self.game_running = True

        self.players = [player1, player2]
        self.current_player = self.players[0]
        self.game_board = game_board

        self.screen_width = width
        self.screen_height = height
        self.columns = columns
        self.rows = rows
        self.collision_columns = [None for i in range(self.columns)]

        self.grid_width = self.screen_width / 8.0
        self.grid_height = self.screen_width / 8.0
        self.grid_bar_width = 25
        self.grid_bar_length = self.grid_bar_width * 2.0 + self.grid_width * 3.0

        self.marker_width = 10
        self.o_radius = int(self.grid_width / 2.0)
        self.player_markers = [[], []]
        self.collision_squares = []

        self.screen = pygame.display.set_mode((self.screen_width, self.screen_height))
        self.center = (int(self.screen_width / 2.0), int(self.screen_height / 2.0))

        self.board_rect = None
        self.board_height = 0
        self.board_width = 0
        self.grid_bars = {}

        pygame.init()
        pygame.font.init()

        self.title_font = pygame.font.SysFont(None, 96)
        self.title_text = None
        self.set_title_text("Player 0 wins!!")
        self.clicked = False

    def create_board(self):
        self.grid_bars = self.create_grid()
        self.collision_squares = self.create_collision_squares()
        self.player_markers[0] = self.create_x_markers()

    def create_grid(self):
        lv = pygame.Rect((self.center[0] - (self.grid_width / 2.0) - self.grid_bar_width,
                          self.center[1] - 1.5*self.grid_height - self.grid_bar_width,
                          self.grid_bar_width,
                          self.grid_bar_length))
        rv = pygame.Rect((self.center[0] + (self.grid_width / 2.0),
                          self.center[1] - 1.5*self.grid_height - self.grid_bar_width,
                          self.grid_bar_width,
                          self.grid_bar_length))
        th = pygame.Rect((self.center[0] - 1.5*self.grid_height - self.grid_bar_width,
                          self.center[1] - (self.grid_width / 2.0) - self.grid_bar_width,
                          self.grid_bar_length,
                          self.grid_bar_width))
        bh = pygame.Rect((self.center[0] - 1.5*self.grid_height - self.grid_bar_width,
                          self.center[1] + (self.grid_width / 2.0),
                          self.grid_bar_length,
                          self.grid_bar_width))

        return {'lv': lv, 'rv': rv, 'th': th, 'bh': bh}

    def create_collision_squares(self):
        tl = pygame.Rect((self.grid_bars['lv'].topleft[0]-self.grid_width,
                          self.grid_bars['lv'].topleft[1],
                          self.grid_width,
                          self.grid_height))
        tm = pygame.Rect((self.grid_bars['lv'].topright[0],
                          self.grid_bars['lv'].topright[1],
                          self.grid_width,
                          self.grid_height))
        tr = pygame.Rect((self.grid_bars['rv'].topright[0],
                          self.grid_bars['rv'].topright[1],
                          self.grid_width,
                          self.grid_height))

        ml = pygame.Rect((self.grid_bars['th'].bottomleft[0],
                          self.grid_bars['th'].bottomleft[1],
                          self.grid_width,
                          self.grid_height))
        mm = pygame.Rect((self.grid_bars['lv'].topright[0],
                          self.grid_bars['th'].bottomleft[1],
                          self.grid_width,
                          self.grid_height))
        mr = pygame.Rect((self.grid_bars['rv'].topright[0],
                          self.grid_bars['th'].bottomright[1],
                          self.grid_width,
                          self.grid_height))

        bl = pygame.Rect((self.grid_bars['bh'].bottomleft[0],
                          self.grid_bars['bh'].bottomleft[1],
                          self.grid_width,
                          self.grid_height))
        bm = pygame.Rect((self.grid_bars['lv'].topright[0],
                          self.grid_bars['bh'].bottomleft[1],
                          self.grid_width,
                          self.grid_height))
        br = pygame.Rect((self.grid_bars['rv'].bottomright[0],
                          self.grid_bars['bh'].bottomleft[1],
                          self.grid_width,
                          self.grid_height))

        #return {'tl': tl, 'tm': tm, 'tr': tr, 'ml': ml, 'mm': mm, 'mr': mr, 'bl': bl, 'bm': bm, 'br': br}
        return tl, tm, tr, ml, mm, mr, bl, bm, br

    def create_o_markers(self):
        o = []
        for grid in range(len(self.collision_squares)):
            o.append((self.collision_squares[grid].center[0], self.collision_squares[grid].center[1]))

    def create_x_markers(self):
        x = []
        for grid in range(len(self.collision_squares)):
            # Top left '\' (top)
            tlt_b = (self.collision_squares[grid].topleft[0] + self.marker_width, self.collision_squares[grid].topleft[1])
            tlt_e = (self.collision_squares[grid].center[0], self.collision_squares[grid].center[1] - self.marker_width)

            # Top right '/' (top)
            trt_b = (self.collision_squares[grid].center[0], self.collision_squares[grid].center[1] - self.marker_width)
            trt_e = (self.collision_squares[grid].topright[0] - self.marker_width, self.collision_squares[grid].topright[1])

            # Top right cap
            trc_b = (self.collision_squares[grid].topright[0] - self.marker_width, self.collision_squares[grid].topright[1])
            trc_e = (self.collision_squares[grid].topright[0],self.collision_squares[grid].topright[1] + self.marker_width)

            # Top right '/' (bottom)
            trb_b = (self.collision_squares[grid].topright[0], self.collision_squares[grid].topright[1] + self.marker_width)
            trb_e = (self.collision_squares[grid].center[0] + self.marker_width, self.collision_squares[grid].center[1])

            # Bottom right '\' (top)
            brt_b = (self.collision_squares[grid].center[0] + self.marker_width, self.collision_squares[grid].center[1])
            brt_e = (self.collision_squares[grid].bottomright[0],self.collision_squares[grid].bottomright[1] - self.marker_width)

            # Bottom right cap
            brc_b = (self.collision_squares[grid].bottomright[0],self.collision_squares[grid].bottomright[1] - self.marker_width)
            brc_e = (self.collision_squares[grid].bottomright[0] - self.marker_width, self.collision_squares[grid].bottomright[1])

            # Bottom right '\' (bottom)
            brb_b = (self.collision_squares[grid].bottomright[0] - self.marker_width, self.collision_squares[grid].bottomright[1])
            brb_e = (self.collision_squares[grid].center[0], self.collision_squares[grid].center[1] + self.marker_width)

            # Bottom left '/' (bottom)
            blb_b = (self.collision_squares[grid].center[0], self.collision_squares[grid].center[1] + self.marker_width)
            blb_e = (self.collision_squares[grid].bottomleft[0] + self.marker_width, self.collision_squares[grid].bottomleft[1])

            # Bottom left cap
            blc_b = (self.collision_squares[grid].bottomleft[0] + self.marker_width, self.collision_squares[grid].bottomleft[1])
            blc_e = (self.collision_squares[grid].bottomleft[0], self.collision_squares[grid].bottomleft[1] - self.marker_width)

            # Bottom left '/' (top)
            blt_b = (self.collision_squares[grid].bottomleft[0], self.collision_squares[grid].bottomleft[1] - self.marker_width)
            blt_e = (self.collision_squares[grid].center[0] - self.marker_width, self.collision_squares[grid].center[1])

            # Top left '\' (bottom)
            tlb_b = (self.collision_squares[grid].center[0] - self.marker_width, self.collision_squares[grid].center[1])
            tlb_e = (self.collision_squares[grid].topleft[0], self.collision_squares[grid].topleft[1] + self.marker_width)

            # Top left cap
            tlc_b = (self.collision_squares[grid].topleft[0], self.collision_squares[grid].topleft[1] + self.marker_width)
            tlc_e = (self.collision_squares[grid].topleft[0] + self.marker_width, self.collision_squares[grid].topleft[1])
            x.append(
                (tlt_b, tlt_e,
                 trt_b, tlt_e,
                 trc_b, trc_e,
                 trb_b, trc_e,
                 brt_b, brt_e,
                 brc_b, brc_e,
                 brb_b, brb_e,
                 blb_b, blb_e,
                 blc_b, blc_e,
                 blt_b, blt_e,
                 tlb_b, tlb_e,
                 tlc_b, tlc_e)
            )
        return x

    def check_if_mouse_is_hovering(self):
        mouse = pygame.mouse.get_pos()
        for square in range(len(self.collision_squares)):
            if self.collision_squares[square].collidepoint(mouse):
                return square
        return None

    def play_piece(self):
        if self.current_player.is_human:
            if self.clicked:
                self.clicked = False
                active_square = self.check_if_mouse_is_hovering()
                if active_square is not None and self.game_board.check_if_valid(active_square):
                    pos = (convert_to_position(active_square, self.game_board.rows, self.game_board.cols)[0],
                           convert_to_position(active_square, self.game_board.rows, self.game_board.cols)[1])
                    self.game_board.board[pos] = self.current_player.number
                    self.game_board.played_pos.append(pos)
                    self.current_player = self.players[1] if self.players.index(self.current_player) == 0 \
                        else self.players[0]
        else:
            requested_pos = self.current_player.move(self.game_board)
            if requested_pos is None:
                return
            self.game_board.board[requested_pos[0], requested_pos[1]] = self.current_player.number
            self.current_player = self.players[1] if self.players.index(self.current_player) == 0 else self.players[0]

    def set_title_text(self, string, color=white, antialiasing=False):
        self.title_text = self.title_font.render(string, antialiasing, color)

    def update(self):
        self.screen.fill(black)

        for bar in self.grid_bars.values():
            pygame.draw.rect(self.screen, white, bar)

        for square in range(len(self.collision_squares)):
            pos = (convert_to_position(square, self.game_board.rows, self.game_board.cols)[0],
                   convert_to_position(square, self.game_board.rows, self.game_board.cols)[1])

            if self.game_board.board[pos] == 1:
                pygame.draw.polygon(self.screen, white, self.player_markers[0][square])
            if self.game_board.board[pos] == 2:
                pygame.draw.circle(self.screen, white, self.collision_squares[square].center, self.o_radius,
                                   self.marker_width)

        active_square = self.check_if_mouse_is_hovering()
        if active_square is not None and self.game_board.check_if_valid(active_square):
            if self.current_player.number == 1:
                pygame.draw.polygon(self.screen, white, self.player_markers[self.current_player.number-1][active_square])
            elif self.current_player.number == 2:
                pygame.draw.circle(self.screen, white, self.collision_squares[active_square].center, self.o_radius,
                                   self.marker_width)

        self.screen.blit(self.title_text,
                         (self.screen.get_rect().center[0] - self.title_text.get_width() // 2,
                          10))
        player_won = self.game_board.check_for_win()


        pygame.display.flip()
        #return False



if __name__ == '__main__':
    board = GameBoard()
    player1 = Agent(1, True)
    player2 = Agent(2, False)
    game_gui = GUI(1280, 900, 6, 7, board, player1, player2)
    game_gui.create_board()
    while game_gui.game_running:
        game_gui.set_title_text("Player %d\'s turn" % game_gui.current_player.number)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # this enables clicking the X in the program bar to kill program.
                game_gui.game_running = False
                break
            if event.type == pygame.MOUSEBUTTONDOWN and game_gui.current_player.is_human:
                game_gui.clicked = True

        game_gui.play_piece()
        player_won = game_gui.game_board.check_for_win()
        if player_won > 0:
            game_gui.set_title_text("Player %d wins!!" % player_won)
            #break
        elif player_won < 0:
            game_gui.set_title_text("Tie game!!")
        game_gui.update()

    pygame.quit()
