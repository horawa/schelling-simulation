from numpy import vectorize, dstack, unique, amax
from matplotlib.image import imsave
from skimage.transform import resize


def _get_color(color_index):
	"""Get color in W, R, G, B, C, M, Y, K for indices 0-7"""
	try:
		return _get_color.colors[color_index]
	except AttributeError:
		w = (255, 255, 255)
		r = (255, 0, 0)
		g = (0, 255, 0)
		b = (0, 0, 255)
		c = (0, 255, 255)
		m = (255, 0, 255)
		y = (255, 255, 0)
		k = (0, 0, 0)

		_get_color.colors = (w, r, g, b, c, m, y, k)
		return _get_color.colors[color_index]


def to_image(array, size=800):
	"""Convert array to rgb image.
	White represents vacancy
	RGBCMYK represent agents of up to 7 types.

	Args:
	    array (ndarray): 2d square array
	    size (int, optional): size in pixels of output image (default 800)
	
	Returns:
	    ndarray: array representing image
	"""
	if unique(array).size > 8:
		raise ValueError("Array contains more than 8 unique elements. Only 8 colors are currently supported")

	if amax(array) > 7:
		raise ValueError("Array contains value >7.")

	# get tuple of 3 arrays with each rgb component
	get_rgb_arrays = vectorize(_get_color)
	rgb_arrays = get_rgb_arrays(array)

	# zip the arrays along new third axis
	image_array = dstack(rgb_arrays).astype('uint8')

	image_array = resize(image_array, (size, size), order=0, preserve_range=True).astype('uint8')

	return image_array


def image_save(image_array, output):
	"""Save image to file
	
	Args:
	    image_array (ndarray): 3d array representing rgb image
	    output (file): file to save
	"""
	# TODO convert this to use either scipy or skimage, so matplotlib requirement can be removed.
	imsave(output, image_array)
