'''
Programa: GLC v1.1
Autor: Reyes Vilchis Juan Jose
Grupo: 2CM11
'''
import re
'''
Clase Regla que nos va a ayudar a agrupar 1 sola regla
para una gramática.Ejemplo de uso:
>>>r = Regla("S")
>>>r = Regla("S","λ")
>>>r.insert("a")
>>>r.insert("aSb","b")
>>>r.insert("") # Simbolo vacio :o
>>>r
S->a|aSb|b|λ
'''
class Regla():
    def __init__(self,id,vacio="λ"): #Podemos establecer cual puede ser el caracter vacio
        self.id = id #Se compone de id 
        self.simbolos = [] #Un arreglo para los simbolos
        self.vacio = vacio #El caracter vacio
    def insert(self,*simbolo): #Este metodo permite agregar 1 o más simbolos
        for s in simbolo:
            if type(s)!=str: #Solo se aceptan caracteres
                print("Solo acepto caracteres!")
                return
            if s == "": #Si vamos a meter el caracter vacio se reemplaza por el nuestro
                s = self.vacio
            if s in self.simbolos:#Si queremos insertar un simbolo que ya esta
                pass#en nuestro arreglo no lo insertamos
            else:
                self.simbolos.append(s)#En caso contrario lo insertamos.
    def search(self,simbolo):#Metodo para buscar un simbolo
        if simbolo=="":
            simbolo = self.vacio
        return simbolo in self.simbolos
    def searchByRegex(self,regex):#Metodo para busqueda "inteligente" usando expresiones regulares
        r = re.compile(regex)
        resultado = list(filter(r.findall,self.simbolos))
        return resultado #devuelve un arreglo con las coincidencias
    def remove(self,simbolo):#Funcion para borrar algun simbolo
        if simbolo == "":#Si el simbolo es el caracter vacio lo reemplazamos
            simbolo = self.vacio#por nuestro propio caracter
        try:
            self.simbolos.remove(simbolo)#Si no existe, simplemente no lo borramos
        except:pass
    def removeContain(self,simbolo):#Metodo que ayuda a borrar todos los simbolos
        arr_remove = [] #que contengan otro simbolo dado :o
        for s in self.simbolos:
            if simbolo in s:
                arr_remove.append(s)
        for r in arr_remove:
            self.simbolos.remove(r)
    '''El metodo replace ya no lo ocupo para limpiar epsilon, ya que este solo quitaba
    1 por 1 las letras, yo necesitaba todas las combinaciones, lo dejo por que quiza
    sea de utilidad despues.'''
    def replace(self,simbolo,rep): #metodo para reemplazar un simbolo por otro
        for s in self.simbolos:#si la cadena resultane es el caracter vacio
            if s.replace(simbolo,rep,1)=="":
                self.insert("")#lo insertamos
            else:
                self.insert(s.replace(simbolo,rep,1))#Solo reemplazamos 1 caracter
    '''Metodo para obtener todas las reglas (Letras mayusculas) de nuestros simbolos, para
    ello nos apoyamos de las expresion regular.'''
    def getReglas(self,arr):#Debe recibir de parametro un arreglo para que funcione
        for s in self.simbolos:#Ya que así ahorra mas memoria y no inserta caracteres
        #ya existentes en el arreglo
            simbolos = list(filter(re.compile(r"[A-Z]").match,s))
            for s2 in simbolos:
                if s2 in arr:pass
                else:arr.append(s2)
    '''Metodo que ayuda a obtener todas las combinaciones usando numeros binarios
    Basicamente de una cadena, por ejemplo AaA, si se quieren obtener las combinaciones
    que se pueden hacer reemplazando la letra A por el caracter vacio, contaremos desde
    0-2^caracteres_a_reemplazar.
    Entonces contaremos del 0 al 2^2
    nos genera en binario los numeros:
    * 00 = ""
    * 01 = "A"
    * 10 = "A"
    * 11 = "AA"
    si reemplazamos estos caracteres en nuestra cadena original "AaA" iterando los valores
    de "prendido" y "apagado" del caracter, nos resultará algo como:
    ["AaA","a","aA","Aa"]
    '''
    def getCombinaciones(self,simbolo):
        combinaciones = [] #arreglo para las combinaciones
        for cadena in self.simbolos:
            if simbolo in cadena:
                cadena = cadena.replace(simbolo,"%s") #Reemplazamos el caracter por "%s"
                count = cadena.count("%s")#Contamos el numero de veces que aparece
                for i in range(2**count):#contamos de 0 al 2^(caracteres a  reemplazar)
                    lista = list(format(i,"0%db"%count))#Lista de caracteres prendidos y apagados
                    temp_lista = []
                    for l in lista:
                        if "0" in l:#Reemplazaremos los caracteres 0 por vacios
                            temp_lista.append("")
                        else:
                            temp_lista.append(simbolo) # Los caracteres 1 por el simbolo a combinar
                    temp = cadena%tuple(temp_lista)#Reemplazamos los %s por caracteres "" o "simbolo"
                    combinaciones.append(temp)#Agregamos la combinacion a  un arreglo
        return combinaciones#Devolvemos el arreglo
    #Forma de representar la regla cuando se manda a llamar
    def __repr__(self):
        return ''.join((self.id,"->",'|'.join(map(str, self.simbolos))))
    def __str__(self):
        return ''.join((self.id,"->",'|'.join(map(str, self.simbolos))))
    #getters
    def getId(self):
        return self.id
    def getSimbolos(self):
        return self.simbolos
'''
Clase Gramatica que nos va a ayudar a agrupar multiples reglas
para una gramática, Ejemplo de uso:
g.insert(Id,*reglas)
>>>g = Gramatica()
>>>g.insert("S","aSb","","aA")
>>>g
S->aSb|λ|aA
>>>g.insert("A","b")
>>>g
S->aSb|λ|aA
A->b
'''
class Gramatica():
    def __init__(self):
        self.reglas = {}#Diccionario que contendra nuestras reglas
    def insert(self,r,*simbolos):#El metodo insert nos permite agregar gramaticas
        if r in self.reglas:#si ya existe la regla solo insertamos simbolos
            self.reglas[r].insert(*simbolos)
        else:#Si no existe creamos la regla
            self.reglas[r] = Regla(r)
            self.reglas[r].insert(*simbolos)
    def __clearEpsilon(self):
        vacio = [] #reglas con epsilon
        iteregla = iter(self.reglas)
        next(iteregla)#Iterador que se salta la raiz
        for r in iteregla:
            if self.reglas[r].search(""):#Si encontramos el caracter vacio
                vacio.append(r)#Lo agregamos al arreglo de vacios
        for v in vacio:#Por cada arreglo en vacios
            self.reglas[v].remove("")#Vamos a quitar el vacio de sus simbolos
            for r in self.reglas:#Por cada se obtendran las combinaciones
                comb = self.reglas[r].getCombinaciones(v)
                self.reglas[r].insert(*comb)#Se insertaran a la propia regla
        if not vacio:
            return
        self.__clearEpsilon()#Se hará recursivo por si genera otras reglas con el caracter vacio
    def __clearUnitarias(self):
        for r in self.reglas:#Por cada regla buscaremos si hay unitarias
            unitarias = self.reglas[r].searchByRegex(r"^[A-Z]{1}$")
            for u in unitarias:#Por cada unitaria que encontremos
                self.reglas[r].remove(u)#Vamos a eliminar su unitaria
                for r2 in self.reglas[u].getSimbolos():#Reemplazaremos por cada caracter
                    self.reglas[r].insert(r2)#De la regla unitaria
                if not unitarias:
                    break
                self.__clearUnitarias()#Debe ser recursivo por si agregamos
                #otra regla unitaria en el proceso
    def __clearInutiles(self):#Buscamos reglas que no se usen nunca
        inutiles = []
        iteregla = iter(self.reglas)#S no se itera
        next(iteregla)
        for r in iteregla:#Por cada regla se busca en cada regla que no sea ella misma
            inutil = True
            for r2 in self.reglas:
                if r2==r:pass
                else:
                    if self.reglas[r2].searchByRegex(r):#Si se encuentra que se uso la regla
                    #en otra regla, esta regla quedara descartada de ser inutil
                        inutil = False
                        break
            if inutil:#Si resulta qe nunca fue usada, se añade a un arreglo 
                inutiles.append(r)
        for i in inutiles:#para despues eliminar la regla
            self.remove(i)
        if not inutiles:
            return
        self.__clearInutiles()
        '''Para encontrar las no generativas, para cada regla R debe existir
        al menos una regla que no lo incluya, por ejemplo:
        D->Da, esta regla solo se produce así misma creando un bucle, por lo que
        es no generativa.'''
    def __clearNoGenerativas(self):
        arr_remove = []
        for r in self.reglas:
            if self.reglas[r].searchByRegex("^((?!%s).)*$"%r):#Buscamos simbolos en reglas que
            #no se contengan así mismas
                pass
            else:
                arr_remove.append(r)#Si hay reglas no  generativas, se almacenan en un arreglo
        for rdelete in arr_remove:#por cada regla a eliminar, esta se borra de las demas reglas
            self.remove(rdelete)
            for r in self.reglas:
                self.reglas[r].removeContain(rdelete)
        if not arr_remove:
            return
        self.__clearNoGenerativas()
        '''Este metodo busca todas las reglas que se encuentran en la gramatica,
        si se encuentran reglas que no pertenecen a la gramatica, se borran todos los simbolos
        que contengan dicha letra en todas las reglas de la gramatica'''
    def __clearMuertas(self):
        reglas = []
        remove = []
        for r in self.reglas:
            self.reglas[r].getReglas(reglas)#Obtenemos las distintas reglas que aparecen
        for r in reglas:#buscamos cada regla en nuestra gramatica
            if not r in self.reglas: #Si no esta la borraremos
                remove.append(r)
        for r in remove:
            for r2 in self.reglas:#Removemos cada simbolo de cada regla
                self.reglas[r2].removeContain(r)#Que contenga reglas que esten muertas

    def remove(self,regla):#Metodo para borrar toda una regla de una gramatica
        try:
            self.reglas.pop(regla)
        except:pass

    def clear(self,stepbystep=False): #metodo que agrupa a los demás metodos
        if stepbystep:
            print("== Limpiar Muertas ==")
            self.__clearMuertas()
            print(self)
            print("== Limpiando epsilon ==")
            self.__clearEpsilon()
            print(self)
            print("=== Limpiar unitarias ==")
            self.__clearUnitarias()
            print(self)
            print("== Limpiar inutiles ==")
            self.__clearInutiles()
            print(self)
            print("== Limpiar Bucles ==")
            self.__clearNoGenerativas()
            print(self)
            print("== Limpiar inutiles ==")
            self.__clearInutiles()
            print(self)
        else:
            self.__clearMuertas()
            self.__clearEpsilon()
            self.__clearUnitarias()
            self.__clearInutiles()
            self.__clearNoGenerativas()
            self.__clearInutiles()
    '''
    Metodos para mostrar la gramatica cuando se llame a un objeto de esta clase
    '''
    def __repr__(self):
        rep = ""
        for r in self.reglas:
            rep = rep+str(self.reglas[r])+"\n"
        rep = rep[:-1]
        return rep
    def __str__(self):
        rep = ""
        for r in self.reglas:
            rep = rep+str(self.reglas[r])+"\n"
        rep = rep[:-1]
        return rep
