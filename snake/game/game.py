# game.py controls as the actual snake game. It does not include, for example, the main menu.

import tkinter as tk
from snake.game import snake_handler, apple, tile_manager, coord_converter
from snake import assets
import random

class Game(tk.Frame):
    def __init__(self, master):
        super().__init__(master)
        self.master = master
        self.bind("<Key>", self.key_handler)
        self.started = False
        self.converter = coord_converter.Coord_Converter()

        # Create Canvas
        canvas_width = assets.rect_length * tile_manager.rows
        canvas_height = assets.rect_length * tile_manager.columns
        # +1 so tile borders aren't cut off.
        self.canvas = tk.Canvas(self, width=canvas_width, height=canvas_height)
        self.canvas.pack()

        # Create Objects
        self.tile_manager = tile_manager.Tile_Manager(self.canvas)
        self.tile_manager.draw_grid()
        self.snake = snake_handler.Snake(self.canvas, tile_manager.rows, tile_manager.columns)


        # WASD TO START label
        self.wasd_to_start_label = self.canvas.create_image(
            (canvas_width/2, assets.wasd_to_start_label_height/2 + 10), 
            image=assets.wasd_to_start_label)

    # Input Handler
    def key_handler(self, event):
        if not self.started:
            if event.char == 'w' and self.snake.direction != 's':
                self.snake.new_direction = 'n'
            elif event.char == 'a' and self.snake.direction != 'e':
                self.snake.new_direction = 'w'
            elif event.char == 's' and self.snake.direction != 'n':
                self.snake.new_direction = 's'
            elif event.char == 'd' and self.snake.direction != 'w':
                self.snake.new_direction = 'e'

            self.started = True
            self.canvas.delete(self.wasd_to_start_label)
            self.create_new_apple()
            self.update_snake()
            
        elif self.started:
            if event.char == 'w' and self.snake.direction != 's':
                self.snake.new_direction = 'n'
            elif event.char == 'a' and self.snake.direction != 'e':
                self.snake.new_direction = 'w'
            elif event.char == 's' and self.snake.direction != 'n':
                self.snake.new_direction = 's'
            elif event.char == 'd' and self.snake.direction != 'w':
                self.snake.new_direction = 'e'

    def update_snake(self):
        self.snake.update_position()

        if self.snake_is_dead():   # if dead
            self.snake_death_handler()
            return
        else:
            self.snake.draw_snake()

        snake_x = self.snake.snake_pos[0]
        snake_y = self.snake.snake_pos[1]
        tile = self.tile_manager.tile_array[snake_x][snake_y]
        apple_index = tile.is_holding(apple.Apple)
        if apple_index != None:
            tile.drop(apple_index)
            self.create_new_apple()
            self.snake.create_new_body()

        # Loop
        self.after(120, self.update_snake)
    
    def create_new_apple(self):
        x = random.randint(0, tile_manager.columns - 1)
        y = random.randint(0, tile_manager.rows - 1)
        new_apple = apple.Apple(self.canvas)
        self.tile_manager.tile_array[x][y].holding.append(new_apple)
        self.tile_manager.tile_array[x][y].render()

    def snake_is_dead(self):

        raw_snake_pos = self.converter.to_raw(self.snake.snake_pos)

        # Check if snake hit itself
        for snake_part in self.snake.body:
            if tuple(self.canvas.coords(snake_part)) == raw_snake_pos:
                return True

        # Check if snake hit barrier
        snake_pos = self.snake.snake_pos
        if self.tile_manager.tile_array[snake_pos[0]][snake_pos[1]].type == "barrier":
            return True

        return False

    def snake_death_handler(self):
        pass