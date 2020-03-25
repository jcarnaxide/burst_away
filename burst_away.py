import time
import subprocess
import ctypes
import shutil
import random

def ansi_cursor_sel_str(x, y):
	return "\033[" + str(y+1) + ";" + str(x+1)

def init_window(col, row, color, char):
	# clean up current window
	subprocess.run("cls", shell=True)
	
	# prepare initial window for changes later
	untouched_list = []
	for j in range(row):
		for i in range(col):
			print(ansi_cursor_sel_str(i,j) + "H" + color + char, end='')
			untouched_list.append(i + j*col)
	print('', end='', flush=True)
	return untouched_list

# Setup terminal for ANSI escape characters
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# get size of terminal window
col, row = shutil.get_terminal_size()
new_col, new_row = shutil.get_terminal_size()

#list of possible colors to use
colors_to_use = ["\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[35m", "\u001b[36m", "\u001b[37m"]
color = random.choice(colors_to_use)
colors_to_use.remove(color)

#list of possible chars to use
chars_to_use = ['.', '*', 'X', '$', '@', '#', '%', '+', '`']
char = random.choice(chars_to_use)
chars_to_use.remove(char)

untouched_list = init_window(col, row, color, char)

#blink out elements from window one by one, randomly
while(True):
	new_col, new_row = shutil.get_terminal_size()
	if(col != new_col or row != new_row):
		col = new_col
		row = new_row
		untouched_list = init_window(col, row, color, char)

	mod_list = untouched_list.copy()
	size = len(mod_list)
	
	old_char = char
	char = random.choice(chars_to_use)
	chars_to_use.remove(char)
	chars_to_use.append(old_char)
	
	old_color = color
	color = random.choice(colors_to_use)
	colors_to_use.remove(color)
	colors_to_use.append(old_color)
	
	while(size > 0):
		new_col, new_row = shutil.get_terminal_size()
		if(col != new_col or row != new_row):
			break
		choice = random.choice(mod_list)
		mod_list.remove(choice)
		j = int(choice / col)
		i = choice % col
		print(ansi_cursor_sel_str(i,j) + "H" + color + char, end='', flush=True)
		size = len(mod_list)
		time.sleep(0.00001)
