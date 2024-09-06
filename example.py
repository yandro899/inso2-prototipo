# Importa las librerias de tkinter.
# La primera linea es el general y la segunda son mas opciones
from tkinter import *
from tkinter import ttk

def calculate(*args):
    """
    Funcion que hace el calculo de los pies a metros. *args es solo un parametro de relleno, por ahora.
    """
    try:
        value = float(feet.get()) # Se obtiene el valor de "feet", que es la variable StringVar() que toma el dato
        meters.set(int(0.3048 * value * 10000.0 + 0.5)/10000.0) # El resultado del calculo lo muestra en el otro StringVar() "meters"
    except ValueError:
        # Si ingresaste un caracter por chistoso, no hace el calculo.
        pass

# Crea la ventana y le asigna el nombre
root = Tk()
root.title("Feet to Meters")

"""
Frame es una clase en donde se puede alojar varios objetos de manera ordenada
Se divide en columnas y filas.
En general al crear un objeto, se pone como primer parametro la referencia al
objto padre (en este caso de la linea siguiente, el objeto padre es "root" que es la ventana
de la interfaz). El otro parametro es el padding (funciona muy parecido al padding de CSS).
Lean manga de gatos, no soy una enciclopedia.
"""
mainframe = ttk.Frame(root, padding="3 3 12 12")
"""
El grid creado se ingresa dentro de la ventana "root" en la columna y fila 0 (el origen pues).
El parametro sticky sirve para decirle al objeto que se "pegue" a las "paredes" de su grid.
Se indica como los puntos cardinales Norte, Oeste, Este y Sur respectivamente. En este caso se 
adhiere alrededor de la ventana "root".
"""
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
# Las siguientes dos lineas no entiendo exactamente que hacem, pero al borrarlas no cambia la ventana.
root.columnconfigure(0, weight=1)
root.rowconfigure(0, weight=1)

"""
StringVar() es una clase que sirve para poner textos dinamicos en la ventana,
como para tomar un tento de una entrada de texto (que es Entry()).
Primero crea esta clase StringVar(); despues crea Entry() con:
 * Primer parametro: el objeto padre, en este caso el Frame "mainframe".
 * Segundo parametro: ancho, muy explicativo.
 * Tercer parametro: el objeto StringVar() que va a leer el dato.
 Al ultimo, posiciona el objeto Entry() recien creado en la columna 2 y fila 1, pegado a los laterales.
"""
feet = StringVar()
feet_entry = ttk.Entry(mainframe, width=7, textvariable=feet)
feet_entry.grid(column=2, row=1, sticky=(W, E))

"""
Parecido al anterior, se instancia StringVar() como "meters" pero esta vez para mostrar en pantalla el resultado.
Despues, crea el Label() (que es texto simple) donde asigna al objeto padre y a la variable "meters".
Luego se la ubica con grid, como se vio antes (col 2, fila 2, pegada a los laterales).
"""
meters = StringVar()
ttk.Label(mainframe, textvariable=meters).grid(column=2, row=2, sticky=(W, E))

"""
Se instancia Button(), que es un boton. El argumento "text" es el texto que llevaria el boton, 
y "command" es la funcion que se va a ejecutar al presionar el boton que ya debe ser definida con anterioridad
(revisar la funcion "calculate" mas arriba). Se la ubica con "grid".
"""
ttk.Button(mainframe, text="Calculate", command=calculate).grid(column=3, row=3, sticky=W)

# Se agregan textos simples Label()
ttk.Label(mainframe, text="feet").grid(column=3, row=1, sticky=W)
ttk.Label(mainframe, text="is equivalent to").grid(column=1, row=2, sticky=E)
ttk.Label(mainframe, text="meters").grid(column=3, row=2, sticky=W)

# Esto solo hace que todos los objetos del Frame tengan espacios entre si de 5px.
# Es para que no se vean pegados en las columnas.
for child in mainframe.winfo_children(): 
    child.grid_configure(padx=5, pady=5)

# Esto enfoca el cursor en el Entry().
feet_entry.focus()
# Esto solo indica al programa que al presionar Enter se ejecute "calculate".
root.bind("<Return>", calculate)

"""
esta funcion es importante para que se muestre todo en pantalla.
Lo que hace es un loop infinito para mostrar todo en pantalla hasta que el usuario cierre
la ventana. Aun estoy viendo como podemos cortar esta ventana con botones, pero debe ser facil.
"""
root.mainloop()