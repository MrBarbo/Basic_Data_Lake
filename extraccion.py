import requests


#Los links de las APIs para la extracción de datos están relacionados con el anime. Para la extracción full, se utiliza un endpoint
#que devuelve los 20 animes más populares. Para la extracción incremental, se utiliza un endpoint que devuelve las 20 últimas reseñas de anime que existan en la página
# ,incluyendo spoilers.

def extraccion_full(url_full):
    response = requests.get(url_full)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error en la extracción full de datos")
        return None

def extraccion_incremental(url_incremental):
    response = requests.get(url_incremental)
    if response.status_code == 200:
        return response.json()
    else:
        print("Error en la extracción incremental de datos")
        return None