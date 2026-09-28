import streamlit as st
import json
import os
import google.generativeai as genai
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
                st.error("Error: No se encontró la GEMINI_API_KEY en Secrets de Streamlit.")
            else:
                try:
                    genai.configure(api_key=api_key)
                    
                    prompt = f"""
                    Extrae la información para una factura fiscal en Venezuela del siguiente texto.
                    Devuelve ÚNICAMENTE un objeto JSON válido con estas claves exactas:
                    - razon_social
                    - rif
                    - especialidad
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
                    
                    # Probar con los alias oficiales activos de la librería
                    modelos = ['gemini-1.5-flash-latest', 'gemini-1.5-pro-latest', 'gemini-pro']
                    response = None
                    
                    for m in modelos:
                        try:
                            model = genai.GenerativeModel(m)
                            response = model.generate_content(prompt)
                            if response and response.text:
                                break
                        except Exception:
                            continue
                    
                    if response and response.text:
                        texto_limpio = response.text.replace("```json", "").replace("```", "").strip()
                        datos = json.loads(texto_limpio)
                        
                        # Crear el PDF
                        pdf_bytes = generar_pdf_factura(datos)
                        
                        st.success("¡Boceto generado perfectamente!")
                        st.download_button(
                            label="⬇️ Descargar PDF para Cliente",
                            data=pdf_bytes,
                            file_name=f"Boceto_{datos.get('razon_social', 'Cliente')}.pdf",
                            mime="application/pdf"
                        )
                    else:
                        st.error("No se pudo obtener respuesta del modelo de IA. Intenta de nuevo.")
                        
                except Exception as e:
                    st.error(f"Detalle del error: {e}")
    else:
        st.warning("Por favor pega un texto antes de presionar el botón.")
