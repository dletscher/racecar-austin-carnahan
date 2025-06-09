import random

class Agent:
	def chooseAction(self, observations, possibleActions):

		speed = observations['velocity']
		left = observations['lidar'][0]
		left_front = observations['lidar'][1]
		ahead = observations['lidar'][2]
		right_front = observations['lidar'][3]
		right = observations['lidar'][4]
	

		# Implement your rule-based decision-making here
		if speed < 0.05:
			return ('straight', 'accelerate')
		if speed > 0.22:
			return ('straight', 'brake')

		if ahead < 1:
			if left_front > right_front:
				return ('left', 'brake')
			else:
				return ('right', 'brake')
		if ahead < 0.5:
			if left_front > right_front:
				return ('left', 'coast')
			else:
				return ('right', 'coast')
		else:
			if left < 1.2:
				return ('right', 'accelerate')
			elif right < 1.2:
				return ('left', 'accelerate')
			else:
				return ('straight', 'accelerate')