from __future__ import print_function
import time
from sr.robot import *

max_grab_radius = sim_robot.GRAB_RADIUS

R = Robot()
""" instance of the class Robot"""

def stop():
  """
  Function for halting the robot's movement
  """
  R.motors[0].m0.power = 0
  R.motors[0].m1.power = 0

def drive(speed, seconds):
  """
  Function for setting a linear velocity

  Args: speed (int): the speed of the wheels
  seconds (int): the time interval before stopping
  """
  R.motors[0].m0.power = speed
  R.motors[0].m1.power = speed
  time.sleep(seconds)
  stop()

def drive(speed):
  """
  Function for setting a linear velocity (without stopping)

  Args: speed (int): the speed of the wheels
  """
  R.motors[0].m0.power = speed
  R.motors[0].m1.power = speed

def turn(speed, seconds):
  """
  Function for setting an angular velocity

  Args: speed (int): the speed of the wheels
  seconds (int): the time interval before stopping
  """
  R.motors[0].m0.power = speed
  R.motors[0].m1.power = -speed
  time.sleep(seconds)
  stop()

def turn(speed):
  """
  Function for setting an angular velocity (without stopping)

  Args: speed (int): the speed of the wheels
  """
  R.motors[0].m0.power = speed
  R.motors[0].m1.power = -speed

def turn180(speed):
  """
  Turn 180 degrees clockwise
  R.heading values:
    0deg = 0
    90deg = -1.5
    180deg = -3 = +3
    270deg = 1.5
  Args: speed (int): the speed of the wheels
  """
  max_error = 0.25
  start_heading = R.heading
  curr_heading = R.heading
  discrepancy = abs(start_heading) # |(start_heading + 3) - 3|
  goal_heading = -3 + discrepancy

  # correcting heading if value negative
  if (start_heading < 0):
    goal_heading *= -1

  while(abs(curr_heading - goal_heading) > max_error):
    curr_heading = R.heading
    R.motors[0].m0.power = speed
    R.motors[0].m1.power = -speed
    time.sleep(0.01)

  stop()

def circle(speed, seconds):
  """
  Function for driving in a circle

  Args: speed (int): the speed of the wheels
  seconds (int): the time interval
  """
  R.motors[0].m0.power = speed
  R.motors[0].m1.power = speed/2
  time.sleep(seconds)
  stop()

def find_token_cone(max_deg):
  """
  Function to find the closest token in restricted cone of angle max_deg

  Args: max_deg (float): cone size to search in (directed in front of robot)

  Returns:
  dist (float): distance of the closest token (-1 if no token is detected)
  rot_y (float): angle between the robot and the token (-1 if no token is detected)
  is_silver: the closest token is silver
  """
  dist=100
  is_silver = 0

  for token in R.see():
    if token.dist < dist and (-max_deg < token.rot_y < max_deg):
        dist=token.dist
        rot_y=token.rot_y
        if token.info.marker_type == MARKER_TOKEN_SILVER:
          is_silver = 1

  if dist==100:
    return -1, -1
  else:
    return dist, rot_y, is_silver

def grab_and_turn(turn_speed):
  """
    Grabs a token, turns 180 degrees, places it down, turns back
  """

  R.grab()
  turn180(turn_speed)
  R.release()
  turn180(turn_speed)

def main():
  """
  CONFIG
  """
  max_search_deg = 40
  fwd_speed = 40
  rot_speed = 40
  max_rot_error_deg = 1
  max_obstacle_dist = 1

  # main game loop
  while(1):
    dist, rot_y, is_silver = find_token_cone(max_search_deg)
    if (is_silver):
      # if found silver token ahead

      # if token close, grab it
      if (dist < max_grab_radius):
        grab_and_turn(rot_speed)
      # otherwise, turn to face it and drive towards it
      if (abs(rot_y) > max_rot_error_deg):
        turn(rot_speed)
        print("Aligning to silver")
      else:
        drive(fwd_speed)
        print("Driving to silver")

    else:
      # if found gold token ahead
      # drive until too close
      if (dist > max_obstacle_dist):
        drive(fwd_speed)
        print("Driving...")
      else:
        # make sure we are always turning towards the next silver
        # dist_s, rot_y_s = find_next_silver()
        # find next silver rotation direction
        # change rot_speed to match correct direction

        turn(rot_speed)
        print("Turning...")

    time.sleep(0.25)

main()
