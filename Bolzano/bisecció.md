# Mètode

En aquest document he posat una serie de problemes de creixent dificultat sobre el **Metode de bisecció**, tot i que també podria servir per la majoria de problemes de l'estil *Bolzano*. Us recomano que feu **Inicial** i **Avançat** de la majoria de mètodes i si teniu ganes proveu de fer l'*Expert* d'un dels algoritmes.

# Inicial
Desenvolupa un fitxer de Python que apliqui el mètode de la bisecció on es puguin personalitzar els paràmetres i la funció (sempre que compleixi les condicions), per exemple:
```python
presició = 1e-3
a = 0
b = 10

def funcio_a_optimitzar(x)
    return np.e^x - 3 * x
```

S'ha d'imprimir per pantalla el resultat final; com a extra, també es pot imprimir el nombre total d'iteracions realitzades.

**Recomanació**: Fes funcions auxiliars per ajudar-te a calcular l'error i punt mig.

*Recorda*: Si has d'executar la mateixa funció multiples vegades (amb les mateixes variables) guarda-ho en una variable. Aixo és per quan aquesta operació sigui molt complexa computacionalment.

## Ajudes
<details>
<summary>Ajuda 1</summary>
<br>
Fes un esquema/diagrama per saber les accions i càlculs que has de fer (bucles i condicionals).
</details>

<details>
<summary>Ajuda 2</summary>
<br>
Per fer l'algoritme has de fer alguna iterció (bucle)? De quin tipus? Quina condició s'ha de complir per sortir del bucle?
</details>


<details>
<summary>Ajuda 3</summary>
<br>
Que vol dir presició en aquest algoritme? Sense infinites iteracions, hem de considerar que f(x) està suficientment aprop de 0.
</details>

# Avançat
Fer l'algoritme dins d'una funció que es pugui cridar des de altres fitxers i accepti els paràmetres:
* Funció a optimitzar
* a,b inicials (a<b)
* Presició

Ha de retornar el valor final trobat c, opcionalment, la quantitat d'iteracions realitzades.

# Expert

Fes una funció que resolgui l'algoritme, pero els únics paràmetres que accepta són:
* Funció a optimitzar (dona per suposat que compleix les condicions)
* Presició (amb un valor per defecte)
Has de trobar tots els possibles punts c que facin f(c) = 0.

<details>
<summary>Ajuda 4</summary>
<br>
Per trobar els punts:

$$a,b \; | \; f(a)<0 \; \& \; f(b)>0$$

Agafeu un interval de valors i avanceu en pasos del mateix tamany fins trobar aquests punts


</details>

*Opcional*: Substitueix el `while` per un `for` (és més eficient)

*Opcional*: Afegir un altre argument a la funció `guess` com a punt inicial i trobar el 0 més proper a aquest punt

*Opcional*: Afegir `type hints` i comprovar que tots els arguments, són del tipus que haurien de ser, en cas de no ser-ho, llançar un error.

