import io
import re
import csv
import time
import html
from collections import Counter

import streamlit as st

st.set_page_config(
    page_title="Escola Sem Barreiras",
    page_icon="📘",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Paleta: azul, roxo e branco. Fontes com boa legibilidade.
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Atkinson+Hyperlegible:wght@400;700&family=Nunito:wght@400;500;600;700;800;900&display=swap');
:root {
  --navy:#20245f; --blue:#4169d8; --purple:#7654c8;
  --lavender:#f0edff; --ice:#f3f6ff; --ink:#25294b;
  --muted:#68708d; --line:#e3e7f5; --white:#ffffff;
}
html, body, [class*="css"] { font-family:'Atkinson Hyperlegible','Nunito',sans-serif; }
.stApp { background:linear-gradient(180deg,#f7f8ff 0%,#f4f6fc 100%); color:var(--ink); }
.block-container { max-width:1240px; padding-top:1.35rem; padding-bottom:3.5rem; }
h1,h2,h3,h4 { font-family:'Nunito',sans-serif!important; color:var(--navy); }
h2 { font-weight:900!important; letter-spacing:-.02em; }
p, label, .stMarkdown { color:var(--ink); }
[data-testid="stSidebar"] { background:linear-gradient(180deg,#242866 0%,#37347f 100%); }
[data-testid="stSidebar"] * { color:#fff!important; }
[data-testid="stSidebar"] [data-baseweb="select"] div { color:#25294b!important; }
[data-testid="stSidebar"] [data-testid="stWidgetLabel"] p { color:#fff!important; }
[data-testid="stSidebar"] hr { border-color:rgba(255,255,255,.2); }
.brand-mini { display:flex; gap:11px; align-items:center; padding:8px 2px 18px; }
.brand-icon { width:43px;height:43px;border-radius:14px;background:#fff;color:#37347f;display:flex;align-items:center;justify-content:center;font-size:23px;font-weight:900;box-shadow:0 7px 18px #17194b55; }
.brand-name { font:900 17px 'Nunito',sans-serif; line-height:1.1; color:#fff; }
.brand-caption { font-size:11px; color:#d8dcff; margin-top:4px; letter-spacing:.08em; text-transform:uppercase; }
.hero {
  position:relative; overflow:hidden; border-radius:26px; padding:34px 38px;
  background:linear-gradient(105deg,rgba(31,36,97,.97) 0%,rgba(61,65,150,.92) 58%,rgba(104,76,184,.78) 100%),
  url('https://images.unsplash.com/photo-1509062522246-3755977927d7?auto=format&fit=crop&w=1800&q=85') center/cover;
  box-shadow:0 16px 40px rgba(38,43,112,.16); margin-bottom:22px; min-height:250px;
}
.hero:after { content:"✦"; position:absolute; right:7%; top:10%; font-size:100px; color:#ffffff18; }
.hero-content { position:relative; z-index:1; max-width:720px; }
.hero-tag { display:inline-block; background:#ffffff20; border:1px solid #ffffff45; color:#fff; border-radius:30px; padding:6px 12px; font-size:12px; font-weight:700; letter-spacing:.08em; }
.hero h1 { color:#fff!important; font-size:clamp(2rem,4vw,3.05rem); line-height:1.08; margin:15px 0 10px; font-weight:900; letter-spacing:-.04em; }
.hero p { color:#eff0ff!important; font-size:1.08rem; line-height:1.55; max-width:630px; margin:0; }
.hero-note { color:#dfe1ff; font-size:.84rem; margin-top:19px; }
.section-kicker { color:var(--purple); font-size:.76rem; text-transform:uppercase; letter-spacing:.12em; font-weight:900; margin-bottom:3px; }
.section-title { font:900 1.5rem 'Nunito',sans-serif; color:var(--navy); margin:0 0 5px; }
.section-desc { color:var(--muted); margin:0 0 18px; }
.feature-card { background:#fff; border:1px solid var(--line); border-radius:19px; padding:19px; min-height:145px; box-shadow:0 5px 18px #252c6410; }
.feature-icon { width:43px;height:43px;border-radius:14px;display:flex;align-items:center;justify-content:center;font-size:22px;background:var(--lavender);margin-bottom:12px; }
.feature-card h3 { font:800 1rem 'Nunito',sans-serif; margin:0 0 5px; color:var(--navy); }
.feature-card p { font-size:.88rem; color:var(--muted); margin:0; line-height:1.45; }
.soft-card { background:#fff; border:1px solid var(--line); border-radius:18px; padding:20px 22px; box-shadow:0 5px 18px #252c640a; }
.callout { background:linear-gradient(100deg,#eeedff,#f4f7ff); border:1px solid #dfdcff; border-radius:16px; padding:15px 18px; color:#35356f; }
.step-number { display:inline-flex; width:28px;height:28px;align-items:center;justify-content:center;border-radius:50%;background:#e9e6ff;color:#5140a4;font-weight:900;margin-right:8px; }
div.stButton > button[kind="primary"] { background:linear-gradient(100deg,#3f60ce,#7351c2); border:0; color:white; border-radius:12px; font-weight:800; min-height:45px; box-shadow:0 6px 14px #554bb52a; }
div.stButton > button { border-radius:12px; font-weight:700; border-color:#dfe3f2; }
div.stDownloadButton > button { border-radius:11px; font-weight:700; }
[data-testid="stMetric"] { background:#fff; border:1px solid var(--line); padding:16px 17px; border-radius:16px; box-shadow:0 4px 14px #252c6408; }
[data-testid="stMetricLabel"] { color:var(--muted)!important; }
[data-testid="stMetricValue"] { color:var(--navy)!important; font-family:'Nunito',sans-serif; font-weight:900; }
.stTabs [data-baseweb="tab-list"] { gap:7px; background:#eceffd; border-radius:14px; padding:6px; }
.stTabs [data-baseweb="tab"] { border-radius:10px; height:43px; font-weight:800; color:#555b83; }
.stTabs [aria-selected="true"] { background:#fff!important; color:#343b91!important; box-shadow:0 2px 8px #242a6615; }
.stTextArea textarea, .stTextInput input { border-radius:12px!important; border-color:#dce1f2!important; background:#fff!important; }
[data-testid="stFileUploader"] { border:1.5px dashed #b9bce7; border-radius:15px; padding:10px; background:#fafaff; }
div[data-testid="stExpander"] { border:1px solid var(--line); border-radius:14px; background:#fff; }
.stAlert { border-radius:13px; }
.small-muted { color:var(--muted);font-size:.86rem; }
.footer { text-align:center; color:#858ba7; font-size:.78rem; padding:28px 0 4px; }
button:focus-visible, textarea:focus-visible, input:focus-visible { outline:3px solid #f0a34a!important; outline-offset:2px; }
@media(max-width:700px) {
 .hero { padding:25px 22px; min-height:220px; }
 .hero h1 { font-size:2rem; }
 .block-container { padding-left:1rem; padding-right:1rem; }
}
</style>
""", unsafe_allow_html=True)

# ------------------------- Estado -------------------------
defaults = {
    "texto": "", "nome_arquivo": "", "adaptacoes": {}, "originais": {},
    "revisoes": {}, "historico": [], "materiais": 0,
    "arquivo_midia": None, "tipo_midia": None,
}
for key, value in defaults.items():
    if key not in st.session_state:
        st.session_state[key] = value

with st.sidebar:
    st.markdown("""
    <div class="brand-mini">
      <div class="brand-icon">✦</div>
      <div><div class="brand-name">Escola Sem<br>Barreiras</div>
      <div class="brand-caption">Aprender é para todos</div></div>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("### Preferências de acessibilidade")
    nivel = st.selectbox(
        "Nível da linguagem",
        ["Muito simples (anos iniciais)", "Simples (ensino fundamental)", "Intermediário (ensino médio)"],
    )
    tamanho = st.slider("Tamanho do texto", 14, 26, 18)
    alto_contraste = st.toggle("Alto contraste")
    espaco = st.toggle("Espaçamento amplo")
    st.divider()
    st.markdown("**Um espaço de aprendizagem inclusiva**")
    st.caption("Ajuste a leitura para deixar a experiência mais confortável.")
    st.markdown("---")
    st.caption("Protótipo demonstrativo • Sem chave de API")

if alto_contraste:
    st.markdown("""<style>
    .stApp{background:#fff!important;color:#000!important}
    .hero{background:#000!important;border:2px solid #000}
    .hero *,.hero h1,.hero p{color:#fff!important}
    .feature-card,.soft-card,[data-testid="stMetric"]{border:2px solid #000!important}
    .feature-card p,.section-desc,.small-muted{color:#111!important}
    </style>""", unsafe_allow_html=True)
st.markdown(f"""<style>
.stMarkdown p,.stTextArea textarea,label {{font-size:{tamanho}px!important;
{'line-height:1.9!important;letter-spacing:.03em;word-spacing:.08em;' if espaco else ''}}}
</style>""", unsafe_allow_html=True)

# ------------------------- Cabeçalho e apresentação -------------------------
st.markdown("""
<div class="hero"><div class="hero-content">
  <span class="hero-tag">✦ EDUCAÇÃO MAIS ACESSÍVEL</span>
  <h1>Todo estudante merece<br>uma forma de aprender.</h1>
  <p>Um espaço para transformar materiais de estudo em diferentes formatos, respeitando ritmos, necessidades e maneiras de compreender.</p>
  <div class="hero-note">INCLUSÃO • ACESSIBILIDADE • AUTONOMIA</div>
</div></div>
""", unsafe_allow_html=True)

st.markdown("""
<div class="section-kicker">Bem-vindo ao seu espaço de aprendizagem</div>
<div class="section-title">Pequenos caminhos para grandes descobertas.</div>
<p class="section-desc">Envie um conteúdo, escolha como deseja trabalhá-lo e acompanhe cada etapa.</p>
""", unsafe_allow_html=True)

f1, f2, f3 = st.columns(3, gap="medium")
for col, icon, title, desc in [
    (f1, "📚", "Conteúdos flexíveis", "Trabalhe com textos, PDFs, apresentações e materiais multimídia."),
    (f2, "🧩", "Diferentes formatos", "Crie versões mais simples, resumos, glossários e perguntas."),
    (f3, "💜", "Acessibilidade em foco", "Ajuste a leitura, ouça os textos e revise cada adaptação."),
]:
    with col:
        st.markdown(f'<div class="feature-card"><div class="feature-icon">{icon}</div><h3>{title}</h3><p>{desc}</p></div>', unsafe_allow_html=True)

st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)
st.markdown('<div class="callout">💡 <b>Importante:</b> esta versão funciona sem serviços pagos. As adaptações são demonstrativas e baseadas em regras simples, não em inteligência artificial. Revise todo o conteúdo antes de utilizá-lo com estudantes.</div>', unsafe_allow_html=True)
st.markdown("<div style='height:18px'></div>", unsafe_allow_html=True)

# ------------------------- Funções locais -------------------------
def extrair_pdf(arquivo):
    import fitz
    doc = fitz.open(stream=arquivo, filetype="pdf")
    return "\n\n".join(p.get_text("text") for p in doc).strip()

def extrair_pptx(arquivo):
    from pptx import Presentation
    prs = Presentation(io.BytesIO(arquivo))
    blocos = []
    for i, slide in enumerate(prs.slides, start=1):
        linhas = []
        for shape in slide.shapes:
            if getattr(shape, "has_text_frame", False) and shape.text.strip():
                linhas.append(shape.text.strip())
        if linhas:
            blocos.append(f"Slide {i}\n" + "\n".join(linhas))
    return "\n\n".join(blocos).strip()

def frases(texto):
    texto = re.sub(r"\s+", " ", texto).strip()
    return [x.strip() for x in re.split(r"(?<=[.!?])\s+", texto) if x.strip()]

def simplificar(texto, nivel_escolhido):
    substituicoes = {
        " realizar ": " fazer ", " utilizar ": " usar ", " adquirir ": " comprar ",
        " aproximadamente ": " cerca de ", " posteriormente ": " depois ",
        " entretanto ": " mas ", " portanto ": " por isso ", " devido a ": " por causa de ",
        " necessário ": " preciso ", " metodologia ": " forma de fazer ",
        " compreender ": " entender ", " identificar ": " encontrar ",
        " apresenta ": " mostra ", " apresentar ": " mostrar ",
        " indivíduos ": " pessoas ", " crianças e adolescentes ": " crianças e jovens ",
    }
    resultado = " " + re.sub(r"\s+", " ", texto).strip() + " "
    if nivel_escolhido.startswith(("Muito simples", "Simples")):
        for antigo, novo in substituicoes.items():
            resultado = re.sub(re.escape(antigo), novo, resultado, flags=re.IGNORECASE)
    return "\n\n".join(frases(resultado)).strip()

def resumo(texto):
    itens = frases(texto)
    if not itens:
        return "Não há texto suficiente para criar um resumo."
    return "\n".join("• " + x for x in itens[:min(6, len(itens))])

def glossario(texto):
    palavras = re.findall(r"\b[A-Za-zÀ-ÿ]{9,}\b", texto.lower())
    comuns = {"importância", "diferentes", "necessidade", "possibilidade", "utilização", "desenvolvimento"}
    termos = [p for p, _ in Counter(palavras).most_common(8) if p not in comuns]
    if not termos:
        return "Não foram encontrados termos longos suficientes para sugerir um glossário."
    return "\n".join(f"• {t.capitalize()}: palavra que pode precisar de explicação no contexto do texto." for t in termos)

def perguntas(texto):
    itens = frases(texto)
    if not itens:
        return "Adicione um texto para criar perguntas."
    saida = []
    for i, frase in enumerate(itens[:5], start=1):
        curta = frase[:180].rstrip()
        saida.append(f"{i}. O que o texto informa sobre: “{curta}”?\nResposta esperada: o estudante deve explicar a informação apresentada nesse trecho.")
    return "\n\n".join(saida)

def apoio_visual(texto):
    mapa = [
        (["água", "rio", "mar", "chuva"], "💧"), (["planta", "árvore", "flor", "floresta"], "🌱"),
        (["escola", "aluno", "estudante", "professor"], "🏫"), (["número", "conta", "matemática", "somar"], "🔢"),
        (["sol", "planeta", "terra", "espaço"], "🌎"), (["livro", "leitura", "texto", "história"], "📖"),
        (["animal", "cachorro", "gato", "ser vivo"], "🐾"), (["corpo", "saúde", "coração"], "❤️"),
    ]
    linhas = []
    for f in frases(texto)[:8]:
        low = f.lower()
        emoji = next((e for palavras, e in mapa if any(p in low for p in palavras)), "💡")
        linhas.append(f"{emoji}  {f[:110]}")
    return "\n".join(linhas) if linhas else "Adicione um texto para criar apoio visual."

def gerar_descricao_imagem():
    return ("A imagem foi carregada e está disponível para visualização. "
            "Neste protótipo sem IA, a descrição acessível deve ser preenchida por uma pessoa que consiga observar a imagem. "
            "Descreva o que aparece, a organização dos elementos, textos, gráficos e informações importantes.")

def limpar():
    for key, value in defaults.items():
        st.session_state[key] = value.copy() if isinstance(value, (dict, list)) else value

# ------------------------- Área de trabalho -------------------------
abas = st.tabs(["📥 Enviar material", "✨ Criar adaptações", "✅ Revisar", "🔊 Acessibilidade", "📊 Painel", "ℹ️ Sobre"])

opcoes = {
    "simples": "Texto em linguagem simples", "resumo": "Resumo em tópicos",
    "glossario": "Glossário de palavras", "perguntas": "Perguntas de compreensão",
    "visual": "Apoio visual com emojis", "imagem": "Orientação para descrição de imagem",
}

with abas[0]:
    st.markdown('<div class="section-kicker">Etapa 01</div><div class="section-title">Vamos começar pelo conteúdo</div><p class="section-desc">Envie um material ou cole o texto que deseja adaptar.</p>', unsafe_allow_html=True)
    col1, col2 = st.columns([1.35, .85], gap="large")
    with col1:
        arquivo = st.file_uploader(
            "Escolha um arquivo para enviar",
            type=["pdf", "pptx", "txt", "png", "jpg", "jpeg", "webp", "mp3", "wav", "m4a", "ogg", "mp4", "mov", "webm"],
            help="Formatos aceitos: PDF, PPTX, TXT, imagens, áudio e vídeo.",
        )
        texto_manual = st.text_area("Ou cole/digite o conteúdo aqui", height=190, placeholder="Cole aqui o texto da atividade, apostila ou material...")
        if st.button("📚 Carregar conteúdo", type="primary", use_container_width=True):
            conteudo = texto_manual.strip()
            if arquivo:
                dados = arquivo.getvalue()
                ext = arquivo.name.rsplit(".", 1)[-1].lower()
                st.session_state.nome_arquivo = arquivo.name
                try:
                    if ext == "pdf":
                        conteudo = extrair_pdf(dados) or conteudo
                    elif ext == "pptx":
                        conteudo = extrair_pptx(dados) or conteudo
                    elif ext == "txt":
                        conteudo = dados.decode("utf-8", errors="replace")
                    elif ext in ["png", "jpg", "jpeg", "webp"]:
                        st.session_state.arquivo_midia, st.session_state.tipo_midia = dados, ext
                    elif ext in ["mp3", "wav", "m4a", "ogg", "mp4", "mov", "webm"]:
                        st.session_state.arquivo_midia, st.session_state.tipo_midia = dados, ext
                        st.warning("Áudio e vídeo podem ser reproduzidos, mas a transcrição automática não está ativada nesta versão.")
                    st.session_state.materiais += 1
                except Exception as e:
                    st.error(f"Não foi possível ler o arquivo: {e}")
            if conteudo:
                st.session_state.texto = conteudo
            if not conteudo and not st.session_state.arquivo_midia:
                st.warning("Envie um arquivo compatível ou cole um texto.")
            else:
                st.success("Material carregado! Confira o conteúdo abaixo.")
    with col2:
        st.markdown("""
        <div class="soft-card">
          <div class="feature-icon">🗂️</div><h3>O que você pode enviar?</h3>
          <p class="small-muted">Textos, PDFs, apresentações, imagens, áudios e vídeos.</p>
          <hr style="border:0;border-top:1px solid #e7e9f5;margin:15px 0">
          <div class="feature-icon">🔐</div><h3>Privacidade</h3>
          <p class="small-muted">O processamento demonstrativo de texto acontece localmente. Não é necessário conectar uma conta de IA.</p>
        </div>
        """, unsafe_allow_html=True)
    if st.session_state.arquivo_midia:
        ext = st.session_state.tipo_midia
        if ext in ["png", "jpg", "jpeg", "webp"]:
            st.image(st.session_state.arquivo_midia, caption="Imagem enviada", use_container_width=True)
        elif ext in ["mp3", "wav", "m4a", "ogg"]:
            st.audio(st.session_state.arquivo_midia)
        else:
            st.video(st.session_state.arquivo_midia)
    if st.session_state.texto:
        st.markdown("#### Conteúdo extraído")
        st.session_state.texto = st.text_area("Revise o texto antes de continuar", value=st.session_state.texto, height=230, key="editor_conteudo")
        st.caption(f"{len(st.session_state.texto.split())} palavras • {len(st.session_state.texto)} caracteres")
    if st.button("Limpar material", type="secondary"):
        limpar()
        st.rerun()

with abas[1]:
    st.markdown('<div class="section-kicker">Etapa 02</div><div class="section-title">Escolha como transformar o conteúdo</div><p class="section-desc">Selecione os recursos que deseja experimentar.</p>', unsafe_allow_html=True)
    st.markdown('<div class="callout">🧠 As ferramentas desta versão aplicam regras simples. Elas ajudam a demonstrar a proposta, mas não substituem uma adaptação pedagógica feita por profissionais.</div>', unsafe_allow_html=True)
    selecionados = st.multiselect("Adaptações", list(opcoes), default=["simples", "resumo"], format_func=lambda x: opcoes[x])
    if st.button("✨ Gerar adaptações", type="primary", disabled=not bool(st.session_state.texto.strip()), use_container_width=True):
        inicio = time.time()
        texto = st.session_state.texto
        funcoes = {
            "simples": lambda: simplificar(texto, nivel),
            "resumo": lambda: resumo(texto),
            "glossario": lambda: glossario(texto),
            "perguntas": lambda: perguntas(texto),
            "visual": lambda: apoio_visual(texto),
            "imagem": gerar_descricao_imagem,
        }
        for item in selecionados:
            resultado = funcoes[item]()
            st.session_state.adaptacoes[item] = resultado
            st.session_state.originais[item] = resultado
            st.session_state.revisoes[item] = False
            st.session_state.historico.append({"recurso": opcoes[item], "segundos": round(time.time()-inicio, 2)})
        st.success("Adaptações demonstrativas criadas. Acesse a aba Revisar.")
    if not st.session_state.texto.strip():
        st.info("Primeiro carregue um material ou digite um texto na aba Enviar material.")

with abas[2]:
    st.markdown('<div class="section-kicker">Etapa 03</div><div class="section-title">Revise com atenção</div><p class="section-desc">Ajuste os resultados e marque quando a revisão estiver concluída.</p>', unsafe_allow_html=True)
    if not st.session_state.adaptacoes:
        st.info("Nenhuma adaptação foi criada ainda.")
    for chave, valor in list(st.session_state.adaptacoes.items()):
        with st.expander(opcoes.get(chave, chave), expanded=True):
            editado = st.text_area("Edite o conteúdo", value=valor, height=190, key=f"rev_{chave}")
            st.session_state.adaptacoes[chave] = editado
            st.session_state.revisoes[chave] = st.checkbox(
                "Revisado por profissional responsável",
                value=st.session_state.revisoes.get(chave, False), key=f"check_{chave}",
            )

with abas[3]:
    st.markdown('<div class="section-kicker">Etapa 04</div><div class="section-title">Acessibilidade para acompanhar</div><p class="section-desc">Ouça os textos e baixe os materiais gerados.</p>', unsafe_allow_html=True)
    st.markdown("#### Leitura em voz alta")
    st.caption("Utiliza a voz disponível no próprio navegador, sem serviço externo.")
    if st.session_state.adaptacoes:
        lista_textos = {"Texto original": st.session_state.texto}
        lista_textos.update({opcoes.get(k, k): v for k, v in st.session_state.adaptacoes.items()})
        escolhido = st.selectbox("Escolha o conteúdo", list(lista_textos))
        fala = lista_textos[escolhido]
        if escolhido != "Texto original":
            chave_escolhida = next((k for k in st.session_state.adaptacoes if opcoes.get(k) == escolhido), None)
            if chave_escolhida and not st.session_state.revisoes.get(chave_escolhida):
                st.warning("Este conteúdo ainda não foi marcado como revisado.")
        fala_html = html.escape(fala)
        st.components.v1.html(f"""
        <div style="font-family:Arial,sans-serif;padding:8px 0">
          <button id="play" style="background:#465bd0;color:white;border:0;border-radius:10px;padding:12px 18px;font-size:15px;font-weight:bold;cursor:pointer">▶ Ouvir texto</button>
          <button id="stop" style="background:#f0edff;color:#30346f;border:1px solid #d8d4fa;border-radius:10px;padding:12px 18px;font-size:15px;cursor:pointer;margin-left:8px">■ Parar</button>
          <span id="status" style="margin-left:10px;color:#526087;font-size:13px"></span>
        </div>
        <script>
        const texto = {fala_html!r};
        const status = document.getElementById('status');
        document.getElementById('play').onclick = () => {{
          if (!('speechSynthesis' in window)) {{ status.textContent='Leitura em voz alta não disponível neste navegador.'; return; }}
          window.speechSynthesis.cancel();
          const fala = new SpeechSynthesisUtterance(texto);
          fala.lang='pt-BR'; fala.rate=0.9;
          fala.onstart=()=>status.textContent='Lendo...';
          fala.onend=()=>status.textContent='Leitura concluída.';
          window.speechSynthesis.speak(fala);
        }};
        document.getElementById('stop').onclick = () => {{ window.speechSynthesis.cancel(); status.textContent='Leitura pausada.'; }};
        </script>
        """, height=72)
    else:
        st.info("Gere uma adaptação primeiro para habilitar a leitura em voz alta.")
    st.markdown("#### Baixar materiais")
    if st.session_state.adaptacoes:
        pacote = "\n\n".join(f"### {opcoes.get(k,k)}\n{v}" for k,v in st.session_state.adaptacoes.items())
        st.download_button("⬇️ Baixar adaptações (.txt)", pacote, "adaptacoes_escola_sem_barreiras.txt", use_container_width=True)
    if st.session_state.texto:
        st.download_button("⬇️ Baixar texto original (.txt)", st.session_state.texto, "texto_original.txt", use_container_width=True)

with abas[4]:
    st.markdown('<div class="section-kicker">Acompanhamento</div><div class="section-title">Seu painel de atividades</div><p class="section-desc">Indicadores registrados nesta sessão.</p>', unsafe_allow_html=True)
    total = len(st.session_state.historico)
    revisadas = sum(bool(x) for x in st.session_state.revisoes.values())
    editadas = sum(st.session_state.adaptacoes.get(k, "") != v for k, v in st.session_state.originais.items())
    c1,c2,c3,c4 = st.columns(4)
    c1.metric("Materiais carregados", st.session_state.materiais)
    c2.metric("Adaptações criadas", total)
    c3.metric("Revisões concluídas", revisadas)
    c4.metric("Conteúdos editados", editadas)
    st.caption("Os indicadores se referem apenas à sessão atual e não representam resultados de aprendizagem.")
    if st.session_state.historico:
        csv_buffer = io.StringIO()
        writer = csv.DictWriter(csv_buffer, fieldnames=["recurso", "segundos"])
        writer.writeheader()
        writer.writerows(st.session_state.historico)
        st.download_button("Baixar indicadores (.csv)", csv_buffer.getvalue(), "indicadores_sessao.csv")

with abas[5]:
    st.markdown('<div class="section-kicker">Conheça o projeto</div><div class="section-title">Aprendizagem com menos barreiras</div>', unsafe_allow_html=True)
    st.markdown("""
    <div class="soft-card">
      <p>O <b>Escola Sem Barreiras</b> é uma proposta de apoio à inclusão escolar. A ideia é facilitar o acesso ao conteúdo por meio de diferentes formatos de leitura e compreensão.</p>
      <h3>O que este protótipo demonstra</h3>
      <ul>
        <li>Importação de textos, PDFs e apresentações.</li>
        <li>Simplificação básica de linguagem e organização de conteúdo.</li>
        <li>Resumo, glossário, perguntas e apoio visual.</li>
        <li>Edição e revisão por uma pessoa responsável.</li>
        <li>Leitura em voz alta pelo navegador e exportação de arquivos.</li>
        <li>Painel de indicadores da sessão.</li>
      </ul>
      <h3>Limitações desta versão</h3>
      <ul>
        <li>Não utiliza IA generativa; os resultados são demonstrativos e podem ser superficiais ou inadequados.</li>
        <li>Imagens podem ser exibidas, mas a descrição deve ser escrita por uma pessoa.</li>
        <li>Não há transcrição automática de áudio/vídeo.</li>
        <li>Não gera Libras nem Braille.</li>
      </ul>
      <p><b>Compromisso com a acessibilidade:</b> o aplicativo é um protótipo de apoio e não substitui professores, profissionais do Atendimento Educacional Especializado (AEE), intérpretes de Libras ou profissionais de Braille. Toda adaptação deve ser avaliada por um profissional antes de ser utilizada.</p>
    </div>
    """, unsafe_allow_html=True)
    st.warning("Privacidade: evite inserir nomes, laudos ou outros dados pessoais de estudantes em demonstrações públicas.")

st.markdown('<div class="footer">Escola Sem Barreiras · Aprender é para todos · Protótipo demonstrativo</div>', unsafe_allow_html=True)
