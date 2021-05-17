import curses 
from random import randint
import threading
import math
from math import isclose

## -------------global variable------------##
ship = (0,0)

score = 0


## -------------Function defenition------------##
def show_collision(win, ship):
	"""

    This function show the collision seneriao :ship, obstacle it hits and 
    final score) It waits for keyborad inout ESC to exit.
    """
	win.addch(ship[0] - 1, ship[1], 'X')
	win.addstr(0, 2, 'Fianl Score ' + str(score - 1) + '. ' + 
		"(Please press ESC to exit.)")
	key = curses.KEY_RIGHT
	ESC = 27
	while key != ESC:
		key = win.getch()


def setup_window(height, width):
	"""

	Basic setup of curses and window.
    """
	curses.initscr()
	win = curses.newwin(height, width, 0, 0) 
	win.keypad(1)
	curses.noecho()
	curses.curs_set(0)
	win.border(0)
	win.nodelay(1)
	return win, curses


def move_ship(win, ship):
	"""

    This function capture user's keyboard input. The ship moves left if user
    press or hold "<-". The ship moves right if user press or hold "<-".
    The ship will be bounded with the window.
    """
	event = win.getch()

	x = ship[1]
	if x > 1 and event == curses.KEY_LEFT:
	   x -= 1
	if x < width - 2 and event == curses.KEY_RIGHT:
	   x += 1

	new_ship = (height - 2, x)

	if new_ship != ship:
		draw_ship(win, ship, ' ')
		draw_ship(win, new_ship, '*')

	return new_ship


def update_obstacle(obstacles):
	"""

	This function wipe out all the old obstacles first.

    In each iteration, the obstacles will move down a small step according
    to it moving speed (0.01 in this case). The obstacles will only update 
    their position only when they accumulate one big step (1).

    :return: 
    	1. new_obs: a list of tuple that contains exact coordinates of all 
    	obstacles
    	2. integer_obs : a list of tuple that contains rounded-to-integer 
    	coordinates of all obstacles
    """
	global score
	new_obs = []
	integer_obs = []

	if obstacles != []:
		for obs in obstacles:
			win.addch(math.floor(obs[0]), obs[1], ' ')
			if math.floor(obs[0]) != height - 2:
				new_obs.append((obs[0] + 0.01, obs[1]))

	if new_obs == [] or isclose(new_obs[0][0], int(new_obs[0][0])):
		score += 1
		for i in range(num_obs):
			new_obs.insert(0, (1, randint(1,width-2)))

	for obs in new_obs:
		integer_obs.append((math.floor(obs[0]), obs[1]))

	return new_obs, integer_obs


def draw_obs(win,obstacles):
	for obs in obstacles:
		win.addch(math.floor(obs[0]), obs[1], '-')


def draw_ship(win, ship, symbol):
	win.addch(ship[0], ship[1], symbol)


def update_score(win):
	win.addstr(0, 2, 'Score ' + str(score) + ' ')


def increase_speed(win):
	win.timeout(int(500 * 1.0 / (score + 100)))


def get_user_input():
	while True:
		try:
			width = int(input("Please input screan width (range: 20 - 70): "))
			height = int(input("Please input screen height (range: 15 - 30): "))
			difficulity = int(input("Please input level of difficulity (range: 1 - 10): "))
		except ValueError:
			print("Please input integer number")
			continue
		if difficulity > 10 or difficulity < 1 or width < 20 or width > 70 or height < 15 or height > 30:
			print("Please input number within the range")
			continue
		else: 
			break

	difficulity = float(difficulity / 10.0)
	return width, height, difficulity


if __name__ == '__main__':

	width, height, difficulity = get_user_input()

	num_obs = math.ceil(width / 5 * difficulity)

	win, curses = setup_window(height,width)

	obstacles = []

	ship = (height - 2, int(width / 2))

	draw_ship(win, ship, '*')

	while True:
		update_score(win)
		increase_speed(win)
		ship = move_ship(win, ship)
		new_obs, integer_obs = update_obstacle(obstacles)

		# If the coordinate of the ship overlap one of the new obstacles
		# we draw the old obstacles. Otherwise, we draw the new obstacles.
		# And break the while loop.
		if ship in integer_obs:
			draw_obs(win, obstacles)
			break

		draw_obs(win, integer_obs)
		obstacles = new_obs

	show_collision(win, ship)
	curses.endwin()
	print(f"Final score = {score - 1}")












