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
from DISClib.Algorithms.Sorting import mergesort as mg
from DISClib.Algorithms.Graphs import scc
from DISClib.Algorithms.Graphs import dijsktra as dj
from DISClib.Algorithms.Graphs import prim
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
                'IATA': None, #combinación IATA - NAME
                'vuelo-peso':None, #peso del vuelo
                'grafodir': None, #grafo de conexiones entre aeropuertos dirigido
                'grafonodir': None, #grafo de conexiones no dirigidas
                'infociudad': None, #información de las ciudades donde hay aeropuertos
                'grafodirigido': None, #mapa creado sólo para la carga de datos
                'grafonodirigido': None, #mapa creado sólo para la carga de datos
                'ciudad-aero': None #mapa creado para el requerimiento 3
        }
    analyzer['infociudad'] = mp.newMap(numelements=41002,
                                        maptype='CHAINING')

    analyzer['grafodirigido'] = mp.newMap(numelements=92605,
                                        maptype='CHAINING')

    analyzer['ciudad-aero'] = mp.newMap(numelements=92605,
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
    iata = analyzer["IATA"]
    ciudad = analyzer['ciudad-aero']
    mp.put(iata, airport["IATA"], airport)
    mp.put(ciudad, airport["City"] + "-" + airport['Country'], airport)
    if not gr.containsVertex(analyzer['grafodir'], airport["IATA"]):
        gr.insertVertex(analyzer['grafodir'], airport["IATA"])
    return analyzer

def addcity(analyzer, city):
    name = city['city']
    mapa = analyzer['infociudad']
    if mp.contains(mapa, name):
        lst = mp.get(mapa, name)['value']
        lt.addLast(lst, city)
        mp.put(mapa, name, lst)
    else:
        lst = lt.newList("ARRAY_LIST")
        lt.addLast(lst, city)
        mp.put(mapa, name, lst)
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
            if lt.isPresent(nodir, salida + '-' + llegada) == 0 and lt.isPresent(nodir, llegada + '-' + salida) == 0:
                lt.addLast(nodir, salida + '-' + llegada)
    return analyzer


def addgrafodir(analyzer):
    grafo = analyzer['grafodir']
    dir = analyzer['grafodirigido']
    pesos = analyzer['vuelo-peso']
    lstdir = mp.keySet(dir)
    for ini in lt.iterator(lstdir):
        addarcos(grafo, dir, ini, pesos)
    return analyzer


def addarcos(grafo, dir, ini, pesos):
    lst = mp.get(dir, ini)['value']
    for fin in lt.iterator(lst):
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

# Funciones de consulta

def primeraeropuerto(analyzer, tipo):
    grafo = analyzer['grafo' + tipo]
    lista = gr.vertices(grafo)
    ultimo = lt.getElement(lista, 0)
    iatas = analyzer['IATA']
    nombre = mp.get(iatas, ultimo)['value']
    return nombre

def ultimaciudad(analyzer):
    ciudades = analyzer['infociudad']
    keys = mp.keySet(ciudades)
    ultima = lt.lastElement(keys)
    ultima = mp.get(ciudades, ultima)['value']
    return ultima


def mayorpuntodeinterconexion(analyzer, dir):
    dirigido = scc.KosarajuSCC(dir) #Algoritmo
    keys = mp.keySet(dirigido['idscc'])
    map = mp.newMap(lt.size(keys))
    values = mp.valueSet(dirigido['idscc'])
    j = 1
    for val in lt.iterator(values):
        key = lt.getElement(keys, j)
        if mp.contains(map, val):
            lst = mp.get(map, val)['value']
            lt.addLast(lst, key)
            mp.put(map, val, lst)
        else:
            lst = lt.newList("ARRAY_LIST")
            lt.addLast(lst, key)
            mp.put(map, val, lst)
        j += 1
    llaves = mp.keySet(map)
    mayor = 0
    may = None
    for y in lt.iterator(llaves):
        size = lt.size(mp.get(map, y)['value'])
        if size > mayor:
            mayor = size
            may = y
    lista = mp.get(map, may)['value']
    num = mp.size(dirigido['idscc'])
    analyzer['lista'] = lista
    analyzer['num'] = num
    analyzer['algk'] = dirigido
    analyzer['mapa'] = map
    return analyzer

def clusteresaereos(i1, i2, algk):
    return scc.stronglyConnected(algk, i1, i2)

def caminomascorto(analyzer, c1, c2, n1, n2):
    ciudad1 = mp.get(analyzer['infociudad'], c1)['value']
    ciudad1 = lt.getElement(ciudad1, n1)
    ciudad2 = mp.get(analyzer['infociudad'], c2)['value']
    ciudad2 = lt.getElement(ciudad2, n2)
    if (ciudad1['city'])[:5] == "Saint":
        ciudad1['city'] = "St." + (ciudad1['city'])[5:]
    areo1 = mp.get(analyzer['ciudad-aero'], ciudad1['city'] + "-" + ciudad1["country"])['value']
    areo2 = mp.get(analyzer['ciudad-aero'], ciudad2['city'] + "-" + ciudad2["country"])['value']
    algd = (dj.Dijkstra(analyzer['grafodir'], areo1['IATA']))
    return algd, areo1, areo2



def aeropuertocerrado(closed, analyzer):
    aeropuertos = (gr.adjacents(analyzer['grafodir'], closed))
    lst = lt.newList("ARRAY_LIST")
    vuelos = gr.indegree(analyzer['grafodir'], closed) + gr.outdegree(analyzer['grafodir'], closed)
    for ae in lt.iterator(aeropuertos):
        if lt.isPresent(lst, ae) == 0:
            lt.addLast(lst, ae)
    lt.addLast(lst, vuelos)
    return lst


def millasviajero(analyzer, inicio, n):
    inicio = mp.get(analyzer['infociudad'], inicio)['value']
    inicio = lt.getElement(inicio, n)
    inicio = mp.get(analyzer['ciudad-aero'], inicio['city'] + "-" + inicio["country"])['value']
    inicio = inicio['IATA']
    mst = prim.PrimMST(analyzer['grafonodir'])['edgeTo']
    suma = 0
    for k in lt.iterator(mp.valueSet(mst)):
        suma += k['weight']
    a = inicio
    x = "centinela"
    lst = lt.newList("ARRAY_LIST")
    lt.addLast(lst, mst)
    f = mp.get(mst, inicio)['value']
    lt.addLast(lst, f['vertexB'] + "-" + f['vertexA'])
    while mp.contains(mst, a):
        a = (mp.get(mst, a)['value'])['vertexA']
        if mp.contains(mst, a):
            x = mp.get(mst, a)['value']
            lt.addLast(lst, x['vertexB'] + "-" + x['vertexA'])
    lt.addLast(lst, suma)
    return lst


def contarciudades(analyzer):
    num = 0
    lstciudades = mp.keySet(analyzer['infociudad'])
    for city in lt.iterator(lstciudades):
        ciudad = mp.get(analyzer['infociudad'], city)['value']
        num += lt.size(ciudad)
    return num

# Funciones utilizadas para comparar elementos dentro de una lista

# Funciones de ordenamiento

def ordenar_componentes(lst):
    mg.sort(lst, compareccc)
    return lst

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

def compareccc(ufo1, ufo2):
    value1 = ufo1['value']
    value2 = ufo2['value']
    return value1 > value2
    
