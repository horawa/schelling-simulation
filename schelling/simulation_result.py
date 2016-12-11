import json
import os

class SimulationResult:
	"""
	This class stores the values of segregation measures 
	calculated for each iteration of simulation
	"""
	def __init__(self):
		self.switch_rate_average = []
		self.entropy_average = []

	def save_JSON(self, output_path):
		json_data = json.dumps(self.__dict__, sort_keys=True, indent=4)
		file = open(output_path, 'w')
		file.write(json_data)
		file.close()

	def __str__(self):
		output = ""
		for seg_name, seg_values in self.__dict__.items():
			output += seg_name + ": " + str(round(seg_values[-1], 4)) + os.linesep

		return output

