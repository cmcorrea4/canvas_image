import streamlit as st
from PIL import Image 
from openai import OpenAI
import os


st.title("Generación de Imágenes")
ke = st.text_input('Ingresa tu Clave')
#os.environ['OPENAI_API_KEY'] = st.secrets['OPENAI_API_KEY']
os.environ['OPENAI_API_KEY'] = ke


# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)

image_size = st.selectbox("Selecciona el tamaño de la imagen:", ["256x256", "512x512", "1024x1024"])
modelo=      st.selectbox("Selecciona el modelo:", ["dall-e-2", "dall-e-3"])
prompt_= st.text_area("Que quieres dibujar?")
if prompt_ :
 response = client.images.generate(
   model=modelo,
   prompt=prompt_,
   size=image_size ,
   quality="standard",
   n=1,
 )

 image_url = response.data[0].url
 st.image(image_url, caption="Imagen Generada")
