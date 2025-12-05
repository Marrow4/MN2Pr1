import numpy as np

from heartless.configuracio import constants, settings
from heartless.normalitzacio import desnormalitza_temperatura, normalitza_temperatura
from heartless.utils import gauss_pivotatge, guardar_matriu


def euler_implicit(dx, dt) -> np.ndarray:
    # definim els paràmetres
    x = constants.N
    t = int(constants.t_a // dt + 1)
    T_c = normalitza_temperatura(constants.T_COS)

    a = dt
    b = dt / (dx**2)

    # Mariu de temperatures
    T = np.zeros((t, x))

    T[0, :] = T_c  # generem la condició inicial (tots punts a temperatura cos)

    """Apunt important:
    Tant la matriu A com el vector c es defineixen amb n_files = len(T) - 2
    Aixo succeeix perque els extrems de T estan connectats a una font i
    per tant estan a una temperatura constant i no han de ser calculats.
    Aquest mètode troba les temperatures T des de `i = 1,...,n-2`
    T_0 = T_{n-1} = T_COS
    """

    # Definim el vector c, de l'equacio Ax = c
    def vec_c(T_actual, a, b, T_cc_esq, T_cc_dret):
        x = len(T_actual)
        c = np.zeros(x - 2)

        for j in range(1, x - 1):
            c_i = j - 1

            # Equació trobada d'Euler implicit
            c[c_i] = T_actual[j] + a

            # Els extrems tenen una forma diferent
            if j == 1:
                c[c_i] += b * T_cc_esq
            elif j == x - 2:
                c[c_i] += b * T_cc_dret

        return c

    # Definim la matriu, de l'equacio Ax = c
    # segons l'equació d'Euler Implícit
    def matriu_A(b, x):
        n_interior = x - 2

        A = np.zeros((n_interior, n_interior))

        for i in range(n_interior):
            A[i, i] = 1 + 2 * b  # diagonal principal

            if i > 0:
                A[i, i - 1] = -b  # diagonal inferior

            if i < n_interior - 1:  # diagonal superior
                A[i, i + 1] = -b

        return A

    A = matriu_A(b, x)  # La matriu és una constant en totes les iteracions

    for i in range(t - 1):
        c = vec_c(
            T[i, :], a, b, T_c, T_c
        )  # calcular vector c segons les condicions anteriors

        T_interior = gauss_pivotatge(A, c)  # trobem les x solucions del sistema

        # definim les temperatures de la matriu T aplicant les condicions de contorn
        T[i + 1, 0] = T_c
        T[i + 1, -1] = T_c
        T[i + 1, 1:-1] = T_interior

    return T


def executa_sequencia_implicit():
    # Per cada valor de T_implicit, calculem i guardem el mètode d'Euler Implícit
    print("Executant Euler Implícit")
    for q in constants.T_implicit:
        dx = 1 / (constants.N - 1)
        dt = q * dx * dx
        result = euler_implicit(dx, dt)
        guardar_matriu(
            desnormalitza_temperatura(result), f"{settings.fitxer_implicit}_{q}"
        )
    print("Euler Implícit finalitzat")
