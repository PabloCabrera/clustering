# -*- coding: utf-8 -*-
from forgy import forgy
from numpy import loadtxt, array
from scipy.cluster.vq import kmeans, whiten
from numpy import std
from normalizacion import normalizar
from matplotlib import pyplot
from radar import radar_graph

NUM_CARACTERISTICAS = 13
VALORES_K = [2,3,4,5,10,30]

def main ():
	datos = loadtxt ("wines.csv", delimiter=",", usecols=range(1,NUM_CARACTERISTICAS+1))
	datos_norm = normalizar (datos, "max1")

	colores = {
		"kmeans": "#0022bb",
		"forgy": "#119911"
	}

	imprimir_referencias ()
	for k in VALORES_K:
		resultados = dict()
		resultados["kmeans"] = ordenar_centroides (kmeans (datos_norm, k))
		resultados["forgy"] = ordenar_centroides (forgy (datos_norm, k))
		grafico = pyplot.figure()
		n_subplot = 1
		n_metodo = 0
		for metodo in resultados:
			# print ("%s, K: %i, distorsion: %s"%(metodo, k, resultados[metodo][1]))
			pyplot.figtext (0.1, 1-n_metodo*0.5, "Clusters encontrados con %s (K=%i)\nError medio: %s"%(metodo.capitalize(), k, resultados[metodo][1]), {"verticalalignment": "top"})
			for num_centroide in xrange (0, len (resultados[metodo][0])):
				centroide = resultados[metodo][0][num_centroide]
				radar_graph ([""]*NUM_CARACTERISTICAS, centroide, [1]*NUM_CARACTERISTICAS, grafico, 2, k, n_subplot, line_color=colores[metodo])
				n_subplot += 1 
			n_metodo += 1
		grafico.savefig ("comparacion_k%i.png" % k, dpi=96)
		pyplot.close()

def imprimir_referencias ():
	referencias = [
		"Alcohol",
		"Acido \nmalico",
		"Ceniza",
		"Alcalinidad \nde la ceniza",
		"Magensio",
		"Total de \nfenoles",
		"Flavonoides",
		"Fenoles \nno flavonoides",
		"Proantocianidinas",
		"Intensidad \ndel color",
		"Tono",
		"OD280 / OD315 \nde vinos diluidos",
		"Prolina"
	]
	grafico = pyplot.figure()
	radar_graph (referencias, [1]*len(referencias), [1]*len(referencias), grafico)
	pyplot.title ("Caracteristicas de Vinos")
	grafico.savefig ("caracteristicas_vinos.png", dpi=96)
	pyplot.close()
	

def medir_centroide (centroide):
	suma = 0
	for caracteristica in centroide:
		suma += caracteristica
	return suma

def ordenar_centroides (resultado_clusterizacion):
	centroides_desordenados = list (resultado_clusterizacion[0])
	distorsion = resultado_clusterizacion[1]
	centroides_ordenados = sorted (centroides_desordenados, key=medir_centroide)

	return [centroides_ordenados, distorsion]


	
main ()
