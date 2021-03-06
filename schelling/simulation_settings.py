from schelling.agent_distributions import get_distribution_including_vacancies
import schelling.segregation_measures as sm

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
			agent_picking_regime='random',
			vacancy_picking_regime='random',
			agent_roulette_base_weight=None,
			vacancy_roulette_base_weight=None,
			radius=1,
			count_vacancies=False,
			segregation_measure_names=['entropy_average', 'clusters', 
				'ghetto_rate', 'mix_deviation_average'],
			iterations=10000,
			save_period=100):

		self.grid_size = grid_size
		self.vacancy_proportion = vacancy_proportion
		self.agent_proportions = agent_proportions
		self.initial_random_allocation = initial_random_allocation
		self.utility_function = utility_function
		self.satisficers = satisficers
		self.agent_picking_regime = agent_picking_regime
		self.vacancy_picking_regime = vacancy_picking_regime
		self.agent_roulette_base_weight = agent_roulette_base_weight
		self.vacancy_roulette_base_weight = vacancy_roulette_base_weight
		self.radius = radius
		self.count_vacancies = count_vacancies
		self.segregation_measure_names = segregation_measure_names
		self.iterations = iterations
		self.save_period = save_period

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

		try:
			for u in self.utility_function:
				if not callable(u):
					raise ValueError("Utility function must be callable or list of callables")
		except TypeError:
			if not callable(self.utility_function):
				raise ValueError("Utility function must be callable or list of callables")


		if is_not_bool(self.satisficers):
			raise ValueError("Satisficers must be true or false")

		if self.agent_picking_regime not in ['random', 'first', 'roulette']:
			raise ValueError("vacancy_picking_regime must be either "
				"'random', 'first' or 'roulette'.")

		if self.vacancy_picking_regime not in ['random', 'first', 'roulette']:
			raise ValueError("vacancy_picking_regime must be either "
				"'random', 'first' or 'roulette'.")

		if self.vacancy_picking_regime == 'roulette':
			if self.vacancy_roulette_base_weight < 0.0:
				raise ValueError("Roulette base weight must be > 0")
		elif self.vacancy_roulette_base_weight is not None:
			raise ValueError("Roulette base weight should be left None, "
				"if the picking regime is not set to 'roulette'.")

		if self.agent_picking_regime == 'roulette':
			if self.agent_roulette_base_weight < 0.0:
				raise ValueError("Roulette base weight must be > 0")
		elif self.agent_roulette_base_weight is not None:
			raise ValueError("Roulette base weight should be left None, "
				"if the picking regime is not set to 'roulette'.")

		if self.radius < 1:
			raise ValueError("Radius must be > 1")

		if is_not_bool(self.count_vacancies):
			raise ValueError("Count vacancies must be true or false")

		if any(measure not in sm.segregation_measures \
				for measure in self.segregation_measure_names):
			raise ValueError("Invalid segregation measure name")

		if self.iterations < 1:
			raise ValueError("Iterations must be > 1")

		if self.save_period < 1:
			raise ValueError("Iterations must be > 1")

	def get_agent_type_proportions(self):
		return get_distribution_including_vacancies(self.vacancy_proportion, 
			self.agent_proportions)

	def __str__(self):
		return str(self.__dict__)

