import os
import csv
import sys
import glob
#import pandas as pd

extension = 'csv'
fileNames = [i for i in glob.glob('*.{}'.format(extension))]

hasHeader = False
outputFile = open('COMBINED_USD.csv', 'w')

for file in fileNames:
	if file == 'COMBINED_USD.csv': continue

	print(f'\nProcessing {file}...')
	with open(file, 'r') as csvFile:
		reader = csv.reader(x.replace('\0', '') for x in csvFile)
		header1 = next(reader)
		header2 = next(reader)
		print(f'    Header 1: {header1}')
		print(f'    Header 2: {header2}')
		if not hasHeader:
			line = ','.join(header2) + '\n'
			outputFile.write(line)
			hasHeader = True

		for row in reader:
			line = ','.join(row) + '\n'
			outputFile.write(line)

outputFile.close()
print('Done!')