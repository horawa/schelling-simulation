class SimulationSettings:
	def __init__(
		self,
		grid_size=10,
		vacancy_proportion=0.2,
		agent_proportions=(0.5, 0.5),
		initial_random_allocation=True,
		utility_function=None,
		satisficers=False,
		move_to_random=True,
		radius=1,
		iterations=10000):

		self.grid_size = grid_size
		self.vacancy_proportion = vacancy_proportion
		self.agent_proportions = agent_proportions
		self.initial_random_allocation = initial_random_allocation
		self.utility_function = utility_function
		self.satisficers = satisficers
		self.move_to_random = move_to_random
		self.radius = radius
		self.iterations = iterations

	def validate(self):
		if self.grid_size < 1:
			raise ValueError("Grid size must be > 1")

		if self.vacancy_proportion < 0.0 or self.vacancy_proportion > 1.0:
			raise ValueError("Vacancy proportion must be in [0, 1]")

		if sum(self.agent_proportions) != 1.0:
			raise ValueError("Agent proportions must sum up to 1")

		if self.initial_random_allocation != True and self.initial_random_allocation != False:
			print(type(self.initial_random_allocation))
			raise ValueError("Initial random allocation must be true or false")

		if not callable(self.utility_function):
			raise ValueError("Utility function must be callable")

		if self.move_to_random != True and self.move_to_random != False:
			raise ValueError("Move to random must be true or false")

		if self.radius < 1:
			raise ValueError("Radius must be > 1")

		if self.iterations < 1:
			raise ValueError("Iterations must be > 1")


	def get_agent_type_proportions(self):
		agent_proportion = 1.0 - self.vacancy_proportion
		agent_type_proporitons = [p * agent_proportion for p in self.agent_proportions]
		agent_type_proporitons = [self.vacancy_proportion] + agent_type_proporitons
		return tuple(agent_type_proporitons)

