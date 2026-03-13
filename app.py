import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from pathlib import Path
import base64

# ============================================================
# CONFIGURACION DE PAGINA
# ============================================================
st.set_page_config(
    page_title="CET Analytics Dashboard",
    page_icon="K",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ============================================================
# CSS PROFESIONAL CORPORATIVO
# ============================================================
CUSTOM_CSS = """
<style>
@import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&display=swap');

@keyframes fadeInUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeIn {
    from { opacity: 0; }
    to { opacity: 1; }
}

@keyframes slideInLeft {
    from { opacity: 0; transform: translateX(-15px); }
    to { opacity: 1; transform: translateX(0); }
}

@keyframes scaleIn {
    from { opacity: 0; transform: scale(0.95); }
    to { opacity: 1; transform: scale(1); }
}

@keyframes shimmer {
    0% { background-position: -200% 0; }
    100% { background-position: 200% 0; }
}

:root {
    --blue: #2563EB;
    --blue-dark: #1E40AF;
    --blue-deeper: #1E3A5F;
    --blue-light: #DBEAFE;
    --blue-50: #EFF6FF;
    --slate-900: #0F172A;
    --slate-700: #334155;
    --slate-500: #64748B;
    --slate-300: #CBD5E1;
    --slate-100: #F1F5F9;
    --slate-50: #F8FAFC;
    --white: #FFFFFF;
    --success: #059669;
    --success-bg: #ECFDF5;
    --warning: #D97706;
    --warning-bg: #FFFBEB;
    --danger: #DC2626;
    --danger-bg: #FEF2F2;
    --purple: #7C3AED;
}

html, body, [class*="css"] {
    font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
}

.main-header {
    background: linear-gradient(135deg, var(--blue) 0%, var(--blue-dark) 50%, var(--purple) 100%);
    padding: 1.8rem 2.2rem;
    border-radius: 14px;
    margin-bottom: 1.8rem;
    color: white;
    box-shadow: 0 4px 24px rgba(37, 99, 235, 0.25);
    animation: fadeInUp 0.6s ease-out;
}

.main-header h1 {
    color: white !important;
    font-weight: 800;
    font-size: 1.7rem;
    margin: 0;
    letter-spacing: -0.02em;
}

.main-header p {
    color: rgba(255,255,255,0.8);
    font-size: 0.9rem;
    margin: 0.4rem 0 0 0;
    font-weight: 400;
}

.kpi-card {
    background: var(--white);
    border-radius: 14px;
    padding: 1.3rem 1.5rem;
    box-shadow: 0 1px 3px rgba(0,0,0,0.06), 0 1px 2px rgba(0,0,0,0.04);
    border: 1px solid var(--slate-100);
    border-left: 4px solid var(--blue);
    transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
    margin-bottom: 0.8rem;
    animation: fadeInUp 0.5s ease-out both;
}

.kpi-card:hover {
    transform: translateY(-4px);
    box-shadow: 0 12px 28px rgba(37, 99, 235, 0.15);
    border-color: var(--blue-light);
}

.kpi-card .kpi-value {
    font-size: 1.9rem;
    font-weight: 800;
    color: var(--slate-900);
    line-height: 1.1;
    letter-spacing: -0.02em;
}

.kpi-card .kpi-label {
    font-size: 0.72rem;
    color: var(--slate-500);
    text-transform: uppercase;
    letter-spacing: 0.8px;
    font-weight: 600;
    margin-bottom: 0.4rem;
}

.kpi-card .kpi-delta {
    font-size: 0.72rem;
    color: var(--slate-500);
    font-weight: 500;
    margin-top: 0.3rem;
}

.kpi-card-red { border-left-color: var(--danger); }
.kpi-card-red .kpi-value { color: var(--danger); }

.kpi-card-cyan { border-left-color: var(--blue); }
.kpi-card-cyan .kpi-value { color: var(--blue); }

.kpi-card-green { border-left-color: var(--success); }
.kpi-card-green .kpi-value { color: var(--success); }

.insight-box {
    background: var(--blue-50);
    border-left: 4px solid var(--blue);
    border-radius: 10px;
    padding: 1.3rem 1.6rem;
    margin: 1rem 0;
    font-size: 0.88rem;
    line-height: 1.7;
    color: var(--slate-700);
    animation: slideInLeft 0.5s ease-out both;
    transition: all 0.3s ease;
}

.insight-box:hover {
    box-shadow: 0 4px 16px rgba(0,0,0,0.06);
    transform: translateX(4px);
}

.insight-box-warning {
    background: var(--warning-bg);
    border-left-color: var(--warning);
}

.insight-box-success {
    background: var(--success-bg);
    border-left-color: var(--success);
}

.insight-box-danger {
    background: var(--danger-bg);
    border-left-color: var(--danger);
}

.insight-title {
    font-weight: 700;
    color: var(--slate-900);
    margin-bottom: 0.5rem;
    font-size: 0.95rem;
}

.section-title {
    color: var(--slate-900);
    font-weight: 700;
    font-size: 1.2rem;
    border-bottom: 3px solid var(--blue);
    padding-bottom: 0.5rem;
    margin: 1.5rem 0 1rem 0;
    display: inline-block;
    letter-spacing: -0.01em;
    animation: fadeIn 0.4s ease-out;
}

section[data-testid="stSidebar"] {
    background: var(--white);
    border-right: 1px solid var(--slate-100);
}

section[data-testid="stSidebar"] .stMarkdown p,
section[data-testid="stSidebar"] .stMarkdown label,
section[data-testid="stSidebar"] label {
    color: var(--slate-700) !important;
}

section[data-testid="stSidebar"] h1,
section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] h3 {
    color: var(--slate-900) !important;
}

.stTabs [data-baseweb="tab-list"] {
    gap: 2px;
    background: var(--slate-50);
    border-radius: 12px;
    padding: 4px;
    border: 1px solid var(--slate-100);
    animation: fadeIn 0.4s ease-out;
}

.stTabs [data-baseweb="tab"] {
    border-radius: 10px;
    font-weight: 600;
    font-size: 0.82rem;
    padding: 0.5rem 1rem;
    transition: all 0.25s ease;
}

.stTabs [data-baseweb="tab"]:hover {
    background: var(--blue-light);
}

.custom-divider {
    height: 1px;
    background: linear-gradient(90deg, transparent, var(--slate-300), transparent);
    border: none;
    margin: 2rem 0;
}

.footer-text {
    text-align: center;
    color: var(--slate-500);
    font-size: 0.75rem;
    padding: 2rem 0 1rem 0;
    border-top: 1px solid var(--slate-100);
    margin-top: 3rem;
    animation: fadeIn 0.6s ease-out;
}

/* Plotly chart containers */
[data-testid="stPlotlyChart"] {
    animation: scaleIn 0.5s ease-out both;
    transition: transform 0.3s ease;
}

[data-testid="stPlotlyChart"]:hover {
    transform: scale(1.005);
}

/* Dataframe tables */
[data-testid="stDataFrame"] {
    animation: fadeInUp 0.5s ease-out both;
}

/* Login animation */
.login-card {
    animation: fadeInUp 0.7s ease-out;
}

.login-logos {
    animation: fadeIn 0.8s ease-out;
}
</style>
"""

st.markdown(CUSTOM_CSS, unsafe_allow_html=True)

# ============================================================
# PALETA DE COLORES PARA GRAFICOS
# ============================================================
COLORS = {
    "navy": "#1E40AF",
    "red": "#DC2626",
    "cyan": "#2563EB",
    "dark_navy": "#1E3A5F",
    "light_blue": "#3B82F6",
    "green": "#059669",
    "amber": "#D97706",
    "purple": "#7C3AED",
    "pink": "#DB2777",
    "orange": "#EA580C",
    "teal": "#0D9488",
    "indigo": "#4F46E5",
}

COLOR_SEQUENCE = [
    "#2563EB", "#7C3AED", "#059669", "#EA580C", "#DC2626",
    "#D97706", "#0D9488", "#DB2777", "#4F46E5", "#0891B2",
    "#65A30D", "#9333EA", "#C026D3", "#2DD4BF", "#F97316"
]

PLOTLY_LAYOUT = dict(
    plot_bgcolor="white",
    paper_bgcolor="white",
    font=dict(family="Inter, sans-serif"),
)


# ============================================================
# FUNCIONES AUXILIARES
# ============================================================
@st.cache_data
def get_logo_b64(filename):
    logo_path = Path(__file__).parent / "assets" / filename
    if logo_path.exists():
        data = logo_path.read_bytes()
        return base64.b64encode(data).decode()
    return ""


def logo_img_tag(filename, width=160):
    b64 = get_logo_b64(filename)
    if b64:
        return f'<img src="data:image/png;base64,{b64}" width="{width}">'
    return ""


def render_kpi_card(label, value, variant="", delta=""):
    css_class = f"kpi-card kpi-card-{variant}" if variant else "kpi-card"
    delta_html = f'<div class="kpi-delta">{delta}</div>' if delta else ""
    return f"""
    <div class="{css_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        {delta_html}
    </div>
    """


def render_insight(title, text, variant=""):
    css_class = f"insight-box insight-box-{variant}" if variant else "insight-box"
    return f"""
    <div class="{css_class}">
        <div class="insight-title">{title}</div>
        <div>{text}</div>
    </div>
    """


def tiempo_a_minutos(t):
    try:
        if pd.isna(t) or str(t).strip() == "" or str(t).strip() == "nan":
            return 0
        parts = str(t).strip().split(":")
        if len(parts) == 2:
            h, m = int(parts[0]), int(parts[1])
            return h * 60 + m
        return 0
    except (ValueError, TypeError):
        return 0


def hora_inicio(t):
    try:
        if pd.isna(t) or str(t).strip() == "" or str(t).strip() == "nan":
            return None
        parts = str(t).strip().split(":")
        if len(parts) >= 1:
            return int(parts[0])
        return None
    except (ValueError, TypeError):
        return None


# ============================================================
# CARGA DE DATOS
# ============================================================
@st.cache_data(ttl=60)
def load_data():
    csv_path = Path(__file__).parent / "dataset_cet.csv"
    df = pd.read_csv(csv_path, sep=";", encoding="utf-8")

    df["FECHA"] = pd.to_datetime(df["FECHA"], format="%d/%m/%Y", errors="coerce", dayfirst=True)
    df["MES"] = df["MES"].astype(str).str.strip().str.upper()
    df["MARCA"] = df["MARCA"].astype(str).str.strip()
    df["MARCA"] = df["MARCA"].replace({"TPLINK": "TP-LINK"})
    df["MINUTOS_ATENCION"] = df["TIEMPO ATENCION"].apply(tiempo_a_minutos)
    df["HORA_INICIO"] = df["INICIO"].apply(hora_inicio)

    df["DIA_SEMANA"] = df["FECHA"].dt.day_name()
    dias_map = {
        "Monday": "Lunes", "Tuesday": "Martes", "Wednesday": "Mi\u00e9rcoles",
        "Thursday": "Jueves", "Friday": "Viernes", "Saturday": "S\u00e1bado", "Sunday": "Domingo"
    }
    df["DIA_SEMANA_ES"] = df["DIA_SEMANA"].map(dias_map)
    df["SEMANA"] = df["FECHA"].dt.isocalendar().week.astype(int)
    df["ANIO_SEMANA"] = df["FECHA"].dt.strftime("%Y-W%W")

    for col in ["MARCA", "CANAL", "TIPO DE ATENCION", "MOTIVO", "VENDEDOR", "CLIENTE", "TECNICO", "USUARIO"]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip()
            df[col] = df[col].replace("nan", "")

    mes_orden = {"OCTUBRE": 1, "NOVIEMBRE": 2, "DICIEMBRE": 3, "ENERO": 4}
    df["MES_ORDEN"] = df["MES"].map(mes_orden).fillna(5).astype(int)

    return df


# ============================================================
# AUTENTICACION
# ============================================================
def show_login():
    cet_img = logo_img_tag("logo_cet.png", 160)
    kroton_img = logo_img_tag("logo_kroton.png", 140)

    st.markdown("""
    <style>
    .login-logos {
        display: flex;
        justify-content: center;
        align-items: center;
        gap: 2.5rem;
        margin: 4rem 0 2.5rem 0;
    }
    .login-card {
        background: #FFFFFF;
        border-radius: 16px;
        padding: 2.5rem 2.5rem 1rem 2.5rem;
        box-shadow: 0 20px 60px rgba(0,0,0,0.07);
        border: 1px solid #F1F5F9;
        text-align: center;
        max-width: 420px;
        margin: 0 auto 0.5rem auto;
    }
    .login-card h2 {
        color: #0F172A;
        font-weight: 800;
        font-size: 1.4rem;
        margin: 0 0 0.4rem 0;
        letter-spacing: -0.02em;
    }
    .login-card p {
        color: #64748B;
        font-size: 0.85rem;
        margin: 0;
        line-height: 1.5;
    }
    .login-footer {
        text-align: center;
        color: #94A3B8;
        font-size: 0.75rem;
        margin-top: 2rem;
    }
    </style>
    """, unsafe_allow_html=True)

    col1, col2, col3 = st.columns([1, 1.5, 1])
    with col2:
        st.markdown(f'<div class="login-logos">{cet_img}{kroton_img}</div>', unsafe_allow_html=True)
        st.markdown("""
        <div class="login-card">
            <h2>Acceso al Dashboard</h2>
            <p>Centro de Entrenamiento Tecnol\u00f3gico<br>Ingrese el c\u00f3digo de acceso para continuar</p>
        </div>
        """, unsafe_allow_html=True)

        code = st.text_input("C\u00f3digo de acceso", type="password", placeholder="Ingrese el c\u00f3digo...", label_visibility="collapsed")
        login_btn = st.button("Ingresar", use_container_width=True, type="primary")

        if login_btn:
            if code == "krt2030":
                st.session_state["authenticated"] = True
                st.rerun()
            else:
                st.error("C\u00f3digo incorrecto. Intente nuevamente.")

        st.markdown('<div class="login-footer">CET Analytics Dashboard v1.0 · Powered by Kroton SAC</div>', unsafe_allow_html=True)


# ============================================================
# SIDEBAR CON FILTROS
# ============================================================
def render_sidebar(df):
    with st.sidebar:
        cet_img = logo_img_tag("logo_cet.png", 150)
        kroton_img = logo_img_tag("logo_kroton.png", 120)
        st.markdown(f"""
        <div style="text-align:center; padding: 1rem 0;">
            {cet_img}<br><br>{kroton_img}
        </div>
        """, unsafe_allow_html=True)

        st.markdown("""
        <div style="background: linear-gradient(135deg, #2563EB, #7C3AED); padding: 0.8rem 1rem; border-radius: 10px; margin-bottom: 1.2rem;">
            <div style="color: white; font-weight: 700; font-size: 0.9rem; letter-spacing: -0.01em;">Panel de Filtros</div>
            <div style="color: rgba(255,255,255,0.7); font-size: 0.72rem; margin-top: 0.15rem;">Segmente los datos por periodo, equipo o producto</div>
        </div>
        """, unsafe_allow_html=True)

        min_date = df["FECHA"].min().date()
        max_date = df["FECHA"].max().date()
        date_range = st.date_input("Per\u00edodo de an\u00e1lisis", value=(min_date, max_date), min_value=min_date, max_value=max_date, format="DD/MM/YYYY")

        tecnicos = sorted([t for t in df["TECNICO"].unique() if t and t != ""])
        sel_tecnicos = st.multiselect("T\u00e9cnico", tecnicos, default=[], placeholder="Todos los t\u00e9cnicos")

        marcas = sorted([m for m in df["MARCA"].unique() if m and m != ""])
        sel_marcas = st.multiselect("Marca", marcas, default=[], placeholder="Todas las marcas")

        canales = sorted([c for c in df["CANAL"].unique() if c and c != ""])
        sel_canales = st.multiselect("Canal", canales, default=[], placeholder="Todos los canales")

        motivos = sorted([m for m in df["MOTIVO"].unique() if m and m != ""])
        sel_motivos = st.multiselect("Motivo", motivos, default=[], placeholder="Todos los motivos")

        st.markdown("<div style='height: 0.5rem'></div>", unsafe_allow_html=True)
        if st.button("Limpiar filtros", use_container_width=True):
            st.rerun()

        st.markdown("""
        <hr style="border-color: #E2E8F0; margin: 1.5rem 0 1rem 0;">
        <div style="text-align:center; color: #94A3B8; font-size: 0.68rem; line-height: 1.5;">
            CET Analytics Dashboard v1.0<br>Powered by Kroton SAC
        </div>
        """, unsafe_allow_html=True)

        st.markdown("<div style='height: 0.3rem'></div>", unsafe_allow_html=True)
        if st.button("Cerrar sesi\u00f3n", use_container_width=True):
            st.session_state["authenticated"] = False
            st.rerun()

    filtered = df.copy()
    if isinstance(date_range, tuple) and len(date_range) == 2:
        start, end = date_range
        filtered = filtered[(filtered["FECHA"].dt.date >= start) & (filtered["FECHA"].dt.date <= end)]
    if sel_tecnicos:
        filtered = filtered[filtered["TECNICO"].isin(sel_tecnicos)]
    if sel_marcas:
        filtered = filtered[filtered["MARCA"].isin(sel_marcas)]
    if sel_canales:
        filtered = filtered[filtered["CANAL"].isin(sel_canales)]
    if sel_motivos:
        filtered = filtered[filtered["MOTIVO"].isin(sel_motivos)]

    return filtered


# ============================================================
# TAB 1: DASHBOARD GENERAL
# ============================================================
def tab_dashboard_general(df):
    st.markdown('<div class="main-header"><h1>Dashboard General</h1><p>Vista integral de las operaciones del Centro de Entrenamiento Tecnol\u00f3gico</p></div>', unsafe_allow_html=True)

    total_atenciones = len(df)
    df_con_tiempo = df[df["MINUTOS_ATENCION"] > 0]
    tiempo_prom = df_con_tiempo["MINUTOS_ATENCION"].mean() if len(df_con_tiempo) > 0 else 0
    clientes_unicos = df[df["CLIENTE"] != ""]["CLIENTE"].nunique()
    tecnicos_activos = df[df["TECNICO"] != ""]["TECNICO"].nunique()
    pct_presencial = (len(df[df["TIPO DE ATENCION"] == "PRESENCIAL"]) / total_atenciones * 100) if total_atenciones > 0 else 0
    top_marca = df[df["MARCA"] != ""]["MARCA"].value_counts().index[0] if len(df[df["MARCA"] != ""]) > 0 else "N/A"

    c1, c2, c3, c4, c5, c6 = st.columns(6)
    with c1:
        st.markdown(render_kpi_card("Total Atenciones", f"{total_atenciones:,}"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card("Tiempo Promedio", f"{tiempo_prom:.0f} min", "red"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card("Clientes \u00danicos", f"{clientes_unicos:,}", "cyan"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card("T\u00e9cnicos Activos", f"{tecnicos_activos}", "green"), unsafe_allow_html=True)
    with c5:
        st.markdown(render_kpi_card("% Presencial", f"{pct_presencial:.1f}%", "red"), unsafe_allow_html=True)
    with c6:
        st.markdown(render_kpi_card("Top Marca", top_marca, "cyan"), unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        mes_data = df.groupby(["MES", "MES_ORDEN"]).size().reset_index(name="Atenciones")
        mes_data = mes_data.sort_values("MES_ORDEN")
        fig_mes = px.bar(mes_data, x="MES", y="Atenciones", title="Atenciones por Mes",
                         color_discrete_sequence=[COLORS["navy"]], text="Atenciones")
        fig_mes.update_traces(textposition="outside", cliponaxis=False)
        fig_mes.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Cantidad", margin=dict(t=40, b=20))
        st.plotly_chart(fig_mes, use_container_width=True)

    with col2:
        semana_data = df.copy()
        semana_data["SEMANA_INICIO"] = semana_data["FECHA"] - pd.to_timedelta(semana_data["FECHA"].dt.dayofweek, unit="D")
        semana_data = semana_data.groupby("SEMANA_INICIO").size().reset_index(name="Atenciones")
        semana_data = semana_data.sort_values("SEMANA_INICIO")
        semana_data["Semana"] = range(1, len(semana_data) + 1)
        semana_data["Etiqueta"] = "Sem " + semana_data["Semana"].astype(str)
        fig_semana = px.line(semana_data, x="Etiqueta", y="Atenciones", title="Tendencia Semanal de Atenciones",
                             markers=True, color_discrete_sequence=[COLORS["purple"]],
                             custom_data=["SEMANA_INICIO"])
        fig_semana.update_traces(line_shape="spline", line=dict(width=2.5),
                                 hovertemplate="<b>%{x}</b><br>Inicio: %{customdata[0]|%d %b %Y}<br>Atenciones: %{y}<extra></extra>")
        fig_semana.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Cantidad", margin=dict(t=40, b=20))
        st.plotly_chart(fig_semana, use_container_width=True)

    col3, col4 = st.columns(2)

    with col3:
        tipo_data = df[df["TIPO DE ATENCION"] != ""]["TIPO DE ATENCION"].value_counts().reset_index()
        tipo_data.columns = ["Tipo", "Cantidad"]
        fig_tipo = px.bar(tipo_data, x="Cantidad", y="Tipo", orientation="h", title="Remoto vs Presencial",
                          color="Tipo", color_discrete_map={"REMOTO": COLORS["navy"], "PRESENCIAL": COLORS["purple"]},
                          text="Cantidad")
        fig_tipo.update_traces(textposition="outside", cliponaxis=False)
        fig_tipo.update_layout(**PLOTLY_LAYOUT, showlegend=False, margin=dict(t=40, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_tipo, use_container_width=True)

    with col4:
        motivo_data = df[df["MOTIVO"] != ""]["MOTIVO"].value_counts().reset_index()
        motivo_data.columns = ["Motivo", "Cantidad"]
        fig_motivo = px.bar(motivo_data, x="Cantidad", y="Motivo", orientation="h", title="Distribuci\u00f3n por Motivo",
                            color_discrete_sequence=[COLORS["cyan"]], text="Cantidad")
        fig_motivo.update_traces(textposition="outside", cliponaxis=False)
        fig_motivo.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"),
                                 margin=dict(t=40, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_motivo, use_container_width=True)


# ============================================================
# TAB 2: ANALISIS TECNICO
# ============================================================
def tab_analisis_tecnico(df):
    st.markdown('<div class="main-header"><h1>An\u00e1lisis T\u00e9cnico</h1><p>Evaluaci\u00f3n pericial detallada de las operaciones de soporte t\u00e9cnico</p></div>', unsafe_allow_html=True)

    st.markdown('<div class="section-title">Mapa de Calor: Atenciones por D\u00eda y Hora</div>', unsafe_allow_html=True)

    df_heatmap = df[df["HORA_INICIO"].notna()].copy()
    if len(df_heatmap) > 0:
        dias_orden = ["Lunes", "Martes", "Mi\u00e9rcoles", "Jueves", "Viernes", "S\u00e1bado"]
        heatmap_data = df_heatmap.groupby(["DIA_SEMANA_ES", "HORA_INICIO"]).size().reset_index(name="Atenciones")
        heatmap_pivot = heatmap_data.pivot_table(index="DIA_SEMANA_ES", columns="HORA_INICIO", values="Atenciones", fill_value=0)
        existing_dias = [d for d in dias_orden if d in heatmap_pivot.index]
        heatmap_pivot = heatmap_pivot.reindex(existing_dias)

        fig_heat = px.imshow(heatmap_pivot, aspect="auto",
                             color_continuous_scale=["#F8FAFC", "#93C5FD", "#1E40AF"],
                             labels=dict(x="Hora del D\u00eda", y="D\u00eda de la Semana", color="Atenciones"))
        fig_heat.update_layout(**PLOTLY_LAYOUT, margin=dict(t=20, b=20), height=350)
        st.plotly_chart(fig_heat, use_container_width=True)

        hora_pico = heatmap_data.groupby("HORA_INICIO")["Atenciones"].sum().idxmax()
        dia_pico = heatmap_data.groupby("DIA_SEMANA_ES")["Atenciones"].sum().idxmax()
        st.markdown(render_insight(
            "Hallazgo: Horarios Pico",
            f"La mayor concentraci\u00f3n de atenciones se registra los <b>{dia_pico}</b> a las <b>{int(hora_pico)}:00 hrs</b>. "
            f"Se recomienda reforzar la dotaci\u00f3n t\u00e9cnica en este horario para optimizar tiempos de respuesta.",
        ), unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)

    with col1:
        st.markdown('<div class="section-title">Top 20 Modelos m\u00e1s Atendidos</div>', unsafe_allow_html=True)
        modelo_data = df[df["MODELO"] != ""]["MODELO"].value_counts().head(20).reset_index()
        modelo_data.columns = ["Modelo", "Atenciones"]
        fig_modelos = px.bar(modelo_data, x="Atenciones", y="Modelo", orientation="h",
                             color_discrete_sequence=[COLORS["navy"]], text="Atenciones")
        fig_modelos.update_traces(textposition="outside", cliponaxis=False)
        fig_modelos.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=550, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_modelos, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Distribuci\u00f3n del Tiempo de Atenci\u00f3n</div>', unsafe_allow_html=True)
        df_tiempo = df[df["MINUTOS_ATENCION"] > 0]
        if len(df_tiempo) > 0:
            fig_hist = px.histogram(df_tiempo, x="MINUTOS_ATENCION", nbins=30,
                                    color_discrete_sequence=[COLORS["purple"]], labels={"MINUTOS_ATENCION": "Minutos"})
            fig_hist.update_layout(**PLOTLY_LAYOUT, xaxis_title="Minutos de Atenci\u00f3n", yaxis_title="Frecuencia", height=550, margin=dict(t=20, b=20))
            st.plotly_chart(fig_hist, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Motivo por marca
    st.markdown('<div class="section-title">Motivo de Atenci\u00f3n por Marca</div>', unsafe_allow_html=True)
    df_marca_motivo = df[(df["MARCA"] != "") & (df["MOTIVO"] != "")]
    if len(df_marca_motivo) > 0:
        marca_motivo = df_marca_motivo.groupby(["MARCA", "MOTIVO"]).size().reset_index(name="Cantidad")
        top_marcas = df_marca_motivo["MARCA"].value_counts().head(10).index.tolist()
        marca_motivo = marca_motivo[marca_motivo["MARCA"].isin(top_marcas)]
        fig_stacked = px.bar(marca_motivo, x="MARCA", y="Cantidad", color="MOTIVO",
                             color_discrete_sequence=COLOR_SEQUENCE, barmode="stack")
        fig_stacked.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Atenciones", margin=dict(t=20, b=20), height=400,
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_stacked, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Tasa de garantia por marca
    st.markdown('<div class="section-title">Tasa de Garant\u00eda por Marca</div>', unsafe_allow_html=True)
    df_marcas_valid = df[df["MARCA"] != ""]
    if len(df_marcas_valid) > 0:
        garantia_por_marca = df_marcas_valid.groupby("MARCA").apply(
            lambda x: pd.Series({
                "Total": len(x),
                "Garantias": len(x[x["MOTIVO"] == "GARANTIA"]),
                "Tasa_Garantia": len(x[x["MOTIVO"] == "GARANTIA"]) / len(x) * 100 if len(x) > 0 else 0
            })
        ).reset_index()
        garantia_por_marca = garantia_por_marca[garantia_por_marca["Total"] >= 10].sort_values("Tasa_Garantia", ascending=False)

        if len(garantia_por_marca) > 0:
            col_g1, col_g2 = st.columns([2, 1])
            with col_g1:
                fig_garant = px.bar(garantia_por_marca, x="MARCA", y="Tasa_Garantia",
                                    color="Tasa_Garantia", color_continuous_scale=["#059669", "#D97706", "#DC2626"],
                                    text=garantia_por_marca["Tasa_Garantia"].apply(lambda x: f"{x:.1f}%"))
                fig_garant.update_traces(textposition="outside", cliponaxis=False)
                fig_garant.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="% Garant\u00eda", margin=dict(t=20, b=20), height=350, showlegend=False)
                st.plotly_chart(fig_garant, use_container_width=True)
            with col_g2:
                st.markdown("**Detalle por Marca**")
                display_df = garantia_por_marca[["MARCA", "Total", "Garantias", "Tasa_Garantia"]].copy()
                display_df["Tasa_Garantia"] = display_df["Tasa_Garantia"].apply(lambda x: f"{x:.1f}%")
                display_df.columns = ["Marca", "Total", "Garant\u00edas", "% Garant\u00eda"]
                st.dataframe(display_df, use_container_width=True, hide_index=True)

    # Top 10 modelos con mayor tiempo acumulado
    st.markdown('<div class="section-title">Top 10 Modelos con Mayor Tiempo Acumulado</div>', unsafe_allow_html=True)
    df_modelo_tiempo = df[(df["MODELO"] != "") & (df["MINUTOS_ATENCION"] > 0)]
    if len(df_modelo_tiempo) > 0:
        modelo_tiempo = df_modelo_tiempo.groupby("MODELO").agg(
            Tiempo_Total=("MINUTOS_ATENCION", "sum"),
            Atenciones=("MINUTOS_ATENCION", "count"),
            Tiempo_Promedio=("MINUTOS_ATENCION", "mean")
        ).reset_index().sort_values("Tiempo_Total", ascending=False).head(10)
        modelo_tiempo["Tiempo_Promedio"] = modelo_tiempo["Tiempo_Promedio"].round(1)
        modelo_tiempo["Horas_Total"] = (modelo_tiempo["Tiempo_Total"] / 60).round(1)
        display_mt = modelo_tiempo[["MODELO", "Atenciones", "Tiempo_Total", "Horas_Total", "Tiempo_Promedio"]].copy()
        display_mt.columns = ["Modelo", "Atenciones", "Min. Totales", "Hrs. Totales", "Prom. (min)"]
        st.dataframe(display_mt, use_container_width=True, hide_index=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Hallazgos del perito tecnico
    st.markdown('<div class="section-title">Hallazgos del Perito T\u00e9cnico</div>', unsafe_allow_html=True)
    total = len(df)
    homologaciones = len(df[df["MOTIVO"] == "HOMOLOGACION"])
    pct_homologacion = homologaciones / total * 100 if total > 0 else 0
    pct_remoto = len(df[df["TIPO DE ATENCION"] == "REMOTO"]) / total * 100 if total > 0 else 0
    df_tiempo_valid = df[df["MINUTOS_ATENCION"] > 0]
    remoto_prom = df_tiempo_valid[df_tiempo_valid["TIPO DE ATENCION"] == "REMOTO"]["MINUTOS_ATENCION"].mean() if len(df_tiempo_valid[df_tiempo_valid["TIPO DE ATENCION"] == "REMOTO"]) > 0 else 0
    presencial_prom = df_tiempo_valid[df_tiempo_valid["TIPO DE ATENCION"] == "PRESENCIAL"]["MINUTOS_ATENCION"].mean() if len(df_tiempo_valid[df_tiempo_valid["TIPO DE ATENCION"] == "PRESENCIAL"]) > 0 else 0

    st.markdown(render_insight(
        "1. An\u00e1lisis de Horarios Pico y Dotaci\u00f3n de Personal",
        f"El <b>{pct_remoto:.1f}%</b> de las atenciones se realizan de forma remota, "
        f"con un tiempo promedio de <b>{remoto_prom:.0f} minutos</b> por atenci\u00f3n remota versus "
        f"<b>{presencial_prom:.0f} minutos</b> por atenci\u00f3n presencial. "
        f"La concentraci\u00f3n de demanda en horarios matutinos (9:00-12:00) sugiere la necesidad de "
        f"escalonar los turnos t\u00e9cnicos para cubrir adecuadamente los picos de solicitudes.",
    ), unsafe_allow_html=True)

    top_garant_marca = df[df["MOTIVO"] == "GARANTIA"]["MARCA"].value_counts()
    top_garant_modelo = df[df["MOTIVO"] == "GARANTIA"]["MODELO"].value_counts().head(5)
    if len(top_garant_marca) > 0:
        top_g_marca = top_garant_marca.index[0]
        top_g_count = top_garant_marca.iloc[0]
        modelos_list = ", ".join([f"<b>{m}</b> ({c})" for m, c in zip(top_garant_modelo.index, top_garant_modelo.values)])
        st.markdown(render_insight(
            "2. Productos con Mayor Incidencia de Garant\u00eda (Alerta de Calidad)",
            f"La marca <b>{top_g_marca}</b> concentra <b>{top_g_count}</b> casos de garant\u00eda. "
            f"Los modelos con mayor incidencia son: {modelos_list}. "
            f"Se recomienda elevar un reporte al fabricante con el an\u00e1lisis estad\u00edstico de fallas por modelo y serie.",
            "warning"
        ), unsafe_allow_html=True)

    st.markdown(render_insight(
        "3. Eficiencia: Atenci\u00f3n Remota vs Presencial",
        f"La atenci\u00f3n remota promedia <b>{remoto_prom:.0f} min</b> por caso, mientras que la presencial "
        f"promedia <b>{presencial_prom:.0f} min</b>. "
        f"{'La atenci\u00f3n remota es m\u00e1s eficiente en tiempo, lo que sugiere potenciar este canal para casos de diagn\u00f3stico y consulta t\u00e9cnica.' if remoto_prom < presencial_prom else 'La atenci\u00f3n presencial muestra tiempos comparables, lo que indica que los casos presenciales requieren manipulaci\u00f3n f\u00edsica del equipo.'} "
        f"Se recomienda implementar un protocolo de triaje donde los casos de garant\u00eda inicien siempre con diagn\u00f3stico remoto.",
        "success"
    ), unsafe_allow_html=True)

    st.markdown(render_insight(
        "4. Carga de Trabajo en Homologaciones",
        f"Las homologaciones de equipos en MTC representan <b>{pct_homologacion:.1f}%</b> del total de atenciones "
        f"(<b>{homologaciones}</b> registros). Esta es una actividad interna de Kroton que consume tiempo t\u00e9cnico "
        f"significativo. Se recomienda evaluar si este proceso puede optimizarse mediante plantillas estandarizadas "
        f"o la asignaci\u00f3n de un t\u00e9cnico dedicado exclusivamente a homologaciones.",
        "danger"
    ), unsafe_allow_html=True)


# ============================================================
# TAB 3: ANALISIS EJECUTIVO
# ============================================================
def tab_analisis_ejecutivo(df):
    st.markdown('<div class="main-header"><h1>An\u00e1lisis Ejecutivo</h1><p>Informe estrat\u00e9gico para la Gerencia Comercial y Direcci\u00f3n General</p></div>', unsafe_allow_html=True)

    total = len(df)
    df_tiempo = df[df["MINUTOS_ATENCION"] > 0]
    eficiencia = df_tiempo["MINUTOS_ATENCION"].mean() if len(df_tiempo) > 0 else 0
    tasa_garantia = len(df[df["MOTIVO"] == "GARANTIA"]) / total * 100 if total > 0 else 0
    canales_activos = df[df["CANAL"] != ""]["CANAL"].nunique()
    tecnicos_list = df[df["TECNICO"] != ""]["TECNICO"].unique()
    productividad_promedio = total / len(tecnicos_list) if len(tecnicos_list) > 0 else 0

    c1, c2, c3, c4 = st.columns(4)
    with c1:
        st.markdown(render_kpi_card("Eficiencia Operativa", f"{eficiencia:.0f} min", "", "Tiempo promedio por atenci\u00f3n"), unsafe_allow_html=True)
    with c2:
        st.markdown(render_kpi_card("Tasa de Garant\u00edas", f"{tasa_garantia:.1f}%", "red", f"{len(df[df['MOTIVO'] == 'GARANTIA']):,} de {total:,}"), unsafe_allow_html=True)
    with c3:
        st.markdown(render_kpi_card("Canales Activos", f"{canales_activos}", "cyan", "Canales de venta"), unsafe_allow_html=True)
    with c4:
        st.markdown(render_kpi_card("Productividad/T\u00e9cnico", f"{productividad_promedio:,.0f}", "green", "Atenciones promedio"), unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Rendimiento por Vendedor</div>', unsafe_allow_html=True)
        vendedor_data = df[df["VENDEDOR"] != ""]["VENDEDOR"].value_counts().head(15).reset_index()
        vendedor_data.columns = ["Vendedor", "Atenciones"]
        fig_vendedor = px.bar(vendedor_data, x="Atenciones", y="Vendedor", orientation="h",
                              color_discrete_sequence=[COLORS["navy"]], text="Atenciones")
        fig_vendedor.update_traces(textposition="outside", cliponaxis=False)
        fig_vendedor.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=450, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_vendedor, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Top 15 Clientes por Atenciones</div>', unsafe_allow_html=True)
        cliente_data = df[df["CLIENTE"] != ""]["CLIENTE"].value_counts().head(15).reset_index()
        cliente_data.columns = ["Cliente", "Atenciones"]
        fig_clientes = px.bar(cliente_data, x="Atenciones", y="Cliente", orientation="h",
                              color_discrete_sequence=[COLORS["purple"]], text="Atenciones")
        fig_clientes.update_traces(textposition="outside", cliponaxis=False)
        fig_clientes.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=450, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_clientes, use_container_width=True)

    col3, col4 = st.columns(2)
    with col3:
        st.markdown('<div class="section-title">Distribuci\u00f3n por Canal</div>', unsafe_allow_html=True)
        canal_data = df[df["CANAL"] != ""]["CANAL"].value_counts().reset_index()
        canal_data.columns = ["Canal", "Atenciones"]
        fig_canal = px.bar(canal_data, x="Canal", y="Atenciones", color="Canal",
                           color_discrete_sequence=COLOR_SEQUENCE, text="Atenciones")
        fig_canal.update_traces(textposition="outside", cliponaxis=False)
        fig_canal.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=400, margin=dict(t=20, b=20), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_canal, use_container_width=True)

    with col4:
        st.markdown('<div class="section-title">Evoluci\u00f3n Mensual por Motivo</div>', unsafe_allow_html=True)
        evol_data = df[(df["MOTIVO"] != "") & (df["MES"] != "")].groupby(["MES", "MES_ORDEN", "MOTIVO"]).size().reset_index(name="Cantidad")
        evol_data = evol_data.sort_values("MES_ORDEN")
        fig_evol = px.bar(evol_data, x="MES", y="Cantidad", color="MOTIVO", barmode="group",
                          color_discrete_sequence=COLOR_SEQUENCE,
                          text="Cantidad")
        fig_evol.update_traces(textposition="outside", textfont_size=10, cliponaxis=False)
        fig_evol.update_layout(**PLOTLY_LAYOUT, height=420, margin=dict(t=20, b=20), xaxis_title="", yaxis_title="Atenciones",
                               legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1),
                               bargap=0.15, bargroupgap=0.05)
        st.plotly_chart(fig_evol, use_container_width=True)

    # Treemap
    st.markdown('<div class="section-title">Mapa de Clientes por Canal</div>', unsafe_allow_html=True)
    df_tree = df[(df["CLIENTE"] != "") & (df["CANAL"] != "")]
    if len(df_tree) > 0:
        tree_data = df_tree.groupby(["CANAL", "CLIENTE"]).size().reset_index(name="Atenciones")
        tree_data = tree_data[tree_data["Atenciones"] >= 3]
        if len(tree_data) > 0:
            fig_tree = px.treemap(tree_data, path=["CANAL", "CLIENTE"], values="Atenciones",
                                  color="Atenciones", color_continuous_scale=["#DBEAFE", "#1E40AF"])
            fig_tree.update_layout(font=dict(family="Inter, sans-serif"), height=450, margin=dict(t=20, b=20))
            st.plotly_chart(fig_tree, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Informe para la gerencia
    st.markdown('<div class="section-title">Informe para la Gerencia</div>', unsafe_allow_html=True)

    preventa_count = len(df[df["MOTIVO"] == "PREVENTA"])
    config_count = len(df[df["MOTIVO"] == "CONFIGURACION"])
    capacitacion_count = len(df[df["MOTIVO"] == "CAPACITACION"])
    canal_minorista = len(df[df["CANAL"] == "MINORISTA"])
    canal_integrador = len(df[df["CANAL"] == "INTEGRADOR"])

    st.markdown(render_insight(
        "Resumen Ejecutivo",
        f"Durante el per\u00edodo analizado, el CET proces\u00f3 <b>{total:,}</b> atenciones t\u00e9cnicas, "
        f"atendiendo a <b>{df[df['CLIENTE'] != '']['CLIENTE'].nunique()}</b> clientes \u00fanicos a trav\u00e9s de "
        f"<b>{len(tecnicos_list)}</b> t\u00e9cnicos especializados. "
        f"El tiempo promedio de atenci\u00f3n fue de <b>{eficiencia:.0f} minutos</b>. "
        f"Las garant\u00edas representan el <b>{tasa_garantia:.1f}%</b> de la carga operativa.",
    ), unsafe_allow_html=True)

    st.markdown(render_insight(
        "Oportunidades Comerciales Identificadas",
        f"<b>Preventa:</b> {preventa_count} atenciones de preventa indican un flujo activo de oportunidades comerciales. "
        f"Cada consulta de preventa es un lead calificado que debe ser rastreado hasta el cierre.<br>"
        f"<b>Capacitaci\u00f3n:</b> Con {capacitacion_count} sesiones, existe oportunidad de monetizar este servicio como valor agregado.<br>"
        f"<b>Configuraci\u00f3n:</b> Las {config_count} configuraciones representan clientes activos candidatos para upselling.<br>"
        f"<b>Canal Integrador:</b> Con {canal_integrador} atenciones, este canal de alto valor debe ser priorizado con soporte premium.",
        "success"
    ), unsafe_allow_html=True)

    top_g = df[df["MOTIVO"] == "GARANTIA"]["MARCA"].value_counts().head(3)
    marcas_riesgo = ", ".join([f"<b>{m}</b> ({c} casos)" for m, c in zip(top_g.index, top_g.values)])
    st.markdown(render_insight(
        "An\u00e1lisis de Riesgo: Garant\u00edas por Marca",
        f"Las marcas con mayor volumen de garant\u00edas son: {marcas_riesgo}. "
        f"Se recomienda: (1) Negociar con fabricantes la absorci\u00f3n de costos de diagn\u00f3stico, "
        f"(2) Implementar un programa de certificaci\u00f3n de integradores, "
        f"(3) Crear una base de conocimiento con las fallas m\u00e1s frecuentes.",
        "warning"
    ), unsafe_allow_html=True)

    top_vendedores = df[df["VENDEDOR"] != ""]["VENDEDOR"].value_counts().head(5)
    vendedores_list = ", ".join([f"<b>{v}</b> ({c})" for v, c in zip(top_vendedores.index, top_vendedores.values)])
    st.markdown(render_insight(
        "Rendimiento de Vendedores",
        f"Los vendedores con mayor generaci\u00f3n de atenciones t\u00e9cnicas son: {vendedores_list}. "
        f"Se recomienda cruzar estos datos con las ventas cerradas para determinar la tasa de conversi\u00f3n.",
    ), unsafe_allow_html=True)

    st.markdown(render_insight(
        "Estrategia de Canales",
        f"<b>Minorista ({canal_minorista} atenciones):</b> Canal dominante. Automatizar diagn\u00f3sticos frecuentes.<br>"
        f"<b>Integrador ({canal_integrador} atenciones):</b> Canal de alto valor. Implementar partners certificados con SLAs diferenciados.",
        "success"
    ), unsafe_allow_html=True)


# ============================================================
# TAB 4: PRODUCTIVIDAD
# ============================================================
def tab_productividad(df):
    st.markdown('<div class="main-header"><h1>Productividad del Equipo T\u00e9cnico</h1><p>An\u00e1lisis de rendimiento individual y comparativo del equipo de soporte</p></div>', unsafe_allow_html=True)

    tecnicos = df[df["TECNICO"] != ""]["TECNICO"].unique()
    df_tiempo = df[df["MINUTOS_ATENCION"] > 0]

    cols_per_row = min(len(tecnicos), 4)
    if cols_per_row > 0:
        cols = st.columns(cols_per_row)
        for i, tec in enumerate(sorted(tecnicos)):
            df_tec = df[df["TECNICO"] == tec]
            df_tec_t = df_tiempo[df_tiempo["TECNICO"] == tec]
            total_tec = len(df_tec)
            prom_tec = df_tec_t["MINUTOS_ATENCION"].mean() if len(df_tec_t) > 0 else 0
            top_motivo = df_tec[df_tec["MOTIVO"] != ""]["MOTIVO"].value_counts().index[0] if len(df_tec[df_tec["MOTIVO"] != ""]) > 0 else "N/A"
            variant = ["", "red", "cyan", "green"][i % 4]
            with cols[i % cols_per_row]:
                st.markdown(render_kpi_card(tec, f"{total_tec:,} atenciones", variant, f"Prom: {prom_tec:.0f} min | {top_motivo}"), unsafe_allow_html=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Atenciones por T\u00e9cnico por Mes</div>', unsafe_allow_html=True)
        tec_mes = df[(df["TECNICO"] != "") & (df["MES"] != "")].groupby(["TECNICO", "MES", "MES_ORDEN"]).size().reset_index(name="Atenciones")
        tec_mes = tec_mes.sort_values("MES_ORDEN")
        fig_tec_mes = px.bar(tec_mes, x="MES", y="Atenciones", color="TECNICO", barmode="group",
                             color_discrete_sequence=COLOR_SEQUENCE, text="Atenciones")
        fig_tec_mes.update_traces(textposition="outside", cliponaxis=False)
        fig_tec_mes.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Atenciones", height=420, margin=dict(t=20, b=20),
                                  legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1))
        st.plotly_chart(fig_tec_mes, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Distribuci\u00f3n de Tiempo por T\u00e9cnico</div>', unsafe_allow_html=True)
        if len(df_tiempo[df_tiempo["TECNICO"] != ""]) > 0:
            fig_box = px.box(df_tiempo[df_tiempo["TECNICO"] != ""], x="TECNICO", y="MINUTOS_ATENCION",
                             color="TECNICO", color_discrete_sequence=COLOR_SEQUENCE,
                             labels={"MINUTOS_ATENCION": "Minutos", "TECNICO": "T\u00e9cnico"})
            fig_box.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=420, margin=dict(t=20, b=20), xaxis_title="", yaxis_title="Minutos")
            st.plotly_chart(fig_box, use_container_width=True)

    # Radar chart
    st.markdown('<div class="section-title">Perfil Comparativo de T\u00e9cnicos</div>', unsafe_allow_html=True)
    radar_data = []
    for tec in sorted(tecnicos):
        df_tec = df[df["TECNICO"] == tec]
        df_tec_t = df_tiempo[df_tiempo["TECNICO"] == tec]
        radar_data.append({
            "T\u00e9cnico": tec,
            "Atenciones": len(df_tec),
            "Tiempo Prom.": df_tec_t["MINUTOS_ATENCION"].mean() if len(df_tec_t) > 0 else 0,
            "Marcas": df_tec[df_tec["MARCA"] != ""]["MARCA"].nunique(),
            "Motivos": df_tec[df_tec["MOTIVO"] != ""]["MOTIVO"].nunique(),
            "Clientes": df_tec[df_tec["CLIENTE"] != ""]["CLIENTE"].nunique()
        })
    radar_df = pd.DataFrame(radar_data)

    if len(radar_df) > 0:
        categories = ["Atenciones", "Tiempo Prom.", "Marcas", "Motivos", "Clientes"]
        fig_radar = go.Figure()
        for i, row in radar_df.iterrows():
            values = []
            for cat in categories:
                max_val = radar_df[cat].max()
                values.append(row[cat] / max_val * 100 if max_val > 0 else 0)
            values.append(values[0])
            fig_radar.add_trace(go.Scatterpolar(
                r=values, theta=categories + [categories[0]], fill="toself",
                name=row["T\u00e9cnico"], line=dict(color=COLOR_SEQUENCE[i % len(COLOR_SEQUENCE)])
            ))
        fig_radar.update_layout(
            polar=dict(radialaxis=dict(visible=True, range=[0, 100])),
            font=dict(family="Inter, sans-serif"), height=450, margin=dict(t=30, b=30),
            legend=dict(orientation="h", yanchor="bottom", y=-0.15, xanchor="center", x=0.5)
        )
        st.plotly_chart(fig_radar, use_container_width=True)

    # Tabla
    st.markdown('<div class="section-title">Estad\u00edsticas Detalladas por T\u00e9cnico</div>', unsafe_allow_html=True)
    if len(radar_data) > 0:
        stats_df = pd.DataFrame(radar_data)
        stats_df["Tiempo Prom."] = stats_df["Tiempo Prom."].round(1)
        st.dataframe(stats_df, use_container_width=True, hide_index=True)

    # Balance de carga
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    if len(radar_df) > 0:
        max_tec = radar_df.loc[radar_df["Atenciones"].idxmax(), "T\u00e9cnico"]
        max_atenciones = radar_df["Atenciones"].max()
        min_tec = radar_df.loc[radar_df["Atenciones"].idxmin(), "T\u00e9cnico"]
        min_atenciones = radar_df["Atenciones"].min()
        ratio = max_atenciones / min_atenciones if min_atenciones > 0 else 0
        st.markdown(render_insight(
            "Balance de Carga de Trabajo",
            f"Existe un desbalance de <b>{ratio:.1f}x</b> entre el t\u00e9cnico con mayor carga "
            f"(<b>{max_tec}</b>: {max_atenciones:,} atenciones) y el de menor carga "
            f"(<b>{min_tec}</b>: {min_atenciones:,} atenciones). "
            f"Se recomienda redistribuir la asignaci\u00f3n de casos.",
            "warning"
        ), unsafe_allow_html=True)


# ============================================================
# TAB 5: MARCAS Y PRODUCTOS
# ============================================================
def tab_marcas_productos(df):
    st.markdown('<div class="main-header"><h1>Marcas y Productos</h1><p>An\u00e1lisis profundo del portafolio de productos y marcas atendidas</p></div>', unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Participaci\u00f3n por Marca</div>', unsafe_allow_html=True)
        marca_data = df[df["MARCA"] != ""]["MARCA"].value_counts().reset_index()
        marca_data.columns = ["Marca", "Atenciones"]
        total_marcas = marca_data["Atenciones"].sum()
        marca_data["Porcentaje"] = (marca_data["Atenciones"] / total_marcas * 100).round(1)
        marca_data["Label"] = marca_data.apply(lambda r: f"{r['Atenciones']} ({r['Porcentaje']}%)", axis=1)
        fig_marca_bar = px.bar(marca_data, x="Atenciones", y="Marca", orientation="h",
                               color_discrete_sequence=[COLORS["navy"]], text="Label")
        fig_marca_bar.update_traces(textposition="outside", cliponaxis=False)
        fig_marca_bar.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=420, margin=dict(t=20, b=20, r=100), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_marca_bar, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Top 15 Productos m\u00e1s Atendidos</div>', unsafe_allow_html=True)
        modelo_data = df[df["MODELO"] != ""]["MODELO"].value_counts().head(15).reset_index()
        modelo_data.columns = ["Modelo", "Atenciones"]
        fig_top_mod = px.bar(modelo_data, x="Atenciones", y="Modelo", orientation="h",
                             color_discrete_sequence=[COLORS["purple"]], text="Atenciones")
        fig_top_mod.update_traces(textposition="outside", cliponaxis=False)
        fig_top_mod.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=420, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_top_mod, use_container_width=True)

    # Heatmap marca vs motivo
    st.markdown('<div class="section-title">Marca vs Motivo de Atenci\u00f3n</div>', unsafe_allow_html=True)
    df_mm = df[(df["MARCA"] != "") & (df["MOTIVO"] != "")]
    if len(df_mm) > 0:
        top_marcas_list = df_mm["MARCA"].value_counts().head(10).index.tolist()
        df_mm_filtered = df_mm[df_mm["MARCA"].isin(top_marcas_list)]
        heat_data = df_mm_filtered.groupby(["MARCA", "MOTIVO"]).size().reset_index(name="Cantidad")
        heat_pivot = heat_data.pivot_table(index="MARCA", columns="MOTIVO", values="Cantidad", fill_value=0)
        fig_heat2 = px.imshow(heat_pivot, aspect="auto",
                              color_continuous_scale=["#F8FAFC", "#93C5FD", "#1E40AF"],
                              labels=dict(x="Motivo", y="Marca", color="Atenciones"))
        fig_heat2.update_layout(**PLOTLY_LAYOUT, height=380, margin=dict(t=20, b=20))
        st.plotly_chart(fig_heat2, use_container_width=True)

    # Sunburst
    st.markdown('<div class="section-title">Jerarqu\u00eda: Marca / L\u00ednea / Modelo</div>', unsafe_allow_html=True)
    df_sun = df[(df["MARCA"] != "") & (df["LINEA"] != "") & (df["MODELO"] != "")]
    if len(df_sun) > 0:
        sun_data = df_sun.groupby(["MARCA", "LINEA", "MODELO"]).size().reset_index(name="Atenciones")
        sun_data = sun_data[sun_data["Atenciones"] >= 2]
        if len(sun_data) > 0:
            fig_sun = px.sunburst(sun_data, path=["MARCA", "LINEA", "MODELO"], values="Atenciones",
                                  color_discrete_sequence=COLOR_SEQUENCE)
            fig_sun.update_layout(font=dict(family="Inter, sans-serif"), height=500, margin=dict(t=20, b=20))
            st.plotly_chart(fig_sun, use_container_width=True)

    # Productos con mas garantias
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Productos con Mayor Incidencia de Garant\u00eda</div>', unsafe_allow_html=True)
    df_garant = df[(df["MOTIVO"] == "GARANTIA") & (df["MODELO"] != "")]
    if len(df_garant) > 0:
        garant_prod = df_garant.groupby(["MODELO", "MARCA"]).size().reset_index(name="Garantias")
        garant_prod = garant_prod.sort_values("Garantias", ascending=False).head(20)
        garant_prod.columns = ["Modelo", "Marca", "Casos de Garant\u00eda"]
        st.dataframe(garant_prod, use_container_width=True, hide_index=True)

    if len(marca_data) > 0:
        top_marca = marca_data.iloc[0]
        pct_top = top_marca["Atenciones"] / marca_data["Atenciones"].sum() * 100
        st.markdown(render_insight(
            "Concentraci\u00f3n de Marca",
            f"<b>{top_marca['Marca']}</b> domina con el <b>{pct_top:.1f}%</b> de las atenciones totales "
            f"({top_marca['Atenciones']} casos). Esta concentraci\u00f3n indica dependencia de una sola marca. "
            f"Se recomienda diversificar el portafolio de servicios.",
        ), unsafe_allow_html=True)


# ============================================================
# TAB 6: CLIENTES
# ============================================================
def tab_clientes(df):
    st.markdown('<div class="main-header"><h1>An\u00e1lisis de Clientes</h1><p>Segmentaci\u00f3n y comportamiento de la cartera de clientes</p></div>', unsafe_allow_html=True)

    df_clientes = df[df["CLIENTE"] != ""].copy()

    col1, col2 = st.columns(2)
    with col1:
        st.markdown('<div class="section-title">Top 20 Clientes por Atenciones</div>', unsafe_allow_html=True)
        top_cli = df_clientes["CLIENTE"].value_counts().head(20).reset_index()
        top_cli.columns = ["Cliente", "Atenciones"]
        fig_cli = px.bar(top_cli, x="Atenciones", y="Cliente", orientation="h",
                         color_discrete_sequence=[COLORS["navy"]], text="Atenciones")
        fig_cli.update_traces(textposition="outside", cliponaxis=False)
        fig_cli.update_layout(**PLOTLY_LAYOUT, yaxis=dict(autorange="reversed"), height=550, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_cli, use_container_width=True)

    with col2:
        st.markdown('<div class="section-title">Atenciones por Canal</div>', unsafe_allow_html=True)
        canal_cli = df_clientes[df_clientes["CANAL"] != ""]["CANAL"].value_counts().reset_index()
        canal_cli.columns = ["Canal", "Atenciones"]
        fig_canal_cli = px.bar(canal_cli, x="Atenciones", y="Canal", orientation="h",
                               color="Canal", color_discrete_sequence=COLOR_SEQUENCE, text="Atenciones")
        fig_canal_cli.update_traces(textposition="outside", cliponaxis=False)
        fig_canal_cli.update_layout(**PLOTLY_LAYOUT, showlegend=False, height=350, margin=dict(t=20, b=20, r=70), xaxis_title="", yaxis_title="")
        st.plotly_chart(fig_canal_cli, use_container_width=True)

        st.markdown('<div class="section-title">Clientes \u00danicos por Canal</div>', unsafe_allow_html=True)
        uniq_canal = df_clientes[df_clientes["CANAL"] != ""].groupby("CANAL")["CLIENTE"].nunique().reset_index()
        uniq_canal.columns = ["Canal", "Clientes \u00danicos"]
        st.dataframe(uniq_canal, use_container_width=True, hide_index=True)

    # Scatter
    st.markdown('<div class="section-title">Segmentaci\u00f3n: Atenciones vs Tiempo Promedio</div>', unsafe_allow_html=True)
    df_cli_tiempo = df_clientes[df_clientes["MINUTOS_ATENCION"] > 0]
    if len(df_cli_tiempo) > 0:
        cli_agg = df_cli_tiempo.groupby("CLIENTE").agg(
            Total_Atenciones=("MINUTOS_ATENCION", "count"),
            Tiempo_Promedio=("MINUTOS_ATENCION", "mean")
        ).reset_index()
        cli_agg["Tiempo_Promedio"] = cli_agg["Tiempo_Promedio"].round(1)
        cli_agg = cli_agg[cli_agg["Total_Atenciones"] >= 3]
        if len(cli_agg) > 0:
            fig_scatter = px.scatter(cli_agg, x="Total_Atenciones", y="Tiempo_Promedio",
                                    size="Total_Atenciones", hover_name="CLIENTE",
                                    color_discrete_sequence=[COLORS["navy"]],
                                    labels={"Total_Atenciones": "Total Atenciones", "Tiempo_Promedio": "Tiempo Promedio (min)"})
            fig_scatter.update_layout(**PLOTLY_LAYOUT, height=400, margin=dict(t=20, b=20))
            st.plotly_chart(fig_scatter, use_container_width=True)

    # Tabla detallada
    st.markdown('<div class="section-title">Detalle de Clientes</div>', unsafe_allow_html=True)
    if len(df_clientes) > 0:
        cli_detail = df_clientes.groupby("CLIENTE").agg(
            Total_Atenciones=("FECHA", "count"),
            Canal=("CANAL", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "N/A"),
            Marca_Principal=("MARCA", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "N/A"),
            Motivo_Principal=("MOTIVO", lambda x: x.mode().iloc[0] if len(x.mode()) > 0 else "N/A"),
        ).reset_index()
        cli_time = df_cli_tiempo.groupby("CLIENTE")["MINUTOS_ATENCION"].mean().reset_index()
        cli_time.columns = ["CLIENTE", "Tiempo_Prom"]
        cli_detail = cli_detail.merge(cli_time, on="CLIENTE", how="left")
        cli_detail["Tiempo_Prom"] = cli_detail["Tiempo_Prom"].round(1).fillna(0)
        cli_detail = cli_detail.sort_values("Total_Atenciones", ascending=False).head(50)
        cli_detail.columns = ["Cliente", "Atenciones", "Canal", "Marca Principal", "Motivo Principal", "Tiempo Prom. (min)"]
        st.dataframe(cli_detail, use_container_width=True, hide_index=True)

    # Clientes con mayor tasa de garantia
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Clientes con Mayor Tasa de Garant\u00eda</div>', unsafe_allow_html=True)
    if len(df_clientes) > 0:
        cli_garant = df_clientes.groupby("CLIENTE").apply(
            lambda x: pd.Series({
                "Total": len(x),
                "Garantias": len(x[x["MOTIVO"] == "GARANTIA"]),
                "Tasa": len(x[x["MOTIVO"] == "GARANTIA"]) / len(x) * 100 if len(x) > 0 else 0
            })
        ).reset_index()
        cli_garant = cli_garant[cli_garant["Total"] >= 5].sort_values("Tasa", ascending=False).head(15)
        cli_garant["Tasa"] = cli_garant["Tasa"].round(1)
        cli_garant.columns = ["Cliente", "Total Atenciones", "Garant\u00edas", "% Garant\u00eda"]
        cli_garant["% Garant\u00eda"] = cli_garant["% Garant\u00eda"].apply(lambda x: f"{x}%")
        st.dataframe(cli_garant, use_container_width=True, hide_index=True)

    st.markdown(render_insight(
        "Segmentaci\u00f3n de Clientes",
        "Los clientes con alta frecuencia de atenciones y alto porcentaje de garant\u00edas representan un segmento "
        "de riesgo que requiere intervenci\u00f3n proactiva: capacitaci\u00f3n en instalaci\u00f3n, verificaci\u00f3n de condiciones "
        "de almacenamiento y revisi\u00f3n de los procesos de venta.",
        "warning"
    ), unsafe_allow_html=True)


# ============================================================
# TAB 7: INDICADORES KPI
# ============================================================
def tab_indicadores_kpi(df):
    st.markdown('<div class="main-header"><h1>Indicadores KPI</h1><p>Panel de indicadores clave de rendimiento operativo</p></div>', unsafe_allow_html=True)

    total = len(df)
    df_tiempo = df[df["MINUTOS_ATENCION"] > 0]

    st.markdown('<div class="section-title">Cumplimiento de SLA</div>', unsafe_allow_html=True)

    pct_30 = pct_60 = pct_sobre_60 = 0
    if len(df_tiempo) > 0:
        bajo_30 = len(df_tiempo[df_tiempo["MINUTOS_ATENCION"] <= 30])
        bajo_60 = len(df_tiempo[df_tiempo["MINUTOS_ATENCION"] <= 60])
        sobre_60 = len(df_tiempo[df_tiempo["MINUTOS_ATENCION"] > 60])
        pct_30 = bajo_30 / len(df_tiempo) * 100
        pct_60 = bajo_60 / len(df_tiempo) * 100
        pct_sobre_60 = sobre_60 / len(df_tiempo) * 100
        mediana = df_tiempo["MINUTOS_ATENCION"].median()

        c1, c2, c3, c4 = st.columns(4)
        with c1:
            st.markdown(render_kpi_card("Hasta 30 minutos", f"{pct_30:.1f}%", "green", f"{bajo_30:,} atenciones"), unsafe_allow_html=True)
        with c2:
            st.markdown(render_kpi_card("Hasta 60 minutos", f"{pct_60:.1f}%", "cyan", f"{bajo_60:,} atenciones"), unsafe_allow_html=True)
        with c3:
            st.markdown(render_kpi_card("M\u00e1s de 60 minutos", f"{pct_sobre_60:.1f}%", "red", f"{sobre_60:,} atenciones"), unsafe_allow_html=True)
        with c4:
            st.markdown(render_kpi_card("Mediana", f"{mediana:.0f} min", "", "Tiempo mediano"), unsafe_allow_html=True)

        # Gauges
        col1, col2, col3 = st.columns(3)
        with col1:
            fig_g1 = go.Figure(go.Indicator(mode="gauge+number", value=pct_30,
                title={"text": "SLA 30 min", "font": {"family": "Inter", "size": 16}}, number={"suffix": "%"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": COLORS["green"]},
                       "steps": [{"range": [0, 50], "color": "#FEE2E2"}, {"range": [50, 75], "color": "#FEF3C7"}, {"range": [75, 100], "color": "#D1FAE5"}],
                       "threshold": {"line": {"color": COLORS["red"], "width": 3}, "value": 80}}))
            fig_g1.update_layout(height=250, margin=dict(t=50, b=20), font=dict(family="Inter"))
            st.plotly_chart(fig_g1, use_container_width=True)

        with col2:
            dias_unicos = df["FECHA"].nunique()
            prod_diaria = total / dias_unicos if dias_unicos > 0 else 0
            fig_g2 = go.Figure(go.Indicator(mode="gauge+number", value=pct_60,
                title={"text": "SLA 60 min", "font": {"family": "Inter", "size": 16}}, number={"suffix": "%"},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": COLORS["cyan"]},
                       "steps": [{"range": [0, 60], "color": "#FEE2E2"}, {"range": [60, 85], "color": "#FEF3C7"}, {"range": [85, 100], "color": "#D1FAE5"}],
                       "threshold": {"line": {"color": COLORS["red"], "width": 3}, "value": 90}}))
            fig_g2.update_layout(height=250, margin=dict(t=50, b=20), font=dict(family="Inter"))
            st.plotly_chart(fig_g2, use_container_width=True)

        with col3:
            dias_unicos = df["FECHA"].nunique()
            prod_diaria = total / dias_unicos if dias_unicos > 0 else 0
            fig_g3 = go.Figure(go.Indicator(mode="gauge+number", value=prod_diaria,
                title={"text": "Atenciones/D\u00eda", "font": {"family": "Inter", "size": 16}},
                gauge={"axis": {"range": [0, max(50, prod_diaria * 1.5)]}, "bar": {"color": COLORS["navy"]},
                       "steps": [{"range": [0, prod_diaria * 0.5], "color": "#FEE2E2"}, {"range": [prod_diaria * 0.5, prod_diaria], "color": "#FEF3C7"}, {"range": [prod_diaria, prod_diaria * 1.5], "color": "#D1FAE5"}]}))
            fig_g3.update_layout(height=250, margin=dict(t=50, b=20), font=dict(family="Inter"))
            st.plotly_chart(fig_g3, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Capacidad diaria
    st.markdown('<div class="section-title">Utilizaci\u00f3n de Capacidad Diaria</div>', unsafe_allow_html=True)
    daily_data = df.groupby("FECHA").size().reset_index(name="Atenciones")
    daily_data = daily_data.sort_values("FECHA")
    if len(daily_data) > 0:
        avg_daily = daily_data["Atenciones"].mean()
        fig_daily = px.bar(daily_data, x="FECHA", y="Atenciones", color_discrete_sequence=[COLORS["navy"]])
        fig_daily.add_hline(y=avg_daily, line_dash="dash", line_color=COLORS["red"], annotation_text=f"Promedio: {avg_daily:.1f}")
        fig_daily.update_layout(**PLOTLY_LAYOUT, xaxis_title="Fecha", yaxis_title="Atenciones", height=350, margin=dict(t=20, b=20))
        st.plotly_chart(fig_daily, use_container_width=True)

    # Crecimiento mensual
    st.markdown('<div class="section-title">Crecimiento Mensual</div>', unsafe_allow_html=True)
    mes_growth = df.groupby(["MES", "MES_ORDEN"]).size().reset_index(name="Atenciones")
    mes_growth = mes_growth.sort_values("MES_ORDEN")
    if len(mes_growth) > 1:
        mes_growth["Crecimiento"] = mes_growth["Atenciones"].pct_change() * 100
        mes_growth["Crecimiento"] = mes_growth["Crecimiento"].fillna(0).round(1)

        col_g1, col_g2 = st.columns(2)
        with col_g1:
            fig_growth = px.bar(mes_growth, x="MES", y="Atenciones", color_discrete_sequence=[COLORS["navy"]], text="Atenciones")
            fig_growth.update_traces(textposition="outside", cliponaxis=False)
            fig_growth.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="Atenciones", height=350, margin=dict(t=20, b=20))
            st.plotly_chart(fig_growth, use_container_width=True)

        with col_g2:
            fig_pct = px.bar(mes_growth[mes_growth["MES_ORDEN"] > 1], x="MES", y="Crecimiento",
                             color="Crecimiento", color_continuous_scale=["#DC2626", "#D97706", "#059669"],
                             text=mes_growth[mes_growth["MES_ORDEN"] > 1]["Crecimiento"].apply(lambda x: f"{x:+.1f}%"))
            fig_pct.update_traces(textposition="outside", cliponaxis=False)
            fig_pct.update_layout(**PLOTLY_LAYOUT, xaxis_title="", yaxis_title="% Crecimiento", height=350, margin=dict(t=20, b=20), showlegend=False)
            st.plotly_chart(fig_pct, use_container_width=True)

    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)

    # Indice de equidad
    st.markdown('<div class="section-title">\u00cdndice de Equidad en Distribuci\u00f3n de Carga</div>', unsafe_allow_html=True)
    tecnicos_load = df[df["TECNICO"] != ""].groupby("TECNICO").size()
    equidad = 0
    if len(tecnicos_load) > 1:
        values = sorted(tecnicos_load.values)
        n = len(values)
        cumulative = np.cumsum(values)
        total_sum = cumulative[-1]
        gini = (2 * sum((i + 1) * v for i, v in enumerate(values)) - (n + 1) * total_sum) / (n * total_sum) if total_sum > 0 else 0
        equidad = (1 - gini) * 100

        c1, c2 = st.columns([1, 2])
        with c1:
            fig_eq = go.Figure(go.Indicator(mode="gauge+number", value=equidad,
                title={"text": "\u00cdndice de Equidad", "font": {"family": "Inter", "size": 16}},
                number={"suffix": "%", "font": {"size": 36, "color": COLORS["navy"]}},
                gauge={"axis": {"range": [0, 100]}, "bar": {"color": COLORS["green"] if equidad > 70 else COLORS["amber"]},
                       "steps": [{"range": [0, 50], "color": "#FEE2E2"}, {"range": [50, 75], "color": "#FEF3C7"}, {"range": [75, 100], "color": "#D1FAE5"}]}))
            fig_eq.update_layout(height=300, margin=dict(t=50, b=40), font=dict(family="Inter"))
            st.plotly_chart(fig_eq, use_container_width=True)

        with c2:
            st.markdown(render_insight(
                "Interpretaci\u00f3n del \u00cdndice de Equidad",
                f"El \u00edndice de equidad en la distribuci\u00f3n de carga es <b>{equidad:.1f}%</b> "
                f"(donde 100% = distribuci\u00f3n perfectamente equitativa). "
                f"{'La distribuci\u00f3n de carga es razonablemente equitativa.' if equidad > 75 else 'Existe un desbalance significativo en la distribuci\u00f3n de carga entre t\u00e9cnicos.'}"
                f"<br><br><b>Carga por t\u00e9cnico:</b><br>"
                + "<br>".join([f"&bull; <b>{tec}</b>: {count:,} atenciones" for tec, count in tecnicos_load.sort_values(ascending=False).items()]),
                "success" if equidad > 75 else "warning"
            ), unsafe_allow_html=True)

    # Resumen KPIs
    st.markdown('<div class="custom-divider"></div>', unsafe_allow_html=True)
    st.markdown('<div class="section-title">Resumen de Indicadores Clave</div>', unsafe_allow_html=True)

    if len(df_tiempo) > 0:
        kpi_summary = pd.DataFrame({
            "Indicador": [
                "Total de Atenciones", "Tiempo Promedio de Atenci\u00f3n", "Mediana de Tiempo",
                "Desviaci\u00f3n Est\u00e1ndar del Tiempo", "% Atenciones hasta 30 min", "% Atenciones hasta 60 min",
                "Clientes \u00danicos Atendidos", "T\u00e9cnicos Activos",
                "Atenciones por D\u00eda (promedio)", "Tasa de Garant\u00eda", "\u00cdndice de Equidad de Carga",
            ],
            "Valor": [
                f"{total:,}", f"{df_tiempo['MINUTOS_ATENCION'].mean():.1f} minutos",
                f"{df_tiempo['MINUTOS_ATENCION'].median():.0f} minutos",
                f"{df_tiempo['MINUTOS_ATENCION'].std():.1f} minutos",
                f"{pct_30:.1f}%", f"{pct_60:.1f}%",
                f"{df[df['CLIENTE'] != '']['CLIENTE'].nunique()}",
                f"{df[df['TECNICO'] != '']['TECNICO'].nunique()}",
                f"{total / df['FECHA'].nunique():.1f}" if df["FECHA"].nunique() > 0 else "N/A",
                f"{len(df[df['MOTIVO'] == 'GARANTIA']) / total * 100:.1f}%",
                f"{equidad:.1f}%",
            ]
        })
        st.dataframe(kpi_summary, use_container_width=True, hide_index=True)


# ============================================================
# APP PRINCIPAL
# ============================================================
def main():
    if "authenticated" not in st.session_state:
        st.session_state["authenticated"] = False

    if not st.session_state["authenticated"]:
        show_login()
        return

    try:
        df = load_data()
    except Exception as e:
        st.error(f"Error al cargar los datos: {e}")
        return

    filtered_df = render_sidebar(df)

    if len(filtered_df) == 0:
        st.warning("No hay datos para los filtros seleccionados. Ajuste los filtros en la barra lateral.")
        return

    tab1, tab2, tab3, tab4, tab5, tab6, tab7 = st.tabs([
        "Dashboard General",
        "An\u00e1lisis Ejecutivo",
        "Productividad",
        "Marcas y Productos",
        "Clientes",
        "Indicadores KPI",
        "An\u00e1lisis T\u00e9cnico"
    ])

    with tab1:
        tab_dashboard_general(filtered_df)
    with tab2:
        tab_analisis_ejecutivo(filtered_df)
    with tab3:
        tab_productividad(filtered_df)
    with tab4:
        tab_marcas_productos(filtered_df)
    with tab5:
        tab_clientes(filtered_df)
    with tab6:
        tab_indicadores_kpi(filtered_df)
    with tab7:
        tab_analisis_tecnico(filtered_df)

    st.markdown("""
    <div class="footer-text">
        CET Analytics Dashboard v1.0 · Desarrollado para <b>Kroton SAC</b> · Centro de Entrenamiento Tecnol\u00f3gico
    </div>
    """, unsafe_allow_html=True)


if __name__ == "__main__":
    main()
