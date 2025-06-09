# Logs for development of the racecar project

1. Successfull completion of the track with rule based agent. Avg. Score 122.
- intial bounds on maximum and minimum speeds for break/accellerate (0.05, 0.20)
- if a wall is ahead, determine the direction of a turn and break or coast left/right depending on distance away
- Checks for left and right lidar to keep away from sidewalls. 

2. Bump max speed to 0.22 -- Avg. Score 123

3. Add straightaway detection to bump max speed. Start slowing and turning earlier at high speeds. Avg. Score - 129

4. Revert to original setup. Better at following the line, but slower. Fix ahead distance check so coasting actually works. Score 126

5. try to re-implement straightaway detection. score: 123.5 ahead threshhold 0.5 max speed 4

6. improve straightaway thresholds. score 129. ahead 4, max speed 32, add frontleft and frontright at 2

7. set leftfront and rightfront straightwaway thresholds to 1.8 -- score 130

8. increase max speed to 36 score 132

9. bump speed to 4 and coast threshold from 2.5 to 3 --- score 128

10. max speed 38, reg speed bump to 24. ahead 3, lf, rf 1.8, coast threshold 3 --- 133


