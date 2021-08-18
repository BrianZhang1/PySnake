# snake_control.py creates and controls the snake (head and body)
# It manages movement, growth, and rendering of snake.
# It does not manage collisions of the snake with other objects, those are managed in game.py

from snake.game import coord_converter
from snake import assets

class Snake():
    def __init__(self, canvas, grid_rows, grid_columns):
        self.canvas = canvas
        self.grid_rows = grid_rows
        self.grid_columns = grid_columns
        self.converter = coord_converter.Coord_Converter()
        self.snake_pos = (10, 10)         # (x, y)

        inital_coords = self.converter.to_raw(self.snake_pos)

        self.direction = 's'      # north, east, south, west
        self.new_direction = 's'

        initial_image = assets.snake_head_down
        if self.direction == 'w':
            initial_image = assets.snake_head_left
        elif self.direction == 'n':
            initial_image = assets.snake_head_up
        elif self.direction == 'e':
            initial_image = assets.snake_head_right

        self.snake_head = self.canvas.create_image(inital_coords, image=initial_image)
        self.previous_moves = []
        self.body = []

    def update_position(self):
        self.previous_moves.insert(0, self.snake_pos)
        if len(self.previous_moves) - len(self.body) > 1:
            self.previous_moves.pop()

        # Move one tile in the direction the snake faces
        if self.new_direction == 'w':
            self.direction = 'w'
            new_x = self.snake_pos[0] - 1
            new_y = self.snake_pos[1]
            self.canvas.itemconfig(self.snake_head, image=assets.snake_head_left)
        elif self.new_direction == 'e':
            self.direction = 'e'
            new_x = self.snake_pos[0] + 1
            new_y = self.snake_pos[1]
            self.canvas.itemconfig(self.snake_head, image=assets.snake_head_right)
        elif self.new_direction == 's':
            self.direction = 's'
            new_x = self.snake_pos[0]
            new_y = self.snake_pos[1] + 1
            self.canvas.itemconfig(self.snake_head, image=assets.snake_head_down)
        elif self.new_direction == 'n':
            self.direction = 'n'
            new_x = self.snake_pos[0]
            new_y = self.snake_pos[1] - 1
            self.canvas.itemconfig(self.snake_head, image=assets.snake_head_up)
        self.snake_pos = (new_x, new_y)

        self.check_bounds()


    # Check bounds. If out of bounds, teleport to opposite side.
    def check_bounds(self):
        if self.snake_pos[0] < 0:
            new_x = self.grid_columns - 1
            new_y = self.snake_pos[1]
        elif self.snake_pos[0] > self.grid_columns - 1:
            new_x = 0
            new_y = self.snake_pos[1]
        elif self.snake_pos[1] < 0:
            new_x = self.snake_pos[0]
            new_y = self.grid_rows - 1
        elif self.snake_pos[1] > self.grid_rows - 1:
            new_x = self.snake_pos[0]
            new_y = 0
        else:
            return

        self.snake_pos = (new_x, new_y)
    
    # Doesn't actually redraw, it just changes coords.
    def draw_snake(self):
        # Draw snake head
        self.canvas.coords(self.snake_head, self.converter.to_raw(self.snake_pos))

        # Move last snake body part to front of snake body.
        if len(self.body) > 0:
            raw_coords = self.converter.to_raw(self.previous_moves[0])

            self.canvas.coords(self.body[-1], raw_coords)
            self.body.insert(0, self.body[-1])
            self.body.pop()

    def create_new_body(self):
        coords = self.previous_moves[len(self.body)]
        raw_coords = self.converter.to_raw(coords)
        self.body.append(self.canvas.create_image(raw_coords, image=assets.snake_body_sprite))
    