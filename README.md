# Prototipo SIGEAD para Ingenieria de Software II
## Diagrama de clases
![Diagrama de clases](https://github.com/yandro899/inso2-prototipo/blob/main/diag_clases.png)
## Explicación breve de las reglas de programacion a seguir (ideal).
* Al crear clases, los atributos que deben ser leidos deben ser accedidos usando @property (concepto de propiedad en POO), ademas de instanciarse con "__".
```@property
    def Dni(self):
        """DNI del usuario"""
        return self.__dni
```
* Cada ventana se crearia en un archivo aparte.
* Version de Python que yo uso es 3.9
* Al crear metodos o funciones, especificar cuál es su salida, agregar una descripcion de lo que hace y los tipos de dato de los argumentos.
` def BuscarUsuarioPorDNI(self, dni: str) -> Usuario | None:`
* Preparense para llorar
* Usar PascalCase para las funciones y SnakeCase para las variables (discutible, veamos en https://builtin.com/articles/pascal-case-vs-camel-case)
* Repasemos los diagramas de clase xd (https://blog.visual-paradigm.com/es/what-are-the-six-types-of-relationships-in-uml-class-diagrams/)
* "Tutoriales" Libreria TKinter [aqui](https://realpython.com/python-gui-tkinter/#making-your-applications-interactive) y [aqui](https://tkdocs.com/pyref/)
* ¿Usamos una DB o JSON como el prototipo del año pasado?
* No se formatear readmes [ayuda](https://github.com/jfasebook/SoyInformatico/blob/master/README.md)
