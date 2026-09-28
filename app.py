import streamlit as st
import json
import re
from generator import generar_pdf_factura

st.set_page_config(page_title="Tipografía Anzoátegui - Generador", layout="centered")

st.title("📄 Generador de Boceto Media Carta")
st.write("Pega el texto del cliente recibido por WhatsApp:")

def extraer_datos(texto):
    """Extrae la información del mensaje mediante expresiones regulares."""
    def buscar(patron, texto_fuente, default=""):
        coincidencia = re.search(patron, texto_fuente, re.IGNORECASE | re.MULTILINE)
        return coincidencia.group(1).strip() if coincidencia else default

    # Patrones para capturar campos habituales
    razon_social = buscar(r"(?:razon social|cliente|nombre|empresa)[:\s]+([^\n]+)", texto)
    rif = buscar(r"(?:rif|j-?|v-?|e-?|g-?)[:\s]*([jvegJVEG][-\s]?\d+[-\s]?\d)", texto)
    if not rif:
        rif = buscar(r"([jvegJVEG][-\s]?\d{8,9}[-\s]?\d)", texto)
        
    especialidad = buscar(r"(?:especialidad|rama|médico|area)[:\s]+([^\n]+)", texto)
    direccion = buscar(r"(?:direccion|dirección|ubicacion|ubicación)[:\s]+([^\n]+)", texto)
    telefono = buscar(r"(?:telefono|teléfono|tlf|celular|whatsapp)[:\s]+([^\n]+)", texto)
    correo = buscar(r"(?:correo|email|e-mail)[:\s]+([^\n]+)", texto)
    
    control_desde = buscar(r"(?:control desde|nro control desde|control del)[:\s]+([^\n]+)", texto)
    control_hasta = buscar(r"(?:control hasta|nro control hasta|control al)[:\s]+([^\n]+)", texto)
    factura_desde = buscar(r"(?:factura desde|facturas desde|num desde)[:\s]+([^\n]+)", texto)
    factura_hasta = buscar(r"(?:factura hasta|facturas hasta|num hasta)[:\s]+([^\n]+)", texto)
    fecha_impresion = buscar(r"(?:fecha|fecha de impresion|fecha impresion)[:\s]+([^\n]+)", texto)

    # Si no se encuentra razón social, tomar la primera línea no vacía
    if not razon_social:
        lineas = [l.strip() for l in texto.splitlines() if l.strip()]
        razon_social = lineas[0] if lineas else "CLIENTE REGISTRADO"

    return {
        "razon_social": razon_social,
        "rif": rif,
        "especialidad": especialidad,
        "direccion": direccion,
        "telefono": telefono,
        "correo": correo,
        "control_desde": control_desde,
        "control_hasta": control_hasta,
        "factura_desde": factura_desde,
        "factura_hasta": factura_hasta,
        "fecha_impresion": fecha_impresion
    }

# Casilla de texto libre
raw_text = st.text_area("Mensaje de WhatsApp", height=150, placeholder="Pega aquí el texto...")

if st.button("⚡ Generar Boceto PDF", type="primary"):
    if raw_text.strip():
        with st.spinner("Procesando datos y generando PDF..."):
            try:
                datos = extraer_datos(raw_text)
                
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
                st.error(f"Error al generar el PDF: {e}")
    else:
        st.warning("Por favor pega un texto antes de presionar el botón.")
