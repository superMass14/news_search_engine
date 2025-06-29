import streamlit as st
import chromadb
from chromadb.utils import embedding_functions
from utils import format_label, format_time

server = chromadb.PersistentClient(path="v_db1")
embedder =  embedding_functions.SentenceTransformerEmbeddingFunction(model_name="paraphrase-multilingual-MiniLM-L12-v2", normalize_embeddings=True)
collection =  server.get_or_create_collection(
                                            "articles",
                                            embedding_function=embedder,
                                            metadata={
                                                "title": "News article",
                                                "description": "to provide",
                                                "author": "mthiaw",
                                            }
                                           )
def search_articles(query):
    res = collection.query(
        query_texts=query,
        n_results=5,
        include=["metadatas", "documents"]
        )
    return res


def show_search_page():
    st.title("🔍 Moteur de recherche d'actualités")

    query = st.text_input(label="Recherche",placeholder= "Taper votre recherche ici...", label_visibility="collapsed")
    st.button("Rechercher", icon="🔍", type="primary", use_container_width=True)
    if query:
        results = search_articles(query)
        size = len(results["ids"][0])
        st.subheader(f"{size} résultats trouvés", divider="red", width="stretch")
        for i in range(size):
            meta = results["metadatas"][0][i]
            document =results["documents"][0][i]
            ids=results["ids"][0][i]
            btn = st.button(meta["headline"], key=ids)
            subh = st.caption(f"{document[:150]}...")
            if btn:
                st.session_state.page = "detail"
                st.session_state.article_id = ids
                st.rerun()



# Fonction pour afficher les détails d'un article
def show_article_detail(article_id):
    article = collection.get(ids=article_id, include=["metadatas", "documents"])
    if article:
        metadatas = article["metadatas"][0]
        st.title(metadatas["headline"])
        st.caption(format_time(metadatas["Date scraped"]))
        st  .caption(format_label("Entités", metadatas["Org_label"]))
        st.divider()
        st.container(border=True).subheader(f"{article['documents'][0]}")

        if st.button("Retour", icon="⬅️", type="tertiary", help="retourner à la page d'accueil"):
            st.session_state.page = "search"
            st.rerun()
    else:
        st.error("Aucun résultat trouvé")

# Initialiser les états
if "page" not in st.session_state:
    st.session_state.page = "search"

st.logo(image="img/news_logo.png", icon_image="img/news_logo.png", size="large")
with st.sidebar:
    st.markdown("""
👋 Hello !  
Bienvenue sur votre **moteur de recherche d’actualités.**  
Tapez un **`mot-clé`** ou une **`phrase`**, et explorez les articles collectés depuis *Senego* rien que pour vous!

    """)
    with st.container():

        st.html(
            """
            <style>
            .footer {
                position: fixed;
                bottom: 0;
                left: 3%;
                color: #555;    
                padding: 10px;
                font-size: 100%;
                width: 100%;
            }
            </style>
            
            <div class="footer">
                version beta 0.0.0 
            </div>
               """)



# Navigation
if st.session_state.page == "search":
    show_search_page()
elif st.session_state.page == "detail":
    show_article_detail(st.session_state.get("article_id"))
