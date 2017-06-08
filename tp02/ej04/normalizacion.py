from numpy import array, mean, transpose
from numpy import std as std_dev

def normalizar_z (datos):
	media = mean (datos)
	desvio = std_dev (datos)
	estandarizado = list (map (lambda valor: (valor-media)/desvio, datos))
	return estandarizado

def normalizar_med1 (datos):
	media = mean (datos)
	estandarizado = list (map  (lambda valor: valor/media, datos))
	return estandarizado

def normalizar_max1 (datos):
	maximo = max (datos)
	minimo = min (datos)
	estandarizado = list (map (lambda valor: (valor-minimo) / (maximo-minimo), datos))
	return estandarizado

def normalizar (datos, metodo="max1"):
	func_std = {
		"z": normalizar_z,
		"med1": normalizar_med1,
		"max1": normalizar_max1
	}

	datos_tr = transpose (datos)
	datos_std_tr = []

	for observacion in datos_tr:
		obs_std = func_std[metodo] (observacion)
		datos_std_tr.append (obs_std)

	return array (transpose (datos_std_tr), ndmin=2, dtype=float)

