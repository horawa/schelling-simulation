import appJar
import numpy as np
import os
import threading

import schelling.simulation
import schelling.arr_to_img as im
from schelling.simulation_settings import SimulationSettings
from schelling.utility_functions import create_flat_utility

image_path = "/Users/Stas/simulation"
app = appJar.gui()
running = False



blank_image_data = \
"R0lGODdh9AH0AfAAAP///wAAACwAAAAA9AH0AQAC/oSPqcvtD6OctNqLs968+w+G4kiW5omm6sq27gvH8kzX9o3n+s73/g8MCofEovGITCqXzKbzCY1Kp9Sq9YrNarfcrvcLDovH5LL5jE6r1+y2+w2Py+f0uv2Oz+v3/L7/DxgoOEhYaHiImKi4yNjo+AgZKTlJWWl5iZmpucnZ6fkJGio6SlpqeoqaqrrK2ur6ChsrO0tba3uLm6u7y9vr+wscLDxMXGx8jJysvMzc7PwMHS09TV1tfY2drb3N3e39DR4uPk5ebn6Onq6+zt7u/g4fLz9PX29/j5+vv8/f7/8PMKDAgQQLGjyIMKHChQwbOnwIMaLEiRQrWryIMaPG/o0cO3r8CDKkyJEkS5o8iTKlypUsW7p8CTOmzJk0a9q8iTOnzp08e/r8CTSo0KFEixo9ijSp0qVMmzp9CjWq1KlUq1q9ijWr1q1cu3r9Cjas2LFky5o9izat2rVs27p9Czeu3Ll069q9izev3r18+/r9Cziw4MGECxs+jDix4sWMGzt+DDmy5MmUK1u+jDmz5s2cO3v+DDq06NGkS5s+jTq16tWsW7t+DTu27Nm0a9u+jTu37t28e/v+DTy48OHEixs/jjy58uXMmzt/Dj269OnUq1u/jj279u3cu3v/Dj68+PHky5s/jz69+vXs27t/Dz++/Pn069u/jz+//v38/vv7/w9ggAIOSGCBBh6IYIIKLshggw4+CGGEEk5IYYUWXohhhhpuyGGHHn4IYogijkhiiSaeiGKKKq7IYosuvghjjDLOSGONNt6IY4467shjjz7+CGSQQg5JZJFGHolkkkouyWSTTj4JZZRSTklllVZeiWWWWm7JZZdefglmmGKOSWaZZp6JZppqrslmm26+CWeccs5JZ5123olnnnruyWeffv4JaKCCDkpooYYeimiiii7KaKOOPgpppJJOSmmlll6Kaaaabsppp55+Cmqooo5Kaqmmnopqqqquymqrrr4Ka6yyzkprrbbeimuuuu7Ka6++/gpssMIOS2yxxsZWAQAAOw=="


def press(btn):
	global running

	if btn == "Go":
		if not running:
			print("started")
			sim_thread = threading.Thread(target=start_simulation)
			sim_thread.start()
			running=True

	elif btn == "Stop" and running:
		stop_simulation()


def scale_changed(scale):
	if scale != "pos":
		return

	pos = app.getScale(scale)
	images = get_images()
	image = images[pos]
	app.setImage("simulation", image)


def start_simulation():
	settings = SimulationSettings(
		grid_size=int(app.getSpinBox("Grid size")),
		vacancy_proportion=float(app.getSpinBox("Vacancy proportion")),
		agent_proportions=(0.5, 0.5),
		utility_function=create_flat_utility(
			float(app.getSpinBox("Agent tolerance"))),
		count_vacancies=True,
		iterations=int(app.getSpinBox("Iterations")),
		save_period=1
	)
	schelling.simulation.run_simulation(settings, gui_callback)
	print("done")
	global running

	running = False



def stop_simulation():
	schelling.simulation.stop()

	global running
	running = False



def gui_callback(array, result, iteration):
	size = 600
	image = im.to_image(array, size=size)
	name = str(iteration).zfill(8) + ".png"
	im.image_save(image, os.path.join(image_path, name))
	app.setImage("simulation", name)
	app.setScaleRange("pos", 0, iteration)
	app.setScale("pos", iteration, callFunction=False)
	print(iteration)



def create_gui():

	app.setFont(20)

	app.addLabel("title", "Schelling simulation", 0, 0, 2)

	app.addLabelSpinBoxRange("Grid size", 1, 300, 1, 0, 2)
	app.setSpinBoxPos("Grid size", 29, callFunction=True)

	app.addLabelSpinBox("Agent tolerance", 
		list(reversed(np.arange(0, 1, 0.125))), 2, 0, 2)
	app.setSpinBox("Agent tolerance", 0.375, callFunction=True)

	app.addLabelSpinBox("Vacancy proportion", 
		list(reversed(np.arange(0, 1, 0.01))), 3, 0, 2)
	app.setSpinBox("Vacancy proportion", 0.2, callFunction=True)

	app.addLabelSpinBoxRange("Iterations", 1, 1000000, 4, 0, 2)
	app.setSpinBoxPos("Iterations", 9999)

	app.addButton("Stop", press, 5, 0, 1)
	app.addButton("Go", press, 5, 1, 1)

	#os.mkdir(image_path)
	app.setImageLocation(image_path)
	app.addImageData("simulation", blank_image_data, 6, 0, 1)
	#app.setImageSize("simulation", 600, 600)


	app.addScale("pos", 7, 0, 2)
	app.setScaleRange("pos", 0, 0)
	app.showScaleValue("pos")
	app.setScaleFunction("pos", scale_changed)

	app.addEmptyLabel("Segregation", 8, 0, 2)


	app.go()


def get_images():
	return list(filter(
		lambda str: str.endswith(".png"), os.listdir(image_path)))


# def update_images(image_path):
# 	images = get_images(image_path)
# 	app.setScaleRange

if __name__ == '__main__':
	create_gui()
