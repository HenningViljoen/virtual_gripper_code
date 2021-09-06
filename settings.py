#Stratlytic 2020

from enum import Enum


environment_text_file_path = '/Users/johanneshenningviljoen/Dropbox/Projects-DB/StratLytic/virtual_gripper/data_models/virtual_gripper_environment.txt'

class Actions(Enum):
    Up = 0
    Right = 1
    Down = 2
    Left = 3

nr_actions = len(Actions)

"""Simulation constants"""
total_episodes = 20

"""Environment constants"""
start_location_char = 'S'
goal_location_char = 'G'

environment_graphics_start_x = 100
environment_graphics_start_y = 10
distance_between_chars_env = 13

"""Agent drawing constants"""
agent_q_function_font_size = 8
agent_q_function_distance_between_chars_env = 14
agent_q_function_map_start_x = [100, 700, 100, 700]
agent_q_function_map_start_y = [280, 280, 550, 550]

"""Machine Learning constants for Gripper brain"""
agent_alpha = 0.9
agent_gamma = 0.9
iterations_for_model_exploring = 100
epsilon = 0.025

