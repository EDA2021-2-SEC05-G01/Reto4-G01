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
                'grafocon': None, #grafo de conexiones entre aeropuertos
                'infociudad': None #información de las ciudades donde hay aeropuertos
        }

    analyzer['Name'] = mp.newMap(numelements=10702,
                                        maptype='CHAINING')

    analyzer['infociudad'] = mp.newMap(numelements=41002,
                                        maptype='CHAINING')

    analyzer['IATA'] = mp.newMap(numelements=10702,
                                        maptype='CHAINING',
                                        comparefunction=compareIATAS)
                                    
    analyzer['grafocon'] = gr.newGraph(datastructure='ADJ_LIST',
                                        directed=True,
                                        size=92605,
                                        comparefunction=compareIATAS)

    return analyzer

# Funciones para agregar informacion al catalogo

def addInfo(analyzer, airport):
    addairport(analyzer, airport)
    addairportgraf(analyzer, airport)



def addairport(analyzer, airport):
    name = analyzer["Name"]
    iata = analyzer["IATA"]
    mp.put(name, airport["Name"], airport["IATA"])
    mp.put(iata, airport["IATA"], airport["Name"])
    return analyzer


def addcity(analyzer, city):
    name = city['city']
    mapa = analyzer['infociudad']
    mp.put(mapa, name, city)
    return analyzer

def addairportgraf(analyzer, airport):
    iatair = airport['IATA']
    try:
        if not gr.containsVertex(analyzer['grafocon'], iatair):
                gr.insertVertex(analyzer['grafocon'], iatair)
        return analyzer
    except Exception as exp:
        error.reraise(exp, 'model:addairportgraf')

def addconexgraf(analyzer, vuelo):
    return None


# Funciones para creacion de datos

# Funciones de consulta

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
