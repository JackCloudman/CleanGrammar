'''
Programa: Limpiar Gramatica v1.0
Autor: Reyes Vilchis Juan Jose
Grupo: 2CM11
'''
from GLC import Gramatica #Importamos nuestras clases
import re #Biblioteca de regex para python
#Metodo que nos permitira leer una Gramatica
def leerArchivo(g,archivo): 
	f = open(archivo,'r')#Leemos el archivo
	texto = f.readlines()#Leemos cada linea
	for l in texto:
		rid,reglas = l.replace("\n","").split("=")#Eliminamos los saltos de linea
		reglas = reglas.split("|")#Separamos los "or"
		for r in reglas:#Por cada regla obtenida la insertaremos en la gramatica
			g.insert(rid,r)#rid es el simbolo didentifica la regla, r los simbolos que produce
def help():#Mini menu de ayuda para el modo lectura
	print("Comando disponibles:\nhelp():Muestra ayuda\nexit():salir del programa\nsave():guarda los cambios")
	print("Ejemplo de uso:")
	print("S=ab|aB|")
	print("B=aa")
	print("===========")
'''Metodo que simula un mini prompt
Lo que hace realmente es escribir en un .txt
las distintas reglas que le asignemos.
Usa una expresion regular para identificar si la regla que escribimos
es correcta o incorrecta.
'''
def leerTerminal():
	print("Modo Lectura activado. Escribe: help() para recibir ayuda.")
	f = open("gramatica.txt",'w')#guardamos lo que escribimos en gramatica.txt
	while True:
		text = input("input>")#Texto a leer
		if text == "help()":
			help()
		elif text == "save()":
			f.close()
			break
		elif text == "exit()":
			exit()
		elif text == "":pass
		elif re.match(r"^[A-Z]=(\w|\|)+$",text):
			f.write(text+"\n")
		else:
			print("ERROR: La regla no esta bien escrita, escribe help() para ayuda")
'''
Main del programa, permite elegir entre leer de un archivo o desde la terminal,
posteriormente se limpiar la gramática.
'''
def main():
	while True:
		print("Limpiador GLC v1.0\nEscribe exit() para salir.")
		print("Elige una opcion")
		print("1- Leer un archivo")
		print("2- Lee desde la terminal")
		g = Gramatica() #Objeto que contendra nuestra gramatica
		op = input("Numero de opcion: ")
		print("===========")
		if op == "1":
			f = input("Nombre del archivo: ")
			'''
			Leer achivo recibe de parametro la gramatica donde se guardara
			la información y el nombre del archivo donde leerá.
			'''
			leerArchivo(g,f)
			break
		elif op == "2":
			'''
			Se ejecutara el mini prompt y despues se leera del archivo creado
			'''
			leerTerminal()
			leerArchivo(g,'gramatica.txt')
			break
		elif op == "exit()":
			exit()
		else:pass
	print("== Cadena leida ==")
	print(g) #Mostraremos la gramatica
	g.clear() #Se llama al metodo clear de gramatica
	print("== Cadena final ==")
	print(g)#Mostramos la gramatica final

if __name__ == '__main__': 
	try:
		main()
	except Exception as e: #Si se rompe el programa por haber escrito mal una gramatica
		print("Hiciste algo mal!")#Mostramos el error
		print(e)
