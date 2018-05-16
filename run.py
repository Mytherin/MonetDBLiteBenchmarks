
import os
import time

initfile = os.environ['INITFILE']
timefiles = os.environ['TIMEFILE'].split(',')
nruns = int(os.environ['NRUNS'])

for tf in timefiles:
	if not os.path.isfile(tf):
		raise Exception("Timing file not found")

if os.path.isfile(initfile):
	exec(open(initfile).read(), globals())


with open('start_experiments.csv', 'w+') as f:
	f.write("lala")

results = {}
for tf in timefiles:
	results[tf] = []
	source = open(tf).read()
	for j in range(0, nruns + 1):
		start = time.time()
		exec(source)
		end = time.time()
		if j != 0:
			results[tf].append(end - start)


with open('tmp_results.csv', 'w+') as f:
	keys = results.keys()
	for i in range(len(keys)):
		entry = keys[i]
		f.write(entry)
		f.write(',' if i < len(keys) - 1 else '\n')
	for j in range(0, nruns):
		for i in range(len(keys)):
			val = results[keys[i]][j]
			f.write(str(val))
			f.write(',' if i < len(keys) - 1 else '\n')

