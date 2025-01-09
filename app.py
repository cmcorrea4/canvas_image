import os
import streamlit as st
import base64
from openai import OpenAI
import openai
from PIL import Image
import numpy as np

# Page configuration with improved styling
st.set_page_config(
    page_title='Smart Board AI',
    page_icon='✏️',
    layout='wide',
    initial_sidebar_state='expanded'
)

# Custom CSS to improve the appearance
st.markdown("""
    <style>
    .main {
        padding: 2rem;
    }
    .stButton>button {
        width: 100%;
        margin-top: 1rem;
    }
    .streamlit-expanderHeader {
        font-size: 1.2em;
    }
    </style>
""", unsafe_allow_html=True)

# Initialize session state
if 'mi_respuesta' not in st.session_state:
    st.session_state.mi_respuesta = None

def encode_image_to_base64(image_path):
    try:
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode("utf-8")
    except FileNotFoundError:
        return "Error: Imagen no encontrada en la ruta especificada."

# Sidebar configuration and documentation
with st.sidebar:
    st.title('🎨 Smart Board AI')
    
    # App information in an expander
    with st.expander("ℹ️ Acerca de la aplicación"):
        st.markdown("""
        Smart Board AI es una herramienta que permite:
        - Interpretar bocetos y dibujos
        - Analizar contenido matemático
        - Generar historias basadas en imágenes
        - Revisar código de programación
        - Mejorar y describir imágenes
        """)
    
    # Usage instructions in an expander
    with st.expander("📖 Guía de uso"):
        st.markdown("""
        1. Ingresa tu clave API de OpenAI
        2. Selecciona las herramientas de dibujo
        3. Dibuja o carga una imagen
        4. Añade contexto adicional (opcional)
        5. Selecciona el modo de análisis
        6. Presiona 'Analizar imagen'
        """)
    
    # API Key input in a separate expander for security
    with st.expander("🔑 Configuración API"):
        api_key = st.text_input('OpenAI API Key:', type='password')
        if api_key:
            os.environ['OPENAI_API_KEY'] = api_key

    st.divider()
    
    # Drawing tools configuration
    st.subheader("🎨 Herramientas de dibujo")
    
    drawing_mode = st.selectbox(
        "Seleccionar herramienta:",
        ("freedraw", "line", "rect", "circle", "transform", "polygon", "point"),
        format_func=lambda x: {
            "freedraw": "✏️ Dibujo libre",
            "line": "📏 Línea",
            "rect": "⬜ Rectángulo",
            "circle": "⭕ Círculo",
            "transform": "🔄 Transformar",
            "polygon": "📐 Polígono",
            "point": "📍 Punto"
        }[x]
    )
    
    stroke_width = st.slider('Grosor del trazo:', 1, 30, 5)
    stroke_color = st.color_picker("Color del trazo:", "#000000")
    bg_color = st.color_picker("Color del fondo:", "#FFFFFF")

# Main content area
st.title('🎨 Smart Board AI')
st.markdown("---")

# Create two columns for better layout
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("🖌️ Área de dibujo")
    
    # Image upload
    bg_image = st.file_uploader("📤 Cargar imagen de fondo:", type=["png", "jpg"])
    
    # Canvas component
    from streamlit_drawable_canvas import st_canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.3)",
        stroke_width=stroke_width,
        stroke_color=stroke_color,
        background_color=bg_color,
        background_image=Image.open(bg_image) if bg_image else None,
        height=400,
        width=600,
        drawing_mode=drawing_mode,
        key="canvas"
    )

with col2:
    st.subheader("🤖 Configuración del análisis")
    
    # Analysis options
    profile_ = st.radio(
        "Selecciona el modo de análisis:",
        ["Matemáticas", "Historia", "Programación", "Mejoramiento de imágenes"],
        format_func=lambda x: {
            "Matemáticas": "🔢 Matemáticas",
            "Historia": "📚 Historia",
            "Programación": "💻 Programación",
            "Mejoramiento de imágenes": "🖼️ Análisis de imagen"
        }[x]
    )
    
    # Context input
    additional_details = st.text_area("📝 Contexto adicional:", 
                                    placeholder="Añade información adicional para mejorar el análisis...")

    # Analysis button
    analyze_button = st.button("🔍 Analizar imagen", type="primary", use_container_width=True)

# Expert profiles
profile_Math = """Eres un experto en matemáticas que resuelve ecuaciones paso a paso.
                # Prompt para Resolución de Ecuaciones Matemáticas

            Como experto matemático, tu tarea es:
            1. Transcribir la ecuación de la imagen usando LaTeX
            2. Resolver paso a paso
            3. Explicar cada paso
            4. Presentar todo usando notación matemática LaTeX
            
            Estructura a seguir:
            ```
            Ecuación original:
            $[ecuación]$
            
            Resolución:
            Paso 1: [explicación]
            $[operación]$
            
            [Siguientes pasos...]
            
            Resultado final:
            $[resultado]$
            
            Verificación:
            [comprobación]
            ```
            
            Ejemplos de notación LaTeX básica:
            - Potencias: $x^2$, $x^{23}$
            - Fracciones: $\frac{a}{b}$
            - Raíces: $\sqrt{x}$, $\sqrt[3]{x}$
            - Integrales: $\int f(x)dx$, $\int_{a}^{b} f(x)dx$
            - Límites: $\lim_{x \to \infty}$
            - Sumas/Productos: $\sum_{i=1}^{n}$, $\prod_{i=1}^{n}$
            - Trigonometría: $\sin(x)$, $\cos(x)$
            - Matrices: $\begin{pmatrix} a & b \\ c & d \end{pmatrix}$
            
            Requisitos:
            - Explicar cada paso claramente
            - Usar LaTeX para todas las expresiones matemáticas
            - Verificar el resultado final
            - Mantener formato consistente
                      
                 
                 """

profile_Hist = """Eres un experto en narración infantil. Crea una historia breve y 
                 cautivadora basada en la imagen proporcionada."""

profile_Prog = """Eres un experto en programación. Analiza el código en la imagen,
                 describe su funcionamiento y corrige errores si los encuentras."""

profile_imgenh = """Describe brevemente en español todos los objetos que aparecen 
                    en la imagen de manera profesional y detallada."""

# Set expert profile based on selection
Expert = {
    "Matemáticas": profile_Math,
    "Historia": profile_Hist,
    "Programación": profile_Prog,
    "Mejoramiento de imágenes": profile_imgenh
}.get(profile_, "")

# Analysis logic
if canvas_result.image_data is not None and api_key and analyze_button:
    try:
        with st.spinner("🔄 Analizando..."):
            # Process image
            input_numpy_array = np.array(canvas_result.image_data)
            input_image = Image.fromarray(input_numpy_array.astype('uint8'), 'RGBA')
            input_image.save('img.png')
            
            if bg_image:
                image_ = Image.open(bg_image)
                image_.save('img.png')
            
            base64_image = encode_image_to_base64("img.png")
            
            # Create OpenAI client and prompt
            client = OpenAI(api_key=api_key)
            prompt_text = f"{Expert}, describe en español brevemente la imagen, {additional_details}"
            
            # Make API request with corrected image_url format
            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{
                    "role": "user",
                    "content": [
                        {"type": "text", "text": prompt_text},
                        {
                            "type": "image_url",
                            "image_url": {
                                "url": f"data:image/png;base64,{base64_image}"
                            }
                        }
                    ],
                }],
                max_tokens=500,
            )
            
            # Display response
            st.markdown("### 📝 Resultado del análisis")
            st.markdown(response.choices[0].message.content)
            
            if profile_ == "Mejoramiento de imágenes":
                st.session_state.mi_respuesta = response.choices[0].message.content
                
    except Exception as e:
        st.error(f"❌ Error: {str(e)}")
elif not api_key and analyze_button:
    st.warning("⚠️ Por favor, ingresa tu API key de OpenAI para continuar.")
