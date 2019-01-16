def damerau_levenshtein_distance(s1, s2, ignoreCase=False):
    """
    Implementación de la función de demerau_levenshtein. Calcula dicha distancia
    entre dos cadenas.

    :s1: Cadena 1 (sin restricciones)

    :s2: Cadena 2 (sin restricciones)

    :ignoreCase: Si es True ignora la diferencia entre mayusculas y minusculas

    :return: valor numérico entero que representa la distancia entre estas dos
    cadenas.
    """

    dict = {}
    str1 = s1.lower() if ignoreCase else s1
    str2 = s2.lower() if ignoreCase else s2
    lenstr1 = len(str1)
    lenstr2 = len(str2)
    for i in range(-1, lenstr1+1):
        dict[(i, -1)] = i + 1
    for j in range(-1, lenstr2+1):
        dict[(-1, j)] = j+1

    for i in range(lenstr1):
        for j in range(lenstr2):
            if str1[i] == str2[j]:
                cost = 0
            else:
                cost = 1
            dict[(i, j)] = min(
                dict[(i-1, j)] + 1, # deletion
                dict[(i, j-1)] + 1, # insertion
                dict[(i-1, j-1)] + cost, # substitution
            )
            if i and j and str1[i] == str2[j-1] and str1[i-1] == str2[j]:
                dict[(i, j)] = min(dict[(i, j)], dict[i-2, j-2] + cost) # transposition

    return dict[lenstr1-1, lenstr2-1]
