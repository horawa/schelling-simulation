import json
import os
import matplotlib.pyplot as plt
import numpy as np

class SimulationResult:
	"""
	This class stores the values of segregation measures 
	calculated for each iteration of simulation
	"""
	def __init__(self):
		self.switch_rate_average = []
		self.entropy_average = []
		self.ghetto_rate = []
		self.clusters = []
		self.distance_average = []
		self.mix_deviation_average = []


	def save_JSON(self, output_path):
		json_data = json.dumps(self.__dict__, sort_keys=True, indent=4)
		file = open(output_path, 'w')
		file.write(json_data)
		file.close()


	def parse_JSON(self, input_path):
		file = open(input_path)
		data = file.read()
		file.close()
		json_data = json.loads(data)
		self.__dict__ = json_data


	def plot_measures(self): # pragma: nocover
		measures = self.__dict__.items()
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
		for measure_name, measure_values in self.__dict__.items():
			if measure_values:
				seg_final_value = str(round(measure_values[-1], 4))
			else:
				seg_final_value = ""
			output += (measure_name + ": " + seg_final_value + os.linesep)

		return output
