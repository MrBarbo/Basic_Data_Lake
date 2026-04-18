import os
import pandas as pd
import dotenv
from deltalake import DeltaTable
import xtraccion, almacenamiento , transformaciones

delta_sincontroles = "./data_lake/full"
delta_incr_sincontroles = "./data_lake/incremental"
delta_transf_full = "./data_lake_transformado/full"
delta_transf_incremental = "./data_lake_transformado/incremental"

# Cargamos las variables de entorno
dotenv.load_dotenv()
api_url = os.getenv("API_URL")

# Definimos las URLs para la extracción de datos, utilizando las variables de entorno y los endpoints correspondientes para cada tipo de extracción.
url_full = f"{api_url}/top/anime?limit=20"
url_incremental = f"{api_url}/reviews/anime?limit=20"

# Los links de las APIs para la extracción de datos están relacionados con el anime. Para la extracción full, se utiliza un endpoint
# que devuelve los 20 animes más populares. Para la extracción incremental, se utiliza un endpoint que devuelve las 20 últimas reseñas de anime que existan en la página,
# incluyendo spoilers.

# Extracción de datos
data_full = extraccion.extraccion_full(url_full)
data_incremental = xtraccion.extraccion_incremental(url_incremental)


# Creación de DataFrames a partir de los datos extraídos, para luego ser almacenados en archivos Delta Lake utilizando el módulo write_deltalake. Tenemos que
# utilizar la función json_normalize de pandas para convertir los datos JSON en un formato adecuado para su almacenamiento sin errores.
top_anime = pd.json_normalize(data_full, record_path=['data'])
reviews_anime = pd.json_normalize(data_incremental, record_path=['data'])

# Para la extracción incremental, se formatea la columna date para poder usarla como partición del data lake, para facilitar la organización.
reviews_anime['date_dt'] = pd.to_datetime(reviews_anime['date'])
reviews_anime['partition_date'] = reviews_anime['date_dt'].dt.strftime('%Y-%m-%d')
reviews_anime = reviews_anime.drop(columns=['date_dt'])

# Eliminamos las columnas que contienen solo valores nulos, para evitar errores al querer almacenar el data lake. Además, convertimos las columnas de tipo object a 
# string para evitar problemas de tipos de datos al almacenar en Delta Lake.
top_anime = top_anime.dropna(axis=1, how='all')
reviews_anime = reviews_anime.dropna(axis=1, how='all')
for col in top_anime.select_dtypes(include=['object']).columns:
        top_anime[col] =top_anime[col].astype(str)
for col in reviews_anime.select_dtypes(include=['object']).columns:
        reviews_anime[col] =reviews_anime[col].astype(str)

# Almacenamos los datos en el archivo delta lake
almacenamiento.almacenamiento_full(delta_sincontroles, top_anime)
almacenamiento.almacenamiento_incremental(delta_incr_sincontroles, reviews_anime, 'partition_date')

# Ahora, para la segunda parte vamos a leer los datos almacenados en el data lake utilizando el módulo DeltaTable, 
# para luego realizar algunas transformaciones. En el mismo pasa, vamos a pasarlos a pandas.
top_de_animes = DeltaTable(delta_sincontroles).to_pandas()
ultimas_reseñas = DeltaTable(delta_incr_sincontroles).to_pandas()

#A la lista de animes populares, se le aplica una transformación para seleccionar las columnas más relevantes para el análisis, renombrarlas y 
# agregar una nueva columna que indique si el anime es popular o no, dependiendo del número de miembros que tenga. 
top_de_animes_transformado = transformaciones.transformacion_top_anime_columnas(top_de_animes)

# Para las reseñas de anime, se realiza una transformación para seleccionar las columnas más relevantes para el análisis, renombrarlas y 
# agregar una nueva columna que indique si la reseña es positiva o negativa, dependiendo de la puntuación que tenga. 
ultimas_reseñas_transformadas = transformaciones.transformacion_reseñas_anime_columnas(ultimas_reseñas)

# Almacenamos los datos transformados en el data lake para datos transformados.
almacenamiento.almacenamiento_full(delta_transf_full, top_de_animes_transformado)
almacenamiento.almacenamiento_incremental(delta_transf_incremental, ultimas_reseñas_transformadas, 'Fecha')
