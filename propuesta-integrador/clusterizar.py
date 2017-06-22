from Cell import Cell
from TestAnalyzer import TestAnalyzer
from CellDescriptor import CellDescriptor

from os import listdir
from os.path import isfile, join, basename
from math import sqrt, ceil

from PIL import Image
from scipy.cluster.hierarchy import fclusterdata
from scipy.cluster.vq import kmeans2
from numpy import array, zeros, empty
from matplotlib import pyplot

INPUT_DIR = "input"
CELLS_DIR = "cells"
CELL_SIZE = 24
METRICS_CLUSTER = ["mean_r", "mean_g", "mean_b"]

def main ():
	analyzer = TestAnalyzer ()
	cells_by_file = {}
	for filename in get_input_files (INPUT_DIR):
		image = load_image (filename)
		cells = get_cells (image, CELL_SIZE)
		cells_by_file[filename] = cells
		cluster_data = empty (shape=(len(cells), len(METRICS_CLUSTER)))
		cell_row = 0
		for cell in cells:
			metrics = analyzer.analyze (cell)
			for col in xrange (0, len (METRICS_CLUSTER)):
				cluster_data [cell_row, col] = metrics[METRICS_CLUSTER[col]]
			cell_row += 1
			# cell.save (join (CELLS_DIR, basename ("%s.%i.%i.jpg" % (filename, cell.x, cell.y))))

		print ("Clustering %i cells  (%s)" % (len (cells), filename))
		# groups = fclusterdata (cluster_data, 1.15)
		centroids, groups = kmeans2 (cluster_data, 18)
		num_clusters = max (groups)
		print ("Found %i clusters" % num_clusters)
		generate_cluster_images(groups, cells, filename)

def generate_cluster_images (clusters, cells, filename_prefix):
	print "clusters: %i elementos" % len (clusters)
	print "cells: %i elementos" % len (cells)
	num_clusters = max (clusters)
	cell_width = cells[0].w
	cell_height = cells[0].h

	# Create and populate cells_by_cluster
	cells_by_cluster = []
	for n_cluster in xrange (0, num_clusters):
		cells_by_cluster.append ([])

	# Assign cells to cells_by_cluster
	for cell_number in xrange (0, len (cells)):
		cell = cells [cell_number]
		group = clusters[cell_number]-1
		cells_by_cluster[group].append (cell)

	# Generate images
	for n_cluster in xrange (0, num_clusters):
		num_cells_in_cluster = len(cells_by_cluster[n_cluster])
		square_size = int (ceil (sqrt (num_cells_in_cluster)))
		print "Cluster %i, elements: %i, square_size: %i" % (n_cluster, num_cells_in_cluster, square_size)
		if num_cells_in_cluster > 0:
			image = Image.new ("RGB", (square_size*cell_width, square_size*cell_height))
			for cell_number in xrange (0, len (cells_by_cluster[n_cluster])):
				cell = cells_by_cluster [n_cluster][cell_number]
				x = cell_width * (cell_number % square_size)
				y = cell_height * (cell_number / square_size)
				image.paste (cell.image, (x, y))
			image.save (join (CELLS_DIR, basename ("%s.%i.jpg"% (filename_prefix, n_cluster))))

def get_input_files (dirname):
	all_files = listdir (dirname)
	valid_files = []
	for filename in all_files:
		path = join (dirname, filename)
		if (isfile (path)):
			valid_files.append (path)
	return valid_files


def load_image (filename):
	image = Image.open (filename)
	print ("%s [%i x %i]" % (filename, image.size[0], image.size[1]))
	return image

def get_cells (image, cell_size):
	cells = []
	width, height = image.size
	offset_x, offset_y = (0, 0)
	while (offset_y < height):
		offset_x = 0
		while (offset_x < width):
			cell = Cell (image, offset_x, offset_y, cell_size)
			cells.append (cell)
			offset_x += cell_size
		offset_y += cell_size
	return cells

main ()
