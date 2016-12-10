class SimulationsSettings:
	def __init__(
		self,
		grid_size=10,
		vacancy_proportion=0.2,
		agent_proportions=(0.5, 0.5),
		initial_random_allocation=True,
		utility_function=None,
		satisficers=False,
		move_to_random=True,
		iterations=10000):

		self.grid_size = grid_size
		self.vacancy_proportion = vacancy_proportion
		self.agent_proportions = agent_proportions
		self.initial_random_allocation = initial_random_allocation
		self.utility_function = utility_function
		self.satisficers = satisficers
		self.move_to_random = move_to_random
		self.iterations = iterations

	def validate(self):
		if grid_size < 1:
			raise ValueError("Grid size must be > 1")

		if vacancy_proportion < 0.0 or vacancy_proportion > 1.0:
			raise ValueError("Vacancy proportion must be in [0, 1]")

		if sum(agent_proportions) != 1.0:
			raise ValueError("Agent proportions must sum up to 1")

		if initial_random_allocation != True or initial_random_allocation != False:
			raise ValueError("Initial random allocation must be true or false")

		if not callable(utility_function):
			raise ValueError("Utility function must be callable")

		if move_to_random != True or move_to_random != False:
			raise ValueError("Move to random must be true or false")

		if iterations < 1:
			raise ValueError("Iterations must be > 1")


	def get_agent_type_proportions(self):
		agent_proportion = 1.0 - vacancy_proportion
		agent_type_proporitons = [p * agent_proportion for p in agent_proportions]
		agent_type_proporitons = [vacancy_proportion] + agent_type_proporitons
		return tuple(agent_type_proporitons)

