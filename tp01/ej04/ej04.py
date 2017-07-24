from numpy import array
from scipy.spatial.distance import pdist, squareform
from scipy.cluster.hierarchy import dendrogram, ward
from matplotlib.pyplot import show

datos = array ([
	[125, 148, 100, 36, 189],
	[13, 45, 203, 120, 164],
	[152, 26, 27, 118, 98],
	[64, 56, 103, 65, 178],
	[110, 112, 115, 78, 19]
]);

vector_distancia = pdist (datos)
dendrogram (ward (datos))
show()
