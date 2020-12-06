"""
analyze_folders freezes after a handful of videos, so this recalls it again and again... fml
"""

import time
import subprocess

while True:
	print('\n------STARTING PYTHON PROCESS------')
	subprocess.run(r'python predict\analyze_folders.py stim')
	time.sleep(.1)