import urllib.request
import json
import unidecode
import math

def elements_ordenation(total_elements):
    TOTAL_ELEMENTS = total_elements
    
    custo_inicial = TOTAL_ELEMENTS**2 #Definido um custo inicial, ou seja, a maior quantidade de solicitações possível
    for o in range (1,11): #Vai ser no máximo 25 destinos (4*25)
        for d in range (1,26): #Vai ser no máximo 10 origens (10*10)
            if (o*d<=100): #Limite de 100 elementos
                custo = math.ceil(TOTAL_ELEMENTS/o)*math.ceil(TOTAL_ELEMENTS/d) #Ceil arredonda para cima. Multiplicação de solicitações verticais e horizontais
                if (custo_inicial>custo): #busca o menor custo
                    custo_inicial = custo
                    N_ROWS_PER_ITERATION = o
                    N_COLUMNS_PER_ITERATION = d                
                else:
                    pass
            else:
                pass    
    
    TOTAL_ROWS_ITERATION    = int(TOTAL_ELEMENTS/N_ROWS_PER_ITERATION)
    TOTAL_COLUMNS_ITERATION = int(TOTAL_ELEMENTS/N_COLUMNS_PER_ITERATION)

    RESTO_ROWS    = TOTAL_ELEMENTS % N_ROWS_PER_ITERATION
    RESTO_COLUMNS = TOTAL_ELEMENTS % N_COLUMNS_PER_ITERATION

    origem = []
    destino = []
    quantidade_blocos = -1
    elementos = {}
    for r in range(TOTAL_ROWS_ITERATION + (1 if RESTO_ROWS != 0 else 0)): 
        for c in range(TOTAL_COLUMNS_ITERATION + (1 if RESTO_COLUMNS != 0 else 0)): 
            quantidade_blocos += 1
            origem = []
            destino = []
            for i in range(N_ROWS_PER_ITERATION): 
                if r > TOTAL_ROWS_ITERATION-1:
                    if i+r*N_ROWS_PER_ITERATION >= TOTAL_ELEMENTS:
                        break
                origem.append(i+r*N_ROWS_PER_ITERATION)    
            for j in range(N_COLUMNS_PER_ITERATION):                             
                if c > TOTAL_COLUMNS_ITERATION-1:                    
                    if j+c*N_COLUMNS_PER_ITERATION >= TOTAL_ELEMENTS:
                        break
                destino.append(j+c*N_COLUMNS_PER_ITERATION)
                elementos.update({quantidade_blocos:{'origem':origem, 'destino':destino}})
    return(elementos)

def get_distances_json(origins, destinations, api_key):
    
    ## build the url for the API call
    ELEVATION_BASE_URL = 'https://maps.googleapis.com/maps/api/distancematrix/json'

    # REMOVE ACCENTS AND REPLACE SPACES FOR + IN ORIGINS
    clean_origins = []
    for i in range(len(origins)):
        clean_origins.append(unidecode.unidecode(origins[i]).replace(" ", "+"))

    # COCATENATING ALL ORIGINS
    ORIGINS = 'origins='
    for clean_origin in clean_origins:
        ORIGINS += clean_origin + "|"
    ORIGINS = ORIGINS[:-1]

    # REMOVE ACCENTS AND REPLACE SPACES FOR + IN DESTINATIONS
    clean_destinations = []
    for i in range(len(destinations)):
        clean_destinations.append(unidecode.unidecode(destinations[i]).replace(" ", "+"))  

    # COCATENATING ALL DESTINATIONS
    DESTNATIONS = 'destinations='
    for clean_destination in clean_destinations:
        DESTNATIONS += clean_destination + "|"
    DESTNATIONS = DESTNATIONS[:-1]  

    URL_PARAMS = ORIGINS + '&' + DESTNATIONS + '&mode=driving&language=pt-BR&key=%s' % (api_key)

    url = ELEVATION_BASE_URL + "?" + URL_PARAMS
    
    print(url)
   
    with urllib.request.urlopen(url) as f:
        response = json.loads(f.read().decode())

    status = response['status']

    distance = []
    duration = []
    for row in response['rows']:
        for element in row['elements']:
            try:
                distance.append(element['distance']['value'])
                duration.append(element['duration']['value'])
            except KeyError or IndexError:
                distance.append("ERRO")    
                duration.append("ERRO")    
    return (distance, duration, status)


def convtime(t):
    horas = int(t // 3600)
    horas_rest = t % 3600
    minutos = int(horas_rest // 60)
    segundos_rest = int(round(horas_rest % 60, 0))
    print("Tempo de Processamento // " + str(horas) + ":" + str(minutos) + ":" + str(segundos_rest))
    return



