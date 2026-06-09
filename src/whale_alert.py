'''
1. requests al whale alert
2. utilizar el beautifulsoup para extraer la informacion. 
3. parsear la data que me retorna el response
4. utilizar pandas para transformar la data en un dataframe.
5.cargar el dataframe a un archivo csv. 
6. subir el archivo a un bucket de minio. 

'''
import requests 
from bs4 import BeautifulSoup 
import pandas as pd

url="https://whale-alert.io/whales.html"
response=requests.get(url)
response.encoding='utf-8'

soup=BeautifulSoup(response.content,'html.parser')
table =soup.select('table.table tbody tr')

print(table)