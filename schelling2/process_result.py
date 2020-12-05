import numpy as np
import os
import csv
import statistics

output_dir = os.path.join(os.path.expanduser("~"),"results_2020")
output_csv = os.path.join(output_dir,"result.csv")

def read_csv():
	results = list()
	with open(output_csv) as f:
		csv_reader = csv.reader(f, delimiter=",")
		
		for row in csv_reader:
			v=row[0]
			th0=int(row[1])
			th1=int(row[2])
			no=int(row[3])
			unf=float(row[5])
			results.append([v,(th0, th1), no, unf])

	return results

def heatmap_csv(results):
	vs = np.arange(0,1,.01)	

	th = list()
	for t0 in range(9):
		for t1 in range(9):
			th.append((t0,t1))

	for v in vs:
		v = "%.2f" % v
		row = list()
		for t0, t1 in th:
			if t0 > t1:
				t0, t1 = t1, t0
			unfs = list(map(lambda r: r[3],filter(lambda r: r[0]==v and r[1]==(t0,t1),results)))
			# print(v, t0, t1, unfs)
			unf_avg = statistics.mean(unfs)
			row.append(str(unf_avg))
		print(",".join(row))

if __name__ == '__main__':
	heatmap_csv(read_csv())
