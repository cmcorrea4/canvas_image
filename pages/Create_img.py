import streamlit as st
from PIL import Image 
from openai import OpenAI
import os


st.title("Generación de Imágenes")
#if 'mi_respuesta' not in st.session_state:
#    st.session_state.mi_respuesta = None


# Retrieve the OpenAI API Key from secrets
api_key = os.environ['OPENAI_API_KEY']

# Initialize the OpenAI client with the API key
client = OpenAI(api_key=api_key)
with st.sidebar:
  image_size = st.selectbox("Selecciona el tamaño de la imagen:", ["256x256", "512x512", "1024x1024"])
  modelo=      st.selectbox("Selecciona el modelo:", ["dall-e-2", "dall-e-3"])
  calidad=     st.selectbox("Selecciona el Calidad:", ["Standard", "HD"])
  ke = st.text_input('Ingresa tu Clave')
  os.environ['OPENAI_API_KEY'] = ke

prompt_= st.text_area("Que quieres dibujar?",f"crea una imagen mejorada realista con la siguiente descripción:{st.session_state.mi_respuesta}")
if prompt_ and os.environ['OPENAI_API_KEY'] :
 response = client.images.generate(model=modelo,prompt=prompt_,size=image_size ,quality="standard", n=1,)

 image_url = response.data[0].url
 st.image(image_url, caption="Imagen Generada")

