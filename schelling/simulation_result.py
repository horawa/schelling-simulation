import json
import os
import numpy as np
import schelling.segregation_measures as sm

class SimulationResult:
	"""
	This class stores the values of segregation measures 
	calculated for each iteration of simulation
	"""
	_segregation_measures = {}

	def __init__(self, 
			segregation_measure_names=sm.segregation_measures.keys()):
		for segregation_measure_name in segregation_measure_names:
			self._segregation_measures[segregation_measure_name] = []


	def save_JSON(self, output_path):
		json_data = json.dumps(self._segregation_measures, 
			sort_keys=True, indent=4)
		file = open(output_path, 'w')
		file.write(json_data)
		file.close()


	def parse_JSON(self, input_path):
		file = open(input_path)
		data = file.read()
		file.close()
		json_data = json.loads(data)
		self._segregation_measures = json_data


	def save_measure(self, name, value):
		self._segregation_measures[name].append(value)


	def get_measures(self):
		return self._segregation_measures


	def plot_measures(self): # pragma: nocover
		import matplotlib.pyplot as plt

		measures = self._segregation_measures.items()
		plots = len(measures)

		f, axarr = plt.subplots(plots, sharex=True)
		
		for i, measure in enumerate(measures):
			measure_name = measure[0]
			measure_values = np.array(measure[1])
			x_axis_values = np.arange(0, len(measure_values))

			axarr[i].plot(x_axis_values, measure_values)
			axarr[i].set_title(measure_name)

		plt.xlabel('Iteration')
		plt.show()


	def __str__(self):
		output = ""
		for measure_name, measure_values in self._segregation_measures.items():
			if measure_values:
				seg_last_value = str(round(measure_values[-1], 4))
			else:
				seg_last_value = ""
			output += (measure_name + ": " + seg_last_value + os.linesep)

		return output
