import streamlit as st
import PIL
from openai import OpenAI

st.title("Generación de Imágenes")



client = OpenAI()

prompt_= st.text_area("Que quieres dibujar?")
if prompt_ :
 response = client.images.generate(
   model="dall-e-3",
   prompt=prompt_,
   size="1024x1024",
   quality="standard",
   n=1,
 )

 image_url = response.data[0].url
 st.image(image_url, caption="Imagen Generada")
