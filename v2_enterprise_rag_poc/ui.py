import streamlit as st
import requests
import os
st.set_page_config(page_title="Assistant RAG & Web", page_icon="", layout="centered")
API_URL = os.getenv("API_URL", "http://localhost:8000/api/chat")

st.title(" Assistant Documentaire IA")
st.caption("Discutez avec vos documents locaux. Fallback automatique sur le Web.")
st.markdown("---")

if "messages" not in st.session_state:
    st.session_state.messages = [{"role": "assistant", "content": "Bonjour ! Posez-moi une question."}]

for message in st.session_state.messages:
    with st.chat_message(message["role"]):
        st.markdown(message["content"])

if prompt := st.chat_input("Tapez votre question ici..."):
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("user"):
        st.markdown(prompt)

    with st.chat_message("assistant"):
        with st.spinner("Recherche en cours..."):
            try:
                response = requests.post(API_URL, json={"question": prompt})
                if response.status_code == 200:
                    data = response.json()
                    # AJOUT : On récupère la source et on formate le message final
                    bot_reply = f"{data['answer']}\n\n---\n*🏷️ Source utilisée : {data['source']}*"
                else:
                    bot_reply = f" Erreur serveur : {response.text}"
            except requests.exceptions.ConnectionError:
                bot_reply = " Impossible de joindre l'API."
            
            st.markdown(bot_reply)
    
    st.session_state.messages.append({"role": "assistant", "content": bot_reply})