import os
import json
import time
import re
import readline



datadir = '' # Virtual machine shared folder
if os.path.exists('/media/sf_Primecoin/blocks'):
	datadir = ' -datadir=/media/sf_Primecoin'


def primecoin(cmd):
	return os.popen(f'src/primecoin-cli{datadir} {cmd}').read()


def console(width):
	os.system('clear')
	print('-' * width)
	print('Primecoin Console'.center(width))
	print('-' * width)
	count = 1
	lastCmd = ''
	while True:
		numTimes = 1
		cmd = input(str(count).ljust(4) + '>   ')
		cmds = re.split(r'\s*\*\s*(?=[0-9]+$)', cmd)
		if len(cmds) == 2: # Add command multiplier
			cmd = cmds[0]
			numTimes = int(cmds[1])

		if len(cmd) == 0:
			cmd = lastCmd

		elif cmd == 'clear':
			os.system('clear')
			continue
		elif str(cmd).endswith('*'): # Infinite loop
			cmd = str(cmd[:-1])
			print(cmd)
			while True:
				primecoin(cmd)
			return
		else:
			cmd = str(cmd)
			lastCmd = cmd
			count += 1
		print()

		internalTime = 0
		externalTime = 0
		for i in range(numTimes):
			# Internal
			t1 = time.perf_counter()
			output = primecoin(cmd)
			t2 = time.perf_counter()
			externalTime += t2 - t1

			# External
			t = re.search(r'That took ([0-9\.]+) clocks', output)
			if t == None: # Support different timer formats (send, mine)
				t = re.search(r'"Elapsed time \(seconds\)": ([0-9\.]+)', output)
			if t != None:
				internalTime += float(t.group(1))

		internalTime /= numTimes
		externalTime /= numTimes

		if numTimes == 1:
			print(output)
			print(f'That took {externalTime} seconds (external).')
		else:
			if t != None:
				# Remove the built in "That took ... clocks"
				print('\n'.join(map(str, output.split('\n')[:-2])))
			else:
				print(output)
			print(f'Number of samples: {numTimes}.')
			print(f'Average time (Internal primecoin): {internalTime} clocks.')
			print(f'Average time (External Console): {externalTime} seconds.')

		print('-' * width)

console(80)
