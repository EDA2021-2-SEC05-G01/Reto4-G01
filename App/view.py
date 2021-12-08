"""
 * Copyright 2020, Departamento de sistemas y Computación, Universidad
 * de Los Andes
 *
 *
 * Desarrolado para el curso ISIS1225 - Estructuras de Datos y Algoritmos
 *
 *
 * This program is free software: you can redistribute it and/or modify
 * it under the terms of the GNU General Public License as published by
 * the Free Software Foundation, either version 3 of the License, or
 * (at your option) any later version.
 *
 * This program is distributed in the hope that it will be useful,
 * but WITHOUT ANY WARRANTY; without even the implied warranty of
 * MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
 * GNU General Public License for more details.
 *
 * You should have received a copy of the GNU General Public License
 * along withthis program.  If not, see <http://www.gnu.org/licenses/>.
 """

import config as cf
import sys
import controller
import threading
from time import process_time
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
assert cf


"""
La vista se encarga de la interacción con el usuario
Presenta el menu de opciones y por cada seleccion
se hace la solicitud al controlador para ejecutar la
operación solicitada
"""

#FUNCIONES DE IMPRESIÓN EN LA CONSOLA

def printmayorpuntodeinterconexion(analyzer):
    print("\n------------------------------------------------------------------------------------------")
    print("La cantidad de aeropuertos interconectados: " + str(analyzer['num']))
    print("\n------------------------------------------------------------------------------------------")
    l = lt.newList("ARRAY_LIST")
    for y in lt.iterator(analyzer['lista']):
        size = gr.indegree(analyzer['grafodir'], y) + gr.outdegree(analyzer['grafodir'], y)
        lt.addLast(l, {"key":y, "value":size})
    controller.ordenar_componentes(l)
    print("La lista de aeropuertos con la mayor cantidad de interconexiones:\n")
    if lt.size(l) >= 5:
        i = 1
        while i <= 5:
            ae = lt.getElement(l, i)
            iata = ae['key']
            aeropuerto = mp.get(analyzer['IATA'], iata)['value']
            print("IATA: "+ str(aeropuerto['IATA']) + "\nNombre: " + str(aeropuerto['Name']) + "\nCiudad: " + str(aeropuerto['City'])
                    + "\nPaís: " + str(aeropuerto["Country"]) + "\nCantidad de conexiones: " + str(ae['value']) + "\n")
            i += 1
    else:
        for ae in lt.iterator(l):
            iata = ae['key']
            aeropuerto = mp.get(analyzer['IATA'], iata)['value']
            print("IATA: "+ str(aeropuerto['IATA']) + "\nNombre: " + str(aeropuerto['Name']) + "\nCiudad: " + str(aeropuerto['City'])
                    + "\nPaís: " + str(aeropuerto["Country"]) + "\nCantidad de conexiones: " + str(ae['value']) + "\n")

def printclusteresaereos(i1, i2, catalog, cluster):
    print("\n------------------------------------------------------------------------------------------\n")
    print("Información de los aeropuertos ingresados:")
    print("\n------------------------------------------------------------------------------------------\n")
    info = catalog['IATA']
    i1 = mp.get(info, i1)['value']
    print("IATA: " + i1['IATA'] + "\nNombre: " + i1['Name'] + "\nCiudad: " + i1['City'] + "\nPaís: " + i1['Country'])
    print("\n------------------------------------------------------------------------------------------\n")
    i2 = mp.get(info, i2)['value']
    print("IATA: " + i2['IATA'] + "\nNombre: " + i2['Name'] + "\nCiudad: " + i2['City'] + "\nPaís: " + i2['Country'])
    print("\n------------------------------------------------------------------------------------------\n")
    print("Cantidad de Clústeres presentes en la red de tranporte: " + str(mp.size(catalog['mapa'])))
    print("\n------------------------------------------------------------------------------------------\n")
    print("¿Pertenecen " + i1['Name'] + " y " + i2['Name'] + " al mismo clúster en la red de transporte?\n")
    print("> " + str(cluster))

def printcaminomascorto(algd, aero1, aero2, catalog):
    print("\n------------------------------------------------------------------------------------------\n")
    print("Aeropuerto de Origen:")
    print("IATA: "+ str(aero1['IATA']) + "\nNombre: " + str(aero1['Name']) + "\nCiudad: " + str(aero1['City'])
                    + "\nPaís: " + str(aero1["Country"]))
    camino = mp.get(algd['visited'], aero2['IATA'])['value']
    print("\n------------------------------------------------------------------------------------------\n")
    print("Aeropuerto de Destino:")
    print("IATA: "+ str(aero2['IATA']) + "\nNombre: " + str(aero2['Name']) + "\nCiudad: " + str(aero2['City'])
                    + "\nPaís: " + str(aero2["Country"]))
    print("\n------------------------------------------------------------------------------------------\n")
    camino = mp.get(algd['visited'], aero2['IATA'])['value']
    distot = camino['distTo']
    camino = camino['edgeTo']
    lst = lt.newList()
    lt.addLast(lst, aero1['IATA'])
    for cam in camino:
        if type(camino[cam]) != float:
            lt.addLast(lst, camino[cam])
    i = 1
    j = 2
    print("Detalles del recorrido:\n")
    print("Distancia total recorrida: " + str(round((distot),3)) + " km\n")
    while j <= lt.size(lst):
        print("Trayecto " + str(i) + ":")
        o = lt.getElement(lst, i)
        d = lt.getElement(lst, j)
        print("Origen: " + (mp.get(catalog['IATA'], o)['value'])['IATA'])
        print("Destino: " + (mp.get(catalog['IATA'], d)['value'])['IATA'])
        vuelo = o + "-" + d
        print("Distancia Recorrida: " + str(mp.get(catalog['vuelo-peso'], vuelo)['value']) + "km\n")
        i += 1
        j += 1


def printaeropuertocerrado(closed, catalog, afectados):
    print("\n------------------------------------------------------------------------------------------\n")
    print("Información del Aeropuerto Cerrado: ")
    x = mp.get(catalog['IATA'], closed)['value']
    print("\nIATA: "+ str(x['IATA']) + "\nNombre: " + str(x['Name']) + "\nCiudad: " + str(x['City'])
                    + "\nPaís: " + str(x["Country"]))
    print("\n------------------------------------------------------------------------------------------\n")
    vuelos = lt.removeLast(afectados)
    print("La cantidad de vuelos afectados por el cierre de " + closed + ": " + str(vuelos))
    print("\n------------------------------------------------------------------------------------------\n")
    aero = lt.size(afectados)
    print("La cantidad de Aeropuertos afectados por el cierre de " + closed + ": " + str(aero))
    print("\n------------------------------------------------------------------------------------------\n")
    if aero > 6:
            i = 1
            l = lt.newList("ARRAY_LIST")
            print("Los primeros tres Aeropuertos afectados por este cierre: ")
            while i <= 3:
                ae = lt.getElement(afectados, i)
                ae = mp.get(catalog['IATA'], ae)['value']
                print("\nIATA: "+ str(ae['IATA']) + "\nNombre: " + str(ae['Name']) + "\nCiudad: " + str(ae['City'])
                    + "\nPaís: " + str(ae["Country"]))
                uf = lt.lastElement(afectados)
                lt.removeLast(afectados)
                lt.addFirst(l, uf)
                i += 1
            print("\n---------------------------------------------------------------------------\n")
            print("Los últimos tres Aeropuertos afectados por este cierre: ")
            for u in lt.iterator(l):
                u = mp.get(catalog['IATA'], u)['value']
                print("\nIATA: "+ str(u['IATA']) + "\nNombre: " + str(u['Name']) + "\nCiudad: " + str(u['City'])
                    + "\nPaís: " + str(u["Country"]))
    else:
        print("\nLos Aeropuertos afectados por este cierre:")
        for ae in lt.iterator(afectados):
            ae = mp.get(catalog['IATA'], ae)['value']
            print("\nIATA: "+ str(ae['IATA']) + "\nNombre: " + str(ae['Name']) + "\nCiudad: " + str(ae['City'])
                    + "\nPaís: " + str(ae["Country"]))



def printmillasviajero(catalog, lst, mv):
    print("\n------------------------------------------------------------------------------------------\n")
    print("Aeropuerto de salida:\n")
    ae = lt.getElement(lst, 2)
    ae = ae[:3]
    ae = mp.get(catalog['IATA'], ae)['value']
    print("\nIATA: "+ str(ae['IATA']) + "\nNombre: " + str(ae['Name']) + "\nCiudad: " + str(ae['City'])
                    + "\nPaís: " + str(ae["Country"]))   
    print("\n------------------------------------------------------------------------------------------\n")
    print("Cantidad de Aeropuertos posibles: " + str(lt.size(lt.removeFirst(lst)))) 
    print("Distancia total de los Aeropuertos posibles: " + str(round((lt.removeLast(lst)),3)))
    i = 1
    millas = 0
    print("\n------------------------------------------------------------------------------------------\n")
    print("Detalles del recorrido:\n")
    while i <= lt.size(lst):
        print("Trayecto " + str(i) + ":")
        o = lt.getElement(lst, i)
        d = o[:3]
        o = o[4:]
        print("Origen: " + (mp.get(catalog['IATA'], d)['value'])['IATA'])
        print("Destino: " + (mp.get(catalog['IATA'], o)['value'])['IATA'])
        vuelo = o + "-" + d
        gasto = mp.get(catalog['vuelo-peso'], vuelo)['value']
        millas += gasto
        print("Distancia Recorrida: " + str(gasto) + " km\n")
        i += 1
    print("\n------------------------------------------------------------------------------------------\n")
    print("Total de Millas Viajero: " + str(mv))
    print("\nTotal de Millas necesarias para el viaje más largo: " + str(round((2*millas*1.6),3)))
    millas = round((2*millas*1.6), 3)
    print("\n Al viajero le faltan " + str(round((millas - mv),3)) + " millas para completar su viaje.")




def printMenu():
    print("\n------------------------------------------------------------------------------------------")
    print("Bienvenido")
    print("1- Cargar información en el catálogo")
    print("2- Consultar los puntos de Interconexión entre los Aeropuertos")
    print("3- Consultar la cantidad de clústeres entre dos aeropuertos")
    print("4- Consultar la ruta más corta entre dos ciudades")
    print("5- Consultar la mayor cantidad de ciudades que pueden visitarse con Millas de Viajero")
    print("6- Consultar el impacto causado por un aeropuerto cerrado")
    print("------------------------------------------------------------------------------------------")

catalog = None
airpfile = 'airports-utf8-large.csv'
routefile = 'routes-utf8-large.csv'
citiesfile = 'worldcities-utf8.csv'

"""
Menu principal
"""

def menu():
    while True:
        printMenu()
        inputs = input('Seleccione una opción para continuar:\n> ')
        if int(inputs[0]) == 1:
            print("\nInicializando el analizador ....")
            catalog = controller.init()
            print("\nCargando información de los archivos ....")
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            controller.loadINFO(catalog, airpfile, routefile, citiesfile)
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            print("\n------------------------------------------------------------------------------------------")
            print("Cantidad de Aeropuertos Cargados: " + str(mp.size(catalog['IATA'])))
            print("Cantidad de Vuelos Dirigidos: " + str(gr.numEdges(catalog['grafodir'])))
            print("\nEl primer Aeropuerto Dirigido Cargado fue: \n")
            ae = controller.primeraeropuerto(catalog, "dir")
            print("Nombre: " + str(ae['Name']) + "\nCiudad: " + str(ae['City']) + "\nPaís: " + str(ae["Country"])
                    + "\nLatitud: " + str(ae['Latitude']) + "\nLongitud: " + str(ae["Longitude"]))
            print("------------------------------------------------------------------------------------------\n")
            print("Cantidad de Aeropuertos Cargados: " + str(mp.size(catalog['IATA'])))
            print("Cantidad de Vuelos No Dirigidos: " + str(gr.numEdges(catalog['grafonodir'])))
            print("\nEl primer Aeropuerto No Dirigido Cargado fue: \n")
            ae = controller.primeraeropuerto(catalog, "nodir")
            print("Nombre: " + str(ae['Name']) + "\nCiudad: " + str(ae['City']) + "\nPaís: " + str(ae["Country"])
                    + "\nLatitud: " + str(ae['Latitude']) + "\nLongitud: " + str(ae["Longitude"]))
            print("------------------------------------------------------------------------------------------\n")
            print("Cantidad de Ciudades Cargadas: " + str(controller.contarciudades(catalog)))
            ci = controller.ultimaciudad(catalog)
            print("\nLa primera Ciudad Cargada fue: \n")
            for c in lt.iterator(ci):
                print("Nombre: " + str(c['city']) + "\nPoblación: " + str(c['population'])
                    + "\nLatitud: " + str(c['lat']) + "\nLongitud: " + str(c["lng"]))

        elif int(inputs[0]) == 2:
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            controller.mayorpuntodeinterconexion(catalog, catalog['grafodir'])
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            printmayorpuntodeinterconexion(catalog)

        elif int(inputs[0]) == 3:
            i1 = input("Ingrese el primer código IATA:\n> ")
            i2 = input("Ingrese el segundo código IATA:\n> ")
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            cluster = controller.clusteresaereos(i1, i2, catalog['algk'])
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            printclusteresaereos(i1, i2, catalog, cluster)


        elif int(inputs[0]) == 4:
            c1 = input("Ingrese el nombre de la ciudad de Partida:\n> ")
            if lt.size(mp.get(catalog['infociudad'], c1)['value']) > 1:
                print("Hemos encontrado más de una ciudad con este nombre.\nPor favor, escoja la ciudad específica:\n")
                i = 1
                while i <= lt.size(mp.get(catalog['infociudad'], c1)['value']):
                    lst = mp.get(catalog['infociudad'], c1)['value']
                    ciudad = lt.getElement(lst, i)
                    print("\nOpción " + str(i) + ": Ciudad: " + ciudad['city'] + " - País: " + ciudad['country'] +
                           " - Latitud: " + ciudad['lat'] + " - Longitud: " + ciudad['lng'])
                    i += 1
                n1 = int(input("\nSu opción:\n> "))
            else:
                n1 = 1
            c2 = input("Ingrese el nombre de la ciudad de Llegada:\n> ")
            if lt.size(mp.get(catalog['infociudad'], c2)['value']) > 1:
                print("Hemos encontrado más de una ciudad con este nombre.\nPor favor, escoja la ciudad específica:\n")
                i = 1
                while i <= lt.size(mp.get(catalog['infociudad'], c2)['value']):
                    lst = mp.get(catalog['infociudad'], c2)['value']
                    ciudad = lt.getElement(lst, i)
                    print("\nOpción " + str(i) + ": Ciudad: " + ciudad['city'] + " - País: " + ciudad['country'] +
                           " - Latitud: " + ciudad['lat'] + " - Longitud: " + ciudad['lng'])
                    i += 1
                n2 = int(input("\nSu opción:\n> "))
            else:
                n2 = 1
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            algd, aero1, aero2 = (controller.caminomascorto(catalog, c1, c2, n1, n2))
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            printcaminomascorto(algd, aero1, aero2, catalog)


        elif int(inputs[0]) == 5:
            mv = int(input("Ingrese la cantidad de Millas Viajero disponibles:\n>"))
            inicio = input("Ingrese el nombre de la ciudad de Partida:\n> ")
            if lt.size(mp.get(catalog['infociudad'], inicio)['value']) > 1:
                print("Hemos encontrado más de una ciudad con este nombre.\nPor favor, escoja la ciudad específica:\n")
                i = 1
                while i <= lt.size(mp.get(catalog['infociudad'], inicio)['value']):
                    lst = mp.get(catalog['infociudad'], inicio)['value']
                    ciudad = lt.getElement(lst, i)
                    print("\nOpción " + str(i) + ": Ciudad: " + ciudad['city'] + " - País: " + ciudad['country'] +
                           " - Latitud: " + ciudad['lat'] + " - Longitud: " + ciudad['lng'])
                    i += 1
                n = int(input("\nSu opción:\n> "))
            else:
                n = 1
                inicio = int(input("\nSu opción:\n> "))
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            lst = controller.millasviajero(catalog, inicio, n)
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            printmillasviajero(catalog, lst, mv)

        elif int(inputs[0]) == 6:
            closed = input("Ingrese el IATA del aeroopuerto que se cerrará:\n>")
            #PRUEBA DE EJECUCIÓN
            start_time = process_time()
            afectados = controller.aeropuertocerrado(closed, catalog)
            #PRUEBAS DE EJECUCIÓN
            stop_time = process_time()
            elapsed_time_mseg = (stop_time - start_time)*1000
            print("tiempo de ejecución: " + str(elapsed_time_mseg))
            printaeropuertocerrado(closed, catalog, afectados)

        else:
            print("------------------------------------------------------------------------------------------")
            print("Cerrando el programa ....")
            print("------------------------------------------------------------------------------------------")
            sys.exit(0)
            sys.exit(0)


if __name__ == "__main__":
    threading.stack_size(67108864)  # 64MB stack
    sys.setrecursionlimit(2 ** 20)
    thread = threading.Thread(target=menu)
    thread.start()