import unittest
from schelling.simulation_settings import SimulationSettings

class SettingsTestCase(unittest.TestCase):
	def test_validate(self):
		bad_settings = [
			{"grid_size": 0},
			{"grid_size": -10},
			{"vacancy_proportion": -1},
			{"vacancy_proportion": 10},
			{"agent_proportions": (1.0, 0.5)},
			{"agent_proportions": (-1.0, 0.5)},
			{"initial_random_allocation": 'asdf'},
			{"utility_function": None},
			{"satisficers": 'asdf'},
			{"agent_picking_regime": 'asdf'},
			{"agent_picking_regime": 10},
			{"vacancy_picking_regime": 'asdf'},
			{"vacancy_picking_regime": 10},
			{"vacancy_roulette_base_weight": 'asdf'},
			{"vacancy_roulette_base_weight": 10},
			{"agent_roulette_base_weight": 'asdf'},
			{"agent_roulette_base_weight": 10},
			{"radius": 0},
			{"radius": -100},
			{"count_vacancies": 'asdf'},
			{"iterations": -1},
			{
				"vacancy_picking_regime": 'roulette',
				"vacancy_roulette_base_weight": -10,
			},
			{
				"agent_picking_regime": 'roulette',
				"agent_roulette_base_weight": -10,

			}
		]

		for bad_setting in bad_settings:
			settings = SimulationSettings(**bad_setting)

			with self.subTest(s=bad_setting):
				with self.assertRaises(ValueError):
					settings.validate()
