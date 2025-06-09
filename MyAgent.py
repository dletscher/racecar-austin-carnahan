import random

class Agent:
	def chooseAction(self, observations, possibleActions):

		speed = observations['velocity']
		left = observations['lidar'][0]
		left_front = observations['lidar'][1]
		ahead = observations['lidar'][2]
		right_front = observations['lidar'][3]
		right = observations['lidar'][4]

		on_straightaway = ahead > 1.8 and left_front > 1.5 and right_front > 1.5
	
		max_speed = 0.35 if on_straightaway else 0.22

		# Speed constraints, max/min
		if speed < 0.05:
			return ('straight', 'accelerate')
		if speed > max_speed:
			return ('straight', 'brake')
		
		# Detect turns and brake or coast
		if ahead < 1.5 and speed > 0.23:
			if left_front > right_front:
				return ('left', 'brake')
			else:
				return ('right', 'brake')
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
			
		# Keep away from the walls
		else:
			if left < 1.2:
				return ('right', 'accelerate')
			elif right < 1.2:
				return ('left', 'accelerate')
			else:
				return ('straight', 'accelerate')