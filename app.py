import streamlit as st
import os
import time
import glob
import cv2
import numpy as np
import pytesseract
from gtts import gTTS
from googletrans import Translator

text = " "

def text_to_speech(input_language, output_language, text, tld):
    translation = translator.translate(text, src=input_language, dest=output_language)
    trans_text = translation.text
    tts = gTTS(trans_text, lang=output_language, tld=tld, slow=False)
    try:
        my_file_name = text[0:20]
    except:
        my_file_name = "audio"
    tts.save(f"temp/{my_file_name}.mp3")
    return my_file_name, trans_text

def remove_files(n):
    mp3_files = glob.glob("temp/*mp3")
    if len(mp3_files) != 0:
        now = time.time()
        n_days = n * 86400
        for f in mp3_files:
            if os.stat(f).st_mtime < now - n_days:
                os.remove(f)
                print("Deleted ", f)

remove_files(7)

st.markdown(
    """
    <style>
    .reportview-container {
        background-color: pink;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.markdown("<h1 style='color: pink;'>Reconocimiento Óptico de Caracteres</h1>", unsafe_allow_html=True)
st.markdown("<h2 style='color: pink;'>Elige la fuente de la imágen, esta puede venir de la cámara o cargando un archivo</h2>", unsafe_allow_html=True)

cam_ = st.checkbox("Usar Cámara")

if cam_:
    img_file_buffer = st.camera_input("Toma una Foto")
else:
    img_file_buffer = None

with st.sidebar:
    st.markdown("<h2 style='color: pink;'>Procesamiento para Cámara</h2>", unsafe_allow_html=True)
    st.markdown("<span style='color: pink;'>Filtro para imagen con cámara</span>", unsafe_allow_html=True)
    filtro = st.radio("Filtro para imagen con cámara", ('Sí', 'No'))

bg_image = st.file_uploader("<span style='color: pink;'>Cargar Imagen:</span>", type=["png", "jpg"], unsafe_allow_html=True)
if bg_image is not None:
    uploaded_file = bg_image
    st.image(uploaded_file, caption='<span style="color: pink;">Imagen cargada.</span>', use_column_width=True, unsafe_allow_html=True)
    with open(uploaded_file.name, 'wb') as f:
        f.write(uploaded_file.read())
    st.success(f"<span style='color: pink;'>Imagen guardada como {uploaded_file.name}</span>", unsafe_allow_html=True)
    img_cv = cv2.imread(f'{uploaded_file.name}')
    img_rgb = cv2.cvtColor(img_cv, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
st.write(text)

if img_file_buffer is not None:
    bytes_data = img_file_buffer.getvalue()
    cv2_img = cv2.imdecode(np.frombuffer(bytes_data, np.uint8), cv2.IMREAD_COLOR)

    if filtro == 'Sí':
        cv2_img = cv2.bitwise_not(cv2_img)

    img_rgb = cv2.cvtColor(cv2_img, cv2.COLOR_BGR2RGB)
    text = pytesseract.image_to_string(img_rgb)
    st.write(text)

with st.sidebar:
    st.markdown("<h2 style='color: pink;'>Parámetros de traducción</h2>", unsafe_allow_html=True)
    try:
        os.mkdir("temp")
    except:
        pass
    translator = Translator()

    in_lang = st.selectbox(
        "<span style='color: pink;'>Seleccione el lenguaje de entrada</span>",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
        format_func=lambda x: f"<span style='color: pink;'>{x}</span>",
        unsafe_allow_html=True
    )
    input_language = {"Ingles": "en", "Español": "es", "Bengali": "bn", "koreano": "ko", "Mandarin": "zh-cn", "Japones": "ja"}[in_lang]

    out_lang = st.selectbox(
        "<span style='color: pink;'>Seleccione el lenguaje de salida</span>",
        ("Ingles", "Español", "Bengali", "koreano", "Mandarin", "Japones"),
        format_func=lambda x: f"<span style='color: pink;'>{x}</span>",
        unsafe_allow_html=True
    )
    output_language = {"Ingles": "en", "Español": "es", "Bengali": "bn", "koreano": "ko", "Chinese": "zh-cn", "Japones": "ja"}[out_lang]

    english_accent = st.selectbox(
        "<span style='color: pink;'>Seleccione el acento</span>",
        (
            "Default",
            "India",
            "United Kingdom",
            "United States",
            "Canada",
            "Australia",
            "Ireland",
            "South Africa",
        ),
        format_func=lambda x: f"<span style='color: pink;'>{x}</span>",
        unsafe_allow_html=True
    )

    tld = {"Default": "com", "India": "co.in", "United Kingdom": "co.uk", "United States": "com", "Canada": "ca", "Australia": "com.au", "Ireland": "ie", "South Africa": "co.za"}[english_accent]

    display_output_text = st.checkbox("Mostrar texto")

    if st.button("Convertir"):
        if text.strip():
            result, output_text = text_to_speech(input_language, output_language, text, tld)
            audio_file = open(f"temp/{result}.mp3", "rb")
            audio_bytes = audio_file.read()
            st.markdown("<h2 style='color: pink;'>Tu audio:</h2>", unsafe_allow_html=True)
            st.audio(audio_bytes, format="audio/mp3", start_time=0)

            if display_output_text:
                st.markdown("<h2 style='color: pink;'>Texto de salida:</h2>", unsafe_allow_html=True)
                st.write(f" {output_text}")
        else:
            st.warning("<span style='color: pink;'>Por favor, ingrese un texto para convertir a audio.</span>", unsafe_allow_html=True)

