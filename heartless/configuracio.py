import json
from dataclasses import dataclass, fields
from typing import Any, Dict


# Definim les constants del problem
@dataclass
class Constants:
    C_V: float = 3686.0
    RHO: float = 1081.0
    K: float = 0.56
    CONDUCTIVITAT: float = 0.472
    L: float = 0.02
    l_mal:float = 0.005
    VOLTATGE: float = 40.0
    T_COS: float = 36.5
    N: int = 101
    t_a: float = 0.025
    T_explicit: tuple[float, ...] = (0.51, 0.49, 0.25)
    T_implicit: tuple[float, ...] = (0.5, 1)
    T_crank: tuple[float, ...] = (0.5, 1)


# Directoris per les dades i gràfiques
@dataclass
class Settings:
    dades_path: str = "dades"
    grafiques_path: str = "grafiques"
    fitxer_explicit: str = "explicit"
    fitxer_implicit: str = "implicit"
    fitxer_crank: str = "crank"
    temps_plot: tuple[float, ...] = (1.0,)
    show_grafiques: bool = True


# Funció per carregar la configuració des del JSON
def carrega_configuracio(json_path: str) -> tuple[Settings, Constants]:
    """Carrega les variables des del JSON als objectes `Settings` i `Constants

    Parameters
    ----------
    json_path : str
        Directory sencer del JSON

    Returns
    -------
    tuple[Settings,Constants]
    """
    # Carreguem el JSON a un diccionary, si no està utilitzem un diccionari buit
    try:
        with open(json_path, "r") as f:
            config_data = json.load(f)
    except FileNotFoundError:
        print(
            f"⚠️ Warning: directory no trobat '{json_path}'.\nUtilitzant valors per defecte."
        )
        config_data = {}

    diccionari_Settings: Dict[str, Any] = {}

    # Per cada "field" (camp) de `Settings` mirem si estava en el JSON i agafem el seu valor
    # Si no estava, utilitzarem el valor per defecte
    for camp in fields(Settings):
        nom_camp = camp.name

        if nom_camp in config_data:
            diccionari_Settings[nom_camp] = config_data[nom_camp]
        else:
            diccionari_Settings[nom_camp] = camp.default

    diccionari_constants: Dict[str, Any] = {}

    # El mateix procediment de `Settings` el fem per `Constants`
    for camp in fields(Constants):
        nom_camp = camp.name

        if nom_camp in config_data:
            diccionari_constants[nom_camp] = config_data[nom_camp]
        else:
            diccionari_constants[nom_camp] = camp.default

    # Els diccionaris generen les classes
    return Settings(**diccionari_Settings), Constants(**diccionari_constants)


settings, constants = carrega_configuracio("config.json")
