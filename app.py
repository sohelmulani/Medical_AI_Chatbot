
import os
from flask import Flask, render_template, request, jsonify
from langchain_openai import ChatOpenAI
from langchain_pinecone import PineconeVectorStore
from langchain.chains import ConversationalRetrievalChain
from langchain.memory import ConversationBufferMemory
from dotenv import load_dotenv
from src.prompts import *
from src.helpers import get_embeddings
from flask_cors import CORS


# Load environment variables
load_dotenv()

PINECONE_API_KEY = os.getenv("PINECONE_API_KEY")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

# Initiate Flask app
app = Flask(__name__)

# LLM model
llm_model = ChatOpenAI(
    openai_api_key=OPENAI_API_KEY,
    model_name="gpt-5-nano"
)

# Pinecone setup
index_name = "medical-assistant"
embeddings = get_embeddings()
vector_store = PineconeVectorStore.from_existing_index(
    index_name=index_name,
    embedding=embeddings
)
retriever = vector_store.as_retriever(search_type="similarity", search_kwargs={"k": 3})

# Buffer Memory setup to memorise past conversations
memory = ConversationBufferMemory(
    memory_key="chat_history",
    return_messages=True
)

# Conversational RAG chain
rag_chain = ConversationalRetrievalChain.from_llm(
    llm=llm_model,
    retriever=retriever,
    memory=memory
)

# Main page
@app.route('/', methods=['GET'])
def index():
    return render_template('bot.html')

# JSON API endpoint
@app.route('/ask', methods=['POST'])
def ask():
    data = request.get_json()
    question = data.get('question')
    if not question:
        return jsonify({"Error": "Please ask a question to proceed"}), 400

    result = rag_chain({"question": question})
    answer = result["answer"]

    return jsonify({"answer": answer}), 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)