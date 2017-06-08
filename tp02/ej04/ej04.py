from normalizacion import normalizar
from numpy import loadtxt
from scipy.cluster.hierarchy import dendrogram, linkage
from matplotlib import pyplot

def main ():
	datos = loadtxt ("venta_autos.csv", delimiter=",", skiprows=1, usecols=range(2,12))
	cabecera = "ventas, precio, motor, CV, pisada, ancho, largo, peso_neto, deposito, mpg"

	metodos = {
		"max1": "Magnitud Maxima de 1",
		"med1": "Media de 1",
		"z": "Puntuaciones estandarizadas Z"
	}

	pyplot.figure() 
	# Sin normalizar
	pyplot.subplot(2, 2, 1)
	agrupamiento = linkage (datos)
	dendrogram (agrupamiento, color_threshold=0)
	pyplot.title ("Datos sin normalizar")

	n_subplot = 2
	for metodo in metodos:
		datos_std = normalizar (datos, metodo)
		guardar_csv (datos_std, "datos_normalizados/%s.csv" % metodo, cabecera);
		agrupamiento = linkage (datos_std)
		pyplot.subplot(2, 2, n_subplot)
		n_subplot += 1
		dendrogram (agrupamiento, color_threshold=0)
		pyplot.title (metodos[metodo])
	pyplot.show()

def guardar_csv (datos, nombre_archivo, cabecera=None):
	archivo = open (nombre_archivo, "w")

	if cabecera is not None:
		archivo.write (cabecera+"\n")

	for fila in datos:
		linea = ", ".join (list(map (lambda valor: str(valor)[:4], fila)))
		archivo.write (linea + "\n")
	archivo.close ()

main ()
