from CellAnalyzer import CellAnalyzer
from metrics import *

class TestAnalyzer (CellAnalyzer):
	def __init__ (analyzer):
		CellAnalyzer.__init__ (analyzer)
		analyzer.setMetric ("mean_r", mean_r)
		analyzer.setMetric ("mean_g", mean_g)
		analyzer.setMetric ("mean_b", mean_b)
		#analyzer.addMultiMetric (mean_rgb) # Este tarda mas

