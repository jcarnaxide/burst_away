import time
import subprocess
import ctypes
import shutil
import random

# Setup terminal for ANSI escape characters
kernel32 = ctypes.windll.kernel32
kernel32.SetConsoleMode(kernel32.GetStdHandle(-11), 7)

# get size of terminal window
col, row = shutil.get_terminal_size()

# clean up current window
subprocess.run("cls", shell=True)

#list of possible chars to use
chars_to_use = ['.', '*', 'X', '$', '@', '#', '%', '+', '`']
char = random.choice(chars_to_use)
chars_to_use.remove(char)

#list of possible colors to use
colors_to_use = ["\u001b[31m", "\u001b[32m", "\u001b[33m", "\u001b[35m", "\u001b[36m", "\u001b[37m"]
color = random.choice(colors_to_use)
colors_to_use.remove(color)

#populate window and list for later removal
untouched_list = []
for j in range(row):
	for i in range(col):
		print("\033[" + str(j+1) + ";" + str(i+1) + "H" + color + char, end='')
		untouched_list.append(i + j*col)
print('', end='', flush=True)

#blink out elements from window one by one, randomly
while(True):
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
		choice = random.choice(mod_list)
		mod_list.remove(choice)
		j = int(choice / col)
		i = choice % col
		print("\033[" + str(j+1) + ";" + str(i+1) + "H" + color + char, end='', flush=True)
		size = len(mod_list)
		time.sleep(0.00001)

#move cursor to end of window when complete, then wait for forced exit
print("\033[" + str(row+1) + ";" + str(col) + "H" + "", end='', flush=True)
while(True):
	time.sleep(1)
