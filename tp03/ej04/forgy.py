from random import random
from scipy.spatial import distance
from operator import add
# from matplotlib import pyplot

def forgy (datos, k, inicializacion="muestra_aleatoria", distancia="euclidean"):

	if (inicializacion == "muestra_aleatoria"):
		centroides = obtener_muestra (datos, k)
		asignaciones = reasignar_clusters (datos, centroides, distancia)
	elif (inicializacion == "puntos_aleatorios"):
		centroides = obtener_puntos_aleatorios (datos, k)
		asignaciones = reasignar_clusters (datos, centroides, distancia)
	elif (inicializacion == "clusters_aleatorios"):
		asignaciones = asignar_centroides_aleatoriamente (datos, k)
	else:
		print "Forgy: Inicializacion no valida"
		return None

	centroides = recalcular_centroides (datos, asignaciones)
	convergencia = False
	ciclos = 0
	#dibujar_centroides (centroides, ciclos)

	while (not convergencia):
		asignaciones_anteriores = asignaciones
		asignaciones = reasignar_clusters (datos, centroides, distancia)
		centroides = recalcular_centroides (datos, asignaciones)
		# dibujar_centroides (centroides, ciclos)
		convergencia = (asignaciones == asignaciones_anteriores)
		ciclos += 1
	
	distorsion = calcular_distorsion (datos, centroides, distancia)
	#print "Forgy: Completado en %i ciclos"%ciclos
	# return (centroides, asignaciones)
	return (centroides, distorsion)

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
	return centroides

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
	return puntos
		

def recalcular_centroides (datos, asignaciones):
	sumas = []
	num_elems_cluster = []
	k = max (asignaciones) + 1
	

	for n in range (0, k):
		sumas.append ([0]*len(datos[0]))
		num_elems_cluster.append (0)
		
	for i in xrange (0, len (datos)):
		elemento = datos[i]
		cluster = asignaciones[i]
		num_elems_cluster[cluster] += 1
		sumas[cluster] = map (add, sumas[cluster], elemento)

	centroides = []
	for n in range (0, k):
		baricentro = []
		suma = sumas[n]
		n_elems = num_elems_cluster[n]
		cluster_vacio = False
		for j in range (0, len (suma)):
			if (n_elems > 0):
				baricentro.append (suma[j]/n_elems)
			else:
				cluster_vacio = True

		if not cluster_vacio:
			centroides.append (baricentro)
		else:
			print "WARNING: Se ha eliminado un cluster por no tener elementos"
	
	return centroides

def asignar_centroides_aleatoriamente (datos, k):
	asignaciones = []
	num_datos = len (datos)
	for n in range (0, num_datos):
		asignaciones.append (int (random () * k))
	return asignaciones

def reasignar_clusters (datos, centroides, metrica):
	nuevos_centroides = []
	dist = getattr (distance, metrica)
	for elemento in datos:
		distancia_a_centroides = []
		for centroide in centroides:
			distancia_a_centroides.append (dist (elemento, centroide))
		minima = min (distancia_a_centroides)
		cluster_elegido = distancia_a_centroides.index (minima)
		nuevos_centroides.append (cluster_elegido)
	return nuevos_centroides

def calcular_distorsion (datos, centroides, metrica):
	dist = getattr (distance, metrica)
	suma_errores = 0
	for elemento in datos:
		distancia_a_centroides = []
		for centroide in centroides:
			distancia_a_centroides.append (dist (elemento, centroide))
		minima = min (distancia_a_centroides)
		suma_errores += abs (minima)
	distorsion = suma_errores / len (datos)
	return distorsion

# def dibujar_centroides (centroides, ciclo=0):
#	for centroide in centroides:
#		pyplot.scatter(centroide[0], centroide[1])
	
