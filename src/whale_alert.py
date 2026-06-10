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
from datetime import datetime,timezone
from logging import Logger,FileHandler,DEBUG



def whale_alert_extractor() -> dict[str,list[str]] | None:
    
    logger =Logger(whale_alert_extractor)
    file_handler= FileHandler('logs.log')
    logger.setLevel(DEBUG)
    logger.info('iniciando')
    logger.addHandler(file_handler)
    logger.info('agregando handler')
    url="https://whale-alert.io/whales.html"
    try:

    
        response=requests.get(url)
        logger.debug(f'Obteniendo datos  de la url: {url}')
        response.encoding='utf-8'

        soup=BeautifulSoup(response.content,'html.parser')
        table_rows =soup.select('table.table tbody tr')

        data ={
        "datetime_utc":[datetime.now(timezone.utc)] * len(table_rows),
        "crypto":[
        (row.find("th",{"scope":"row"}).find("img")["alt"].strip()
        if row.find('th',{"scope":"row"}).find("img")
        else row.find("th",{"scope":"row"}).get_text(strip=True))
        for row in table_rows ],
        "known":[row.find_all("td")[0].get_text(strip=True) for row in table_rows],
        "unknown":[row.find_all('td')[1].get_text(strip=True) for row in table_rows]
        }
        logger.info(f'Datos obtenidos: {len(data)} filas.')

        return data
        """
              whale_alert_df=pd.DataFrame(data) # crea el dataframe.
              print(whale_alert_df.head(10)) # muestra los primeros 10 registros.
              whale_alert_df.to_csv("whale_alert.csv",index=False) # carga el dataframe a un archivo csv. 
        """
      
    except Exception as e:
        logger.error(f'error {str(e)}')
        return None


whale_alert_df =whale_alert_extractor()  
if whale_alert_df is not None:
    whale_alert_df1=pd.DataFrame(whale_alert_df)
    whale_alert_df1.to_csv(f'data/whale_alert_{datetime.now().strftime('%Y-%m-%d')}.csv',index=False,encoding='utf-8')
    print(whale_alert_df1.head(10))  
else:
    print('no se pudo obtener los datos')
    
