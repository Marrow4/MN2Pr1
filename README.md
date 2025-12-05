# MNAlgoritmes

He pensat que podem implementar de forma independent, els algoritmes fets a classe, per millorar programant i si en les entregues necessitem aquests algoritmes, podem venir a aquest repositori i copiar el codi que ja haurem fet.

Tinc la intenció de fer un fitxer amb el format del problema per tal que vosaltres el copieu i feu la vostra versió de l'algoritme per penjar-la al GitHub, així també podem mirar el codi dels altres i veure què podem millorar o a qui se li donen millor certes parts.

Per resoldre un problema, creeu una branca amb el vostre nom, solucioneu-lo al vostre ordinador i si voleu publiqueu la solució.

## No dubteu en preguntar

# Manual d'utilització

## Requisits

- Tenir python 3.13 instal·lat
- Tenir instal·lat el **package manager** `pip`.

## Metodes

Si confieu en nosaltres, hem creat un bash script que automatitza el
procés de descàrrega dels móduls i creació de l'ambient virtual,
depenent del vostre sistema operatiu executeu l'arxiu `start.sh` o `start.

Recomanem utilitzar el **package manager** `uv` que es pot instal·lar
amb `pip` seguint [aquest procediment](#utilitzant-uv) ja que descarrega
automàticament els paquets necessaris abans d'executar el programa i
garantitza l'utilització d'un ambient virtual on les condicions són reproducibles

Sinó, alternativament es poden instal·lar els paquets manualment amb [aquest pas](#utilitzant-pip)

### Arxiu de terminal

- Executant un cop l'arxiu de terminal instal·la totes les
  dependències i crea l'ambient virtual
- Per executar el codi mes cops posar `uv run main.py`

### Utilitzant UV

- Escriure `pip install uv`
- En la carpeta arrel, crear l'ambient virtual `uv venv .venv`
- `.venv\Scripts\activate`
- `uv run main.py`

### Utilitzant `pip`

- Obrir una terminal en la carpeta arrel
- Crear l'ambient virtual `python -m venv .venv`
- `pip install requirements.txt`
- `python main.py`

### Arguments de l'usuari

(Espai per especificar si ha d'entrar algun argument, ej. Temperatura)
(La intenció es fer una interfaç bonica)

## Informació important

S'ha d'utilitzar float64 perquè l'increment de dt és massa petit, quan
creeu l'array, s'ha de posar `np.array([],dtype=np.float64)`