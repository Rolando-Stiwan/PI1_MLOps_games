## PROYECTO STEAM
#### Introducción
La idea de este proyecto es simular el rol de un MLOps Engineer, que es la combinación de un Data Engineer y Data Scientist.

Los datos son tomados de la empresa STEAM, que es una plataforma de distribución digital de videojuegos.

El trabajo básicamente es tomar los datasets que nos proporcionan y entregar una API desplegada tanto localmente como en la nube, donde se puedan hacer ciertas consultas como, por ejemplo, en qué año se jugó más un determinado género y también un sistema de recomendaciones. 

#### Datos Entregados
Estos son los datasets entregados y la información relacionada en cada uno de ellos:

**output_steam_games.json**: En este se encuentra la información sobre el juego en si, como el desarrollador, precio, al año de lanzamiento, genero.

**australian_user_reviews.json**: En este se encuentra principalmente información sobre los usuarios que han recomendado o no los juegos y una reseña sobre cada juego.

**australian_users_items.json**: En este se encuentra principalmente el tiempo de juego acumulado de cada usuario en un determinado juego.

### Fases del Proyecto
A continuación, se va a mostrar la fase de cada proyecto que equivale a la numeración de los jupyter notebook del repositorio.

#### Fase 1 Transformaciones:
En esta fase se llevo a cabo una primera etapa del ETL, donde se extrajeron y desanidaron los datos de cada dataset, se hizo una limpieza de datos como duplicados, valores nulos, se imputaron valores donde había datos faltantes, donde no eran claros y sobre todo se analiza la información que estos contienen. Este proceso se hizo para cada dataset aparte.

#### Fase 2 Feature Engineering:
En esta fase se hizo el análisis de sentimientos al dataset reviews en la columna donde estaban las reseñas de los usuarios. Para esto se usó la librería NLTK (Natural Language Toolkit) de Python, donde a clasificación fue 2 para una reseña positiva, 1 para una neutral y 0 para una negativa.

Después se realizó un análisis al dataset ítems a la columna playtime_forever que muestra el tiempo jugado acumulado del usuario en un juego, aquí se pudo ver que había valores atípicos y anomalías y se determino trabajar con los tiempos que son menores a 10000 horas pues estos datos representan el 96.89% de los datos totales.

También se hizo una segunda etapa del ETL pues se armaron datasets para ser usados en cada consulta, allí se unieron datasets y se borraron columnas según era necesario.

#### Fase 3 Desarrollo de las Funciones 
En esta fase se desarrollaron las consultas que deben ser desplegadas en la API, usando los datasets armados en la fase anterior, se hicieron la funciones primeramente en jupyter notebook para probar su funcionamiento, para luego llevarlas a main.py e implementarlas localmente usando el framework FastAPI. 

Las consultas son las siguientes:

**PlayTimeGenre**: En esta función se ingresa un genero y muestra el año con mas horas jugadas en ese mismo.

**UserForGenre**: Se introduce un genero y muestra el usuario que mas horas jugo en ese género y además muestras los años que jugo en ese género y cuánto tiempo jugo.

**UsersRecommend**: Se introduce un año y muestra el top 3 de los juegos mas recomendados para ese año.

**UsersWorstDeveloper**: Se introduce un año y muestra el top 3 de los desarrolladores con menos juegos recomendados para ese año.

**sentiment_analysis**: Se introduce un desarrollador y muestra la cantidad total de reseñas positivas, neutrales y negativas que ha recibido.

#### Fase 4 EDA
En esta fase se realizó la exploración de los datos para cada dataset, se observo que tan bueno fue el análisis de sentimiento, se entendió un poco más la distribución de los datos de tiempo de juego por usuario, los cambios en el top 10 de los juegos mas jugados descartando los valores mayores de 10.000 y sin descartarlos, también   el top 10 de los géneros mas jugados y de los desarrolladores con más juegos.
En una segunda parte se desarrolló un sistema de valoración usando las recomendaciones y el análisis de sentimientos hecho, el sistema de valoración quedo de 1 - 5 y se armó el dataset para ser usado en las consultas para el sistema de recomendación.

#### Fase 5 Sistema de Recomendación
En esta fase se cargaron los datasets en un jupyter notebook, se procesaron de tal manera que pudieran ser usados por el coseno de similaridad y posteriormente se programaron las funciones para obtener las recomendaciones que se pedían. Cuando se comprobó su correcto funcionamiento se copiaron en el main.py para el posterior despliegue.
También se guardaron algunos datasets para que sean consumidos posteriormente por la API.

Las consultas para este sistema son:

**recomendación_juego**: Dado el id de un juego se recomienda una serie de 5 juegos similares al ingresado.

**recomendación_usuario**: Dado el id de un usuario se recomiendan una serie de 5 juegos relacionados con los juegos que normalmente juega.

NOTA: Se debe tener en cuenta que para esta última función se tomaron solo 3000 datos, se hizo para que funcionara el deploy correctamente en la plataforma render.

Para realizar el deploy en la nube se utilizo la plataforma render, a continuación, se deja el link.  
https://stiwan-fastapi.onrender.com

Link del video
https://youtu.be/kCtaBMHxJ0M
