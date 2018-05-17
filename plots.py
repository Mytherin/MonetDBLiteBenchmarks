
import os
import numpy

sf1_directory = 'results-sf1'
sf10_directory = 'results-sf10'

result_directory = sf1_directory

files = os.listdir(result_directory)

name_map = {
	'sqlite': 'SQLite', 
	'postgres': 'PostgreSQL',
	'monetdb': 'MonetDB',
	'monetdblite': 'MonetDBLite',
	'julia': 'Julia',
	'pandas': 'Pandas',
	'mariadb': 'MariaDB',
	'dplyr': 'dplyr',
	'datatable': 'data.table'
}

name_order = [
	'monetdblite',
	'monetdb',
	'sqlite',
	'postgres',
	'mariadb',
	'datatable',
	'dplyr',
	'pandas',
	'julia'
]

# plot load and write times
load_results = []
write_results = []
for fname in files:
	if '-write.csv' not in fname and '-load.csv' not in fname: continue
	if '-write.csv' in fname:
		results = write_results
	else:
		results = load_results
	fname = os.path.join(result_directory, fname)
	with open(fname, 'r') as f:
		lines = f.read().split('\n')
		timings = []
		system = None
		for line in lines[1:]:
			if len(line) == 0: continue
			(System,File,Run,Timing) = line.split(',')
			timings.append(float(Timing))
			system = System
		if system == None:
			raise Exception("Did not find system in file", fname)
		results.append([system, numpy.median(timings)])


def generate_plot(results, plot_name):
	max_value = 0
	with open('plots/temp_data.csv', 'w+') as f:
		f.write('system,time\n')
		for entry in results:
			print(entry)
			f.write(name_map[entry[0]])
			f.write(',')
			f.write(str(entry[1]))
			f.write('\n')
			if entry[1] > max_value:
				max_value = entry[1]
	os.environ['PLOT_NAME'] = plot_name
	os.environ['Y_MAX_BOUND'] = str(int(max_value / 0.8))

	CURRENT_DIRECTORY = os.getcwd()
	os.chdir('plots')
	os.system('R -f plot.R')
	os.chdir(CURRENT_DIRECTORY)

generate_plot(write_results, 'write.pdf')
generate_plot(load_results, 'load.pdf')


queries = ['q%02d' % x for x in range(1, 11)]

for result_directory in [sf1_directory, sf10_directory]:
	files = os.listdir(result_directory)

	query_time = {}
	for q in queries:
		query_time[q] = {}

	# plot total time for TPC-H
	for fname in files:
		if '-write.csv' in fname or '-load.csv' in fname: continue

		fname = os.path.join(result_directory, fname)
		with open(fname, 'r') as f:
			lines = f.read().split('\n')
			for line in lines[1:]:
				if len(line) == 0: continue
				(System,File,Run,Timing) = line.split(',')
				for q in queries:
					if q in File:
						if System not in query_time[q]:
							query_time[q][System] = []
						query_time[q][System].append(float(Timing))
						break


	query_results = {}
	total_results = {}

	for q in queries:
		query_results[q] = {}
		for system in query_time[q].keys():
			med = numpy.median(query_time[q][system])
			if system not in total_results:
				total_results[system] = 0
			if med > 0:
				total_results[system] += med
			query_results[q][system] = med


	def get_min_system(result_list):
		min_val = 1e32
		min_sys = None
		for key in result_list.keys():
			if result_list[key] > 0 and result_list[key] < min_val:
				min_sys = key
				min_val = result_list[key]
		return min_sys

	print(result_directory)
	print("")

	for name in name_order:
		text = name_map[name] + ' & '
		for q in queries:
			result = query_results[q][name]
			if int(result) == -2:
				text += '{\color{BrickRed}\\textbf{E}} & '
			elif int(result) == -1:
				text += '{\color{BrickRed}\\textbf{T}} & '
			elif get_min_system(query_results[q]) == name:
				text += '\\textbf{' + '%.2f' % result + '} & '
			else:
				text += '%.2f' % result + ' & '
		if get_min_system(total_results) == name:
			text += '\\textbf{' + '%.2f' % total_results[name] + '} \\\\'
		else:
			text += '%.2f' % total_results[name] + ' \\\\'
		print(text)

	print("")



