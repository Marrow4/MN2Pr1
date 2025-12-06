# Manual d'utilització

## Requisits

- Tenir python 3.13 instal·lat
- Tenir instal·lat el **package manager** `pip`.

## Metodes

### Arxiu .bat o .sh
Hem creat un arxiu .bat i un .sh que es pot executar segons el sistema operatiu que s'utilitzi

Un cop instal·lat tot, es pot executar amb `python main.py`

### Utilitzant UV

- Escriure `pip install uv`
- En la carpeta arrel, crear l'ambient virtual `uv venv .venv`
- `.venv\Scripts\activate`
- `uv run main.py`
Automàticament instal·la les dependències en el document **myproject.toml**

### Utilitzant `pip`

- Obrir una terminal en la carpeta arrel
- Crear l'ambient virtual `python -m venv .venv`
- `.venv\Scripts\activate`
- `pip install requirements.txt`
- `python main.py`

### Modificasions
En el document **config.json** estan tots els paràmetres que es podem variar en el programa,
com pot ser el temps límit, temperatura del cos, entre d'altres.
*No hem comprovat els errors que puguin provocar alteracions d'aquestes variables*,
especialment el temps límit, que augmentarà el temps de creació de les animacions de ~1.5 min fins a + 15 min.

Per retornar als valors per defecte, es pot deixar el document en blanc
