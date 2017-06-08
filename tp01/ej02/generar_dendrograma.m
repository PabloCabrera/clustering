pkg load statistics;

% Datos de entrada
datos = [
   125   148   100    36   189
    13    45   203   120   164
   152    26    27   118    98
    64    56   103    65   178
   110   112   115    78    19
];

% Dialogo de seleccion de amalgamiento
metodos_amalg = {"single", "complete", "average", "ward"};
nombres_amalg = {"Simple", "Completo", "Promedio", "Ward"};
sel_amalg = listdlg(
	"ListString", nombres_amalg,
	"SelectionMode", "Single",
	"PromptString", "Metodo de amalgamiento"
);
amalgamiento = metodos_amalg(sel_amalg);

% Mostrar 
vector_distancias = pdist(datos);
dendrogram(linkage(vector_distancias, amalgamiento));
title (["Amalgamiento: " (nombres_amalg(sel_amalg))]);

