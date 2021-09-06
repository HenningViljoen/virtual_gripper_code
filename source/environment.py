#StratLytic 2020

import copy
import time


from source.location import Location
import settings
from source.point import Point


class Environment(object):

    def __init__(self):
        self.grid = list()
        self.start_location = Point()
        self.goal_location = Point()
        self.grid_len_x = 0
        self.grid_len_y = 0


    def read_grid_from_text_file(self, test_file_path: str = ''):
        with open(test_file_path) as f:
            lines = f.readlines()
        for line_i in range(len(lines)):
            self.grid.append([])
            for char_i in range(len(lines[line_i])):
                char = lines[line_i][char_i]
                if char != '\n':
                    #print(char)
                    self.grid[line_i].append(char)
                    if char == settings.start_location_char:
                        self.start_location.setxy(char_i, line_i)
                        print('Start location set', char_i, line_i)
                    elif char == settings.goal_location_char:
                        self.goal_location.setxy(char_i, line_i)
                        print('Goal location set')
        self.grid_len_x = len(self.grid[0])
        self.grid_len_y = len(self.grid)


    def set_goal_content(self):
        self.grid[self.goal_location.y][self.goal_location.x] = settings.goal_location_char


    def execute_action(self,
                       current_state: Point = None,
                       action: settings.Actions = settings.Actions.Up
                       ) -> Point:
        copy_state = copy.copy(current_state)
        reward = 0.0
        if action == settings.Actions.Up:
            copy_state.setxy(ax=copy_state.x,
                                ay=copy_state.y - 1)
        elif action == settings.Actions.Right:
            copy_state.setxy(ax=copy_state.x + 1,
                                ay=copy_state.y)
        elif action == settings.Actions.Left:
            copy_state.setxy(ax=copy_state.x - 1,
                                ay=copy_state.y)
        elif action == settings.Actions.Down:
            copy_state.setxy(ax=copy_state.x,
                                ay=copy_state.y + 1)
        if (copy_state.x == self.goal_location.x) and (copy_state.y == self.goal_location.y):
            reward = 1.0
        return copy_state, reward


    def test_action(self,
                    current_state: Point = None,
                    action: settings.Actions = settings.Actions.Up) -> bool:
        pass


    def draw(self, canvas):
        font_size = 12

        for char_i_y in range(self.grid_len_y):
            for char_i_x in range(self.grid_len_x):
                char_x = settings.environment_graphics_start_x + char_i_x*settings.distance_between_chars_env
                char_y = settings.environment_graphics_start_y + char_i_y*settings.distance_between_chars_env
                grid_string = self.grid[char_i_y][char_i_x]
                grid_text = canvas.create_text(char_x, char_y)
                canvas.itemconfig(grid_text, text=grid_string, fill='blue', font=('Helvetica', str(font_size)))

        #canvas.update_idletasks()
        #time.sleep(2.4)

