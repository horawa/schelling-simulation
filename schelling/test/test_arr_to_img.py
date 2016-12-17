import unittest
from numpy import array, array_equal
from schelling.arr_to_img import to_image

class ArrToImgTest(unittest.TestCase):

	def test_expected_output(self):
		c0 = [255, 255, 255]
		c1 = [255, 0, 0]
		c6 = [255, 255, 0]


		c = [
			[255, 255, 255],
			[255, 0, 0],
			[0, 255, 0],
			[0, 0, 255],
			[0, 255, 255],
			[255, 0, 255],
			[255, 255, 0],
			[0, 0, 0],
		]
		parameters = [
			(array([[0, 1], [0, 1]]), array([[c[0], c[1]], [c[0], c[1]]])),
			(array([[0, 1, 6], [0, 1, 6], [0, 1, 6]]), array([[c[0], c[1], 
				c[6]], [c[0], c[1], c[6]], [c[0], c[1], c[6]]])),
			(
				array(list(range(8))*8).reshape(8,8),
				array([c[x] for x in range(8)] * 8).reshape(8,8,3),
			)
		]

		for arr_in, expected_arr_out in parameters:
			with self.subTest(arr_in=arr_in):
				arr_out = to_image(arr_in, size=arr_in.shape[0])
				self.assertTrue(array_equal(arr_out, expected_arr_out))


	def test_eight_colors_supported_error(self):
		arr = array(list(range(10))*10).reshape((10, 10))
		with self.assertRaises(ValueError):
			to_image(arr)


	def test_value_over_seven_error(self):
		arr = array([[0, 10], [0, 10]])
		with self.assertRaises(ValueError):
			to_image(arr)

if __name__ == '__main__':
	unittest.main()
