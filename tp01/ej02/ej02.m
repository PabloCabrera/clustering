datos = [
  125, 148, 100, 36, 189;
  13, 45, 203, 120, 164;
  152, 26, 27, 118, 98;
  64, 56, 103, 65, 178;
  110, 112, 115, 78, 19
];

function distancia = distancia_euclidea (vec1, vec2)
    num_elems = min (length (vec1), length (vec2));
    sum2 = 0;
    for (num = [1:num_elems])
        sum2 = sum2 + (vec1(num)-vec2(num))**2;
    endfor
    distancia = sqrt (sum2);
endfunction

function ret = min_distancia (matr_dist)
    min_distancia = matr_dist (1,1);
    min_column = 2;
    min_row = 1;
    for (n_col = [1:columns(matr_dist)])
        for (n_row = [1:rows(matr_dist)])
            if ((n_row != n_col) && (matr_dist (n_row, n_col) < min_distancia))
                display ("iterando sobre " +n_col + " "+ n_row)
                min_row = n_row;
                min_column = n_col;
            endif
        endfor
    endfor
    ret = [min_row, min_column];
endfunction

num_observaciones = columns (datos);

matriz_distancias = [];
for (n_col = [1:num_observaciones])
    row = [];
    obs1 = datos (n_col, :);
    for (n_row = [1:num_observaciones])
        obs2 = datos (n_row, :);
        row = [row, distancia_euclidea(obs1, obs2)];
    endfor
    matriz_distancias = [matriz_distancias; row];
endfor

display ("La matriz de distancias es: ");
display (matriz_distancias);

display ("Agrupar clusters: ");
display ("La minima distancia entre clusters se encuentra en: ");
display (min_distancia (matriz_distancias));
