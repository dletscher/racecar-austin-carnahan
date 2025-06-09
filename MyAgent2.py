import pickle
import random
from Racecar import Racecar
from Track import buildTrack

class Agent:
    def __init__(self):
        self._values = {}
        self._Qvalues = {}
        
        # Learning parameters
        self._learningRate = 0.1
        self._discountFactor = 0.9
        self._explorationRate = 0.2
        
    def getBin(self, observations):
        if observations == 'terminal':
            return 'terminal'
        
        # Discretize the observations
        speed = observations['velocity']
        left = observations['lidar'][0]
        left_front = observations['lidar'][1]
        ahead = observations['lidar'][2]
        right_front = observations['lidar'][3]
        right = observations['lidar'][4]
        
        # Simple discretization
        speed_bin = min(int(speed * 10), 9)
        left_bin = min(int(left * 2), 4)
        left_front_bin = min(int(left_front * 2), 4)
        ahead_bin = min(int(ahead * 2), 4)
        right_front_bin = min(int(right_front * 2), 4)
        right_bin = min(int(right * 2), 4)
        
        return (speed_bin, left_bin, left_front_bin, ahead_bin, right_front_bin, right_bin)
    
    def getValue(self, state):
        bin_state = self.getBin(state)
        if bin_state not in self._values:
            self._values[bin_state] = 0
        return self._values[bin_state]
    
    def getQValue(self, state, action):
        bin_state = self.getBin(state)
        if (bin_state, action) not in self._Qvalues:
            self._Qvalues[(bin_state, action)] = 0
        return self._Qvalues[(bin_state, action)]
    
    def load(self, filename):
        try:
            print('Loading data from', filename)
            with open(filename, 'rb') as dataFile:
                self._values = pickle.load(dataFile)
                self._Qvalues = pickle.load(dataFile)
        except:
            print('Could not load data, starting with empty values')
        
    def save(self, filename):
        print('Saving data to', filename)
        with open(filename, 'wb') as dataFile:
            pickle.dump(self._values, dataFile)
            pickle.dump(self._Qvalues, dataFile)
        
    def chooseAction(self, observations, possibleActions):
        # During training: use exploration
        if hasattr(self, '_training') and self._training:
            if random.random() < self._explorationRate:
                return random.choice(possibleActions)
        
        # Use learned policy
        bin_state = self.getBin(observations)
        
        highestValue = float('-inf')
        bestAction = possibleActions[0]  # Default
        
        for action in possibleActions:
            if (bin_state, action) not in self._Qvalues:
                self._Qvalues[(bin_state, action)] = 0
                
            q_value = self._Qvalues[(bin_state, action)]
            if q_value > highestValue:
                highestValue = q_value
                bestAction = action
                
        return bestAction
        
    def updateValues(self, observation1, action, observation2, reward):
        bin_state1 = self.getBin(observation1)
        
        # Create entry if it doesn't exist
        if (bin_state1, action) not in self._Qvalues:
            self._Qvalues[(bin_state1, action)] = 0
        
        # Q-learning update
        if observation2 == 'terminal':
            future_value = 0
        else:
            bin_state2 = self.getBin(observation2)
            
            # Find max Q-value for next state
            max_q = float('-inf')
            for act in self._possibleActions:
                if (bin_state2, act) not in self._Qvalues:
                    self._Qvalues[(bin_state2, act)] = 0
                max_q = max(max_q, self._Qvalues[(bin_state2, act)])
            
            future_value = max_q if max_q != float('-inf') else 0
        
        # Update Q-value
        old_q = self._Qvalues[(bin_state1, action)]
        self._Qvalues[(bin_state1, action)] = (1 - self._learningRate) * old_q + \
                                             self._learningRate * (reward + self._discountFactor * future_value)
        
        # Update state value
        self._values[bin_state1] = max([self.getQValue(observation1, a) for a in self._possibleActions])

    def train(self, repetitions):
        # Store all possible actions
        self._possibleActions = [
            ('left','accelerate'), ('left', 'coast'), ('left','brake'),
            ('straight','accelerate'), ('straight', 'coast'), ('straight','brake'),
            ('right','accelerate'), ('right', 'coast'), ('right','brake')
        ]
        
        # Set training mode
        self._training = True
        
        # Create track for training
        track = buildTrack(1)  # Using track 1 for training
        
        print(f"Training for {repetitions} episodes...")
        
        for i in range(repetitions):
            if i % 10 == 0:
                print(f"Episode {i}/{repetitions}")
                
            # Create a new car
            car = Racecar(track)
            
            # Get initial observation
            obs, reward, done = car.step(('straight', 'coast'))
            total_reward = reward
            
            # Run one episode
            steps = 0
            max_steps = 500  # Prevent infinite loops
            
            while not done and steps < max_steps:
                steps += 1
                
                # Choose an action
                prev_obs = obs
                action = self.chooseAction(obs, car.actions())
                
                # Take the action
                obs, reward, done = car.step(action)
                
                # Update Q-values
                if done:
                    self.updateValues(prev_obs, action, 'terminal', reward)
                else:
                    self.updateValues(prev_obs, action, obs, reward)
                
                total_reward += reward
            
            # Print progress
            if i % 10 == 0:
                print(f"Episode {i} complete. Steps: {steps}, Total reward: {total_reward:.2f}")
        
        # Turn off training mode
        self._training = False
        print("Training complete!")