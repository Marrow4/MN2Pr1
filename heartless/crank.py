import numpy as np

from heartless.configuracio import constants, settings
from heartless.normalitzacio import desnormalitza_temperatura, normalitza_temperatura
from heartless.utils import gauss_pivotatge, guardar_matriu


def crank_nicolson(dx, dt,t_cos=None):
    if t_cos is None:
        t_cos = constants.T_COS
    iteracions = int(constants.t_a // dt) + 1

    beta = dt / (2 * dx * dx)

    # Temperatura amb condicions de contorn
    T = np.zeros((iteracions, constants.N), dtype=np.float64)

    # Creem la matriu tridiagonal A
    diagonal_principal = 1 + 2 * beta
    diagonal_offset = -beta
    # El tamany és 2 menys que T per les condicions de contorn
    A = np.zeros((constants.N - 2, constants.N - 2), dtype=np.float64)
    for i in range(len(A)):
        A[i, i] = diagonal_principal
        if i != 0:
            A[i - 1, i] = diagonal_offset
        if i != len(A) - 1:
            A[i + 1, i] = diagonal_offset

    # Els extrems (inicial i final) són diferents
    A[0, 0] -= beta
    A[-1, -1] -= beta

    for i in range(1, iteracions):
        # Fórmula trobada teòricament
        B = (
            beta * T[i - 1, :-2]
            + (1 - 2 * beta) * T[i - 1, 1:-1]
            + beta * T[i - 1, 2:]
            + dt
        )
        # Les condicions de contorn canvien els extrems
        B[0] += T[i - 1, 0] * beta
        B[-1] += T[i - 1, -1] * beta

        T[i, 1:-1] = gauss_pivotatge(A, B)
    return T + normalitza_temperatura(t_cos)


def executa_sequencia_crank_nicolson():
    """Executa i guarda multiples instàncies del mètode de Crank-Nicolson per diferents dt

    Utilitza dt = q * dx^2 on q és una constant donada per les constants del programa
    """
    print("Executant Crank-Nicolson")
    for q in constants.T_implicit:
        dx = 1 / (constants.N - 1)
        dt = dx * dx * q
        result = crank_nicolson(dx, dt)
        result = desnormalitza_temperatura(result)
        guardar_matriu(result, f"{settings.fitxer_crank}_{q}")
    print("Crank-Nicolson finalitzat")
