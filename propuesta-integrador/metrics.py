import operator

def mean_r (cell):
	total = 0
	data = cell.image.getdata()
	num_elems = len (data)
	for pixel in data:
		total += pixel [0]
	total = float (total) / (256 * num_elems)
	return total

def mean_g (cell):
	total = 0
	data = cell.image.getdata()
	num_elems = len (data)
	for pixel in data:
		total += pixel [1]
	total = float (total) / (256 * num_elems)
	return total

def mean_b (cell):
	total = 0
	data = cell.image.getdata()
	num_elems = len (data)
	for pixel in data:
		total += pixel [2]
	total = float (total) / (256 * num_elems)
	return total

def mean_rgb (cell):
	# Multi Metric, returns dict
	total = [0, 0, 0]
	data = cell.image.getdata()
	num_elems = len (data)
	for pixel in data:
		total = map (operator.add, total, pixel)

	for n in (0, 1, 2):
		total[n] = float (total[n]) / (256 * num_elems)

	results = {
		"R": total[0],
		"G": total[1],
		"B": total[2]
	}

	return results

