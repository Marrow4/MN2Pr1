import os

import numpy as np
from numpy.typing import NDArray

from heartless.configuracio import constants, settings
from heartless.normalitzacio import desnormalitza_distancia


def calcula_divisions() -> np.ndarray:
    """
    Coneixent que x està normalitzada i la quantitat de divisions (N), podem trobar dx i conseqüentment totes les posicions de la matriu $\\hat{x}$

    :return: Array amb tots els valors de $\\hat
    :rtype: ndarray[_AnyShape, dtype[float64]]
    """
    return np.linspace(0, 1, constants.N, dtype=np.float64)


def guardar_matriu(matriu: np.ndarray, fitxer: str = "output") -> None:
    """
    Guarda matrius en csv, afegint com a columnes els intervals de x sense normalitzar

    :param matriu: Matriu de temperatures
    :type matriu: np.ndarray[(NxM),np.float64]
    :param fitxer: Nom del fitxer sense extensió
    :type fitxer: str

    """

    directori_carpeta = os.path.join(os.getcwd(), settings.dades_path)

    # Crea el directori de `dades` si no existeix
    try:
        os.makedirs(directori_carpeta, exist_ok=True)
        # print(f"El directori: '{output_dir}' existeix")
    except Exception as e:
        print(f"Error creant el directori: {e}")
        return

    # Creem l'informació necessària per guardar el csv
    directori_fitxer = os.path.join(directori_carpeta, fitxer + ".csv")
    pos_x = desnormalitza_distancia(calcula_divisions())
    headers = ",".join(["%.17e" % nom for nom in pos_x])

    try:
        np.savetxt(
            directori_fitxer,
            matriu,
            fmt="%.17e",
            delimiter=",",
            header=headers,
            comments="",
        )
        print("Guardat correctament")
    except Exception as e:
        print(f"Error inesperat: {e}")


def carregar_posicions_temperatures(fitxer: str) -> tuple[np.ndarray, np.ndarray]:
    """Llegeix el fitxer (sense extensió de la carpeta de dades) i el retorna en el format personalitzat

    Separa les columnes (posicions en x) dels valors de Temperatura obtinguts

    Arguments:
        fitxer: string del nom del fitxer dins de `dades/` (sense extensió `.csv`)

    Retorna:
        Tupla que conté:
        - Posicions x (np.ndarray): 1D array de les posicions x
        - Matriu T    (np.ndarray): Matriu 2D de les Temperatures.
    """

    # Crea el directory del fitxer i assegura que existeixi
    directori_carpeta = os.path.join(os.getcwd(), settings.dades_path)
    fitxer_complet = os.path.join(directori_carpeta, fitxer + ".csv")
    if not os.path.exists(fitxer_complet):
        print(f"Error: El fitxer '{fitxer_complet}' no existeix.")
        return np.array([], dtype=object), np.array([], dtype=np.float64)

    # Llegim la 1a línia, amb les posicions en l'eix x
    try:
        with open(fitxer_complet, "r") as f:
            # Treiem tots els caracters espai, salts de línia i tabulacions
            encabessat = f.readline().strip()

            elements_encabessat = encabessat.split(",")

            encab_temp = []
            # Convertim tots els valors a np.float64 (sempre que es pugui)
            for item in elements_encabessat:
                try:
                    encab_temp.append(np.float64(item))
                except ValueError:
                    print(" Error al processar els headers, tractats com strings ")
                    encab_temp.append(item)

            pos_x = np.array(encab_temp, dtype=object)

    except Exception as e:
        print(f" Error al llegir els headers: {e}")
        return np.array([], dtype=object), np.array([], dtype=np.float64)

    # Llegim la matriu de temperatures (les files són les iteracions temporals)
    try:
        matriu_temperatura = np.loadtxt(
            fitxer_complet, dtype=np.float64, delimiter=",", skiprows=1
        )

    except Exception as e:
        print(f" Error al llegir la matriu: {e}")
        return pos_x, np.array([], dtype=np.float64)

    return pos_x, matriu_temperatura


def gauss_pivotatge(matriu: NDArray, indep: NDArray) -> NDArray:
    """Resol el sistema: `matriu * x = indep` utilitzant el mètode de Gauss amb pivotatge total.

    És un resultat exacte, si no tenim en compte errors numèrics d'arrodoniment

    Parametres
    ----------
    matriu : NDArray[np.float64,Shape[N]]
        Coeficient d'entrada, corresponents a les x_1, x_2... (m)
    indep : NDArray[np.float64,Shape[N]]
        Variables independents (b)

    Retorna
    -------
    NDArray[np.float64,Shape[N]]
        Resultat del mètode (x)
    """

    # Copiem les matrius per evitar modificar la mateixa memòria
    A = matriu.copy()
    b = indep.copy()

    # Recordarem l'ordre de les columnes per fer el pivotatge
    ordre_columnes = np.arange(len(b))

    for i in range(len(A) - 1):
        # Creem la submatriu per trobar el valor absolut més gran
        subA = A[i:, i:]
        idx_flat = np.argmax(np.abs(subA))
        i_sub, j_sub = np.unravel_index(idx_flat, subA.shape)

        # Trobem l'index del valor més gran de la matriu A sencera
        max_idx = i + i_sub
        max_jdx = i + j_sub

        # Reordenem les matrius perquè el valor més gran de A estigui a la posició [i,i]
        A[[i, max_idx]] = A[[max_idx, i]]
        A[:, [i, max_jdx]] = A[:, [max_jdx, i]]
        b[[i, max_idx]] = b[[max_idx, i]]
        ordre_columnes[[i, max_jdx]] = ordre_columnes[[max_jdx, i]]

        # Fem 0 els elements de la columna `i` per sota la fila `i`
        mult = A[i + 1 :, i] / A[i, i]
        b[i + 1 :] = b[i + 1 :] - mult * b[i]
        A[i + 1 :, i:] -= mult[:, np.newaxis] * A[i, i:]

    # Remuntem les columnes per trobar els valors de x (desordenats)
    x_desord = np.zeros(len(b))
    for i in range(len(b) - 1, -1, -1):
        suma = np.dot(A[i, i + 1 :], x_desord[i + 1 :])
        x_desord[i] = (b[i] - suma) / A[i, i]
    # Utilitzant l'ordre de columnes, reordenem x
    x_ordenat = np.zeros(x_desord.shape)
    x_ordenat[[ordre_columnes]] = x_desord

    return x_ordenat


def guarda_figura(fig, fitxer, **kwargs):
    """
    Saves a Matplotlib figure to the 'grafiques' directory, creating it if needed.
    """

    directori_carpeta = os.path.join(os.getcwd(), settings.grafiques_path)

    # Crea el directori de `dades` si no existeix
    try:
        os.makedirs(directori_carpeta, exist_ok=True)
    except Exception as e:
        print(f"Error creant el directori: {e}")
        return

    # Directori sencer del fitxer
    directori_fitxer = os.path.join(directori_carpeta, fitxer)

    # Guarda la figura amb una configuració específica
    fig.savefig(directori_fitxer, dpi=300, bbox_inches="tight", **kwargs)

    print(f"Gràfica guardada a: {directori_fitxer}")


def error_relatiu(T_exp, T_an):
    return np.abs(T_exp - T_an) / T_an


def troba_maxima_iter_temps(T) -> tuple[int, int]:
    """Troba l'últim índex on es compleixen les següent condicions imposades:
    - El teixit sa ha d'estar per sota de 50 ºC
    - El teixit malalt ha d'estar per sota de 80 ªC
    - El teixit malalt ocupa des de 0.75 cm fins 2 cm

    Els index corresponent a aquests límits són: `i = N*(L-l)/(2L) ; j = N - i`
    on `i` es el límit esquerra, `j` es el límit dret


    Parameters
    ----------
    T : npt.NDArray[2D matrix]
        Matriu corresponent a les temperatures

    Returns
    -------
    tuple[int,int]
        Retorna l'últim índex que compleix les condicions
        i l'índex de la columna on s'ha trobat
    """
    lim_esq = np.ceil(constants.N * (constants.L - constants.l_mal) / (2 * constants.L))
    lim_dret = constants.N - lim_esq

    rows = T.shape
    if len(rows) == 1:
        for j in range(rows[0]):
            # Si el teixit està fora dels límits malalts (es teixit sa)
            # limitem la temperatura a 50 ºC
            if j < lim_esq or j > lim_dret:
                if T[j] > 50:
                    # ha trobat l'índex que no compleix, torna l'anterior
                    return (
                        0,
                        j-1,
                    )
            # Si es teixit malalt, mirem que no superi 80 ºC
            else:
                if T[j] > 80:
                    return 0, j-1
        return 0,-1
        
    rows,cols = rows
    for i in range(rows):
        for j in range(cols):
            # Si el teixit està fora dels límits malalts (es teixit sa)
            # limitem la temperatura a 50 ºC
            if j < lim_esq or j > lim_dret:
                if T[i, j] > 50:
                    # ha trobat l'índex que no compleix, torna l'anterior
                    return (
                        i - 1,
                        j,
                    )
            # Si es teixit malalt, mirem que no superi 80 ºC
            else:
                if T[i, j] > 80:
                    return i - 1, j
    return rows, cols
