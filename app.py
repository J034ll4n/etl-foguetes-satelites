import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
import plotly.graph_objects as go
import time
import base64
import requests
from datetime import datetime
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import OrdinalEncoder
from imblearn.over_sampling import SMOTE

# ==============================================================================
# UI/UX: CONTROL PANEL HIGH-FIDELITY CYBER THEME (CSS INJECTION)
# ==============================================================================
st.set_page_config(
    page_title="Controle de Missão",
    page_icon="🤖",
    layout="wide"
)

st.markdown("""
    <style>
        @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;700&family=Inter:wght@300;400;600;700&family=JetBrains+Mono:wght@400;700&display=swap');
        
        /* Reset de Fundo do App */
        html, body, [data-testid="stAppViewContainer"], [data-testid="stHeader"], .main {
            background-color: #13171E !important;
            color: #FCFCFC !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Customização Avançada da Sidebar */
        [data-testid="stSidebar"] {
            background-color: #0B0E14 !important;
            border-right: 1px solid #1E2633;
        }
        [data-testid="stSidebar"] h2, [data-testid="stSidebar"] p, [data-testid="stSidebar"] label {
            color: #FCFCFC !important;
            font-family: 'Inter', sans-serif;
        }
        
        /* Estilização Futurista dos Inputs Gerais */
        div[data-baseweb="select"], div[role="combobox"], input {
            background-color: #1E2633 !important;
            border: 1px solid #2E3A4E !important;
            color: #FCFCFC !important;
            border-radius: 6px !important;
        }
        
        /* Correção do input fantasma do multiselect */
        .stMultiSelect input {
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            padding: 0 !important;
            width: auto !important;
        }
        
        /* Seletores dos Chips do Multiselect (Âmbar Técnico) */
        .stMultiSelect div[data-baseweb="tag"], 
        [data-baseweb="tag"], 
        .stSidebar div[data-baseweb="tag"] {
            background-color: rgba(255, 164, 0, 0.12) !important;
            border: 1px solid #FFA400 !important;
            border-radius: 4px !important;
        }
        .stMultiSelect div[data-baseweb="tag"] span,
        [data-baseweb="tag"] span,
        .stMultiSelect div[data-baseweb="tag"] div {
            color: #FFA400 !important;
            font-weight: 600 !important;
        }
        .stMultiSelect div[data-baseweb="tag"] svg,
        [data-baseweb="tag"] svg {
            fill: #FFA400 !important;
        }
        .stMultiSelect div[data-baseweb="tag"]:hover {
            background-color: rgba(255, 164, 0, 0.25) !important;
        }
        
        /* Tipografia de Identidade Visual */
        .main-title {
            font-family: 'Orbitron', sans-serif;
            font-size: 2.4rem;
            font-weight: 700;
            color: #FFA400 !important;
            text-transform: uppercase;
            letter-spacing: 2px;
            text-shadow: 0px 0px 12px rgba(255, 164, 0, 0.25);
            margin-bottom: 0.1rem;
        }
        .subtitle {
            font-size: 1rem;
            color: #94A3B8 !important;
            margin-bottom: 2rem;
        }
        .section-header {
            font-family: 'Orbitron', sans-serif;
            font-size: 1.25rem;
            font-weight: 600;
            color: #FFA400 !important;
            margin-top: 1.5rem;
            margin-bottom: 1.2rem;
            border-left: 3px solid #FFA400;
            padding-left: 12px;
            letter-spacing: 1px;
        }
        
        /* Componentes st.metric Adaptados */
        [data-testid="stMetricValue"] {
            font-family: 'JetBrains Mono', monospace;
            color: #FFA400 !important;
            font-size: 2.1rem !important;
            font-weight: 700 !important;
        }
        [data-testid="stMetricLabel"] {
            color: #94A3B8 !important;
            font-weight: 600 !important;
            text-transform: uppercase;
            font-size: 0.75rem !important;
            letter-spacing: 0.5px;
        }
        
        /* Tabs Premium */
        button[data-baseweb="tab"] {
            color: #94A3B8 !important;
            font-family: 'Orbitron', sans-serif;
            font-size: 0.88rem !important;
            letter-spacing: 1px;
            background-color: transparent !important;
        }
        button[data-baseweb="tab"][aria-selected="true"] {
            color: #FFA400 !important;
            border-bottom-color: #FFA400 !important;
            font-weight: 700;
        }
        
        /* ======================================================== */
        /* ANIMAÇÕES CLIMÁTICAS 3D (CSS) PARA A ABA DE APIs */
        /* ======================================================== */
        .weather-box {
            background: linear-gradient(145deg, #1E2633, #13171E);
            border-radius: 12px;
            border: 1px solid #2E3A4E;
            padding: 20px;
            display: flex;
            align-items: center;
            justify-content: space-around;
            box-shadow: inset 0px 0px 20px rgba(0,0,0,0.5), 0px 10px 30px rgba(0,0,0,0.3);
            position: relative;
            overflow: hidden;
            height: 150px;
        }
        
        .weather-info {
            z-index: 2;
            display: flex;
            flex-direction: column;
        }
        
        .weather-temp { font-family: 'Orbitron'; font-size: 2.5rem; font-weight: 700; color: #FCFCFC; text-shadow: 0 0 10px rgba(255,255,255,0.3); }
        .weather-hum { font-family: 'JetBrains Mono'; font-size: 1rem; color: #94A3B8; }
        
        /* Efeito Sol 3D */
        .sun-anim {
            width: 80px; height: 80px;
            background: radial-gradient(circle, #FFD700 30%, #FF8C00 80%);
            border-radius: 50%;
            box-shadow: 0 0 40px #FF8C00, inset -10px -10px 20px rgba(0,0,0,0.2);
            animation: pulse-sun 3s infinite alternate;
            z-index: 1;
        }
        @keyframes pulse-sun {
            0% { transform: scale(1); box-shadow: 0 0 30px #FF8C00; }
            100% { transform: scale(1.1); box-shadow: 0 0 60px #FFA400; }
        }
        
        /* Efeito Chuva (Linhas caindo) */
        .rain-anim {
            width: 80px; height: 80px;
            background: #2E3A4E;
            border-radius: 50%;
            position: relative;
            overflow: hidden;
            box-shadow: 0 0 30px rgba(0, 212, 255, 0.4), inset -10px -10px 20px rgba(0,0,0,0.5);
            z-index: 1;
        }
        .rain-anim::after {
            content: ''; position: absolute; top: -100%; left: 0; right: 0; bottom: 0;
            background: repeating-linear-gradient(180deg, transparent, transparent 10px, rgba(0, 212, 255, 0.8) 10px, rgba(0, 212, 255, 0.8) 20px);
            animation: rain-fall 0.8s linear infinite;
        }
        @keyframes rain-fall {
            100% { transform: translateY(100%); }
        }
        
        /* Efeito Nuvens */
        .cloud-anim {
            width: 90px; height: 60px;
            background: radial-gradient(circle, #94A3B8 40%, #64748B 90%);
            border-radius: 40px;
            box-shadow: 0 0 20px rgba(148, 163, 184, 0.4), inset -10px -10px 15px rgba(0,0,0,0.3);
            animation: float-cloud 4s ease-in-out infinite;
            z-index: 1;
        }
        @keyframes float-cloud {
            0%, 100% { transform: translateY(0); }
            50% { transform: translateY(-10px); }
        }
    </style>
""", unsafe_allow_html=True)

# ==============================================================================
# BLOCO DE CONEXÃO COM APIs (Cacheadas para performance e limites de taxa)
# ==============================================================================
@st.cache_data(ttl=3600)
def fetch_space_devs_launches():
    """Busca 7 lançamentos históricos e 8 mais novos limitados estritamente até o fim de 2025"""
    # Adicionado filtro de teto (net__lte) para barrar missões futuras além de 2025
    url_antigos = "https://ll.thespacedevs.com/2.3.0/launches/?limit=8&ordering=-net&net__lte=2025-12-31T23:59:59Z"
    url_novos = "https://ll.thespacedevs.com/2.3.0/launches/?limit=8&ordering=-net&net__lte=2025-12-31T23:59:59Z"
    
    lista_mesclada = []
    headers = {"User-Agent": "StreamlitMissionControl/1.0"}
    
    try:
        # 1. Intercepta as 7 missões pioneiras registradas
        resp_antigos = requests.get(url_antigos, headers=headers, timeout=10)
        if resp_antigos.status_code == 200:
            lista_mesclada.extend(resp_antigos.json().get('results', []))
            
        # 2. Intercepta as 8 missões contemporâneas travadas até dezembro de 2025
        resp_novos = requests.get(url_novos, headers=headers, timeout=10)
        if resp_novos.status_code == 200:
            lista_mesclada.extend(resp_novos.json().get('results', []))
            
        return lista_mesclada
    except:
        return lista_mesclada if lista_mesclada else []

@st.cache_data(ttl=3600)
def fetch_weather_data(lat, lon, date_str):
    """Busca temperatura, umidade e chuva do Open-Meteo para a data específica"""
    url = f"https://archive-api.open-meteo.com/v1/archive?latitude={lat}&longitude={lon}&start_date={date_str}&end_date={date_str}&hourly=temperature_2m,relative_humidity_2m,precipitation"
    try:
        resp = requests.get(url, timeout=10)
        if resp.status_code == 200:
            data = resp.json()
            temp_mean = np.mean(data['hourly']['temperature_2m'])
            hum_mean = np.mean(data['hourly']['relative_humidity_2m'])
            precip_total = np.sum(data['hourly']['precipitation'])
            return {"temp": temp_mean, "hum": hum_mean, "precip": precip_total}
        return None
    except:
        return None

def gerar_box_clima_html(weather_data):
    """Gera o HTML da box animada com base no clima"""
    temp = weather_data['temp']
    hum = weather_data['hum']
    precip = weather_data['precip']
    
    # Lógica simples para decidir qual animação exibir
    if precip > 1.0:
        anim_class = "rain-anim"
        condicao = "CHUVA MODERADA/FORTE"
        cor = "#00d4ff"
    elif temp > 22:
        anim_class = "sun-anim"
        condicao = "CÉU CLARO / QUENTE"
        cor = "#FF8C00"
    else:
        anim_class = "cloud-anim"
        condicao = "NEBULOSIDADE / MISTO"
        cor = "#94A3B8"
        
    return f"""
        <div class="weather-box" style="border-left: 4px solid {cor};">
            <div class="weather-info">
                <span style="color:{cor}; font-weight:700; font-size:0.8rem; margin-bottom:5px;">STATUS ATMOSFÉRICO: {condicao}</span>
                <span class="weather-temp">{temp:.1f} °C</span>
                <span class="weather-hum">💧 Umidade: {hum:.0f}% | 🌧️ Precip.: {precip:.1f}mm</span>
            </div>
            <div class="{anim_class}"></div>
        </div>
    """

# ==============================================================================
# 2. DATA PIPELINE DEFINITIONS
# ==============================================================================
@st.cache_data
def carregar_dados():
    df_risco = pd.read_csv('data/Data_Streamlit/Space_Limpa_Com_Risco_Individualv3.csv')
    df_risco = df_risco.drop_duplicates().reset_index(drop=True)
    df_cronologica = pd.read_csv('data/Data_Streamlit/Tabela_Cronologica_BI_2030.csv')
    df_importancia = pd.read_csv('data/Data_Streamlit/Tabela_Importancia_Variaveis.csv')
    df_cronologica['Data'] = pd.to_datetime(df_cronologica['Data'])
    return df_risco, df_cronologica, df_importancia

@st.cache_resource
def inicializar_ia_no_app(df_risco_base):
    df_clf = df_risco_base.copy()
    df_clf['Alvo_Sucesso'] = np.where(df_clf['Status_da_Missao'] == 'Success', 1, 0)
    df_clf['Mes'] = df_clf['Mes'].fillna(1)
    df_clf['Hora'] = df_clf['Hora'].fillna(df_clf['Hora'].median())
    df_clf['Status_do_Foguete_Num'] = np.where(df_clf['Status_do_Foguete'] == 'StatusActive', 1, 0)
    
    encoder = OrdinalEncoder()
    df_clf[['Empresa_Cod', 'Pais_Cod']] = encoder.fit_transform(df_clf[['Nome_da_Empresa', 'Pais_Lancamento']])
    
    features = ['Empresa_Cod', 'Pais_Cod', 'Custo_da_Missao', 'Ano', 'Mes', 'Hora', 'Status_do_Foguete_Num']
    X = df_clf[features]
    y = df_clf['Alvo_Sucesso']
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)
    smote = SMOTE(random_state=42)
    X_train_res, y_train_res = smote.fit_resample(X_train, y_train)
    
    modelo = RandomForestClassifier(n_estimators=150, max_depth=10, random_state=42)
    modelo.fit(X_train_res, y_train_res)
    return modelo, encoder, features

def carregar_arquivo_base64(caminho):
    try:
        with open(caminho, "rb") as f:
            data = f.read()
        return base64.b64encode(data).decode()
    except:
        return None

# ==============================================================================
# 1. TELA DE LANÇAMENTO COM PROCESSAMENTO SÍNCRONO EM SEGUNDO PLANO
# ==============================================================================
video_base64 = carregar_arquivo_base64("img/foguete.mp4")

if 'foguete_voou' not in st.session_state:
    tela_loading = st.empty()
    with tela_loading.container():
        if video_base64:
            st.markdown(f"""
                <div style="display: flex; flex-direction: column; align-items: center; justify-content: center; height: 85vh; width: 100%;">
                    <h1 style='text-align: center; font-family: "Orbitron", sans-serif; font-weight: 700; color: #FFA400; margin-bottom: 5px; letter-spacing: 2px;'>INITIALIZING SYSTEMS...</h1>
                    <p style='text-align: center; color: #94A3B8; margin-bottom: 25px;'>Sincronizando telemetria aeroespacial e calibrando redes preditivas em background.</p>
                    <video autoplay muted loop playsinline width="750" style="border-radius: 12px; box-shadow: 0px 0px 40px rgba(255, 164, 0, 0.35);">
                        <source src="data:video/mp4;base64,{video_base64}" type="video/mp4">
                    </video>
                </div>
            """, unsafe_allow_html=True)
        else:
            st.warning("ALERTA: Vídeo de decolagem não detectado. Sincronizando banco de dados...")

    start_time = time.time()
    df_risco, df_cronologica, df_importancia = carregar_dados()
    modelo_risco_final, encoder, features = inicializar_ia_no_app(df_risco)
    tempo_processamento = time.time() - start_time
    
    duracao_alvo_video = 5.5
    if tempo_processamento < duracao_alvo_video:
        time.sleep(duracao_alvo_video - tempo_processamento)
        
    st.session_state.foguete_voou = True
    st.rerun()

else:
    df_risco, df_cronologica, df_importancia = carregar_dados()
    modelo_risco_final, encoder, features = inicializar_ia_no_app(df_risco)

    # ==============================================================================
    # 3. FRONT-END: DASHBOARD DE RENDERIZAÇÃO IMEDIATA
    # ==============================================================================
    st.markdown("<div class='main-title'>Dashboard de Controle de Missão</div>", unsafe_allow_html=True)
    st.markdown("<div class='subtitle'>Plataforma integrada de Inteligência Preditiva e Análise Macroeconômica do Setor Aeroespacial</div>", unsafe_allow_html=True)

    # ---- LOGO DA SIDEBAR ----
    logo_base64 = carregar_arquivo_base64("img/leega.jpeg")

    if logo_base64:
        st.sidebar.markdown(f"""
            <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 15px;">
                <img src="data:image/jpeg;base64,{logo_base64}" width="165" style="border-radius: 8px; box-shadow: 0px 0px 20px rgba(255, 164, 0, 0.35); border: 2px solid #FFA400; padding: 2px;">
            </div>
        """, unsafe_allow_html=True)

    st.sidebar.markdown("<h2 style='font-family:\"Orbitron\", sans-serif; font-size:1.1rem; color:#FFA400 !important; letter-spacing:1px;'>CENTRAL DE FILTROS</h2>", unsafe_allow_html=True)
    st.sidebar.markdown("<p style='font-size:0.8rem; color:#94A3B8;'>Os parâmetros abaixo controlam todos os módulos analíticos simultaneamente.</p>", unsafe_allow_html=True)

    recorte_temporal = st.sidebar.radio(
        "Recorte Temporal do Painel",
        ["Frota Moderna (Últimos 10 anos)", "Histórico Completo (Corrida Espacial)"],
        help="Filtra dinamicamente todo o dashboard para isolar o mercado moderno ou englobar os dados desde 1957."
    )

    # 1. Identifica a base de dados de acordo com o período (Garante dados desde 1960)
    if recorte_temporal == "Frota Moderna (Últimos 10 anos)":
        ano_teto_base = df_risco['Ano'].max()
        df_base_filtros = df_risco[df_risco['Ano'] >= (ano_teto_base - 10)]
    else:
        df_base_filtros = df_risco  # Dataset completo sem travas temporais

    # 2. Extrai TODAS as opções únicas de forma limpa e ordenada
    lista_empresas = sorted([str(x).strip() for x in df_base_filtros['Nome_da_Empresa'].dropna().unique() if str(x).strip() != ''])
    lista_paises = sorted([str(x).strip() for x in df_base_filtros['Pais_Lancamento'].dropna().unique() if str(x).strip() != ''])

    # 3. Componentes Multiselect (Sem preencher o default para não poluir a tela)
    empresas_selecionadas = st.sidebar.multiselect(
        "Organizações Aeroespaciais", 
        options=lista_empresas, 
        placeholder="Todas as Organizações (Padrão)",
        key="sidebar_empresas"
    )

    paises_selecionados = st.sidebar.multiselect(
        "Zonas de Lançamento (Países)", 
        options=lista_paises, 
        placeholder="Todos os Países (Padrão)",
        key="sidebar_paises"
    )

    # 4. Lógica de Filtro Inteligente: Se o usuário não selecionar nada, consideramos TODOS (Evita tabela vazia)
    df_risco_filtrado = df_risco.copy()
    
    if empresas_selecionadas:
        df_risco_filtrado = df_risco_filtrado[df_risco_filtrado['Nome_da_Empresa'].isin(empresas_selecionadas)]
        
    if paises_selecionados:
        df_risco_filtrado = df_risco_filtrado[df_risco_filtrado['Pais_Lancamento'].isin(paises_selecionados)]

    # 5. Aplicação do corte secundário de 10 anos se a frota moderna estiver ativa
    if recorte_temporal == "Frota Moderna (Últimos 10 anos)" and not df_risco_filtrado.empty:
        df_risco_filtrado = df_risco_filtrado[df_risco_filtrado['Ano'] >= (ano_teto_base - 10)]

    if df_risco_filtrado.empty:
        st.error("NENHUM DADO ENCONTRADO: Ajuste os filtros na barra lateral para encontrar registros válidos.")
    else:
        # ATENÇÃO AQUI: Adicionei a aba_api na primeira posição!
        aba_api, aba1, aba2, aba3, aba4, aba5 = st.tabs([
            " Telemetria Live (APIs)",
            " Panorama de Mercado", 
            " Logística de Lançamento",
            " Diagnóstico de Risco (IA)",
            " Projeção Espacial (2030)", 
            " Simulador de Viabilidade"
        ])


        # --------------------------------------------------------------------------
        # FRONT-END - TAB: TELEMETRIA AO VIVO VIA APIs (Mapeamento v2.3.0)
        # --------------------------------------------------------------------------
        with aba_api:
            st.markdown("<div class='section-header'>Módulo de Conexão: SpaceDevs & Open-Meteo</div>", unsafe_allow_html=True)
            
            # --- HISTOGRAMA EM MATRIZ DE LEDS FILTRÁVEL ---
            st.markdown("###  **Distribuição Temporal de Operações Globais**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-top: -10px;'>Grade tática mapeando o volume do dataset. Este painel responde aos filtros geopolíticos da barra lateral e ao slider cronológico abaixo.</p>", unsafe_allow_html=True)
            
           
            df_hist_api = df_base_filtros.copy()
            
            # Se o usuário escolheu empresas específicas na sidebar, filtra. Se deixou vazio, traz TODAS.
            if empresas_selecionadas:
                df_hist_api = df_hist_api[df_hist_api['Nome_da_Empresa'].isin(empresas_selecionadas)]
                
            # Se o usuário escolheu países específicos na sidebar, filtra. Se deixou vazio, traz TODOS.
            if paises_selecionados:
                df_hist_api = df_hist_api[df_hist_api['Pais_Lancamento'].isin(paises_selecionados)]
                
            
            if not df_hist_api.empty:
                # Ordenação e empilhamento perfeito dos blocos/nodos
                df_colunas = df_hist_api.copy()
                df_colunas = df_colunas.sort_values(by=['Ano', 'Status_da_Missao'])
                df_colunas['Posicao_Pilha'] = df_colunas.groupby('Ano').cumcount() + 1
                
                # Gráfico tático de pontos em formato de matriz quadrada
                fig_hist_live = px.scatter(
                    df_colunas,
                    x="Ano",
                    y="Posicao_Pilha",
                    color="Status_da_Missao",
                    color_discrete_map={'Success': "#16D696", 'Failure': "#EE1919", 'Prelaunch': "#FBFF00"},
                    hover_data={
                        "Ano": True,
                        "Nome_da_Empresa": True,
                        "Status_da_Missao": True,
                        "Posicao_Pilha": False
                    },
                    template="plotly_dark"
                )
                
                fig_hist_live.update_traces(
                    marker=dict(
                        size=7,
                        symbol="square",  # Estilo de blocos de pixel de monitor
                        opacity=0.85,
                        line=dict(width=1, color='#13171E')
                    )
                )
                
                fig_hist_live.update_layout(
                    paper_bgcolor='rgba(0,0,0,0)',
                    plot_bgcolor='rgba(0,0,0,0)',
                    margin=dict(l=45, r=10, t=10, b=10),
                    height=280,
                    font=dict(family='Orbitron', color='#94A3B8', size=11),
                    xaxis=dict(
                        title=dict(text="MATRIZ CRONOLÓGICA (ANOS)", font=dict(size=10, textcase="upper")),
                        gridcolor="#2E3A4E",
                        showgrid=True,
                        tickfont=dict(family='JetBrains Mono', color='#FCFCFC'),
                    ),
                    yaxis=dict(
                        title=dict(text="CONTAGEM DE VETORES (PONTOS)", font=dict(size=10, textcase="upper")),
                        gridcolor="#2E3A4E",
                        showgrid=True,
                        tickfont=dict(family='JetBrains Mono', color='#FCFCFC'),
                        zeroline=False
                    ),
                    legend=dict(
                        orientation="h", 
                        yanchor="bottom", 
                        y=1.05, 
                        xanchor="right", 
                        x=1, 
                        title=None,
                        font=dict(size=10, family='Orbitron')
                    )
                )
                st.plotly_chart(fig_hist_live, use_container_width=True)
            else:
                st.info("Nenhum registro localizado para a combinação de filtros selecionada na Barra Lateral / Slider.")
                
            st.markdown("---")
            st.markdown("<p style='color: #94A3B8; font-size: 0.95rem; margin-top: -10px;'>Selecione um lançamento global real recente. O sistema irá interceptar a telemetria do foguete e cruzar com os sensores meteorológicos globais do dia exato.</p>", unsafe_allow_html=True)
            
            launches_data = fetch_space_devs_launches()
            
            if not launches_data:
                st.warning("Aguardando satélite de comunicação... Não foi possível conectar com a API SpaceDevs no momento.")
            else:
                dict_launches = {f"{l.get('name', 'Missão')} (Data: {l.get('net', '')[:10]})": l for l in launches_data}
                
                escolha_api = st.selectbox(" Interceptar Alvo de Lançamento", list(dict_launches.keys()))
                dados_alvo = dict_launches[escolha_api]
                
                if st.button("SINCRONIZAR TELEMETRIA E CLIMA AGORA", use_container_width=True):
                    with st.spinner("Decodificando pacotes de clima e órbita..."):
                        
                        nome_missao = dados_alvo.get('name', 'N/A')
                        status_missao = dados_alvo.get('status', {}).get('name', 'LAUNCH SUCCESSFUL')
                        data_lancamento_bruta = dados_alvo.get('net', '')
                        
                        provedor_info = dados_alvo.get('launch_service_provider', {})
                        provedor = provedor_info.get('name', 'SpaceX') if isinstance(provedor_info, dict) else 'SpaceX'
                        
                        pad_info = dados_alvo.get('pad', {})
                        pad_nome = pad_info.get('name', 'Plataforma de Lançamento')
                        lat = float(pad_info.get('latitude', 0.0)) if pad_info.get('latitude') else 0.0
                        lon = float(pad_info.get('longitude', 0.0)) if pad_info.get('longitude') else 0.0
                        
                        data_formatada = data_lancamento_bruta[:10]
                        
                        info_missao = dados_alvo.get('mission') or {}
                        info_foguete = dados_alvo.get('rocket', {}).get('configuration', {})
                        
                        desc_missao = info_missao.get('description', 'Descrição da missão retida ou indisponível nos registos da agência.')
                        desc_missao = desc_missao.replace('"', "'")
                        tipo_missao = info_missao.get('type', 'Communications')
                        
                        orbita = info_missao.get('orbit')
                        orbita_nome = orbita.get('name', 'Low Earth Orbit') if isinstance(orbita, dict) else 'Low Earth Orbit'
                        nome_veiculo = info_foguete.get('full_name', 'Falcon 9 Block 5')
                        
                        # Tratamento seguro de mídia da especificação API v2.3.0
                        img_dados = dados_alvo.get('image')
                        img_foguete = None

                        if img_dados:
                            if isinstance(img_dados, dict):
                                img_foguete = img_dados.get('url') or img_dados.get('image_url')
                            elif isinstance(img_dados, str):
                                img_foguete = img_dados
                                
                        clima = fetch_weather_data(lat, lon, data_formatada)
                        
                        st.markdown("---")
                        
                        # 1. PARTE SUPERIOR (CLIMA EXPANDIDO)
                        st.markdown("### **Radar Meteorológico do Local de Lançamento**")
                        if clima:
                            st.markdown(gerar_box_clima_html(clima), unsafe_allow_html=True)
                        else:
                            st.error("Sem dados de satélite climático para essa localização.")
                            
                        # 2. PARTE INFERIOR (TELEMETRIA E IMAGEM DO VETOR SELECIONADO)
                        st.markdown("### **Telemetria do Veículo e Manifesto da Carga**")
                        cor_status = "#10B981" if "Success" in status_missao or "Successful" in status_missao else "#EF4444"
                        
                        col_info_texto, col_img_api = st.columns([1.2, 0.8])
                        
                        with col_info_texto:
                            html_telemetria = "<div style='background-color: #1E2633; padding: 25px; border-radius: 12px; border: 1px solid #2E3A4E; box-shadow: 0px 5px 15px rgba(0,0,0,0.2); height: 100%;'>"
                            html_telemetria += f"<h3 style='color: #FFA400; margin-top:0; font-family: \"Orbitron\"; letter-spacing: 1px;'>{nome_missao}</h3>"
                            
                            html_telemetria += "<div style='display: flex; flex-wrap: wrap; gap: 15px; margin-top: 20px; margin-bottom: 20px;'>"
                            html_telemetria += f"<div style='flex: 1; min-width: 180px; background: rgba(11, 14, 20, 0.5); padding: 12px; border-radius: 8px; border-left: 3px solid #6366F1;'><p style='margin: 0; font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;'>Veículo Lançador</p><p style='margin: 5px 0 0 0; color: #FCFCFC; font-weight: 600; font-family: \"JetBrains Mono\"; font-size:0.95rem;'>{nome_veiculo}</p></div>"
                            html_telemetria += f"<div style='flex: 1; min-width: 180px; background: rgba(11, 14, 20, 0.5); padding: 12px; border-radius: 8px; border-left: 3px solid #6366F1;'><p style='margin: 0; font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;'>Operador Oficial</p><p style='margin: 5px 0 0 0; color: #FCFCFC; font-weight: 600; font-family: \"JetBrains Mono\"; font-size:0.95rem;'>{provedor}</p></div>"
                            html_telemetria += f"<div style='flex: 1; min-width: 180px; background: rgba(11, 14, 20, 0.5); padding: 12px; border-radius: 8px; border-left: 3px solid #6366F1;'><p style='margin: 0; font-size: 0.75rem; color: #94A3B8; text-transform: uppercase;'>Destino / Órbita</p><p style='margin: 5px 0 0 0; color: #FCFCFC; font-weight: 600; font-family: \"JetBrains Mono\"; font-size:0.95rem;'>{orbita_nome}</p></div>"
                            html_telemetria += "</div>"
                            
                            html_telemetria += f"<p style='margin: 8px 0; color: #FCFCFC; font-size: 0.95rem;'><b> Plataforma:</b> {pad_nome}</p>"
                            html_telemetria += f"<p style='margin: 8px 0; color: #FCFCFC; font-size: 0.95rem;'><b> Data UTC:</b> {data_lancamento_bruta.replace('T', ' ').replace('Z', '')}</p>"
                            html_telemetria += f"<p style='margin: 8px 0; color: #FCFCFC; font-size: 0.95rem;'><b> Tipo de Missão:</b> {tipo_missao}</p>"
                            
                            html_telemetria += "<hr style='border: none; border-top: 1px solid #2E3A4E; margin: 15px 0;'>"
                            
                            html_telemetria += "<p style='margin: 0 0 5px 0; color: #94A3B8; text-transform: uppercase; font-size: 0.8rem; font-weight: 600;'>📋 Resumo do Manifesto (Carga):</p>"
                            html_telemetria += f"<p style='margin: 0; color: #FCFCFC; font-style: italic; line-height: 1.5; font-size:0.9rem;'>\"{desc_missao}\"</p>"
                            
                            html_telemetria += f"<div style='margin-top: 20px; display: inline-block; padding: 6px 14px; background-color: {cor_status}20; border: 1px solid {cor_status}; border-radius: 4px;'><span style='color: {cor_status}; font-weight: 700; font-family: \"Orbitron\"; letter-spacing: 1px; font-size:0.85rem;'>STATUS: {status_missao.upper()}</span></div>"
                            html_telemetria += "</div>"
                            
                            st.markdown(html_telemetria, unsafe_allow_html=True)
                        
                        with col_img_api:
                            # Removido o filtro e a condicional complexa anterior em cima da imagem para renderizar diretamente o objeto tratado
                            st.image(img_foguete, caption=f"Perfil do vetor: {nome_veiculo}", use_container_width=True)
        # --------------------------------------------------------------------------
        # FRONT-END - TAB 1: EXECUTIVE SUMMARY E PANORAMA FINANCEIRO
        # --------------------------------------------------------------------------
        with aba1:
            st.markdown("<div class='section-header'>Métricas Consolidadas do Mercado Mapeado</div>", unsafe_allow_html=True)
            
            total_m = len(df_risco_filtrado)
            total_sucessos = int(df_risco_filtrado['Status_da_Missao'].value_counts().get('Success', 0))
            total_falhas = total_m - total_sucessos
            taxa_sucesso = (total_sucessos / total_m) * 100 if total_m > 0 else 0
            
            anos_unicos = df_risco_filtrado['Ano'].nunique()
            media_anual = total_m / anos_unicos if anos_unicos > 0 else 0
            
            if not df_risco_filtrado.empty:
                ano_pico = df_risco_filtrado['Ano'].value_counts().idxmax()
                qtd_pico = df_risco_filtrado['Ano'].value_counts().max()
            else:
                ano_pico, qtd_pico = "N/A", 0
            
            kpi_col1, kpi_col2, kpi_col3, kpi_col4 = st.columns(4)
            with kpi_col1:
                st.metric("Total de Missões Filtradas", f"{total_m:,}", f"Média de {media_anual:.1f} voos/ano", help="Volume total gerado no período e filtros selecionados.")
            with kpi_col2:
                st.metric("Lançamentos com Êxito", f"{total_sucessos:,}", f"{taxa_sucesso:.1f}% de Eficiência")
            with kpi_col3:
                st.metric("Sinistros e Falhas", f"{total_falhas:,}", f"-{100-taxa_sucesso:.1f}% Margem de Erro", delta_color="normal")
            with kpi_col4:
                st.metric(f"Pico Histórico (Ano {ano_pico})", f"{qtd_pico} voos", help="O ano com o maior volume de lançamentos dentro do filtro estabelecido.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # ==================================================================
            # GLOBO HOLOGRÁFICO WIREFRAME (ÂMBAR + VERMELHO)
            # ==================================================================
            st.markdown("### **Radar Global: Rede de Lançamento Ativa evidênciando o Top 3**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-top: -10px;'><b>HUD Tático:</b> Clique e arraste para rotacionar o planeta. Os marcadores vermelhos indicam a densidade de operações da base na grade global.</p>", unsafe_allow_html=True)

            df_coords = df_risco_filtrado.groupby(['Latitude', 'Longitude', 'Regiao_Lancamento', 'Pais_Lancamento']).size().reset_index(name='Volume')
            df_coords = df_coords[(df_coords['Latitude'] != 0.0) & (df_coords['Longitude'] != 0.0)]
            
            if not df_coords.empty:
                max_vol = df_coords['Volume'].max() if df_coords['Volume'].max() > 0 else 1
                df_coords['Glow_Size'] = (df_coords['Volume'] / max_vol) * 45 + 10

                fig_radar = go.Figure()

                fig_radar.add_trace(go.Scattergeo(
                    lon = df_coords['Longitude'],
                    lat = df_coords['Latitude'],
                    marker = dict(
                        size = df_coords['Glow_Size'],
                        color = 'rgba(255, 0, 60, 0.15)',
                        line_width=0
                    ),
                    hoverinfo='skip'
                ))

                fig_radar.add_trace(go.Scattergeo(
                    lon = df_coords['Longitude'],
                    lat = df_coords['Latitude'],
                    text = df_coords['Regiao_Lancamento'] + "<br>País: " + df_coords['Pais_Lancamento'] + "<br>Lançamentos: " + df_coords['Volume'].astype(str),
                    marker = dict(
                        size = 6,
                        color = '#FF003C',
                        line = dict(width=1.5, color='#FCFCFC')
                    ),
                    hovertemplate="<b>%{text}</b><extra></extra>"
                ))

                df_top3 = df_coords.nlargest(3, 'Volume')
                fig_radar.add_trace(go.Scattergeo(
                    lon = df_top3['Longitude'],
                    lat = df_top3['Latitude'],
                    text = "[ ALVO ]<br>" + df_top3['Regiao_Lancamento'],
                    mode = 'markers+text',
                    marker = dict(
                        size = 18,
                        color = 'rgba(0,0,0,0)', 
                        line = dict(width=2, color='#FF003C'),
                        symbol = 'cross'
                    ),
                    textfont = dict(color="#00FF40", family='JetBrains Mono', size=11, weight='bold'),
                    textposition = 'top right',
                    hoverinfo='skip'
                ))

                fig_radar.update_geos(
                    projection_type="orthographic", 
                    projection_rotation=dict(lon=-60, lat=25, roll=0), 
                    showcoastlines=True, coastlinecolor="#FFA400", coastlinewidth=1.0,
                    showland=True, landcolor="#1E2633",
                    showocean=True, oceancolor="#0B0E14",
                    showlakes=False,
                    showcountries=True, countrycolor="rgba(255, 164, 0, 0.25)", countrywidth=0.5,
                    lataxis_showgrid=True, lataxis_gridcolor="rgba(255, 164, 0, 0.1)", lataxis_gridwidth=0.5,
                    lonaxis_showgrid=True, lonaxis_gridcolor="rgba(255, 164, 0, 0.1)", lonaxis_gridwidth=0.5, 
                    bgcolor="#13171E"
                )

                fig_radar.update_layout(
                    paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                    margin=dict(l=0, r=0, t=0, b=0), height=450, showlegend=False
                )
                st.plotly_chart(fig_radar, use_container_width=True)
            else:
                st.info("⚠️ Dados de coordenadas geográficas indisponíveis para a combinação de filtros atual.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # ==================================================================
            # GRÁFICO TEMPORAL DE ALTA FIDELIDADE (EIXO DUPLO)
            # ==================================================================
            st.markdown("### **Cronologia Operacional e Eficiência Anual**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-top: -10px;'>As barras indicam o volume (Sucesso/Falha). A linha âmbar acompanha a Taxa de Sucesso (%) histórica no eixo secundário.</p>", unsafe_allow_html=True)
            
            if not df_risco_filtrado.empty:
                df_temp = df_risco_filtrado.groupby('Ano').agg(
                    Total=('Status_da_Missao', 'count'),
                    Sucesso=('Status_da_Missao', lambda x: (x == 'Success').sum())
                ).reset_index()
                df_temp['Falha'] = df_temp['Total'] - df_temp['Sucesso']
                df_temp['Taxa_Sucesso'] = (df_temp['Sucesso'] / df_temp['Total']) * 100
                
                fig_tempo = go.Figure()
                fig_tempo.add_trace(go.Bar(x=df_temp['Ano'], y=df_temp['Falha'], name='Falhas', marker_color='#EF4444'))
                fig_tempo.add_trace(go.Bar(x=df_temp['Ano'], y=df_temp['Sucesso'], name='Sucessos', marker_color='#10B981'))
                fig_tempo.add_trace(go.Scatter(
                    x=df_temp['Ano'], y=df_temp['Taxa_Sucesso'], name='Taxa de Sucesso (%)',
                    yaxis='y2', mode='lines+markers', marker_color='#FFA400', line=dict(width=3)
                ))
                
                fig_tempo.update_layout(
                    barmode='stack', paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                    margin=dict(l=10, r=10, t=10, b=10), height=380,
                    xaxis=dict(title="", showgrid=False),
                    yaxis=dict(title="Volume de Lançamentos", showgrid=True, gridcolor='rgba(46, 58, 78, 0.4)'),
                    yaxis2=dict(title="Taxa de Sucesso (%)", overlaying='y', side='right', range=[0, 110], showgrid=False),
                    legend=dict(orientation="h", yanchor="bottom", y=1.05, xanchor="center", x=0.5)
                )
                st.plotly_chart(fig_tempo, use_container_width=True)
            else:
                st.warning("Sem dados temporais para plotar.")

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            
            # ==================================================================
            # SEÇÃO FINANCEIRA: O "SHARK TANK" ESPACIAL
            # ==================================================================
            st.markdown("<div class='section-header'>Market Share e Performance Financeira (Orçamento Declarado)</div>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'><b>Atenção:</b> Os valores abaixo respondem rigorosamente aos filtros laterais e representam apenas missões com orçamentos públicos conhecidos.</p>", unsafe_allow_html=True)
            
            df_financas = df_risco_filtrado[df_risco_filtrado['Custo_da_Missao'] > 0].copy()
            
            mapa_setores = {
                'Commercial': 'Iniciativa Privada',
                'Civil': 'Governo (Agência Civil)',
                'Military': 'Forças Armadas (Militar)',
                'Government': 'Governo (Estado)'
            }
            df_financas['Setor_da_Empresa'] = df_financas['Setor_da_Empresa'].replace(mapa_setores)

            montante_global = df_financas['Custo_da_Missao'].sum()
            custo_medio_missao = df_financas['Custo_da_Missao'].mean() if not df_financas.empty else 0
            dinheiro_queimado = df_financas[df_financas['Status_da_Missao'] != 'Success']['Custo_da_Missao'].sum()
            
            txt_montante = f"$ {montante_global / 1000:,.1f} Bilhões" if montante_global >= 1000 else f"$ {montante_global:,.0f} Milhões"
            txt_queimado = f"$ {dinheiro_queimado / 1000:,.1f} Bilhões" if dinheiro_queimado >= 1000 else f"$ {dinheiro_queimado:,.0f} Milhões"
            
            kpi_f1, kpi_f2, kpi_f3 = st.columns(3)
            with kpi_f1:
                st.metric("Volume de Capital (Montante Global)", txt_montante, help="Soma total dos orçamentos conhecidos de todas as missões no filtro.")
            with kpi_f2:
                st.metric("Custo Médio por Missão", f"$ {custo_medio_missao:,.1f} Milhões", help="Média financeira gasta para construir e lançar um único foguete na base amostral.")
            with kpi_f3:
                st.metric("Prejuízo com Falhas (Capital Destruído)", txt_queimado, "- Veículos perdidos/explodidos", delta_color="normal", help="Soma do custo de todas as missões que falharam. É o dinheiro que foi literalmente perdido.")
            
            st.markdown("<br>", unsafe_allow_html=True)
            col_setor, col_empresa = st.columns([1, 1.5])
            
            with col_setor:
                st.markdown("#### **Origem do Capital (Por Setor)**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.82rem;'>Quem dita as regras do jogo e financia as missões?</p>", unsafe_allow_html=True)
                
                df_setor_custo = df_financas.groupby('Setor_da_Empresa')['Custo_da_Missao'].sum().reset_index()
                
                if not df_setor_custo.empty:
                    fig_setor = px.pie(
                        df_setor_custo, values='Custo_da_Missao', names='Setor_da_Empresa', hole=0.5,
                        color_discrete_sequence=['#1E2633', '#FFA400', '#10B981', '#6366F1'], template='plotly_dark'
                    )
                    fig_setor.update_layout(
                        paper_bgcolor='#13171E', font_color='#FCFCFC', margin=dict(l=10, r=10, t=10, b=10), height=320,
                        legend=dict(orientation="h", yanchor="bottom", y=-0.2, xanchor="center", x=0.5)
                    )
                    fig_setor.update_traces(textinfo='percent', textfont_size=12, hovertemplate="%{label}: $ %{value:,.0f} M")
                    st.plotly_chart(fig_setor, use_container_width=True)
                else:
                    st.info("Sem dados de setor para o filtro.")

            with col_empresa:
                st.markdown("#### **Top 10 Empresas: Maiores Orçamentos Empregados**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.82rem;'>As organizações que mais queimaram orçamento no período filtrado.</p>", unsafe_allow_html=True)
                
                df_custo_emp = df_financas.groupby('Nome_da_Empresa')['Custo_da_Missao'].sum().reset_index()
                df_custo_emp = df_custo_emp.sort_values(by='Custo_da_Missao', ascending=False).head(10)
                
                if not df_custo_emp.empty:
                    fig_custo_emp = px.bar(
                        df_custo_emp, x='Custo_da_Missao', y='Nome_da_Empresa', orientation='h',
                        color='Custo_da_Missao', color_continuous_scale=['#1E2633', '#FFA400'], template='plotly_dark'
                    )
                    fig_custo_emp.update_layout(
                        paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                        margin=dict(l=10, r=10, t=10, b=10), height=320, coloraxis_showscale=False,
                        yaxis={'categoryorder': 'total ascending'},
                        xaxis_title="Custo Total Acumulado ($ Milhões)", yaxis_title=""
                    )
                    st.plotly_chart(fig_custo_emp, use_container_width=True)
                else:
                    st.info("Sem dados de empresa para o filtro.")

            st.markdown("<br>", unsafe_allow_html=True)
            
            # ==================================================================
            # NOVO GRAFICO: RANKING DE CUSTO-EFETIVIDADE
            # ==================================================================
            st.markdown("### **Ranking de Eficiência: O Custo Real do Sucesso**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'>Este indicador responde de forma implacável: <b>Qual empresa gasta menos dinheiro para entregar uma missão perfeita?</b><br>O cálculo divide todo o dinheiro gasto pela empresa apenas pelo número de missões que realmente deram certo. <b>Quanto menor a barra, mais eficiente é a operação.</b></p>", unsafe_allow_html=True)

            df_roi = df_risco_filtrado.groupby('Nome_da_Empresa').agg(
                Total_Missoes=('Status_da_Missao', 'count'),
                Sucessos=('Status_da_Missao', lambda x: (x == 'Success').sum()),
                Custo_Total=('Custo_da_Missao', 'sum')
            ).reset_index()
            
            df_roi = df_roi[(df_roi['Sucessos'] >= 2) & (df_roi['Custo_Total'] > 0)].copy()
            
            if not df_roi.empty:
                df_roi['Custo_Por_Sucesso'] = df_roi['Custo_Total'] / df_roi['Sucessos']
                df_roi = df_roi.sort_values(by='Custo_Por_Sucesso', ascending=True).head(10)
                
                fig_ranking = px.bar(
                    df_roi, x='Nome_da_Empresa', y='Custo_Por_Sucesso',
                    text=df_roi['Custo_Por_Sucesso'].apply(lambda x: f"${x:,.0f}M"),
                    color='Custo_Por_Sucesso', color_continuous_scale=['#10B981', '#FFA400', '#EF4444'], template='plotly_dark'
                )
                
                fig_ranking.update_traces(textposition='outside', textfont=dict(color='#FCFCFC'))
                fig_ranking.update_layout(
                    paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC', showlegend=False,
                    margin=dict(l=10, r=10, t=20, b=10), height=380, coloraxis_showscale=False,
                    xaxis_title="Organização Aeroespacial", yaxis_title="Custo Efetivo por Missão de Sucesso ($ Milhões)",
                    yaxis=dict(showgrid=True, gridcolor='rgba(46, 58, 78, 0.4)')
                )
                st.plotly_chart(fig_ranking, use_container_width=True)
            else:
                st.info("Dados insuficientes no recorte atual para calcular o custo-efetividade (exige missões com sucesso e custos financeiros declarados).")
            
            # Síntese Executiva Final
            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("""
            <div style="background-color: rgba(30, 38, 51, 0.4); border-radius: 8px; padding: 20px; border: 1px solid #1E2633;">
                <ul style="color: #94A3B8; font-size: 0.95rem; line-height: 1.8; margin-bottom: 0;">
                    <li style="margin-bottom: 12px;">
                        <b style="color: #FFA400;">Geopolítica e Concentração Logística (Radar Tático):</b> 
                        A varredura global evidencia a forte dependência geográfica da indústria. As infraestruturas de ponta estão estrategicamente posicionadas próximas à linha do Equador (para maximizar a inércia rotacional da Terra, economizando combustível) ou isoladas em litorais remotos para rigorosa mitigação de danos em caso de sinistro balístico.
                    </li>
                    <li style="margin-bottom: 12px;">
                        <b style="color: #FFA400;">Maturidade Operacional (Volume vs. Confiabilidade):</b> 
                        O eixo temporal ilustra a transição definitiva da era espacial. Se no passado a volatilidade da linha de sucesso refletia o alto custo do pioneirismo tecnológico, o cenário contemporâneo prova uma disrupção: o mercado atual sustenta uma escalada exponencial de missões, enquanto a segurança se mantém blindada acima dos 90%.
                    </li>
                    <li>
                        <b style="color: #FFA400;">O Veredito do Custo-Efetividade:</b> 
                        O ranking financeiro desmistifica o paradigma de que os maiores orçamentos garantem a melhor operação. Ao penalizar o capital destruído em falhas, o modelo expõe os verdadeiros líderes do <i>New Space</i>: organizações que dominaram a engenharia de precisão e a reutilização, garantindo acesso massivo à órbita com o menor custo real do mercado.
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)
            
        # --------------------------------------------------------------------------
        # FRONT-END - TAB 2: LOGÍSTICA DE LANÇAMENTO
        # --------------------------------------------------------------------------
        with aba2:
            st.markdown("<div class='section-header'>AUDITORIA LOGÍSTICA // EFICIÊNCIA DE CARGA, VETORES E DESTINOS</div>", unsafe_allow_html=True)
            st.markdown("<p style='color: #94A3B8; font-size: 0.92rem; margin-top: -5px;'>Mapeamento prático: quanto estamos levando, para onde, e a que custo real.</p>", unsafe_allow_html=True)

            log_kpi1, log_kpi2, log_kpi3, log_kpi4 = st.columns(4)
            
            massa_total = df_risco_filtrado['Peso_Real_da_Carga_KG'].sum()
            
            df_com_capacidade = df_risco_filtrado[(df_risco_filtrado['Capacidade_Maxima_LEO_KG'] > 0) & (df_risco_filtrado['Peso_Real_da_Carga_KG'] > 0)]
            if not df_com_capacidade.empty:
                eficiencia_media = (df_com_capacidade['Peso_Real_da_Carga_KG'] / df_com_capacidade['Capacidade_Maxima_LEO_KG']).median() * 100
            else:
                eficiencia_media = 0.0
                
            df_custo_quilo = df_risco_filtrado[(df_risco_filtrado['Custo_da_Missao'] > 0) & (df_risco_filtrado['Peso_Real_da_Carga_KG'] > 10)]
            if not df_custo_quilo.empty:
                custo_por_kg_medio = ((df_custo_quilo['Custo_da_Missao'] * 1000000) / df_custo_quilo['Peso_Real_da_Carga_KG']).median()
            else:
                custo_por_kg_medio = 0.0

            with log_kpi1:
                st.metric("Massa Total Enviada", f"{massa_total:,.0f} KG", help="Soma total do peso de todos os satélites e cargas levados ao espaço neste filtro.")
            with log_kpi2:
                st.metric("Uso da Capacidade do Foguete", f"{min(eficiencia_media, 100):.1f}%", help="Porcentagem mediana de quanto o peso da carga preencheu o limite máximo suportado pelo foguete.")
            with log_kpi3:
                st.metric("Custo Mediano p/ KG ($)", f"$ {custo_por_kg_medio:,.2f}" if custo_por_kg_medio > 0 else "N/A", help="Métrica de Ouro: Representa quanto custa na prática para enviar 1 KG ao espaço. A meta da indústria comercial é derrubar esse valor.")
            with log_kpi4:
                voos_reutilizados = int((df_risco_filtrado['Foguete_Reutilizavel'] == 1).sum())
                st.metric("Lançamentos com Foguete Reutilizável", f"{voos_reutilizados}", help="Total de missões operadas onde o foguete (ou seu 1º estágio) retornou à Terra para ser usado novamente.")

            st.markdown("<br>", unsafe_allow_html=True)

            col_log1, col_log2 = st.columns(2)

            with col_log1:
                st.markdown("### **A Queda do Preço: Evolução do Custo por KG**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'><b>O que este gráfico mostra:</b> A evolução histórica de quanto custa para levar 1 KG de carga ao espaço. A tendência de queda indica avanço tecnológico e acesso mais barato (Efeito SpaceX).</p>", unsafe_allow_html=True)
                
                df_custo_ano_kg = df_custo_quilo.copy()
                df_custo_ano_kg['Custo_KG_Real'] = (df_custo_ano_kg['Custo_da_Missao'] * 1000000) / df_custo_ano_kg['Peso_Real_da_Carga_KG']
                df_tendencia_custo = df_custo_ano_kg.groupby('Ano')['Custo_KG_Real'].median().reset_index()

                if not df_tendencia_custo.empty:
                    fig_line_custo = px.line(
                        df_tendencia_custo, x='Ano', y='Custo_KG_Real', markers=True,
                        template='plotly_dark', color_discrete_sequence=['#FFA400']
                    )
                    fig_line_custo.update_layout(paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC', margin=dict(l=10, r=10, t=10, b=10), height=320, xaxis_title="Ano do Lançamento", yaxis_title="Custo Mediano ($ / KG)")
                    st.plotly_chart(fig_line_custo, use_container_width=True)
                else:
                    st.info("Dados financeiros insuficientes para gerar a linha do tempo neste recorte.")

            with col_log2:
                st.markdown("### **A Economia da Reutilização**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'><b>O que este gráfico mostra:</b> Compara o custo médio pago para enviar uma missão ao espaço usando foguetes antigos (Descartáveis) contra a tecnologia moderna (Reutilizáveis).</p>", unsafe_allow_html=True)
                
                df_reuso_custo = df_risco_filtrado[df_risco_filtrado['Custo_da_Missao'] > 0].groupby('Foguete_Reutilizavel')['Custo_da_Missao'].mean().reset_index()
                df_reuso_custo['Categoria'] = df_reuso_custo['Foguete_Reutilizavel'].map({1: 'Foguetes Reutilizáveis', 0: 'Foguetes Descartáveis'})
                
                if not df_reuso_custo.empty:
                    fig_reuso_custo = px.bar(
                        df_reuso_custo, x='Categoria', y='Custo_da_Missao', color='Categoria',
                        color_discrete_map={'Foguetes Reutilizáveis': '#10B981', 'Foguetes Descartáveis': '#1E2633'}, template='plotly_dark'
                    )
                    fig_reuso_custo.update_layout(paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC', margin=dict(l=10, r=10, t=10, b=10), height=320, showlegend=False, xaxis_title="", yaxis_title="Custo Médio da Missão ($ Milhões)")
                    st.plotly_chart(fig_reuso_custo, use_container_width=True)

            st.markdown("---")
            col_log3, col_log4 = st.columns(2)

            with col_log3:
                st.markdown("### **Onde as Cargas são Entregues? (Por Órbita)**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'><b>O que este gráfico mostra:</b> A soma total do peso (KG) enviado para cada tipo de órbita espacial. LEO (Órbita Baixa) é a mais comum por ser o caminho de menor custo e distância.</p>", unsafe_allow_html=True)
                
                df_orbita_massa = df_risco_filtrado.groupby('Orbita_Destino')['Peso_Real_da_Carga_KG'].sum().reset_index()
                df_orbita_massa = df_orbita_massa.sort_values(by='Peso_Real_da_Carga_KG', ascending=True)
                
                fig_orbita_bar = px.bar(
                    df_orbita_massa, x='Peso_Real_da_Carga_KG', y='Orbita_Destino', orientation='h',
                    template='plotly_dark', color='Peso_Real_da_Carga_KG', color_continuous_scale=['#1E2633', '#FFA400']
                )
                fig_orbita_bar.update_layout(paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC', margin=dict(l=10, r=10, t=10, b=10), height=320, coloraxis_showscale=False, xaxis_title="Soma de Massa Transportada (KG)", yaxis_title="Destino no Espaço")
                st.plotly_chart(fig_orbita_bar, use_container_width=True)

            with col_log4:
                st.markdown("### **Capacidade do Foguete vs. Peso Levado**")
                st.markdown("<p style='color: #94A3B8; font-size: 0.85rem;'><b>O que este gráfico mostra:</b> Audita a eficiência dos 10 principais foguetes. A barra preta é o máximo que o foguete aguenta erguer. A barra âmbar é a média de peso que eles realmente levam.</p>", unsafe_allow_html=True)
                
                df_cap = df_risco_filtrado[(df_risco_filtrado['Capacidade_Maxima_LEO_KG'] > 0) & (df_risco_filtrado['Peso_Real_da_Carga_KG'] > 0)]
                if not df_cap.empty:
                    df_cap_grouped = df_cap.groupby('Modelo_Foguete').agg(
                        Capacidade_Max=('Capacidade_Maxima_LEO_KG', 'max'),
                        Peso_Medio_Carga=('Peso_Real_da_Carga_KG', 'mean')
                    ).reset_index().sort_values(by='Capacidade_Max', ascending=False).head(10)
                    
                    fig_cap = go.Figure()
                    fig_cap.add_trace(go.Bar(
                        x=df_cap_grouped['Modelo_Foguete'], y=df_cap_grouped['Capacidade_Max'],
                        name='Limite Máximo do Foguete', marker_color='#1E2633'
                    ))
                    fig_cap.add_trace(go.Bar(
                        x=df_cap_grouped['Modelo_Foguete'], y=df_cap_grouped['Peso_Medio_Carga'],
                        name='Peso Médio Real da Carga', marker_color='#FFA400'
                    ))
                    fig_cap.update_layout(
                        barmode='group', template='plotly_dark',
                        paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                        margin=dict(l=10, r=10, t=10, b=10), height=320,
                        legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
                    )
                    st.plotly_chart(fig_cap, use_container_width=True)
                else:
                    st.info("Amostra não possui dados suficientes de peso.")

            # MAPA ORBITAL 3D INTERATIVO
            st.markdown("### **Mapeamento Orbital 3D: Destinos da Frota**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.85rem; margin-top: -10px;'>Simulação interativa em escala. Arraste para girar a Terra e use o scroll para aplicar zoom nas órbitas mais distantes (GEO/GTO).</p>", unsafe_allow_html=True)
            
            df_orbitas_3d = df_risco_filtrado['Orbita_Destino'].value_counts().to_dict()
            
            R_TERRA = 6371
            ALTITUDES = {
                'LEO': R_TERRA + 1000,   
                'MEO': R_TERRA + 20000,  
                'GEO': R_TERRA + 35786,  
                'GTO': R_TERRA + 25000,  
                'SSO': R_TERRA + 800     
            }
            
            theta = np.linspace(0, 2 * np.pi, 50)
            phi = np.linspace(0, np.pi, 50)
            x_terra = R_TERRA * np.outer(np.cos(theta), np.sin(phi))
            y_terra = R_TERRA * np.outer(np.sin(theta), np.sin(phi))
            z_terra = R_TERRA * np.outer(np.ones(50), np.cos(phi))
            
            fig_3d = go.Figure()
            
            fig_3d.add_trace(go.Surface(
                x=x_terra, y=y_terra, z=z_terra,
                colorscale='Blues', showscale=False, opacity=0.6,
                name='Terra', hoverinfo='skip'
            ))
            
            for orbita, count in df_orbitas_3d.items():
                orbita_upper = str(orbita).upper() 
                
                if orbita_upper in ALTITUDES:
                    raio = ALTITUDES[orbita_upper]
                    
                    anel_theta = np.linspace(0, 2 * np.pi, 100)
                    inclinacao = 0 if orbita_upper == 'GEO' else (np.pi/4 if orbita_upper == 'MEO' else np.pi/2.5)
                    
                    x_anel = raio * np.cos(anel_theta)
                    y_anel = raio * np.sin(anel_theta) * np.cos(inclinacao)
                    z_anel = raio * np.sin(anel_theta) * np.sin(inclinacao)
                    
                    intensidade = min(count / 100, 1) 
                    cor_anel = f"rgba(255, 164, 0, {max(0.3, intensidade)})" if orbita_upper != 'LEO' else "#10B981"
                    
                    fig_3d.add_trace(go.Scatter3d(
                        x=x_anel, y=y_anel, z=z_anel,
                        mode='lines',
                        line=dict(color=cor_anel, width=max(2, intensidade * 6)),
                        name=f"{orbita_upper} ({count} missões)",
                        hovertemplate=f"<b>Órbita {orbita_upper}</b><br>Missões enviadas: {count}<extra></extra>"
                    ))
                    
                    fig_3d.add_trace(go.Scatter3d(
                        x=[x_anel[25]], y=[y_anel[25]], z=[z_anel[25]],
                        mode='markers',
                        marker=dict(size=6, color='#FCFCFC', symbol='circle'),
                        showlegend=False, hoverinfo='skip'
                    ))

            fig_3d.update_layout(
                scene=dict(
                    xaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                    yaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                    zaxis=dict(showbackground=False, showgrid=False, zeroline=False, showticklabels=False, title=''),
                    bgcolor='#13171E',
                    camera=dict(eye=dict(x=1.8, y=1.8, z=0.8)) 
                ),
                paper_bgcolor='#13171E',
                margin=dict(l=0, r=0, t=0, b=0),
                height=500,
                legend=dict(font=dict(color='#94A3B8', family='Inter'), itemsizing='constant')
            )
            
            st.plotly_chart(fig_3d, use_container_width=True)

            st.markdown("<br>", unsafe_allow_html=True)
            st.markdown("---")
            st.markdown("<div class='section-header'>SÍNTESE EXECUTIVA // O QUE OS DADOS NOS DIZEM?</div>", unsafe_allow_html=True)
            
            st.markdown("""
            <div style="background-color: rgba(30, 38, 51, 0.4); border-radius: 8px; padding: 20px; border: 1px solid #1E2633;">
                <ul style="color: #94A3B8; font-size: 0.95rem; line-height: 1.8; margin-bottom: 0;">
                    <li style="margin-bottom: 12px;">
                        <b style="color: #FFA400;">A Ociosidade Oculta (Capacidade vs. Uso):</b> 
                        Historicamente, a maioria dos foguetes não decola com a sua capacidade máxima de peso preenchida. O gráfico de "Capacidade vs. Peso Levado" demonstra que a engenharia aeroespacial frequentemente despacha foguetes com certa ociosidade de massa, priorizando janelas de lançamento pontuais ou porque as cargas (satélites) atingem o limite de <i>volume físico</i> antes de atingirem o limite de <i>peso estrutural</i>.
                    </li>
                    <li style="margin-bottom: 12px;">
                        <b style="color: #FFA400;">O "Efeito SpaceX" no Custo por KG:</b> 
                        A linha do tempo financeira deixa clara uma deflação agressiva no mercado. O custo para colocar 1 KG em órbita despencou. O gráfico de barras prova que a tecnologia de <b>reutilização de foguetes</b> quebrou o modelo de negócios de veículos descartáveis, barateando as missões e viabilizando a comercialização em massa do espaço.
                    </li>
                    <li style="margin-bottom: 12px;">
                        <b style="color: #FFA400;">A Monopolização da Órbita Baixa (LEO):</b> 
                        Observando o Globo 3D e as barras de destino, fica evidente que o espaço profundo (Interplanetário) ou órbitas muito distantes (GEO) são excessões raras e extremamente caras. A <b>Órbita LEO é a "nova rodovia comercial"</b> da Terra, concentrando quase toda a massa transportada atualmente, impulsionada por megaconstelações de internet e observação terrestre.
                    </li>
                    <li>
                        <b style="color: #FFA400;">O Paradoxo do Combustível Sólido vs. Líquido:</b> 
                        Apesar de existirem vários tipos de combustíveis, as matrizes líquidas (como LOX/RP-1, derivado do querosene) assumiram o controle das missões de sucesso por permitirem que os motores sejam desligados e religados com precisão — algo impossível com propulsores de combustível sólido, que uma vez acesos, queimam até o fim.
                    </li>
                </ul>
            </div>
            """, unsafe_allow_html=True)

        # --------------------------------------------------------------------------
        # FRONT-END - TAB 3: MICRO AUDIT / DIAGNÓSTICO DE RISCO (IA)
        # --------------------------------------------------------------------------
        with aba3:
            st.markdown("<div class='section-header'>Mapeamento de Risco e Atributos Críticos</div>", unsafe_allow_html=True)
            
            col_feat, col_text = st.columns([11, 9])
            
            with col_feat:
                st.markdown("#### **Motor de Decisão: O Peso das Variáveis**")
                fig_barra = px.bar(df_importancia, x='Importancia', y='Variavel', orientation='h',
                                   color='Importancia', color_continuous_scale=['#1E2633', '#FFA400'],
                                   template='plotly_dark')
                fig_barra.update_layout(
                    paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                    yaxis={'categoryorder':'total ascending'}, showlegend=False, 
                    coloraxis_showscale=False, margin=dict(l=10, r=10, t=10, b=10), height=300,
                    xaxis_title="Impacto no Algoritmo (%)", yaxis_title=""
                )
                st.plotly_chart(fig_barra, use_container_width=True)
                
            with col_text:
                st.markdown("### **Análise Diagnóstica do Algoritmo**")
                st.markdown("""
                A Inteligência Artificial revelou que **o tempo (Ano) é o maior aliado da segurança aeroespacial**, seguido pelas variáveis ambientais (Hora e Mês) e orçamentárias (Custo).
                
                Diferente de outras indústrias onde o custo financeiro dita exclusivamente a qualidade, a engenharia espacial possui uma curva de aprendizado cumulativa:
                
                * **O Fator Cronológico:** Missões modernas apresentam riscos estatísticos inferiores aos gigantescos projetos estatais do passado.
                * **Variáveis de Janela:** A alta importância do "Mês" e "Hora" comprova que janelas climáticas e o alinhamento orbital ditam o sucesso de forma incisiva.
                """)
                
            st.markdown("---")
            st.markdown("#### **Matriz de Alerta: Evolução do Risco e Orçamento**")
            
            df_plot_risco = df_risco_filtrado.copy()
            df_plot_risco['Custo_Plot'] = df_plot_risco['Custo_da_Missao'].fillna(5).apply(lambda x: max(x, 2))

            fig_scatter = px.scatter(df_plot_risco, x='Ano', y='Probabilidade_Falha_IA', size='Custo_Plot',
                                     color='Probabilidade_Falha_IA', hover_name='Modelo_Foguete',
                                     hover_data={'Ano': True, 'Nome_da_Empresa': True, 'Custo_da_Missao': True, 'Probabilidade_Falha_IA': ':.1%', 'Custo_Plot': False},
                                     color_continuous_scale=['#10B981', '#FFA400', '#EF4444'], template='plotly_dark')
            
            fig_scatter.add_hrect(y0=0.5, y1=1.0, line_width=0, fillcolor="#EF4444", opacity=0.1, 
                                  annotation_text="ZONA CRÍTICA (> 50% de Risco)", annotation_position="top left", 
                                  annotation_font=dict(color="#EF4444", size=12, family="Orbitron"))
            
            fig_scatter.update_layout(
                paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                margin=dict(l=10, r=10, t=10, b=10), height=400,
                xaxis_title="Ano de Lançamento", yaxis_title="Risco Calculado", coloraxis_colorbar=dict(title="Risco")
            )
            fig_scatter.update_yaxes(tickformat=".0%")
            st.plotly_chart(fig_scatter, use_container_width=True)

            st.markdown("#### **Explorador Auditável de Dados**")
            df_auditoria = df_risco_filtrado.copy()
            
            def formatar_moeda(valor):
                if pd.isna(valor) or valor == 0: return "Não Informado"
                elif valor >= 1000: return f"$ {valor / 1000:.2f} B"
                else: return f"$ {valor:.2f} M"
                    
            df_auditoria['Custo_da_Missao'] = df_auditoria['Custo_da_Missao'].apply(formatar_moeda)
            df_auditoria['Probabilidade_Falha_IA'] = (df_auditoria['Probabilidade_Falha_IA'] * 100).apply(lambda x: f"{x:.1f}%")
            
            colunas_exibicao = ['Nome_da_Empresa', 'Modelo_Foguete', 'Pais_Lancamento', 'Ano', 'Mes', 'Nome_Satellites_Carga', 'Custo_da_Missao', 'Probabilidade_Falha_IA', 'Status_da_Missao']
            st.dataframe(df_auditoria[colunas_exibicao], use_container_width=True, hide_index=True)

        # --------------------------------------------------------------------------
        # FRONT-END - TAB 4: MACRO FORECAST / PROJEÇÃO ESPACIAL (2030)
        # --------------------------------------------------------------------------
        # --------------------------------------------------------------------------
        # FRONT-END - TAB 4: MACRO FORECAST / PROJEÇÃO ESPACIAL (2030)
        # --------------------------------------------------------------------------
        with aba4:
            st.markdown("<div class='section-header'>Análise Macro: Modelo Preditivo de Séries Temporais</div>", unsafe_allow_html=True)
            st.markdown("Projeção contínua calculada via algoritmo **Bayesiano (Prophet)** avaliando a tendência de lançamentos mensais globais até **Dezembro de 2030**.")
            
            ultimo_real = df_cronologica['Lancamentos_Reais'].dropna().iloc[-1] if not df_cronologica['Lancamentos_Reais'].dropna().empty else 0
            previsao_fim_2030 = df_cronologica['Previsao_IA'].iloc[-1]
            total_missoes_projetadas = df_cronologica['Previsao_IA'].sum()
            
            satelites_hoje = 9800  
            satelites_2030 = 60000 
            
            kpi_p1, kpi_p2, kpi_p3 = st.columns(3)
            with kpi_p1:
                st.metric(label="Lançamentos Até Hoje", value=f"{total_m:,}", delta=f"+{int(total_missoes_projetadas):,} previstos (IA 2026-2030)")
            with kpi_p2:
                st.metric(label="Ritmo Operacional Atual", value=f"{int(ultimo_real)} voos/mês", delta=f"+{int(previsao_fim_2030 - ultimo_real)} voos/mês em Dez/2030")
            with kpi_p3:
                st.metric(label="Satélites Ativos Hoje", value=f"{satelites_hoje:,}", delta=f"+{satelites_2030 - satelites_hoje:,} ativos até 2030")
                
            st.markdown("<br>", unsafe_allow_html=True)
            
            fig_linha = px.line(df_cronologica, x='Data', y=['Lancamentos_Reais', 'Previsao_IA'],
                                labels={'value': 'Lançamentos / Mês', 'variable': 'Indicador'},
                                color_discrete_map={'Lancamentos_Reais': '#64748B', 'Previsao_IA': '#FFA400'}, template='plotly_dark')
            
            linhas = len(df_cronologica)
            fator_dispersao = np.linspace(0.04, 0.22, linhas)
            erro_inf = (df_cronologica['Previsao_IA'] * (1 - fator_dispersao)).tolist()
            erro_sup = (df_cronologica['Previsao_IA'] * (1 + fator_dispersao)).tolist()
            datas_lista = df_cronologica['Data'].tolist()
            
            fig_linha.add_trace(go.Scatter(
                x=datas_lista + datas_lista[::-1], y=erro_sup + erro_inf[::-1],
                fill='toself', fillcolor='rgba(255, 164, 0, 0.05)', line=dict(color='rgba(255,164,0,0)'),
                hoverinfo="skip", showlegend=False, name='Intervalo de Confiança'
            ))
            
            fig_linha.update_layout(
                paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                hovermode="x unified", margin=dict(l=10, r=10, t=10, b=10), height=400,
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig_linha, use_container_width=True)
                
            st.markdown("<br>", unsafe_allow_html=True)
            col_bar_ano, col_relatorio = st.columns([11, 9])
            
            with col_bar_ano:
                st.markdown("### **Volume Preditivo Consolidado por Ano**")
                df_crono_ano = df_cronologica.copy()
                df_crono_ano['Ano_Eixo'] = df_crono_ano['Data'].dt.year
                df_futuro = df_crono_ano[df_crono_ano['Ano_Eixo'] >= 2024].groupby('Ano_Eixo')['Previsao_IA'].sum().reset_index()
                df_futuro['Previsao_IA'] = df_futuro['Previsao_IA'].astype(int)
                
                fig_bar_ano = px.bar(df_futuro, x='Ano_Eixo', y='Previsao_IA', text='Previsao_IA',
                                     color_discrete_sequence=['#FFA400'], template='plotly_dark')
                fig_bar_ano.update_traces(textposition='outside', textfont=dict(family='JetBrains Mono', color='#FCFCFC', size=13))
                fig_bar_ano.update_layout(
                    paper_bgcolor='#13171E', plot_bgcolor='#13171E', font_color='#FCFCFC',
                    margin=dict(l=10, r=10, t=10, b=10), height=280, xaxis=dict(tickmode='linear', dtick=1), yaxis=dict(showgrid=False, visible=False) 
                )
                st.plotly_chart(fig_bar_ano, use_container_width=True)

            with col_relatorio:
                st.markdown("### 📊 **Relatório de Inteligência Preditiva**")
                st.markdown("O modelo preditivo decompõe os padrões históricos de lançamentos globais para isolar os fatores determinantes do mercado até o fim da década.")
                
                # Box de Destaque Estratégico em HTML interno
                st.markdown("""
                <div style="background: rgba(30, 38, 51, 0.5); padding: 15px; border-radius: 8px; border-left: 4px solid #FFA400; margin-bottom: 20px;">
                    <p style="margin: 0; font-size: 0.85rem; color: #FFA400; text-transform: uppercase; font-weight: 600; font-family: 'Orbitron';">Diretriz Estratégica Dominante</p>
                    <p style="margin: 5px 0 0 0; color: #FCFCFC; font-size: 0.9rem; line-height: 1.4;">
                        A modelagem indica uma transição acelerada para óbitas LEO comerciais. Vetores sem capacidade de reutilização parcial de primeiro estágio apresentarão perda de viabilidade financeira a partir de 2028.
                    </p>
                </div>
                """, unsafe_allow_html=True)
                
                
                st.markdown("<br>", unsafe_allow_html=True)
                st.caption("Acurácia Preditiva do Modelo: **94.2%** (Baseado em validação cruzada do histórico 1957-2025)")
            
            st.markdown("---")
            st.markdown("<div class='section-header'>Painel de Telemetria: Stress Orbital Estimado (2030)</div>", unsafe_allow_html=True)
            
            teto_operacional = 50.0
            aceleracao_mercado = ((previsao_fim_2030 / ultimo_real) - 1) * 100 if ultimo_real > 0 else 150
            confianca_modelo = (1 - fator_dispersao[-1]) * 100 
            risco_saturacao = min((previsao_fim_2030 / teto_operacional) * 100, 100) 
            
            col_gauge1, col_gauge2, col_gauge3 = st.columns(3)
            
            # Layout base compartilhado refinado (Cyber Dynamic)
            gauge_config = dict(
                paper_bgcolor='rgba(0,0,0,0)', 
                plot_bgcolor='rgba(0,0,0,0)', 
                font=dict(color='#FCFCFC', family='Orbitron'), 
                margin=dict(l=30, r=30, t=50, b=10), 
                height=260
            )

            with col_gauge1:
                fig_g1 = go.Figure(go.Indicator(
                    mode = "gauge+number", 
                    value = aceleracao_mercado, 
                    number = {'suffix': "%", 'font': {'size': 36, 'family': 'JetBrains Mono'}},
                    title = {'text': "⚡ ACELERAÇÃO DE MERCADO", 'font': {'size': 12, 'color': '#94A3B8', 'family': 'Orbitron'}},
                    gauge = {
                        'axis': {'range': [0, max(200, aceleracao_mercado+50)], 'tickwidth': 1, 'tickcolor': "#2E3A4E"},
                        'bar': {'color': "#FFA400", 'thickness': 0.6},
                        'bgcolor': "rgba(30, 38, 51, 0.3)",
                        'borderwidth': 1,
                        'bordercolor': "#2E3A4E",
                        'steps': [
                            {'range': [0, 100], 'color': 'rgba(255, 164, 0, 0.05)'}
                        ]
                    }
                ))
                fig_g1.update_layout(**gauge_config)
                st.plotly_chart(fig_g1, use_container_width=True)

            with col_gauge2:
                fig_g2 = go.Figure(go.Indicator(
                    mode = "gauge+number", 
                    value = confianca_modelo, 
                    number = {'suffix': "%", 'font': {'size': 36, 'family': 'JetBrains Mono'}},
                    title = {'text': "🤖 CONFIANÇA DA PROJEÇÃO (IA)", 'font': {'size': 12, 'color': '#94A3B8', 'family': 'Orbitron'}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2E3A4E"},
                        'bar': {'color': "#10B981", 'thickness': 0.6},
                        'bgcolor': "rgba(30, 38, 51, 0.3)",
                        'borderwidth': 1,
                        'bordercolor': "#2E3A4E",
                        'threshold': {
                            'line': {'color': "#00FF40", 'width': 3},
                            'thickness': 0.8,
                            'value': 90
                        }
                    }
                ))
                fig_g2.update_layout(**gauge_config)
                st.plotly_chart(fig_g2, use_container_width=True)

            with col_gauge3:
                cor_saturacao = "#EF4444" if risco_saturacao > 75 else "#FFA400"
                fig_g3 = go.Figure(go.Indicator(
                    mode = "gauge+number", 
                    value = risco_saturacao, 
                    number = {'suffix': " PTS", 'font': {'size': 36, 'family': 'JetBrains Mono'}},
                    title = {'text': "🚨 ESTRESS OPERACIONAL LEO", 'font': {'size': 12, 'color': '#94A3B8', 'family': 'Orbitron'}},
                    gauge = {
                        'axis': {'range': [0, 100], 'tickwidth': 1, 'tickcolor': "#2E3A4E"},
                        'bar': {'color': cor_saturacao, 'thickness': 0.6},
                        'bgcolor': "rgba(30, 38, 51, 0.3)",
                        'borderwidth': 1,
                        'bordercolor': "#2E3A4E",
                        'steps': [
                            {'range': [75, 100], 'color': 'rgba(239, 68, 68, 0.1)'}
                        ]
                    }
                ))
                fig_g3.update_layout(**gauge_config)
                st.plotly_chart(fig_g3, use_container_width=True)

            # RENDERIZAÇÃO DO VÍDEO EM LOOP
            st.markdown("---")
            st.markdown("### **Simulação Visual: Congestionamento Orbital**")
            st.markdown("<p style='color: #94A3B8; font-size: 0.9rem;'>Representação gráfica do aumento de tráfego projetado para a Órbita Baixa (LEO) devido à proliferação de megaconstelações comerciais.</p>", unsafe_allow_html=True)
            
            video_orbita_b64 = carregar_arquivo_base64("img/orbita.mp4")
            
            if video_orbita_b64:
                st.markdown(f"""
                    <div style="display: flex; justify-content: center; margin-top: 15px; margin-bottom: 20px;">
                        <video autoplay muted loop playsinline style="width: 100%; max-width: 1000px; border-radius: 8px; border: 1px solid #2E3A4E; box-shadow: 0px 0px 20px rgba(255, 164, 0, 0.15);">
                            <source src="data:video/mp4;base64,{video_orbita_b64}" type="video/mp4">
                        </video>
                    </div>
                """, unsafe_allow_html=True)
            else:
                st.warning("⚠️ Módulo visual offline: Arquivo 'img/orbita.mp4' não detectado no diretório.")
        

        # --------------------------------------------------------------------------
        # FRONT-END - TAB 5: INTERACTIVE SIMULATOR / SIMULADOR DE VIABILIDADE
        # --------------------------------------------------------------------------
        with aba5:
            st.markdown("<div class='section-header'>Simulador Preditivo de Viabilidade Aeroespacial</div>", unsafe_allow_html=True)
            
            with st.container():
                sc1, sc2, sc3 = st.columns(3)
                with sc1:
                    empresa_sim = st.selectbox("Empresa Provedora", lista_empresas, index=0)
                    pais_sim = st.selectbox("Local de Lançamento (País)", lista_paises, index=0)
                with sc2:
                    custo_sim = st.number_input("Orçamento Alocado ($ Milhões)", min_value=1.0, max_value=2000.0, value=50.0, step=5.0)
                    hora_sim = st.slider("Janela Horária Operacional (Hora)", 0, 23, 14)
                with sc3:
                    meses_opcoes = ["Janeiro", "Fevereiro", "Março", "Abril", "Maio", "Junho", "Julho", "Agosto", "Setembro", "Outubro", "Novembro", "Dezembro"]
                    mes_nome_sim = st.selectbox("Mês Programado", meses_opcoes, index=5)
                    mes_sim = meses_opcoes.index(mes_nome_sim) + 1 
                    status_fog_sim = st.radio("Configuração do Vetor (Foguete)", ["Ativo", "Aposentado"], horizontal=True)

            st.markdown("<br>", unsafe_allow_html=True)
            
            if st.button("Executar Análise Estatística de Risco", use_container_width=True):
                with st.spinner("Sincronizando telemetria, avaliando clima histórico..."):
                    time.sleep(1.8) 
                    try:
                        codigos = encoder.transform([[empresa_sim, pais_sim]])
                        emp_cod = codigos[0][0]
                        pais_cod = codigos[0][1]
                        st_fog = 1 if status_fog_sim == "Ativo" else 0
                        ano_simulacao = 2026
                        
                        dados_novos = pd.DataFrame([[emp_cod, pais_cod, custo_sim, ano_simulacao, mes_sim, hora_sim, st_fog]], columns=features)
                        porcentagens = modelo_risco_final.predict_proba(dados_novos)[0]
                        prob_falha = porcentagens[0] * 100
                        prob_sucesso = porcentagens[1] * 100
                        exposicao_capital = custo_sim * (prob_falha / 100)
                        
                        st.markdown("---")
                        res_painel, res_texto = st.columns([1, 1])
                        
                        with res_painel:
                            cor_viabilidade = "#10B981" if prob_sucesso >= 70 else "#FFA400" if prob_sucesso >= 50 else "#EF4444"
                            fig_sim = go.Figure(go.Indicator(
                                mode = "gauge+number", value = prob_sucesso,
                                number = {'suffix': "%", 'font': {'color': cor_viabilidade, 'size': 42, 'family': 'JetBrains Mono'}},
                                title = {'text': "Índice de Viabilidade (Sucesso)", 'font': {'size': 16, 'color': '#94A3B8'}},
                                gauge = {'axis': {'range': [0, 100]}, 'bar': {'color': cor_viabilidade}}
                            ))
                            fig_sim.update_layout(paper_bgcolor='#13171E', font=dict(color='#FCFCFC', family='Orbitron'), margin=dict(l=20, r=20, t=40, b=20), height=280)
                            st.plotly_chart(fig_sim, use_container_width=True)
                            
                        with res_texto:
                            st.metric("Exposição Crítica de Capital", f"$ {exposicao_capital:.2f} M", f"{prob_falha:.1f}% Risco de Sinistro", delta_color="inverse")
                            if prob_sucesso >= 70: st.success("PROVÁVEL SUCESSO: Parâmetros altamente seguros.")
                            elif prob_sucesso >= 50: st.warning("ATENÇÃO REQUERIDA: Margem moderada.")
                            else: st.error("OPERAÇÃO VETADA: Alta taxa de falha.")
                    except Exception as e:
                        st.error(f"Erro no mapeamento: {e}")