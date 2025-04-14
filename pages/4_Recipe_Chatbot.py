import streamlit as st
import pickle
from langchain.chains import RetrievalQA
from langchain_community.chat_models import ChatOllama

# === Load vector store ===
@st.cache_resource
def load_vector_store():
    with open("./data/embeddings_hf.pickle", "rb") as f:
        return pickle.load(f)

vector_store = load_vector_store()

# ------- Setup RAG QA Chain --------
@st.cache_resource
def setup_qa_chain(_vector_store):
    retriever = vector_store.as_retriever(search_kwargs={"k": 3})
    llm = ChatOllama(
        model="tinyllama",
        temperature=0.3,
        base_url="http://localhost:11434"
    )
    qa_chain = RetrievalQA.from_chain_type(
        llm=llm,
        retriever=retriever,
        return_source_documents=True
    )
    return qa_chain

qa_chain = setup_qa_chain(vector_store)

#-------- Streamlit UI ----------
st.title(" Recipe Help Chatbot")
recipe = st.session_state.get("selected_recipe")
#st.write(recipe)
if recipe:
    st.markdown(f"**👨‍🍳 You're asking about:** `{recipe['name']}`")
    recipe_context = f"""Recipe Name: {recipe['name']}
"""
else:
    recipe_context = ""

st.write("Ask any question about cooking tips, food swaps, or kitchen mishaps!")

query = st.text_input("What do you need help with today? (eg. How can I salvage my burnt dal? )", placeholder="Type your question here...")
submit = st.button("Get Answer")

if submit and query:
    with st.spinner("Thinking..."):
        full_query = f"""
You are a helpful cooking assistant. Here is the recipe the user is working on: {recipe_context}
Based on this recipe, answer the following user question clearly and helpfully.
User Question: {query}
"""

        result = qa_chain(full_query)
        st.markdown("### Answer")
        st.write(result["result"])
        
        # for my ref
        #st.markdown("### 📚 Sources")
        #for doc in result["source_documents"]:
        #    st.write(f"- {doc.metadata['source']}") 
