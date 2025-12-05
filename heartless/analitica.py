import numpy as np

from heartless.configuracio import constants
from heartless.normalitzacio import desnormalitza_distancia, desnormalitza_temperatura


def fxt_t_determinat(t: float, lim_sum: int = 300):
    """Calcula la funció analítica dinat un temps normalitzat

    Parameters
    ----------
    t : float
        Temps normalitzat

    Returns
    -------
    npt.NDArray[np.float64], npt.NDArray[np.float64]
        Resultat per totes les x (normalitzades) en el t donat
    """
    T_list = []
    b = constants.T_COS
    # Treballem amb temperatura normalitzada (per aixo el límit és 1)
    x_arr = np.linspace(0, 1, constants.N, dtype=np.float64)
    for x in x_arr:
        sum = 0
        for i in range(
            lim_sum
        ):  # `lim_sum` és el límit del sumatori, pot fer variar la presició
            # Equació trobada
            sum = sum + (
                (1 - np.exp(-((2 * i + 1) ** 2) * (np.pi) ** 2 * t)) / (2 * i + 1) ** 3
            ) * (np.sin((2 * i + 1) * np.pi * x))
        T_variable = b + desnormalitza_temperatura((4 / (np.pi**3)) * sum)
        T_list.append(T_variable)
    # Desnormalitzem el resultat final per treballar amb resultats amb significat físic
    return desnormalitza_distancia(x_arr), np.array(T_list, dtype=np.float64)
