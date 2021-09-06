#Stratlytic 2020

import time


from source.environment import Environment
from source.agent import Agent
import settings


class Simulation(object):
    def __init__(self):
        self.simulation_environment = Environment()
        self.simulation_environment.read_grid_from_text_file(settings.environment_text_file_path)
        self.simulation_agent = Agent(
            state_len_x=self.simulation_environment.grid_len_x,
            state_len_y=self.simulation_environment.grid_len_y,
            environment=self.simulation_environment
        )


    def draw_simulation(self, canvas):
        canvas.delete("all")
        self.simulation_environment.draw(canvas)
        self.simulation_agent.draw(canvas)


    def simulate_one_step(self, canvas):
        self.simulation_agent.agent_action_step()
        self.draw_simulation(canvas)


    def do_simulation(self, canvas):
        for sim_i in range(settings.total_episodes):
            loop = True
            while loop:
                canvas.update()
                canvas.after(5, self.simulate_one_step(canvas))
                if self.simulation_agent.reward_found():
                    self.draw_simulation(canvas)
                    canvas.update()
                    loop = False

