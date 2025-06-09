import random

class Agent:
	def chooseAction(self, observations, possibleActions):

		speed = observations['velocity']
		left = observations['lidar'][0]
		left_front = observations['lidar'][1]
		ahead = observations['lidar'][2]
		right_front = observations['lidar'][3]
		right = observations['lidar'][4]
	
		on_straightaway = ahead > 3 and left_front > 1.8 and right_front > 1.8

		# if on_straightaway:
		# 	print("On straightaway")

		max_speed = 0.38 if on_straightaway else 0.26

		# Implement your rule-based decision-making here
		if speed < 0.1:
			return ('straight', 'accelerate')
		if speed > max_speed:
			return ('straight', 'brake')

		if ahead < 1.5:
			if left_front > right_front:
				return ('left', 'brake')
			else:
				return ('right', 'brake')
		if ahead > 1.5 and ahead < 3.0:
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