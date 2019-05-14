import time
import xlrd
import googlemaps
import requests
import xlwt
import random
from codigos import *

inicio = time.time()

#ENDEREÇO DA BASE DE DADOS:
file_location = "base-de-dados.xlsx"

#SALVAR COMO? *PRECISA ESTAR NO FORMATO xls
file_location2 = "matrixcompleta.xls" 

#CONTROLE DE API's
api_key = ["<api_key>"]

##PARTE 01 DO CÓDIGO

#ABRINDO O PRIMEIRO ARQUIVO EXCEL
workbook = xlrd.open_workbook(file_location)

#COPIANDO A BASE DE DADOS
sheet = workbook.sheet_by_index(0)
linhas = sheet.nrows           
colunas = sheet.ncols
data = [[sheet.cell_value(r, c) for c in range(colunas)] for r in range(linhas)]

#JUNTANDO AS COLUNAS DA PLANILHA E GERANDO VETORES DE ENDEREÇOS
endereco = []
for i in range(1, linhas):
    a = str(data[i][1])
    b = str(int(data[i][2]))
    c = str(data[i][3])
    d = str(data[i][4])
    e = str(data[i][5])
    endereco.append(a +  ", " + b + " - " + c + ", " + d + " - " + e)
      
#COMANDO PARA FECHAR O PRIMEIRO ARQUIVO EXCEL
workbook.release_resources()

##PARTE 02 DO CÓDIGO

#GERANDO UM SEGUNDO ARQUIVO EXCEL #CHAMANDO O COMANDO WRITE
workbook = xlwt.Workbook()

#COPIANDO A BASE DE DADOS PARA O SEGUNDO ARQUIVO EXCEL
matriz = workbook.add_sheet('Base de Dados')
for i in range(linhas):
    for j in range(colunas):
        matriz.write(i,j,data[i][j])

#DIVIDINDO OS ELEMENTOS EM 10 ORIGENS E 10 DESTINOS #PADRÃO DO GOOGLE
elementos = elements_ordenation(len(endereco))
vetor_dist_tempo = {}
origins = []
destinations = []
for k in range(len(elementos)):
    resposta = 'OVER_QUERY_LIMIT'
    while(resposta == 'OVER_QUERY_LIMIT'):
        api = api_key
        for o in range(len(elementos[k]['origem'])):
            origins.append(endereco[elementos[k]['origem'][o]])
        for d in range(len(elementos[k]['destino'])):
            destinations.append(endereco[elementos[k]['destino'][d]])
        codigo = get_distances_json(origins, destinations, api)
        vetor_dist_tempo.update({k:{'distancia':codigo[0], 'tempo':codigo[1]}})
        resposta = codigo[2]
        controle = 1 + k
        print(str(controle) + '/' + str(len(elementos)) + ' - ' + codigo[2])
        print('\n')
        time.sleep(2)
        origins = []
        destinations = []

#CRIANDO A MATRIZ DE DISTÂNCIA (METROS) E TEMPOS (SEGUNDOS)
#CRIANDO NOVAS ABAS DENTRO DO ARQUIVO EXCEL     
matriz1 = workbook.add_sheet('Matriz de Distância em metros')
matriz1.write(0,0,'Origem\Destino')
matriz2 = workbook.add_sheet('Matriz de Tempo em segundos')
matriz2.write(0,0,'Origem\Destino')
print('Inicializando o API: ')

#COLANDO INDICES NA PRIMEIRA LINHA E PRIMEIRA COLUNA   
for i in range(1, linhas):
    matriz1.write(i,0,data[i][0])
    matriz1.write(0,i,data[i][0])
    matriz2.write(i,0,data[i][0])
    matriz2.write(0,i,data[i][0])        

#ESCREVENDO DISTÂNCIAS E TEMPOS
print(' ')
print('Gerando o Arquivo Final: ')   
for k in range(len(elementos)):
    contador_local = 0    
    for o in range(len(elementos[k]['origem'])):
        for d in range(len(elementos[k]['destino'])):            
            matriz1.write(elementos[k]['origem'][o] + 1, elementos[k]['destino'][d] + 1, str(vetor_dist_tempo[k]['distancia'][contador_local]))
            matriz2.write(elementos[k]['origem'][o] + 1, elementos[k]['destino'][d] + 1, str(vetor_dist_tempo[k]['tempo'][contador_local]))
            contador_local += 1
    workbook.save(file_location2)
    controle = 1 + k
    print(str(controle) + '/' + str(len(elementos)))

#PRINTANDO O TEMPO DE PROCESSAMENTO 
fim = time.time()
t = fim-inicio
print(' ')
convtime(t)
print(' ')


   


    
