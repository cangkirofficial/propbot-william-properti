import streamlit as st
import os
import warnings
warnings.filterwarnings("ignore")

st.set_page_config(
    page_title="William Properti — PROPBOT",
    page_icon="🏠",
    layout="wide",
    initial_sidebar_state="expanded"
)

st.markdown("""
<style>
    @import url("https://fonts.googleapis.com/css2?family=Playfair+Display:wght@400;700&family=Lato:wght@300;400;700&display=swap");
    .stApp { background: linear-gradient(135deg, #0a0a0a 0%, #1a1410 50%, #0f0d0a 100%); font-family: "Lato", sans-serif; }
    .main .block-container { max-width: 900px; padding-top: 2rem; }
    .header-banner { background: linear-gradient(135deg, #1a1208 0%, #2d1f0a 50%, #1a1208 100%); border: 1px solid #c9a84c; border-radius: 16px; padding: 2rem 2.5rem; margin-bottom: 2rem; }
    .header-title { font-family: "Playfair Display", serif; font-size: 2.2rem; font-weight: 700; color: #c9a84c; margin: 0; }
    .header-subtitle { font-size: 0.9rem; color: #9b8c6e; margin-top: 0.3rem; letter-spacing: 0.1em; text-transform: uppercase; }
    .header-badge { display: inline-block; background: rgba(201,168,76,0.15); border: 1px solid rgba(201,168,76,0.4); color: #c9a84c; font-size: 0.7rem; padding: 0.2rem 0.7rem; border-radius: 20px; letter-spacing: 0.1em; text-transform: uppercase; margin-top: 0.8rem; }
    [data-testid="stSidebar"] { background: linear-gradient(180deg, #0d0b08 0%, #1a1208 100%) !important; border-right: 1px solid rgba(201,168,76,0.2) !important; }
    [data-testid="stSidebar"] * { color: #c9a84c !important; }
    .contact-card { background: rgba(201,168,76,0.08); border: 1px solid rgba(201,168,76,0.25); border-radius: 12px; padding: 1rem; margin: 0.5rem 0 1rem; }
    [data-testid="stChatMessage"][data-role="user"] { background: rgba(201,168,76,0.08) !important; border: 1px solid rgba(201,168,76,0.2) !important; border-radius: 16px 4px 16px 16px !important; }
    [data-testid="stChatMessage"][data-role="assistant"] { background: rgba(255,255,255,0.03) !important; border: 1px solid rgba(255,255,255,0.07) !important; border-radius: 4px 16px 16px 16px !important; }
    .stChatInputContainer { border: 1px solid rgba(201,168,76,0.3) !important; border-radius: 12px !important; }
    .stChatInputContainer:focus-within { border-color: #c9a84c !important; }
    .stMarkdown p, .stMarkdown li { color: #c8b99a !important; }
    #MainMenu {visibility: hidden;} footer {visibility: hidden;} header {visibility: hidden;}
</style>
""", unsafe_allow_html=True)

@st.cache_resource(show_spinner=False)
def load_rag():
    import nltk
    nltk.download("punkt_tab", quiet=True)
    nltk.download("punkt", quiet=True)
    from langchain_google_genai import GoogleGenerativeAIEmbeddings, ChatGoogleGenerativeAI
    from langchain_community.vectorstores import Chroma
    from langchain_core.prompts import ChatPromptTemplate
    from langchain_core.messages import SystemMessage
    from langchain_core.prompts import HumanMessagePromptTemplate
    from langchain_core.output_parsers import StrOutputParser
    from langchain_core.runnables import RunnablePassthrough

    api_key = os.environ.get("GOOGLE_API_KEY", "")

    embeddings = GoogleGenerativeAIEmbeddings(
        model="models/gemini-embedding-2",
        google_api_key=api_key,
        output_dimensionality=768
    )
    vectorstore = Chroma(
        persist_directory="./chroma_properti_db",
        embedding_function=embeddings
    )
    retriever = vectorstore.as_retriever(search_kwargs={"k": 5})

    chat_model = ChatGoogleGenerativeAI(
        model="gemini-2.5-flash-lite",
        google_api_key=api_key,
        temperature=0.3
    )

    SYSTEM_PROMPT = (
        "Kamu adalah asisten virtual William, agen properti profesional di Jawa Barat. "
        "Nama kamu adalah PROPBOT. Bantu calon pembeli temukan properti impian mereka. "
        "Jawab ramah, profesional, Bahasa Indonesia yang hangat. "
        "Sertakan harga dan cicilan saat relevan. Gunakan emoji secukupnya. "
        "Kontak William: 123456789. "
        "PENTING: Hanya gunakan info dari konteks. Jangan mengarang data properti."
    )

    HUMAN_TEMPLATE = (
        "Konteks katalog:\n"
        "{context}\n\n"
        "Pertanyaan: {question}\n\n"
        "Jawaban:"
    )

    chat_template = ChatPromptTemplate.from_messages([
        SystemMessage(content=SYSTEM_PROMPT),
        HumanMessagePromptTemplate.from_template(HUMAN_TEMPLATE)
    ])

    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    chain = (
        {"context": retriever | format_docs, "question": RunnablePassthrough()}
        | chat_template
        | chat_model
        | StrOutputParser()
    )
    return chain

with st.sidebar:
    st.markdown("<h2 style='font-family:serif; font-size:1.4rem; color:#c9a84c; margin-bottom:0;'>🏠 PROPBOT</h2>", unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem; color:#6b5c3e; letter-spacing:0.15em; text-transform:uppercase; margin-top:0;'>by William Properti</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(201,168,76,0.2);'/>", unsafe_allow_html=True)
    st.markdown("""
    <div class='contact-card'>
        <p style='margin:0; font-size:0.8rem; font-weight:700;'>📞 HUBUNGI WILLIAM</p>
        <p style='margin:0.3rem 0 0; font-size:1.1rem; font-weight:700;'>123456789</p>
        <p style='margin:0.2rem 0 0; font-size:0.7rem; color:#6b5c3e; text-transform:uppercase; letter-spacing:0.1em;'>Agen Resmi Properti Jawa Barat</p>
    </div>
    """, unsafe_allow_html=True)
    st.markdown("<p style='font-size:0.7rem; letter-spacing:0.1em; text-transform:uppercase; color:#6b5c3e;'>📍 Kota Tersedia</p>", unsafe_allow_html=True)
    for k in ["Bandung","Bekasi","Bogor","Depok","Karawang","Cirebon","Sukabumi","Tasikmalaya","Purwakarta","Cimahi"]:
        st.markdown(f"<p style='font-size:0.82rem; padding:0.1rem 0; margin:0; color:#9b8c6e;'>• {k}</p>", unsafe_allow_html=True)
    st.markdown("<hr style='border-color:rgba(201,168,76,0.2);'/>", unsafe_allow_html=True)
    if st.button("🗑️ Reset Percakapan", use_container_width=True):
        st.session_state.messages = []
        st.rerun()

st.markdown("""
<div class="header-banner">
    <p class="header-title">🏠 William Properti</p>
    <p class="header-subtitle">Katalog Properti Terpercaya Jawa Barat 2026</p>
    <span class="header-badge">✦ PROPBOT Virtual Assistant ✦</span>
</div>
""", unsafe_allow_html=True)

if "messages" not in st.session_state:
    st.session_state.messages = []

with st.spinner("⚙️ Memuat sistem RAG..."):
    try:
        rag_chain = load_rag()
    except Exception as e:
        st.error(f"Gagal memuat RAG: {e}")
        st.stop()

if not st.session_state.messages:
    welcome = "Halo! 👋 Selamat datang di **PROPBOT** — asisten virtual William Properti!\n\nSaya siap membantu Anda menemukan properti impian di **Jawa Barat** 🏡\n\nTanyakan tentang harga, lokasi, cicilan, atau minta rekomendasi sesuai budget Anda!"
    st.session_state.messages.append({"role": "assistant", "content": welcome})

if len(st.session_state.messages) <= 1:
    cols = st.columns(2)
    suggestions = [
        ("🏙️ Properti di Bandung", "Properti apa saja yang tersedia di Bandung?"),
        ("💰 Budget di bawah 1 Miliar", "Rekomendasikan properti dengan harga di bawah 1 miliar rupiah"),
        ("🏗️ Cicilan termurah", "Properti mana yang punya cicilan paling murah?"),
        ("📍 Dekat tol atau stasiun", "Properti apa yang dekat dengan akses tol atau stasiun?"),
    ]
    for i, (label, query) in enumerate(suggestions):
        with cols[i % 2]:
            if st.button(label, use_container_width=True, key=f"sug_{i}"):
                st.session_state.messages.append({"role": "user", "content": query})
                with st.spinner("🔍 Mencari properti..."):
                    response = rag_chain.invoke(query)
                st.session_state.messages.append({"role": "assistant", "content": response})
                st.rerun()

for msg in st.session_state.messages:
    with st.chat_message(msg["role"]):
        st.markdown(msg["content"])

if prompt := st.chat_input("Tanyakan tentang properti impian Anda..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)
    with st.chat_message("assistant"):
        with st.spinner("🔍 PROPBOT sedang mencari informasi..."):
            try:
                response = rag_chain.invoke(prompt)
            except Exception as e:
                response = f"Maaf, terjadi error: {e}. Silakan hubungi William di 123456789."
        st.markdown(response)
    st.session_state.messages.append({"role": "assistant", "content": response})
