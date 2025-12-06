import matplotlib.pyplot as plt
import numpy as np

from heartless.analitica import fxt_t_determinat
from heartless.configuracio import constants, settings
from heartless.crank import crank_nicolson, executa_sequencia_crank_nicolson
from heartless.explicit import euler_explicit, executa_sequencia_explicit
from heartless.grafiques import (
    configura_grafica,
    configura_limits_teixit,
    create_animation_plot,
    mapa_calor,
    plot_llista_temps,
)
from heartless.implicit import euler_implicit, executa_sequencia_implicit
from heartless.normalitzacio import (
    desnormalitza_temperatura,
    desnormalitza_temps,
    normalitza_temps,
)
from heartless.utils import (
    carregar_posicions_temperatures,
    error_relatiu,
    guarda_figura,
    troba_maxima_iter_temps,
)

plt.rcParams.update({"figure.figsize":(6,4)})

def calcula_tots_metodes():
    # Calculem tots els mètodes per totes les dt
    executa_sequencia_explicit()
    executa_sequencia_implicit()
    executa_sequencia_crank_nicolson()


def grafiques_crank():
    # Fem les grafiques corresponents al mètode de Crank-Nicolson
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Posicions [m]")
    ax.set_ylabel("Temperatura [ºC]")
    ax.set_title("Comparació de Crank-Nicolson per diferents $\\Delta$t")

    # Per tal que totes les grafiques siguin semblants, tenim unes funcions que apliquen certs formats
    configura_grafica(ax)
    configura_limits_teixit(ax)

    # Calculem la funció analítica a
    x, T = fxt_t_determinat(constants.t_a)

    # Passem x de metres a cm per visualitzar més clarament
    ax.plot(x * 100, T, label="Funció analítica")

    # Per cada dt diferent, llegim l'arxiu encarregat i fem la representació
    for item in constants.T_crank:
        x, T_c = carregar_posicions_temperatures(f"{settings.fitxer_crank}_{item}")
        plot_llista_temps(x, T_c, f"$\\Delta$t = {item}$\\Delta$x", ax)
    ax.legend()
    guarda_figura(fig, "crank")


def grafiques_explicit():
    # El mateix que hem fet amb Crank-Nicolson ho executem amb Euler Explícit
    # A diferència de Crank-Nicolson, aquí separem en dues gràfiques:
    # aquells dt que convergeixen respecte els que divergeixen
    fig1 = plt.figure()
    fig2 = plt.figure()
    ax1 = fig1.add_subplot(111)
    ax2 = fig2.add_subplot(111)
    ax1.set_xlabel("Posicions [m]")
    ax1.set_ylabel("Temperatura [ºC]")
    ax1.set_title("Comparació de Euler Explícit per diferents $\\Delta$t")
    configura_grafica(ax1)
    configura_limits_teixit(ax1)

    configura_grafica(ax2)
    configura_limits_teixit(ax2)
    ax2.set_xlabel("Posicions [m]")
    ax2.set_ylabel("Temperatura [ºC]")
    ax2.set_title("Comparació de Euler Explícit per diferents $\\Delta$t (divergents)")
    x, T = fxt_t_determinat(constants.t_a)
    ax1.plot(x * 100, T, label="Funció analítica")

    for item in constants.T_explicit:
        x, T_c = carregar_posicions_temperatures(f"{settings.fitxer_explicit}_{item}")
        # Convergiran quan dt < 0.5 * dx**2
        if item < 0.5:
            plot_llista_temps(x, T_c, f"$\\Delta$t = {item}$\\Delta$x", ax1)
        else:
            plot_llista_temps(x, T_c, f"$\\Delta$t = {item}$\\Delta$x", ax2)
    ax1.legend()
    ax2.legend(loc='lower center')
    guarda_figura(fig1, "explicit-convergent")
    guarda_figura(fig2, "explicit-divergent")

def grafiques_implicit():
    # Igual que amb els mètodes anteriors, fem la representació per cada valor de dt
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Posicions [m]")
    ax.set_ylabel("Temperatura [ºC]")
    ax.set_title("Comparació de Euler Implícit per diferents $\\Delta$t")
    configura_grafica(ax)
    configura_limits_teixit(ax)
    x, T = fxt_t_determinat(constants.t_a)
    ax.plot(x * 100, T, label="Funció analítica")
    for item in constants.T_implicit:
        x, T_c = carregar_posicions_temperatures(f"{settings.fitxer_implicit}_{item}")
        plot_llista_temps(x, T_c, f"$\\Delta$t = {item}$\\Delta$x", ax)
    ax.legend()
    guarda_figura(fig, "implicit")


def grafiques_conjunt():
    # Finalment fem una gràfica conjunta de tots els mètodes,
    # utilitzant el dt més petit de cada mètode
    c_petit = min(constants.T_crank)
    e_petit = min(constants.T_explicit)
    i_petit = min(constants.T_implicit)
    fig = plt.figure()
    ax = fig.add_subplot(111)
    ax.set_xlabel("Posicions [m]")
    ax.set_ylabel("Temperatura [ºC]")
    ax.set_title("Comparació de tots els metodes per $\\Delta$t menor")
    configura_grafica(ax)
    configura_limits_teixit(ax)
    x, T_e = carregar_posicions_temperatures(f"{settings.fitxer_explicit}_{e_petit}")
    plot_llista_temps(x, T_e, "Explicit", ax)
    x, T_i = carregar_posicions_temperatures(f"{settings.fitxer_implicit}_{i_petit}")
    plot_llista_temps(x, T_i, "Implicit", ax)
    x, T_c = carregar_posicions_temperatures(f"{settings.fitxer_crank}_{c_petit}")
    plot_llista_temps(x, T_c, "Crank-Nicolson", ax)
    x, T = fxt_t_determinat(constants.t_a)
    ax.plot(x * 100, T, label="Funció analítica")
    ax.legend()
    guarda_figura(fig, "conjunt")


def grafiques_errors():
    # Fem una gràfica dels errors relatius de cada mètode respecte el valor teòric
    # Només de les solucions que convergeixin

    fig2,ax = plt.subplots(1,1)
    configura_grafica(ax)
    x, T_a = fxt_t_determinat(constants.t_a)
    ax.set_xlabel("Posicions [cm]")
    ax.set_ylabel("Error relatiu (sobre 1)")
    ax.set_title("Comparació d'errors del mètode")
    
    llista_metodes = ("Euler Explícit","Euler Implícit","Crank-Nicolson")
    llista_fitxers = (settings.fitxer_explicit,settings.fitxer_implicit,settings.fitxer_crank)
    llista_valors_q = ((q for q in constants.T_explicit if q < 0.5),constants.T_implicit,constants.T_crank)
    for i in range(len(llista_metodes)):
        fig,ax = plt.subplots(1,1)
        ax.set_xlabel("Posicions [cm]")
        ax.set_ylabel("Error relatiu (sobre 1)")
        ax.set_title(f"Comparació d'errors del mètode {llista_metodes[i]}")
        configura_grafica(ax)
        for q in llista_valors_q[i]:
            x, T_c = carregar_posicions_temperatures(f"{llista_fitxers[i]}_{q}")
            err_c = error_relatiu(T_c[-1], T_a)
            ax.plot(x * 100, err_c, label=f"$\\Delta$t = {q}($\\Delta$x)$^{{2}}$")
        ax.legend()
        guarda_figura(fig,f'error-{llista_metodes[i]}')


def grafiques_animades():
    # Aquí farem les animacions respecte el temps de:
    # - l'error relatiu
    # - l'increment de temperatura
    if False:
        fig2 = plt.figure()
        ax2 = fig2.add_subplot(111)
        ax2.set_xlim(0, constants.L*100)
        configura_grafica(ax2)
        print("Començant animació, tarda aproximadament 1 min 30 s")

        x, T = carregar_posicions_temperatures(
            f"{settings.fitxer_explicit}_{min(constants.T_explicit)}"
        )
        dx = 1/(constants.N-1)
        dt = dx*dx * min(constants.T_explicit)
        T = euler_explicit(dx,dt)
        T = desnormalitza_temperatura(T[[i for i in range(len(T)) if i % 4 == 0]])
        dt = dt*4

        T_analitiques = []
        for i in range(len(T)):
            _, t_an = fxt_t_determinat(i * dt)
            T_analitiques.append(error_relatiu(T[i],t_an))
        T_err = np.array(T_analitiques)
        # ax2.set_ylim(0,min(T_err[:-1].max()*1.01,0.006))
        create_animation_plot(
            fig2,
            ax2,
            x * 100,
            T_err,
            erase=True,
            limits=False,
            save_name="errors",
        )

    fig2 = plt.figure()
    ax2 = fig2.add_subplot(111)
    ax2.set_xlabel("Posició [cm]")
    ax2.set_ylabel("Temperatura [ºC]")
    configura_grafica(ax2)
    configura_limits_teixit(ax2)

    print("Començant animació, tarda aproximadament 1 min 30 s")
    x, T = carregar_posicions_temperatures(
        f"{settings.fitxer_implicit}_{min(constants.T_implicit)}"
    )
    create_animation_plot(fig2, ax2, x * 100, T, save_name="implicit")


def troba_limit_conjunt_metodes():
    # Trobem el límit de temps que podem aplicar el tractament segons cada mètode
    print("---- Temps màxim que compleix les condicions imposades ----")
    T_COS = 36


    # Obtenim la matriu de temperatures calculada amb el mètode explicit amb dt menor
    dx = 1/(constants.N-1)
    dt = dx * dx * min(constants.T_explicit)
    T_ds = euler_explicit(dx,dt,T_COS)
    T = desnormalitza_temperatura(T_ds)
    # Obtenim l'última fila que compleix les condicions
    i, _ = troba_maxima_iter_temps(T)
    # Transformem d'índex a temps desnormalitzat utilitzant dt = q * dx**2
    result = desnormalitza_temps(i * (1 / constants.N) ** 2 * min(constants.T_explicit))
    print("Temps Euler Explícit:", result)

    # Repetim el procediment del metode explícit per l'implícit
    dt = dx * dx * min(constants.T_implicit)
    T_ds = euler_implicit(dx,dt,T_COS)
    T = desnormalitza_temperatura(T_ds)
    # _, T = carregar_posicions_temperatures(
    #     f"{settings.fitxer_implicit}_{min(constants.T_implicit)}"
    # )
    i, _ = troba_maxima_iter_temps(T)
    result = desnormalitza_temps(i * (1 / constants.N) ** 2 * min(constants.T_implicit))
    print("Temps Euler Implícit:", result)

    # Repetim el procediment del metode explícit per Crank-Nicolson
    dt = dx * dx * min(constants.T_crank)
    T_ds = crank_nicolson(dx,dt,T_COS)
    T = desnormalitza_temperatura(T_ds)
    i, _ = troba_maxima_iter_temps(T)
    result = desnormalitza_temps(i * (1 / constants.N) ** 2 * min(constants.T_crank))
    print("Temps Crank-Nicolson:", result)
    res_nom = normalitza_temps(result)
    pos_temps = np.linspace(res_nom*0.95,res_nom*1.05,200)
    index = -1
    for t in pos_temps:
        _,T_res = fxt_t_determinat(t)
        _,index = troba_maxima_iter_temps(T_res)
        if index != -1:
            print("Temps analític:      ",desnormalitza_temps(t))
            break
    if index == -1:
        print("La solució analítica divergeix tant de la numèrica que no és un bon mètode")
        



def main():
    print("Començant simulació!")
    calcula_tots_metodes()

    troba_limit_conjunt_metodes()

    grafiques_explicit()
    grafiques_implicit()
    grafiques_crank()

    grafiques_conjunt()

    grafiques_errors()

    x, T = carregar_posicions_temperatures(
        f"{settings.fitxer_explicit}_{min(constants.T_explicit)}"
    )
    fig_h, ax_h = mapa_calor(T, metode="Implícit")
    guarda_figura(fig_h, "mapa-calor")

    if settings.show_grafiques:
        plt.show()

    grafiques_animades()

    if settings.show_grafiques:
        plt.show()

    print("Simulació finalitzada correctament!!!")


if __name__ == "__main__":
    main()
