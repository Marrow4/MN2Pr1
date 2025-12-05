"""
Fitxer encarregat d'utilitzar les constants del problema per
normalitzar i desnormalitzar les diferent magnituds

Cada funció utilitza les equacions trobades a l'informe
segons si passa de magnitud física a normalitzada o a la inversa
"""

from heartless.configuracio import constants


def normalitza_distancia(x):
    return x / constants.L


def normalitza_temps(t):
    return t * constants.K / (constants.C_V * constants.RHO * constants.L * constants.L)


def normalitza_temperatura(T):
    return (
        T
        * constants.K
        / (constants.CONDUCTIVITAT * constants.VOLTATGE * constants.VOLTATGE / 2)
    )


def desnormalitza_distancia(x):
    return x * constants.L


def desnormalitza_temps(t):
    return t * (constants.C_V * constants.RHO * constants.L * constants.L) / constants.K


def desnormalitza_temperatura(T):
    return (
        T
        * (constants.CONDUCTIVITAT * constants.VOLTATGE * constants.VOLTATGE / 2)
        / constants.K
    )
