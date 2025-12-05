import numpy as np

from heartless.configuracio import constants, settings
from heartless.normalitzacio import desnormalitza_temperatura, normalitza_temperatura
from heartless.utils import guardar_matriu


def euler_explicit(dx, dt) -> np.ndarray:
    t_cos = normalitza_temperatura(constants.T_COS)

    def euler_step_arr(Tnow):
        # Creem un array plena de T_COS
        # Simplifica afegir les condicions de contorn,
        # perquè sabem que els extrems estaran sempre a T_COS
        Tnext = np.full(Tnow.shape, t_cos, dtype=np.float64)

        # Mètode d'Euler explicit amb l'equació trobada
        # S'han agafat els intervals adequats pel resultat
        Tnext[1:-1] = (
            (dt / (dx**2)) * (Tnow[2:] - 2 * Tnow[1:-1] + Tnow[:-2]) + dt + Tnow[1:-1]
        )
        return Tnext

    # Generem la matriu amb tots els valors que necessitem
    # Utilitzant dt i el temps que volem arribar coneixem el tamany de la matríu
    Temperatures = np.zeros(
        (int(constants.t_a // dt) + 1, constants.N), dtype=np.float64
    )

    # Imposem les condicions inicials a T_COS
    Temperatures[0, :] = t_cos
    # Iterem per la resta de files per calcular la següent iteració temporal
    for i in range(1, len(Temperatures)):
        Temperatures[i] = euler_step_arr(Temperatures[i - 1])

    # Retornem tots els valors per poder graficar els resultats
    return Temperatures


def executa_sequencia_explicit():
    print("Executant Euler Explicit...")
    for q in constants.T_explicit:
        dx = 1 / (constants.N - 1)
        dt = q * dx * dx
        result = euler_explicit(dx, dt)
        guardar_matriu(
            desnormalitza_temperatura(result), f"{settings.fitxer_explicit}_{q}"
        )
    print("Euler Explicit finalitzat")
