**MSc in Robotics Engineering**<br>
**Research Track 1, Assignment 1**<br>
**Student: Alex Thanaphon Leonardi**

**Introduction**
============================
This is the first assignment of the "Research Track 1" course, in the Robotics Engineering degree, Università di Genova.
In the simulator there is a robot in an "arena" of golden and silver tokens. The robot must keep driving in a counter-clockwise direction whilst avoiding the golden tokens which constitute a "wall". When the robot encounters the silver token, it must grab it, turn around 180 degrees, release it, turn back and continue on its path.

**Running the program**
============================
The simulator requires a Python 2.7 installation, the [pygame](http://pygame.org/) library, [PyPyBox2D](https://pypi.python.org/pypi/pypybox2d/2.1-r331), and [PyYAML](https://pypi.python.org/pypi/PyYAML/).

Simply launch the file "start"

**Description**
============================
There are a few interesting things I have had to come up with to successfully implement a solution, and a few "extras" I had fun coding.

First off, the robot's field of view is 360deg. This is nice, but actually causes problems in navigation, so I have reduced it down to specific "cones" of vision to face specific situations.
Secondly, perhaps the most difficult part was finding a way to keep the robot going in a counter-clockwise direction, because from the robot's point of view there is no preferred direction.
The solution I implemented, after thinking about other techniques too, is the following: whenever the robot comes too close to the arena walls, it will scan to its left and to its right (with configurable scanning angle, although the best values I have found are to scan left [-90deg;0deg] and scan right [0deg;+90deg]) and see all golden tokens up to a certain distance. It will then calculate the AVERAGE distance of all golden tokens to its left and to its right, after which it will go towards the direction where the tokens are FARTHEST away (i.e. where the path is more free). This seems to work, save for very specific cases where the robot approaches the corners at a very awkward angle, that only occur after too many simulation cycles to be relevant to this assignment.
A backup check that is missing (since the robot appears to have no difficulty navigating the arena in its current state) and that could be implemented is to mark each silver token each time the robot grabs one, perhaps increasing a counter "num_grabs". This way, if the robot were to accidentally invert its direction, it would eventually figure it out by coming across a silver token whose counter had already been incremented.

*Extras*:
1) I have redefined the print function to be prettier and to keep only one message on the terminal at any given time, rather than spamming lists of messages.
2) Turning: I wanted to avoid stopping the robot at each turn so I programmed a turning function that would keep the robot moving forwards as well as turning slowly and smoothly, just like it would in a real scenario. Additionally, the robot turns quickly when it encouters hard corners but turns more slowly when it simply needs to perform course corrections. This avoids a "ping-pong" effect where each turn is too abrupt and overshoots, leading to another immediate course-correction and so on.
3) The robot moves back slightly, after releasing the silver token, before turning back. This avoids hitting the token when rotating after the release.

The simulation speed is quite high, but this is because I wanted to allow the robot to make fast decisions and behave as smoothly as possible.

**Pseudocode**
============================
```
while simulation is running
  scan for tokens in front

  if silver token found
    if silver token close enough
      grab token
      turn around 180 deg
      release token
      turn around 180 deg
    elseif silver token too far away
      turn towards silver token
      drive towards silver token
  else
    if golden tokens in front are far away
      drive straight ahead
    else
      turn towards free path to avoid obstacles
```
