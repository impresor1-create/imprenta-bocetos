import streamlit as st
import json
import os
from google import genai
from generator import generar_pdf_factura

st.set_page_config(page_title="Tipografía Anzoátegui - Generador", layout="centered")

st.title("📄 Generador de Boceto Media Carta")
st.write("Pega el texto del cliente recibido por WhatsApp:")

# Casilla de texto libre
raw_text = st.text_area("Mensaje de WhatsApp", height=150, placeholder="Pega aquí el texto...")

if st.button("⚡ Generar Boceto PDF", type="primary"):
    if raw_text.strip():
        with st.spinner("Analizando datos con IA y generando PDF..."):
            api_key = os.environ.get("GEMINI_API_KEY")
            
            if not api_key:
                st.error("Error: No se encontró la API Key de Gemini en Secrets.")
            else:
                client = genai.Client(api_key=api_key)
                
                prompt = f"""
                Extrae la información para una factura fiscal en Venezuela del siguiente texto.
                Devuelve ÚNICAMENTE un objeto JSON válido con estas claves:
                - razon_social
                - rif
                - especialidad (si aplica)
                - direccion
                - telefono
                - correo
                - control_desde
                - control_hasta
                - factura_desde
                - factura_hasta
                - fecha_impresion

                Texto recibido:
                {raw_text}
                """
                
                try:
                    response = client.models.generate_content(
                        model='gemini-2.0-flash',
                        contents=prompt,
                    )
                    
                    # Limpiar formato Markdown si lo incluye
                    clean_json = response.text.replace('```json', '').replace('```', '').strip()
                    datos = json.loads(clean_json)
                    
                    # Crear el PDF
                    pdf_bytes = generar_pdf_factura(datos)
                    
                    st.success("¡Boceto generado perfectamente!")
                    st.download_button(
                        label="⬇️ Descargar PDF para Cliente",
                        data=pdf_bytes,
                        file_name=f"Boceto_{datos.get('razon_social', 'Cliente')}.pdf",
                        mime="application/pdf"
                    )
                except Exception as e:
                    st.error(f"Error al procesar: {e}")
    else:
        st.warning("Por favor pega un texto antes de presionar el botón.")
