from numpy import loadtxt, zeros, array
from random import random
from scipy.cluster.vq import kmeans2
from scipy.misc import imread, imshow, imsave
from matplotlib import pyplot

VALORES_K = [2, 6, 15]
METODOS_INICIALIZACION = ["puntos_aleatorios", "muestras_aleatorias", "puntos_equidistantes"]


def main ():
	imagen = imread ("imagen3_5.png")
	imagen_plana = aplanar_imagen (imagen)

	resultados = {}
	for k in VALORES_K:
		resultados[k] = {}
		for metodo in METODOS_INICIALIZACION:
			centroides_iniciales = inicializar_centroides (imagen_plana, k, metodo)
			resultado = kmeans2 (imagen_plana, centroides_iniciales, minit="matrix")
			resultados[k][metodo] = resultado
	generar_imagenes_comparacion (imagen, resultados)

def aplanar_imagen (imagen):
	alto = imagen.shape[0]
	ancho = imagen.shape[1]
	
	num_pixeles = alto * ancho
	imagen_plana = []
	for y in xrange (0, alto):
		for x in xrange (0, ancho):
			imagen_plana.append(imagen[y][x])
	return array(imagen_plana)

def inicializar_centroides (datos, k, metodo):
	if (metodo == "muestras_aleatorias"):
		return obtener_muestra (datos, k)
	elif (metodo == "puntos_aleatorios"):
		return obtener_puntos_aleatorios (datos, k)
	elif (metodo == "puntos_equidistantes"):
		return obtener_puntos_equidistantes (datos, k)
	else:
		raise ValueError ("metodo de inicializacion desconocido")

def obtener_muestra (datos, k):
	centroides = []
	elegidos = []
	assert (len (datos) >= k)
	while len (centroides) < k:
		index = int (random()*k)
		while (index in elegidos):
			index += 1
		centroides.append (datos[index])
		elegidos.append (index)
	return array(centroides)

def obtener_puntos_aleatorios (datos, k):
	datos_tr = datos.transpose()
	puntos = []
	for n in range (0, k):
		for valores_caracteristica in datos_tr:
			punto = []
			minimo = min (valores_caracteristica)
			maximo = max (valores_caracteristica)
			for dimension in range (0, datos.shape[1]):
				punto.append (minimo + random()*(maximo-minimo))
		puntos.append (punto)
	return array(puntos)

def obtener_puntos_equidistantes (datos, k):
	datos_tr = datos.transpose()
	dimension = datos.shape[1]
	params = []
	for n_dimension in range (0, dimension):
		dim_param = {}
		maximo = (max (datos_tr[n_dimension]))
		minimo = (min (datos_tr[n_dimension]))
		step = (maximo-minimo)/k
		dim_param["step"] = step
		dim_param["offset"] = step/2
		params.append (dim_param)

	clusters = []
	for n in range (0, k):
		cluster = []
		for dim_param in params:
			cluster.append (dim_param["offset"]+n*dim_param["step"])
		clusters.append (cluster)
	return array(clusters)

def generar_imagenes_comparacion (original, resultados):
	for k in VALORES_K:
		for metodo in METODOS_INICIALIZACION:
			filename = "k%i_%s.png" % (k, metodo)
			centroides = resultados[k][metodo][0]
			asignaciones = resultados[k][metodo][1]
			imagen = generar_imagen (centroides, asignaciones, original.shape)
			imsave (filename, imagen)
			
		

def generar_imagen (centroides, asignaciones, dimensiones):
	imagen = zeros (dimensiones)
	alto = dimensiones[0]
	ancho = dimensiones[1]
	for y in xrange (0, alto):
		for x in xrange (0, ancho):
			indice = y*ancho + x
			color = centroides[asignaciones[indice]]
			imagen[y][x] = color
	return imagen

	

main ()

