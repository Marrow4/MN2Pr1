import matplotlib.pyplot as plt
import numpy as np
from matplotlib import cm
from matplotlib.animation import FuncAnimation

from heartless.configuracio import constants, settings
from heartless.normalitzacio import desnormalitza_temps


def plot_llista_temps(x, T: np.ndarray, metode: str, ax):
    dim_y, dim_x = T.shape
    # dt en funció del tamany de T
    # Sabem que la t va de 0 a t_a amb intervals uniformes, podem dividir per dim_y per saber dt
    coef_temps = desnormalitza_temps(constants.t_a) / dim_y

    # Generem una llista amb els index de temps que volem plotejar segons la constant `settings.temps_plot`
    temps_mostrar = [
        max(0, min(int(dim_y * q), dim_y - 1)) for q in settings.temps_plot
    ]

    # Per cada index calculat, corresponent a la temperatura en un temps determinat,
    # calculem el temps real (pel label) i representem la seva x i T[i]
    for temps in temps_mostrar:
        temps_label = (
            round(desnormalitza_temps(constants.t_a), 4)
            if (temps == dim_y - 1)
            else round(temps * coef_temps, 4)
        )
        ax.plot(x * 100, T[temps, :], label=f"{metode}; t = {temps_label}", linewidth=2)

    return ax


def configura_grafica(ax) -> None:
    """
    Adapta la grafica en el lloc en el format escollit
    Afegeix:
    - Tick a les dues bandes
    - Grid

    Parametres
    -
    ax : `plt.axes.Axes`
        Gràfica que es vol modificar
        No retorna res perque fa els canvis en la propia grafica, queda modificat la instància de l'objecte
    """

    ax.grid(alpha=0.6)

    ax.tick_params(
        axis="both",
        direction="in",
        right=True,
        top=True,
        bottom=False,
        labeltop=False,
        labelright=False,
    )
    ax.minorticks_on()
    ax.tick_params(
        which="minor",
        direction="in",
        right=True,
        top=True,
        bottom=True,
    )


def configura_limits_teixit(ax):
    """Genera les línies corresponents als marges de:
    - teixit sa-malalt
    - temperatures 50 ºC i 80 ºC

    Parameters
    ----------
    ax : `plt.axis.Axes`
    """
    ax.axvline(0.75, color="blue", linestyle="--", alpha=0.7)
    ax.axvline(1.25, color="blue", linestyle="--", alpha=0.7, label="Límit sa-malalt")
    ax.axhline(y=50, color="red", linestyle="--", alpha=0.7, label=r"T$_{lim}$ sa")
    ax.axhline(
        y=80, color="orange", linestyle="--", alpha=0.7, label=r"T$_{lim}$ malalt"
    )


def mapa_calor(
    matriu,
    eix_x="Posicions [cm]",
    eix_y="Iteracions temps",
    titol="Evolució temporal de la Temperatura",
    metode="",
):
    fig = plt.figure(layout="constrained")
    ax = fig.add_subplot(111)
    # Fem el mapa de calor amb barra de colors
    im = ax.imshow(matriu, cmap="jet", aspect="auto")
    # Agefim el gradient lateral com a 'llegenda'
    fig.colorbar(im, ax=ax)

    ax.set_title(titol + " " + metode)
    ax.set_xlabel(eix_x)
    ax.set_ylabel(eix_y)
    return fig, ax


def create_animation_plot(
    fig,
    ax,
    x,
    T,
    limits: bool = True,
    erase: bool = False,
    title="Gràfica evolució temporal",
    save_name="trace",
):
    # Límits i background per diferenciar teixit sa de malalt
    if limits:
        ax.set_xlim(0 - x.max() * 0.01, x.max() * 1.01)
        ax.set_ylim(T.min() * 0.99, T.max() * 1.01)

        lim_inf = 0.75
        lim_sup = 1.25
        ax.axvspan(-0.1, lim_inf, color="red", alpha=0.3)
        ax.axvspan(lim_sup, x.max() * 2, color="red", alpha=0.3)
        ax.axvspan(lim_inf, lim_sup, color="blue", alpha=0.3)

    mapa_color = cm.get_cmap("jet")

    n_files, _ = T.shape
    # Sabent que t acaba a `t_a` i els increments són uniformes, podem calcular dt com:
    coef_temps = desnormalitza_temps(constants.t_a) / n_files

    # Creem totes les linies que utilitzarem
    linies = [ax.plot([], [], color=mapa_color(i / n_files))[0] for i in range(n_files)]

    # Decidim el nombre de frames de la nostra animació
    frames_creixement = n_files
    frames_estatic = 30
    frames_totals = frames_creixement + frames_estatic

    def update(frames):
        if frames < frames_creixement:
            # En la 1a fase dibuixem una nova linia amb els següents valors
            ax.set_title(f"{title}, temps = {round(frames * coef_temps, 4)}")
            linies[frames].set_data(x, T[frames])
            # Borra la línia anterior per veure'n només l'última
            if frames != 0 and erase:
                linies[frames - 1].set_data([], [])

        # (ho fem només en el 1r frame per accelerar el càlcul)
        elif frames == n_files or frames == n_files + 1:
            # En la 2a fase, dibuixem totes les linies
            ax.set_title(f"{title}, tots els temps")
            for i in range(n_files):
                linies[i].set_data(x, T[i])

        return linies

    ani = FuncAnimation(fig, update, frames=frames_totals, interval=120, blit=True)

    ani.save(settings.grafiques_path + f"/{save_name}.gif", writer="ffmpeg", fps=60)
