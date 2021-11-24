"""
 * Copyright 2020, Departamento de sistemas y Computación,
 * Universidad de Los Andes
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
 *
 * Contribuciones:
 *
 * Dario Correal - Version inicial
 """


import config as cf
from DISClib.ADT import list as lt
from DISClib.ADT import map as mp
from DISClib.ADT import graph as gr
from DISClib.DataStructures import mapentry as me
from DISClib.Algorithms.Sorting import shellsort as sa
from DISClib.Utils import error as error
assert cf

"""
Se define la estructura de un catálogo de videos. El catálogo tendrá dos listas, una para los videos, otra para las categorias de
los mismos.
"""

# Construccion de modelos

def NewAnalyzer():
    "Crea las estructuras y TADs que serán utilizadas en el proyecto"
    analyzer = {
                'Name': None, #combinación NAME - IATA
                'IATA': None, #combinación IATA - NAME
                'vuelo-peso':None, #peso del vuelo
                'grafodir': None, #grafo de conexiones entre aeropuertos dirigido
                'grafonodir': None, #grafo de conexiones no dirigidas
                'infociudad': None, #información de las ciudades donde hay aeropuertos
                'grafodirigido': None, #mapa creado sólo para la carga de datos
                'grafonodirigido': None #mapa creado sólo para la carga de datos
        }

    analyzer['Name'] = mp.newMap(numelements=10702,
                                        maptype='CHAINING')

    analyzer['infociudad'] = mp.newMap(numelements=41002,
                                        maptype='CHAINING')

    analyzer['grafodirigido'] = mp.newMap(numelements=92605,
                                        maptype='CHAINING')

    analyzer['vuelo-peso'] = mp.newMap(numelements=92605,
                                        maptype='CHAINING')
                                    
    analyzer['grafonodirigido'] = lt.newList("ARRAY_LIST")

    analyzer['IATA'] = mp.newMap(numelements=10702,
                                        maptype='CHAINING',
                                        comparefunction=compareIATAS)
                                    
    analyzer['grafodir'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=92605,
                                        comparefunction=compareIATAS)

    analyzer['grafonodir'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=False,
                                        size=92605,
                                        comparefunction=compareIATAS)

    return analyzer

# Funciones para agregar informacion al catalogo

def addInfo(analyzer, airport):
    addairport(analyzer, airport)



def addairport(analyzer, airport):
    name = analyzer["Name"]
    iata = analyzer["IATA"]
    mp.put(name, airport["Name"], airport)
    mp.put(iata, airport["IATA"], airport["Name"])
    return analyzer


def addcity(analyzer, city):
    name = city['city']
    mapa = analyzer['infociudad']
    mp.put(mapa, name, city)
    return analyzer


def addconexgraf(analyzer, vuelo):
    salida = vuelo['Departure']
    llegada = vuelo['Destination']
    dir = analyzer['grafodirigido']
    nodir = analyzer['grafonodirigido']

    #Agrega los vuelos dirigidos al mapa dirigido
    if mp.contains(dir, salida):
        lst = mp.get(dir, salida)['value']
        lt.addLast(lst, llegada)
        mp.put(dir, salida, lst)
    else:
        lst = lt.newList("ARRAY_LIST")
        lt.addLast(lst, llegada)
        mp.put(dir, salida, lst)
    
    mp.put(analyzer['vuelo-peso'], salida + '-' + llegada, float(vuelo['distance_km']))

    #Código por si el vuelo ya existe de manera dirigida
    if mp.contains(dir, llegada):
        lstllegada = mp.get(dir, llegada)['value']
        if lt.isPresent(lstllegada, salida):
            lt.addLast(nodir, salida + '-' + llegada)
            #---------------------------------------------
            borrar = mp.get(dir, salida)['value']
            lt.deleteElement(borrar, lt.isPresent(borrar, llegada))
            mp.put(dir, salida, borrar)
            #---------------------------------------------
            mp.put(analyzer['vuelo-peso'], llegada + '-' + salida, float(vuelo['distance_km']))
    return analyzer


def addgrafodir(analyzer):
    grafo = analyzer['grafodir']
    dir = analyzer['grafodirigido']
    pesos = analyzer['vuelo-peso']
    lstdir = mp.keySet(dir)
    for dirigidos in lt.iterator(lstdir):
        gr.insertVertex(grafo, dirigidos)
        addarcos(grafo, dir, dirigidos, pesos)
    return analyzer


def addarcos(grafo, dir, ini, pesos):
    lst = mp.get(dir, ini)['value']
    for fin in lt.iterator(lst):
        if not gr.containsVertex(grafo, fin):
            gr.insertVertex(grafo, fin)
        vuelo = ini + str('-') + fin
        peso = mp.get(pesos, vuelo)['value']
        gr.addEdge(grafo, ini, fin, peso)
    return grafo


def addgrafonodir(analyzer):
    grafo = analyzer['grafonodir']
    nodir = analyzer['grafonodirigido']
    pesos = analyzer['vuelo-peso']
    for dirigidos in lt.iterator(nodir):
        ver1 = dirigidos[:3]
        ver2 = dirigidos[4:]
        if not gr.containsVertex(grafo, ver1):
            gr.insertVertex(grafo, ver1)
        if not gr.containsVertex(grafo, ver2):
            gr.insertVertex(grafo, ver2)
        peso = mp.get(pesos, dirigidos)['value']
        gr.addEdge(grafo, ver1, ver2, peso)
    return analyzer


# Funciones para creacion de datos

# Funciones de consulta

def primeraeropuerto(analyzer, tipo):
    grafo = analyzer['grafo' + tipo]
    lista = gr.vertices(grafo)
    ultimo = lt.getElement(lista, 0)
    iatas = analyzer['IATA']
    nombre = mp.get(iatas, ultimo)['value']
    name = analyzer['Name']
    info = mp.get(name, nombre)['value']
    return info

def ultimaciudad(analyzer):
    ciudades = analyzer['infociudad']
    keys = mp.keySet(ciudades)
    ultima = lt.lastElement(keys)
    ultima = mp.get(ciudades, ultima)['value']
    return ultima

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

# Funciones de comparación

def compareIATAS(aero, keyvalueaero):
    """
    Compara dos aeropuertos
    """
    aerocode = keyvalueaero['key']
    if (aero == aerocode):
        return 0
    elif (aero > aerocode):
        return 1
    else:
        return -1
