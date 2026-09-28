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
                Devuelve ÚNICAMENTE un objeto JSON válido con estas claves exactas:
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
                
                # Lista de modelos válidos en la SDK actual
                modelos_validos = ['gemini-2.5-flash', 'gemini-1.5-flash']
                response_text = None
                
                for mod in modelos_validos:
                    try:
                        response = client.models.generate_content(
                            model=mod,
                            contents=prompt,
                        )
                        if response and response.text:
                            response_text = response.text
                            break
                    except Exception:
                        continue
                
                if response_text:
                    try:
                        # Limpiar etiquetas de código si existen
                        clean_json = response_text.strip()
                        if clean_json.startswith("```json"):
                            clean_json = clean_json[7:]
                        if clean_json.startswith("```"):
                            clean_json = clean_json[3:]
                        if clean_json.endswith("```"):
                            clean_json = clean_json[:-3]
                        clean_json = clean_json.strip()
                        
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
                    except Exception as json_err:
                        st.error(f"Error al interpretar la respuesta: {json_err}")
                else:
                    st.error("No se pudo obtener respuesta de la API. Verifica tu API Key en Secrets.")
    else:
        st.warning("Por favor pega un texto antes de presionar el botón.")
