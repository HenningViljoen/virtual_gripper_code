#StratLytic 2020

import random
import copy


from source.point import Point
import settings


class Agent(object):
    def __init__(self,
                 state_len_x: int = 0,
                 state_len_y: int = 0,
                 environment = None):
        self.state = Point()
        self.state_len_x = state_len_x
        self.state_len_y = state_len_y
        self.environment = environment
        self.reset_state_to_start()
        self.previous_state = copy.copy(self.state)
        self.q_function_table = list()
        self.init_q_function_table()
        self.model = dict()
        pass


    def reward_found(self):
        if (self.state.x == self.environment.goal_location.x) and (self.state.y == self.environment.goal_location.y):
            self.reset_state_to_start()
            self.environment.set_goal_content()
            return True
        else:
            return False


    def reset_state_to_start(self):
        self.state.setxy(self.environment.start_location.x, self.environment.start_location.y)


    def init_q_function_table(self):
        for action_i in range(settings.nr_actions):
            self.q_function_table.append(list())
            for row_y in range(self.state_len_y):
                list_of_zeros = [0.0] * self.state_len_x
                self.q_function_table[action_i].append(list_of_zeros)
        pass


    def epsilon_greedy(self):
        pass


    def choose_action(self,
                      state_to_evaluate=None,
                      previous_state_to_evaluate=None,
                      greedy: bool = False):
        current_state = copy.copy(state_to_evaluate)
        previous_state = copy.copy(previous_state_to_evaluate)
        states_to_consider = list()
        for action in settings.Actions:
            print(action)
            new_state, reward = self.environment.execute_action(
                current_state=current_state,
                action=action
            )
            if self.environment.grid[new_state.y][new_state.x] != 'x':
                print(new_state.x, new_state.y)
                states_to_consider.append((new_state, action, reward))
        print(states_to_consider)
        best_action_value = -10000000.0
        best_action = settings.Actions.Up
        best_reward = 0.0
        best_state = copy.copy(current_state)
        random.shuffle(states_to_consider)
        sample_randomly = False
        if (not greedy):
            sample_randomly = random.random() < settings.epsilon
        for state_actions in states_to_consider:
            state = state_actions[0]
            if not ((state.x == previous_state.x) and (state.y == previous_state.y) and (
                    len(states_to_consider) > 1)):
                action = state_actions[1]
                reward = state_actions[2]
                value = self.q_function_table[action.value][self.state.y][self.state.x]
                if (value > best_action_value) or sample_randomly:
                    best_action_value = value
                    best_action = action
                    best_state = state
                    best_reward = reward
                    if sample_randomly:
                        break

        return best_action, best_state, best_reward, best_action_value


    def update_q_function_table(self,
                                best_action=None,
                                previous_state=None,
                                best_reward=None,
                                best_action_value_next_state=None):

        self.q_function_table[best_action.value][previous_state.y][previous_state.x] = \
            self.q_function_table[best_action.value][previous_state.y][previous_state.x] + \
            settings.agent_alpha * (best_reward + settings.agent_gamma * best_action_value_next_state - \
            self.q_function_table[best_action.value][previous_state.y][previous_state.x])


    def take_action(self):

        best_action, best_state, best_reward, best_action_value = self.choose_action(
            state_to_evaluate=self.state,
            previous_state_to_evaluate=self.previous_state,
            greedy=False
        )
        self.environment.grid[self.state.y][self.state.x] = ' '
        self.previous_state = copy.copy(self.state)
        self.state = copy.copy(best_state)
        self.environment.grid[self.state.y][self.state.x] = '*'
        best_action_next_state, best_state_next_state, best_reward_next_state, best_action_value_next_state = self.choose_action(
            state_to_evaluate=self.state,
            previous_state_to_evaluate=self.previous_state,
            greedy=True
        )

        self.update_q_function_table(
            best_action=best_action,
            previous_state=self.previous_state,
            best_reward=best_reward,
            best_action_value_next_state=best_action_value_next_state
        )
        self.model[((self.previous_state.x, (self.previous_state.y)), best_action)] = (best_reward, (best_state.x, best_state.y))


    def explore_model_and_update_q_function(self):
        len_model = len(self.model)
        for explore_i in range(settings.iterations_for_model_exploring):
            state_action = random.choice(list(self.model.keys()))
            reward_next_state = self.model[state_action]
            current_state = Point(ax=state_action[0][0], ay=state_action[0][1])
            action = state_action[1]
            reward = reward_next_state[0]
            next_state = Point(ax=reward_next_state[1][0], ay=reward_next_state[1][1])
            best_action_next_state, best_state_next_state, best_reward_next_state, best_action_value_next_state = self.choose_action(
                state_to_evaluate=next_state,
                previous_state_to_evaluate=current_state,
                greedy=True
            )
            if best_action_value_next_state != 0.0:
                self.update_q_function_table(
                                    best_action=action,
                                    previous_state=current_state,
                                    best_reward=reward,
                                    best_action_value_next_state=best_action_value_next_state)
            pass


    def agent_action_step(self):
        self.take_action()
        self.explore_model_and_update_q_function()



    def draw(self, canvas):
        font_size = settings.agent_q_function_font_size

        for action_i in range(settings.nr_actions):
            for char_i_y in range(self.state_len_y):
                for char_i_x in range(self.state_len_x):
                    char_x = settings.agent_q_function_map_start_x[action_i] + char_i_x*settings.agent_q_function_distance_between_chars_env
                    char_y = settings.agent_q_function_map_start_y[action_i] + char_i_y*settings.agent_q_function_distance_between_chars_env
                    grid_string = str(round(self.q_function_table[action_i][char_i_y][char_i_x]*10,1))
                    grid_text = canvas.create_text(char_x, char_y)
                    canvas.itemconfig(grid_text, text=grid_string, fill='blue', font=('Helvetica', str(font_size)))







