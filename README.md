# CleanGrammar

## Introducción
Una gramática libre de contexto(GLC), es un cierto tipo de gramática formal, es decir un conjunto de reglas de producción que describen todas las cadenas posibles en un lenguaje formal determinado. En las GLC, todas las reglas son de uno a uno, de uno a muchos o de uno a ninguno, estas reglas pueden aplicarse independientemente del contexto, al crear una GLC se pueden cometer errores que no facilitan la generación de cadenas, alguno de estos errores son: 
- 1.Uso de ε en reglas que no son la raíz, ejemplo:  
S➜aBa B➜ε|b Esto se puede sustituir por: S➜aBa|aa B➜b
- 2.Reglas unitarias, ejemplo:  
S➜a|B B➜b|c Esto se puede sustituir por: S➜a|b|c
- 3.Reglas inútiles o no generativas, ejemplo:  
S➜aDB|aB B➜b|c Esto se sustituye por: S➜aB B➜b|c Esto es posible ya que no existe una regla “D” que genere cadenas, otro ejemplo es la eliminación de bucles: S➜a|aB B➜aB Esto queda como: S➜a
- 4.Reglas inalcanzables, ejemplo:  
S➜a B➜aB Esto se sustituye por: S➜a 


Para asegurarnos que nuestra GLC no está sucia debemos verificar los puntos anteriores y de ser necesario limpiarla siguiendo cada uno de los pasos en forma de “jerarquía” para poder limpiar la gramática. 
## Planteamiento del problema
Se pide realizar un programa que dada una GLC (por medio del teclado o desde un archivo) la limpie de: 
1. Producciones vacías 
2. Producciones unitarias 
3. Inútiles, no generativas 
4. Inaccesibles 

## Diseño de la solución
Para solucionar el problema se crearán dos clases llamadas “Gramática” y “Regla” (están dentro GLC.py), estas nos permitirán organizar la información para posteriormente hacer distintas operaciones, el diagrama de clases queda de la siguiente forma:  
Dentro de la clase Gramática se tendrá un diccionario que nos ayudará a organizar la información, por cada regla en la gramática se creará una llave para el diccionario y dentro un objeto de tipo Regla. Una vez creada la gramática con las reglas, si mostramos el objeto gramática se mostrará básicamente como están organizadas nuestras
```python
>>> from GLC import Gramatica  
>>> g = Gramatica() 
#Creamos el objeto de tipo Gramatica 
>>> g.insert("S","aSb","","B") 
#Insertamos la regla S 
>>> g.insert("B","a","b") 
#Insertamos la regla B 
>>> g #Llamamos a la gramática g S->aSb|λ|B B->a|b 
```
Las gramáticas tienen un método llamado clear, el cual manda a llamar a otros métodos privados que se encargaran de limpiar la GLC paso por paso, estos métodos son: 
- **__clearEpsilon** Este método funciona de la siguiente manera  
 1. Buscamos las reglas de la gramática que contengan λ (nuestro símbolo vacío) y las guardamos en un arreglo(No buscamos en la raíz), para esto iteramos cada una de las reglas de nuestra gramática y usamos el método “search” de regla para buscar un símbolo.  
 2.Ya que tenemos nuestras reglas que contienen λ, iteramos el arreglo de vacías y en una segunda iteración analizamos cada regla para ver si contienen la regla que produce λ.  
 3.Si encontramos que un símbolo de la regla “r” contiene el símbolo de una regla “r2” que produce λ, entonces obtenemos todas las combinaciones en las que se sustituye el símbolo de “r2” por λ en cada uno de los símbolos de “r” y las insertamos en la regla “r”, posterior a esto eliminamos el símbolo λ de la regla r2.  
 4.Este método se vuelve recursivo, ya que el símbolo λ se puede heredar de alguna otra regla.  
 5.El método acaba cuando ya no hay reglas que contengan λ y que no estén en la raíz.  
- **__clearUnitarias** Este método funciona de la siguiente manera  
 1.Por cada regla en la gramática se va a buscar símbolos que contengan letras unitarias mayúsculas, para esto usaremos el método “searchByregex” (de la clase Regla).  
 2.Si encontramos el símbolo unitario “u” en la regla “r”, obtendremos los símbolos de la regla “u” y los insertamos en la regla “r”.  
 3.Este método también es recursivo por que al sustituir reglas, están pueden heredar un símbolo unitario.  
 4.Este método acaba cuando no haya símbolos unitarios en ninguna regla.
- **__clearInutiles** Este método funciona de la siguiente manera:  
 1.Se iteran las reglas “r” de la gramática (menos la raiz), en una segunda iteración de cada regla “r2” de la gramática se busca la regla “r” en “r2”.  
 2.Si la regla “r” es igual a la regla “r2” se sigue iterando, en caso contrario, si la regla “r” se encuentra en la regla “r2” se considera que la regla “r” no es inútil.  
 3.Si la regla “r” no se encuentra en ninguna regla “r2” entonces esta regla se considera inútil.  
 4.Las reglas inútiles se eliminan de la gramática, ya que ninguna otra regla las utiliza.
 - **__clearNoGenerativas** Este método funciona de la siguiente manera:  
 1.Se busca en cada una de las reglas “r” que contenga símbolos que no la contengan a la misma, esto para no generar bucles infinitos.  
 2.Si se no se encuentra al menos una regla en “r” que no contenga a “r” esta regla se vuelve no generativa.  
 3.Si la regla se vuelve no generativa, se borra de cada una de las reglas de la gramática.  
 4.Este método es recursivo, por que se pueden generar cadenas vacías al eliminar las no iterativas, creando nuevas reglas no generativas.
 - **__clearMuertas** Este método funciona de la siguiente manera:  
  1.Se iteran todas las reglas y se obtienen los distintos simbolos mayusculas que los componen(las reglas de nuestra gramática).  
  2.Por cada letra mayúscula distinta de la gramática se revisa si tiene una regla asociada.  
  3.Si no hay una regla asociada a una letra “l”, se elimina todos los símbolos de la gramática que contengan a “l”.

## Bibliografía 
- Hopcroft John E., Jeffrey D. Ullman.(2008). Introducción a la Teoría de autómatas, lenguajes y computación. Recuperado de http://www.eafranco.com/docencia/teoriacomputacional/files/books/TeoriaDeAutomatas,lenguajesYComputacion-Hopcroft.pdf
