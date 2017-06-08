from numpy import array, loadtxt, unique
from scipy.cluster.hierarchy import linkage, cophenet, dendrogram, inconsistent, fcluster
from scipy.spatial.distance import pdist
from matplotlib import pyplot

INCONSISTENT_THRESHOLD = 1.15
def main ():
	datos = loadtxt (
		"telecomunicaciones.csv",
		delimiter = ",",
		skiprows = 1, # Primera fila son titiulso
		usecols = range (11,36) # Las primeras 11 columnas son datos personales, no de servicios
	)

	clusterizar (datos, "ward", "euclidean")

	for amalgamiento in ("single", "complete", "average"):
		for metrica in ("euclidean", "chebyshev", "cityblock"):
			clusterizar (datos, amalgamiento, metrica)



def clusterizar (datos, amalgamiento, metrica):
	vector_distancias = pdist (datos, metrica)
	agrupamiento = linkage (datos, amalgamiento, metrica)
	matriz_inconsistencia = generar_matriz_inconsistencia (agrupamiento, amalgamiento, metrica)
	correlacion, matriz_cofenetica = cophenet (agrupamiento, vector_distancias)
	clusters_generados = fcluster (agrupamiento, INCONSISTENT_THRESHOLD, R=matriz_inconsistencia)
	num_clusters = len(unique(clusters_generados))
	generar_dendrograma (agrupamiento, amalgamiento, metrica, correlacion, num_clusters)
	generar_histograma (matriz_inconsistencia[:,3], amalgamiento, metrica)

def generar_dendrograma (agrupamiento, amalgamiento, metrica, correlacion, num_clusters):
	pyplot.figure ()
	dendrogram (agrupamiento, color_threshold=0, no_labels=True)
	pyplot.title ("%s %s, cof: %f, num_clusters=%i"%(amalgamiento, metrica, correlacion, num_clusters))
	filename = "dendrogramas/%s_%s.png" % (amalgamiento, metrica)
	pyplot.savefig (filename)

def generar_matriz_inconsistencia (agrupamiento, amalgamiento, metrica):
	matriz_inconsistencia = inconsistent (agrupamiento)
	archivo = open ("matriz_inconsistencia/%s_%s.csv"%(amalgamiento, metrica), "w")
	index = 0 
	for fila in matriz_inconsistencia:
		archivo.write(", ".join (list(map(lambda valor: str(valor), agrupamiento[index]))) + ", , ")
		archivo.write(", ".join (list(map(lambda valor: str(valor), fila))) + "\n")
		index += 1
	archivo.close ()
	return matriz_inconsistencia

def generar_histograma (observaciones, amalgamiento, metrica):
	filename = "histogramas_inconsistencia/%s_%s.png" % (amalgamiento, metrica)
	fig = pyplot.figure()
	pyplot.hist(observaciones)
	pyplot.title ("Distribucion de inconsistencia, %s %s" % (amalgamiento, metrica))
	fig.savefig (filename)

		
main ()
