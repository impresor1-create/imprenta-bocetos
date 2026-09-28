import io
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.units import inch
from reportlab.pdfgen import canvas

def generar_pdf_factura(datos):
    """
    Genera la maqueta exacta en formato Media Carta Horizontal (8.5 x 5.5 pulg)
    según el estándar físico de Tipografía Anzoátegui, S.A.
    """
    buffer = io.BytesIO()
    
    # Dimensiones Media Carta Horizontal
    ANCHO = 8.5 * inch
    ALTO = 5.5 * inch
    
    c = canvas.Canvas(buffer, pagesize=(ANCHO, ALTO))
    
    # Márgenes de trabajo
    m_izq = 0.3 * inch
    m_der = ANCHO - 0.3 * inch
    m_top = ALTO - 0.3 * inch
    m_bot = 0.3 * inch
    
    # -------------------------------------------------------------------------
    # 1. ENCABEZADO SUPERIOR (Datos Emisor + Bloques Derecha)
    # -------------------------------------------------------------------------
    
    # Razón Social / Nombre
    c.setFont("Helvetica-Bold", 11)
    razon = datos.get("razon_social", "NOMBRE O RAZÓN SOCIAL DEL EMISOR").upper()
    c.drawString(m_izq, m_top, razon)
    
    # Especialidad o Actividad (si aplica)
    y_enc = m_top - 0.15 * inch
    if datos.get("especialidad"):
        c.setFont("Helvetica-Bold", 8)
        c.drawString(m_izq, y_enc, datos.get("especialidad"))
        y_enc -= 0.13 * inch
        
    c.setFont("Helvetica", 7.5)
    # RIF
    rif_emisor = datos.get("rif", "RIF: V-00000000-0")
    c.drawString(m_izq, y_enc, f"RIF: {rif_emisor}")
    y_enc -= 0.12 * inch
    
    # Dirección Fiscal Emisor
    dir_emisor = datos.get("direccion", "Dirección Fiscal del Emisor")
    c.drawString(m_izq, y_enc, dir_emisor[:75])
    y_enc -= 0.12 * inch
    
    # Teléfono / Correo Emisor
    tlf_emisor = datos.get("telefono", "")
    correo_emisor = datos.get("correo", "")
    info_contacto = f"Telfs: {tlf_emisor}" if tlf_emisor else ""
    if correo_emisor:
        info_contacto += f" / Correo: {correo_emisor}"
    c.drawString(m_izq, y_enc, info_contacto)
    
    # --- BLOQUES DERECHA: FACTURA N°, FECHA Y N° DE CONTROL ---
    # Cuadro FACTURA N°
    c.setLineWidth(0.8)
    c.rect(m_der - 2.2 * inch, m_top - 0.35 * inch, 2.2 * inch, 0.35 * inch)
    c.setFont("Helvetica-Bold", 11)
    c.drawString(m_der - 2.1 * inch, m_top - 0.25 * inch, "FACTURA")
    c.drawString(m_der - 0.9 * inch, m_top - 0.25 * inch, "N°")
    
    # Casillas DIA / MES / AÑO
    y_fecha = m_top - 0.42 * inch
    c.setFont("Helvetica-Bold", 7)
    c.drawCentredString(m_der - 1.8 * inch, y_fecha, "DIA")
    c.drawCentredString(m_der - 1.2 * inch, y_fecha, "MES")
    c.drawCentredString(m_der - 0.6 * inch, y_fecha, "AÑO")
    
    c.rect(m_der - 2.0 * inch, y_fecha - 0.22 * inch, 0.45 * inch, 0.2 * inch)
    c.rect(m_der - 1.45 * inch, y_fecha - 0.22 * inch, 0.5 * inch, 0.2 * inch)
    c.rect(m_der - 0.85 * inch, y_fecha - 0.22 * inch, 0.5 * inch, 0.2 * inch)
    
    # N° DE CONTROL (En Rojo Fiscal)
    c.setFillColor(colors.HexColor("#CC0000"))
    c.setFont("Helvetica-Bold", 9)
    c.drawString(m_der - 2.2 * inch, y_fecha - 0.4 * inch, "N° de CONTROL")
    c.setFont("Helvetica-Bold", 12)
    c.drawString(m_der - 1.0 * inch, y_fecha - 0.4 * inch, "00-")
    c.setFillColor(colors.black)

    # -------------------------------------------------------------------------
    # 2. SECCIÓN DATOS DEL CLIENTE
    # -------------------------------------------------------------------------
    y_cli = m_top - 1.05 * inch
    c.setLineWidth(0.5)
    c.setFont("Helvetica-Bold", 8)
    
    # Fila 1: Nombre
    c.drawString(m_izq, y_cli, "Nombre o Razón Social:")
    c.line(m_izq + 1.2 * inch, y_cli - 2, m_der, y_cli - 2)
    
    # Fila 2: Dirección
    y_cli -= 0.18 * inch
    c.drawString(m_izq, y_cli, "Dirección Fiscal:")
    c.line(m_izq + 0.9 * inch, y_cli - 2, m_der, y_cli - 2)
    
    # Fila 3: Teléfono / RIF / Condiciones
    y_cli -= 0.18 * inch
    c.drawString(m_izq, y_cli, "Teléfono:")
    c.line(m_izq + 0.5 * inch, y_cli - 2, m_izq + 2.3 * inch, y_cli - 2)
    
    c.drawString(m_izq + 2.4 * inch, y_cli, "RIF:")
    c.line(m_izq + 2.7 * inch, y_cli - 2, m_izq + 4.2 * inch, y_cli - 2)
    
    c.drawString(m_izq + 4.3 * inch, y_cli, "Condiciones de Pago:")
    c.rect(m_izq + 5.5 * inch, y_cli - 1, 8, 8)
    c.setFont("Helvetica", 7)
    c.drawString(m_izq + 5.65 * inch, y_cli, "CONTADO")
    c.rect(m_izq + 6.3 * inch, y_cli - 1, 8, 8)
    c.drawString(m_izq + 6.45 * inch, y_cli, "CRÉDITO")
    c.drawString(m_izq + 7.2 * inch, y_cli, "DÍAS")

    # -------------------------------------------------------------------------
    # 3. TABLA CENTRAL DE ÍTEMS / PRODUCTOS
    # -------------------------------------------------------------------------
    y_tabla_top = y_cli - 0.12 * inch
    h_tabla = 1.9 * inch
    
    # Marco Exterior Tabla
    c.setLineWidth(0.8)
    c.rect(m_izq, y_tabla_top - h_tabla, m_der - m_izq, h_tabla)
    
    # Cabecera Tabla
    c.line(m_izq, y_tabla_top - 0.22 * inch, m_der, y_tabla_top - 0.22 * inch)
    c.setFont("Helvetica-Bold", 8)
    
    # Coordenadas X de Columnas
    x_cant = m_izq + 0.7 * inch
    x_desc = m_der - 2.2 * inch
    x_punit = m_der - 1.1 * inch
    
    c.drawCentredString(m_izq + 0.35 * inch, y_tabla_top - 0.16 * inch, "CANT.")
    c.drawCentredString((x_cant + x_desc)/2, y_tabla_top - 0.16 * inch, "DESCRIPCIÓN")
    c.drawCentredString((x_desc + x_punit)/2, y_tabla_top - 0.16 * inch, "P. UNITARIO")
    c.drawCentredString((x_punit + m_der)/2, y_tabla_top - 0.16 * inch, "TOTAL")
    
    # Líneas Verticales Divisorias
    c.setLineWidth(0.5)
    c.line(x_cant, y_tabla_top, x_cant, y_tabla_top - h_tabla)
    c.line(x_desc, y_tabla_top, x_desc, y_tabla_top - h_tabla)
    c.line(x_punit, y_tabla_top, x_punit, y_tabla_top - h_tabla)

    # -------------------------------------------------------------------------
    # 4. MÓDULO INFERIOR (OBSERVACIONES, FORMA DE PAGO Y TOTALES)
    # -------------------------------------------------------------------------
    y_inf = y_tabla_top - h_tabla - 0.08 * inch
    
    # Leyenda Estándar
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(m_izq, y_inf, "ESTA FACTURA VA SIN TACHADURA NI ENMENDADURA")
    
    # Bloque Observaciones y Formas de Pago
    y_obs = y_inf - 0.15 * inch
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m_izq, y_obs, "OBSERVACIONES:")
    
    # Casillas Forma de Pago
    y_pago = y_obs - 0.35 * inch
    c.drawString(m_izq, y_pago, "FORMA DE PAGO:")
    c.rect(m_izq + 0.9 * inch, y_pago - 1, 7, 7)
    c.setFont("Helvetica", 6.5)
    c.drawString(m_izq + 1.02 * inch, y_pago, "EFECTIVO")
    c.rect(m_izq + 1.5 * inch, y_pago - 1, 7, 7)
    c.drawString(m_izq + 1.62 * inch, y_pago, "T. DEBITO")
    c.rect(m_izq + 2.1 * inch, y_pago - 1, 7, 7)
    c.drawString(m_izq + 2.22 * inch, y_pago, "TRANF. BAN.")
    
    y_pago2 = y_pago - 0.15 * inch
    c.rect(m_izq + 0.9 * inch, y_pago2 - 1, 7, 7)
    c.drawString(m_izq + 1.02 * inch, y_pago2, "PAGO M.")
    c.rect(m_izq + 1.5 * inch, y_pago2 - 1, 7, 7)
    c.drawString(m_izq + 1.62 * inch, y_pago2, "CHEQ")
    c.setFont("Helvetica-Bold", 6.5)
    c.drawString(m_izq + 2.1 * inch, y_pago2, "BANCO")
    c.line(m_izq + 2.5 * inch, y_pago2 - 1, m_izq + 4.2 * inch, y_pago2 - 1)
    
    # Pie de Copia/Original
    c.setFont("Helvetica-Bold", 6)
    c.drawString(m_izq, m_bot + 0.22 * inch, "ORIGINAL: BLANCO")
    c.drawString(m_izq + 1.2 * inch, m_bot + 0.22 * inch, "COPIA SIN DERECHO A CRÉDITO FISCAL: A COLOR")

    # --- CUADRO DERECHO DE TOTALES ---
    w_tot = 2.3 * inch
    h_tot = 0.8 * inch
    y_box_tot = y_inf - h_tot
    
    c.setLineWidth(0.8)
    c.rect(m_der - w_tot, y_box_tot, w_tot, h_tot)
    
    # Filas Internas Totales
    h_fila = h_tot / 4.0
    c.setLineWidth(0.5)
    c.line(m_der - w_tot, y_box_tot + h_fila*3, m_der, y_box_tot + h_fila*3)
    c.line(m_der - w_tot, y_box_tot + h_fila*2, m_der, y_box_tot + h_fila*2)
    c.line(m_der - w_tot, y_box_tot + h_fila*1, m_der, y_box_tot + h_fila*1)
    c.line(m_der - 1.1 * inch, y_box_tot, m_der - 1.1 * inch, y_box_tot + h_tot)
    
    c.setFont("Helvetica-Bold", 7)
    c.drawString(m_der - w_tot + 0.05 * inch, y_box_tot + h_fila*3 + 0.05 * inch, "BASE IMPONIBLE.")
    c.drawString(m_der - w_tot + 0.05 * inch, y_box_tot + h_fila*2 + 0.05 * inch, "TOTAL EXENT.")
    c.drawString(m_der - w_tot + 0.05 * inch, y_box_tot + h_fila*1 + 0.05 * inch, "I.V.A.          %")
    c.drawString(m_der - w_tot + 0.05 * inch, y_box_tot + 0.05 * inch, "TOTAL A PAGAR.")

    # -------------------------------------------------------------------------
    # 5. PIE DE IMPRENTA SENIAT (Texto Legal al Fondo)
    # -------------------------------------------------------------------------
    c.setFont("Helvetica", 5.5)
    
    # Datos extraídos o predeterminados
    ctrl_d = datos.get("control_desde", "00-0001")
    ctrl_h = datos.get("control_hasta", "00-0050")
    fact_d = datos.get("factura_desde", "0001")
    fact_h = datos.get("factura_hasta", "0050")
    f_imp = datos.get("fecha_impresion", "10-09-2026")
    
    linea_seniat_1 = "Tipografía Anzoátegui, S.A. RIF. J-08005647-7 Av. Jorge Rodríguez (Intercomunal) Edif. Greco piso 1 Ofic. 8 Telefax.: (0281) 2751793 Barcelona Edo. Anzoátegui"
    linea_seniat_2 = f"Providencia: SENIAT / 07/00048 del 30-01-2008  N° de CONTROL Desde el Nº {ctrl_d} Hasta el Nº {ctrl_h}  Fecha de Impresión {f_imp}. Región Nor-Oriental"
    linea_seniat_3 = f"Factura Desde el Nº {fact_d} Hasta el Nº {fact_h}"
    
    c.drawCentredString(ANCHO / 2.0, m_bot + 0.12 * inch, linea_seniat_1)
    c.drawCentredString(ANCHO / 2.0, m_bot + 0.05 * inch, linea_seniat_2)
    c.drawCentredString(ANCHO / 2.0, m_bot - 0.02 * inch, linea_seniat_3)
    
    c.save()
    buffer.seek(0)
    return buffer.getvalue()
