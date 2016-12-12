from .agent_distributions import get_distribution_including_vacancies

class SimulationSettings:
	"""
	This class stores settings for simulation.
	Pass to the run_simulation function.
	"""
	def __init__(
			self,
			grid_size=10,
			vacancy_proportion=0.2,
			agent_proportions=(0.5, 0.5),
			initial_random_allocation=True,
			utility_function=(lambda f: 0.0),
			satisficers=False,
			pick_random=True,
			move_to_random=True,
			radius=1,
			iterations=10000):

		self.grid_size = grid_size
		self.vacancy_proportion = vacancy_proportion
		self.agent_proportions = agent_proportions
		self.initial_random_allocation = initial_random_allocation
		self.utility_function = utility_function
		self.satisficers = satisficers
		self.pick_random = pick_random
		self.move_to_random = move_to_random
		self.radius = radius
		self.iterations = iterations

	def validate(self):
		def is_not_bool(val):
			return val != True and val != False

		if self.grid_size < 1:
			raise ValueError("Grid size must be > 1")

		if self.vacancy_proportion < 0.0 or self.vacancy_proportion > 1.0:
			raise ValueError("Vacancy proportion must be in [0, 1]")

		if sum(self.agent_proportions) != 1.0:
			raise ValueError("Agent proportions must sum up to 1")

		if is_not_bool(self.initial_random_allocation):
			raise ValueError("Initial random allocation must be true or false")

		if not callable(self.utility_function):
			raise ValueError("Utility function must be callable")

		if is_not_bool(self.satisficers):
			raise ValueError("Satisficers must be true or false")

		if is_not_bool(self.pick_random):
			raise ValueError("Pick random must be true or false")

		if is_not_bool(self.move_to_random):
			raise ValueError("Move to random must be true or false")

		if self.radius < 1:
			raise ValueError("Radius must be > 1")

		if self.iterations < 1:
			raise ValueError("Iterations must be > 1")

	def get_agent_type_proportions(self):
		return get_distribution_including_vacancies(self.vacancy_proportion, 
			self.agent_proportions)

