from fastapi import FastAPI, Query
import pandas as pd 
import numpy as np
import pickle
import gzip



app = FastAPI()

# http://127.0.0.1:8000

playtime = pd.read_csv('playtime.csv')
userfor = pd.read_csv('userfor.csv')
user_recom = pd.read_csv('user_recom.csv')
user_worst = pd.read_csv('user_worst.csv')
sa = pd.read_csv('sa.csv')
df_item_cos = pd.read_csv('df_item_cos.csv', index_col=0)
training_2 = pd.read_csv('training_2.csv')
with gzip.open('cosine_sim.pkl.gz', 'rb') as f: cosine_sim = pickle.load(f)




@app.get("/")
def index():
    return "PROYECTO DE ROLANDO STIWAN RODRIGUEZ"



@app.get("/PlayTimeGenre/")
def PlayTimeGenre(genre: str= Query(..., 
                                description="Genero de juego con mas horas jugadas", 
                                example="Action")):
    genre = genre.capitalize()
    filtered_data = playtime[playtime['genres'] == genre]
    grouped = filtered_data.groupby('rel_year')['playtime_forever'].sum().reset_index()
    año_mas_jugado = grouped.loc[grouped['playtime_forever'].idxmax(), 'rel_year']
    
    return {"Género": genre, "Año de lanzamiento con más horas jugadas para Género": int(año_mas_jugado)}



@app.get("/UserForGenre/")
def UserForGenre(genre: str= Query(..., 
                                description="Usuario con mas horas de juego en un genero", 
                                example="Action")):
    genre = genre.capitalize()
    # Filtrar el DataFrame por el género dado
    genero = userfor[userfor['genres'] == genre]
    
    if genero.empty:
        print(f"No hay datos para el género '{genre}'.")
        return
    
    # Encontrar el usuario que más horas ha jugado ese género
    max_user = genero.loc[genero['playtime_forever'].idxmax()]['user_id']
    # Se filtra el DataFrame para obtener solo las filas correspondientes al usuario con más horas jugadas en ese género
    usuario = genero[genero['user_id'] == max_user]
 
    # Calcular la acumulación de horas jugadas por año para ese género y usuario               
    agrupar = usuario.groupby('rel_year')['playtime_forever'].sum().reset_index()
    
    # Se vuelve genre_yearly_playtime en un diccionario para mostrar los resultados
    agrupar.columns = ['Year', 'Time']
    agrupar_dict = agrupar.to_dict(orient='records')
    result = {"Usuario con más horas jugadas para Género " + genre: max_user,
        "Horas jugadas": agrupar_dict}
    
    return result



@app.get("/UsersRecommend/")
def UsersRecommend(año: int= Query(..., 
                                description="Top 3 de juegos mas recomendados para el año dado", 
                                example=2011)):
    # Filtrar el DataFrame por el año proporcionado
    filtro = user_recom[user_recom['año'] == año]
    
    # Obtener los nombres de app_name en el mismo orden que aparecen en el DataFrame original
    nombres_app = filtro['app_name'].tolist()
    resultado = {f'Puesto {i+1}': app for i, app in enumerate(nombres_app)}
    
    return resultado



@app.get("/UsersWorstDeveloper/")
def UsersWorstDeveloper(año: int= Query(..., 
                                description="Top 3 de desarrolladoras con juegos menos recomendados para el año dado", 
                                example=2012)):
    # Filtrar el DataFrame por el año proporcionado
    filtro = user_worst[user_worst['año'] == año]
    
    # Obtener los nombres de app_name en el mismo orden que aparecen en el DataFrame original
    developer = filtro['developer'].tolist()
    resultado = {f'Puesto {i+1}': app for i, app in enumerate(developer)}
    
    return resultado




@app.get("/sentiment_analysis/")
def sentiment_analysis(developer: str= Query(..., 
                                description="Dada la empresa desarrolladora se muestra la cantidad de reseñas de usuarios, categorizadas", 
                                example="Gaijin Games")):
    filtro = sa.loc[sa['developer'] == developer]
    resultado = {
        developer: {
            'Negative': int(filtro.iloc[0, 1]), 
            'Neutral': int(filtro.iloc[0, 2]),   
            'Positive': int(filtro.iloc[0, 3])  
        }
    }
    return resultado


@app.get("/recomendacion_juego/")
def recomendacion_juego(game: str= Query(..., 
                                description="Dado el id del juego se recibe una lista de 5 juegos similares al ingresado", 
                                example="10")):
    recommendations = []
    count = 1
    #game_str = str(game)  # Convertir el valor numérico a cadena
    print('Similar games to {} include:\n'.format(game))
    for item in df_item_cos.sort_values(by=game, ascending=False).index[1:6]:
        recommendations.append({'No.': count, 'Juego': str(item)})
        count += 1
    
    return {"Juegos similares a {}".format(game): recommendations}



@app.get("/recomendacion_usuario/")
def recomendacion_usuario(user_id: str= Query(..., 
                                description="Dado el user_id se recopmienda 5 juegos al usuario", 
                                example="OfficialShroomsy")):
    n=5
    # Encuentra el índice del usuario en el DataFrame
    user_index = training_2[training_2['user_id'] == user_id]['user_id_encoded'].iloc[0]
    
    # Obtener juegos similares ordenados por similitud coseno
    similar_games = list(enumerate(cosine_sim[user_index]))
    similar_games = sorted(similar_games, key=lambda x: x[1], reverse=True)
    
    # Obtener los juegos ya jugados por el usuario
    games_played = set(training_2[training_2['user_id'] == user_id]['item_id'].tolist())
    
    # Filtrar juegos similares que ya han sido jugados y no están en la lista
    top_similar_games = []
    for idx, _ in similar_games:
        if len(top_similar_games) >= n:
            break
        game_id = training_2.iloc[idx]['item_id']
        if game_id not in games_played and game_id not in top_similar_games:
            top_similar_games.append(game_id)
    # Crear el diccionario con el formato deseado
    recommended_games = [{'No.': i+1, 'Juego': str(game_id)} for i, game_id in enumerate(top_similar_games)]
    output = {'Juegos recomendados a {}'.format(user_id): recommended_games}
    
    return output