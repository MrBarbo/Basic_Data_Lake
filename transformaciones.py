import pandas as pd


def transformacion_top_anime_columnas(data):
    # Para la transformación del dataframe de los top animes, se seleccionan las columnas que se consideran más relevantes para el análisis, 
    # como el título, el tipo, el número de episodios, la puntuación y el número de miembros. Además, se renombran las columnas para una mejor comprensión.
    df_top_anime = data[['title', 'type', 'episodes', 'score', 'members']]
    df_top_anime = df_top_anime.rename(columns={'title': 'Título', 'type': 'Tipo', 'episodes': 'Episodios', 'score': 'Puntuación', 'members': 'Miembros'})
    df_top_anime["Popular"] = df_top_anime["Miembros"].apply(lambda x: "Sí" if x > 100000 else "No")
    return df_top_anime

def transformacion_reseñas_anime_columnas(data):
    # Para la transformación del dataframe de las reseñas de anime, se seleccionan las columnas que se consideran más relevantes para el análisis, 
    # como el título del anime, el nombre del usuario, la puntuación, la reseña y la fecha. Además, se renombran las columnas para una mejor comprensión.
    # Luego se crea una columna que indica si la reseña es positiva o negativa en un campo booleano.
    df_reseñas_anime = data[['entry.title', 'user.username', 'score', 'review', 'date']]
    df_reseñas_anime = df_reseñas_anime.rename(columns={'entry.title': 'Título Anime', 'user.username': 'Usuario', 'score': 'Puntuación', 'review': 'Reseña', 'date': 'Fecha'})
    df_reseñas_anime["Reseña Positiva"] = df_reseñas_anime["Puntuación"].apply(lambda x: True if x >= 7 else False)
    return df_reseñas_anime