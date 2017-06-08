from random import random
from scipy.spatial import distance
from operator import add
# from matplotlib import pyplot

def forgy (datos, k, inicializacion="centroides_aleatorios", distancia="euclidean"):

	if (inicializacion == "centroides_aleatorios"):
		centroides = inicializar_centroides (datos, k, "forgy")
		asignaciones = reasignar_clusters (datos, centroides, distancia)
	elif (inicializacion == "clusters_aleatorios"):
		asignaciones = asignar_centroides_aleatoriamente (datos, k)

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

def inicializar_centroides (datos, k, metodo):
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
		for j in range (0, len (suma)):
			if (n_elems > 0):
				baricentro.append (suma[j]/n_elems)
			else:
				baricentro.append (None)
				print "WARNING: Un cluster no tiene elementos"
		centroides.append (baricentro)
	
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
	
