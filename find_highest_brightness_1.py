'''	input: image 36x36 matrix, patch size 
	output: highest average illuminance location starting x and starting y 
   	Author: Jane Sun
   	12/26/2014
'''
from scipy import misc 
import random 
import IPython
# from scipy import plt

class FindBrightness():
	def __init__(self):
		self.A = 3
		self.n = self.A*self.A
		# self.image = misc.imread("piepie.JPG")

		self.image = misc.imread("jane.jpg")
		self.h = len(self.image)
		self.w = len(self.image[0])
		self.image_lum = [[-1] * self.w for i in xrange(self.h)]

	def compute_luminance(self, pixel):
		return 0.212*pixel[0] + 0.7152*pixel[1] + 0.0722*pixel[2]

	def get_ave_luminance_in_the_region(self, start_x, start_y):
		cur_ave = 0
		for x in xrange (start_x, start_x + self.A):
	
			for y in xrange(start_y, start_y + self.A):
				#  dynamic programming: save the luminance value for each pixel 
				if self.image_lum[x][y] == -1:
					
					# get the luminance of the pixel 
					self.image_lum[x][y] = self.compute_luminance(self.image[x][y])

				cur_ave += self.image_lum[x][y]/self.n
	
		return cur_ave


	def main(self):
		curr_start_x, curr_start_y = (0, 0)
		
		# get local optimas: DFS for all directions that has average illumination greater than the current patch, stop when patch doesn't move 
		# initialize current patch only once 
		curr_patch = self.get_ave_luminance_in_the_region(curr_start_x, curr_start_y)
		max_patch =  0
		glb_max_patch = 0
		max_dir = (0, 0)
		q = []
		q_value = [0]
		glb_start_x, glb_start_y = (0,0)

		# 1. coarse search with super pixel, save the brightness for each pixel 
		for curr_start_x, curr_start_y in zip(xrange(0, self.h-self.A, self.A), xrange(0, self.w-self.A, self.A)):
			
			curr_patch = self.get_ave_luminance_in_the_region(curr_start_x, curr_start_y)

			if q_value[-1] < curr_patch:
			
				# put the bigger one in a queue TODO: depends on the starting illuminance 
				q.append((curr_start_x, curr_start_y))
				q_value.append(curr_patch)
		print q
		print q_value

		# 2. fine search: starting at the bightest super pixel location 
		for p_value, p in zip(q_value, q):

			max_patch = p_value 
			
			curr_start_x, curr_start_y = p

			while True:
				
				curr_patch = max_patch
				
				curr_start_x, curr_start_y = curr_start_x + max_dir[0], curr_start_y + max_dir[1]

				# search in 8 directions 
				for d in [(-1, -1), (-1, 0), (-1, 1), 
						   (0, -1),          (0,  1),
						   (1, -1), (1,  0), (1,  1)]: 
					
					if 0 <= curr_start_x + d[0] < self.w and 0 <= curr_start_y + d[1] < self.h:
				
						print "hey", curr_start_x + d[0], curr_start_y + d[1]
						
						dir_patch = self.get_ave_luminance_in_the_region(curr_start_x + d[0], curr_start_y + d[1])
				
						if dir_patch > max_patch:
							
							max_patch = dir_patch
							
							max_dir = d
					
				if max_patch == curr_patch:
					print "break"
					break

			if glb_max_patch < max_patch: 

				glb_max_patch = max_patch
				
				glb_start_x, glb_start_y = curr_start_x, curr_start_y

			print "result", glb_max_patch, glb_start_x, glb_start_y
		IPython.embed()

image_brightness = FindBrightness()
image_brightness.main()

