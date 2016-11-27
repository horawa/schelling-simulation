import numpy as np

def get_agent_indices(array):
	agent_indices = np.argwhere(array != 0)
	return agent_indices

def get_vacancy_indices(array):
	vacancy_indices = np.argwhere(array == 0)
	return vacancy_indices