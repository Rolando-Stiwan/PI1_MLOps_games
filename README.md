# 🎮 Proyecto STEAM – Sistema de Recomendación y Consultas vía API

Este proyecto implementa una solución completa de procesamiento de datos, análisis y despliegue de una API funcional para una plataforma de videojuegos similar a Steam. Utilizando técnicas de MLOps, procesamiento de lenguaje natural y análisis de comportamiento de usuarios, se desarrollaron funcionalidades que permiten realizar consultas clave y obtener recomendaciones personalizadas.

---

## 📦 Datasets Utilizados

Se trabajó con tres conjuntos de datos relacionados con el ecosistema de videojuegos y usuarios:

- **`output_steam_games.json`**: Información general del catálogo de juegos (desarrollador, precio, año de lanzamiento, género, etc.).
- **`australian_user_reviews.json`**: Reseñas y valoraciones emitidas por usuarios, incluyendo texto y recomendación.
- **`australian_users_items.json`**: Datos de tiempo de juego acumulado por usuario en cada título.

---

## 🧱 Arquitectura y Procesamiento

### 🔹 Limpieza y Transformación de Datos

Se desarrolló un proceso ETL completo:
- Desanidamiento de estructuras JSON.
- Detección y tratamiento de valores nulos, duplicados y atípicos.
- Estandarización de formatos.
- Generación de tablas intermedias optimizadas para consulta.

### 🔹 Análisis de Sentimientos

Se aplicó procesamiento de lenguaje natural (NLP) con NLTK para clasificar las reseñas en:
- **2**: Positivas
- **1**: Neutrales
- **0**: Negativas

### 🔹 Filtrado y Enriquecimiento

- Análisis de la variable `playtime_forever` para descartar valores extremos (>10,000 horas).
- Generación de métricas agregadas por usuario, género, desarrollador y juego.
- Construcción de nuevos datasets optimizados para las funcionalidades requeridas.

---

## ⚙️ Funcionalidades de la API

Se implementaron múltiples endpoints con **FastAPI**, disponibles tanto localmente como en la nube:

### 📊 Consultas Analíticas

- **`/PlayTimeGenre`**: Devuelve el año con más horas jugadas para un género específico.
- **`/UserForGenre`**: Informa el usuario con mayor tiempo jugado en un género, junto a detalle por año.
- **`/UsersRecommend`**: Top 3 juegos más recomendados en un año específico.
- **`/UsersWorstDeveloper`**: Top 3 desarrolladores con menor tasa de recomendaciones en un año dado.
- **`/sentiment_analysis`**: Recuento de reseñas positivas, neutras y negativas por desarrollador.

### 🤖 Sistema de Recomendación

Implementado con métricas de similitud de coseno y modelos basados en contenido:

- **`/recomendacion_juego`**: Dado el ID de un juego, sugiere cinco títulos similares.
- **`/recomendacion_usuario`**: Basado en el historial de un usuario, recomienda cinco nuevos juegos.

> Para optimizar el rendimiento del despliegue en Render, esta funcionalidad trabaja con una muestra representativa de 3000 usuarios.

---

## 📊 Exploración de Datos

Se realizaron análisis exploratorios sobre:
- Distribución de horas jugadas.
- Cambios en rankings de juegos y géneros.
- Evaluación de la calidad del análisis de sentimientos.
- Sistema de valoración de 1 a 5 basado en reseñas y recomendaciones.

---

## ☁️ Despliegue

La API se encuentra desplegada en **Render**, accesible públicamente en el siguiente enlace:

🔗 https://stiwan-fastapi.onrender.com/docs

---

## 🛠️ Tecnologías

- Python, FastAPI
- Pandas, NumPy, NLTK
- Cosine Similarity
- Render (cloud deployment)