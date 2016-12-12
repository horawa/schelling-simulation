import unittest
from ..simulation_settings import SimulationSettings

class SettingsTestCase(unittest.TestCase):
	def test_validate(self):
		bad_settings = [
			("grid_size", 0),
			("grid_size", -10),
			("vacancy_proportion", -1),
			("vacancy_proportion", 10),
			("agent_proportions", (1.0, 0.5)),
			("agent_proportions", (-1.0, 0.5)),
			("initial_random_allocation", 'asdf'),
			("utility_function", None),
			("satisficers", 'asdf'),
			("pick_random", 'asdf'),
			("move_to_random", 'asdf'),
			("radius", 0),
			("radius", -100),
			("iterations", -1)
		]

		for bad_setting in bad_settings:
			setting_arg = {bad_setting[0]: bad_setting[1]}
			settings = SimulationSettings(**setting_arg)

			with self.subTest(s=setting_arg):
				with self.assertRaises(ValueError):
					settings.validate()