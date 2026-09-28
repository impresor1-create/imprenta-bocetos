import io
from reportlab.lib.pagesizes import letter, landscape
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def generar_pdf_factura(datos):
    """
    Genera un PDF con formato de factura fiscal en formato Media Carta (Half Letter).
    Aplica márgenes, cuadrículas y jerarquía tipográfica estándar.
    """
    buffer = io.BytesIO()
    
    # Tamaño Media Carta Horizontal (8.5 x 5.5 pulgadas)
    ANCHO = 8.5 * inch
    ALTO = 5.5 * inch
    
    c = canvas.Canvas(buffer, pagesize=(ANCHO, ALTO))
    
    # ---------------------------------------------------------
    # MARCOS Y RAYADO DE BORDES
    # ---------------------------------------------------------
    # Marco exterior
    c.setLineWidth(1.5)
    c.setStrokeColor(colors.HexColor("#1A365D")) # Azul corporativo oscuro
    c.rect(0.25 * inch, 0.25 * inch, ANCHO - 0.5 * inch, ALTO - 0.5 * inch)
    
    # Línea interior del marco
    c.setLineWidth(0.5)
    c.rect(0.28 * inch, 0.28 * inch, ANCHO - 0.56 * inch, ALTO - 0.56 * inch)

    # ---------------------------------------------------------
    # ENCABEZADO (Razón Social y RIF)
    # ---------------------------------------------------------
    c.setFont("Helvetica-Bold", 14)
    c.setFillColor(colors.HexColor("#1A365D"))
    razon = datos.get("razon_social", "NOMBRE O RAZÓN SOCIAL").upper()
    c.drawString(0.4 * inch, ALTO - 0.6 * inch, razon)
    
    c.setFont("Helvetica-Bold", 10)
    c.setFillColor(colors.HexColor("#333333"))
    rif = datos.get("rif", "RIF: J-00000000-0")
    c.drawRightString(ANCHO - 0.4 * inch, ALTO - 0.6 * inch, f"RIF: {rif}")
    
    # Especialidad / Actividad Económica (si aplica)
    y_pos = ALTO - 0.8 * inch
    if datos.get("especialidad"):
        c.setFont("Helvetica-Oblique", 9)
        c.setFillColor(colors.HexColor("#555555"))
        c.drawString(0.4 * inch, y_pos, datos.get("especialidad"))
        y_pos -= 0.2 * inch

    # Línea divisoria superior
    c.setLineWidth(1)
    c.setStrokeColor(colors.HexColor("#1A365D"))
    c.line(0.4 * inch, y_pos, ANCHO - 0.4 * inch, y_pos)
    
    # ---------------------------------------------------------
    # DATOS DE CONTACTO Y DIRECCIÓN
    # ---------------------------------------------------------
    y_pos -= 0.25 * inch
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.black)
    
    direccion = datos.get("direccion", "Dirección no especificada")
    c.drawString(0.4 * inch, y_pos, f"DIRECCIÓN: {direccion[:80]}")
    
    y_pos -= 0.18 * inch
    telefono = datos.get("telefono", "N/A")
    correo = datos.get("correo", "N/A")
    c.drawString(0.4 * inch, y_pos, f"TELÉFONO: {telefono}   |   CORREO: {correo}")

    # ---------------------------------------------------------
    # CUADRO CENTRAL (DATOS DEL CLIENTE / FORMATO DE FACTURA)
    # ---------------------------------------------------------
    y_cuadro = y_pos - 0.25 * inch
    c.setLineWidth(0.8)
    c.setStrokeColor(colors.HexColor("#CBD5E1"))
    c.rect(0.4 * inch, y_cuadro - 1.8 * inch, ANCHO - 0.8 * inch, 1.8 * inch)
    
    # Rayado de filas internas del cuadro
    c.setFillColor(colors.HexColor("#F8FAFC"))
    c.rect(0.4 * inch, y_cuadro - 0.3 * inch, ANCHO - 0.8 * inch, 0.3 * inch, fill=True, stroke=True)
    
    c.setFont("Helvetica-Bold", 9)
    c.setFillColor(colors.HexColor("#1E293B"))
    c.drawString(0.5 * inch, y_cuadro - 0.2 * inch, "CLIENTE / RAZÓN SOCIAL:")
    c.drawString(4.5 * inch, y_cuadro - 0.2 * inch, "FECHA DE EMISIÓN:")
    
    # Filas para items / conceptos
    for i in range(1, 5):
        linea_y = y_cuadro - 0.3 * inch - (i * 0.3 * inch)
        c.setLineWidth(0.5)
        c.setStrokeColor(colors.HexColor("#E2E8F0"))
        c.line(0.4 * inch, linea_y, ANCHO - 0.4 * inch, linea_y)

    # ---------------------------------------------------------
    # PIE DE PÁGINA (DATOS DE IMPRENTA Y CONTROL SENIAT)
    # ---------------------------------------------------------
    y_pie = 0.4 * inch
    
    c.setFont("Helvetica-Bold", 8)
    c.setFillColor(colors.HexColor("#0F172A"))
    
    ctrl_d = datos.get("control_desde", "00-000001")
    ctrl_h = datos.get("control_hasta", "00-000050")
    fact_d = datos.get("factura_desde", "0001")
    fact_h = datos.get("factura_hasta", "0050")
    f_imp = datos.get("fecha_impresion", "DD/MM/AAAA")
    
    c.drawString(0.4 * inch, y_pie + 0.3 * inch, f"N° CONTROL DESDE: {ctrl_d} HASTA: {ctrl_h}")
    c.drawString(0.4 * inch, y_pie + 0.15 * inch, f"FACTURAS DESDE: {fact_d} HASTA: {fact_h}")
    
    c.drawRightString(ANCHO - 0.4 * inch, y_pie + 0.3 * inch, f"FECHA DE IMPRESIÓN: {f_imp}")
    c.drawRightString(ANCHO - 0.4 * inch, y_pie + 0.15 * inch, "TIPOGRAFÍA ANZOÁTEGUI - RIF: J-XXXXXXXX-X")
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
