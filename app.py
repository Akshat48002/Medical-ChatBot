from flask import Flask, request, jsonify,render_template
from langchain_openai import ChatOpenAI
from dotenv import load_dotenv
from src.prompt import prompt_template
from langchain.prompts import PromptTemplate
from langchain.chains import RetrievalQA
from store_index import vectorstore

load_dotenv()

app = Flask(__name__)


llm = ChatOpenAI(
    model="gpt-3.5-turbo",
    temperature=0
)

PROMPT=PromptTemplate(template=prompt_template, input_variables=["context", "question"])
chain_type_kwargs={"prompt": PROMPT}

qa=RetrievalQA.from_chain_type(
    llm=llm, 
    chain_type="stuff", 
    retriever=vectorstore.as_retriever(search_kwargs={"k": 2}),
    return_source_documents=True, 
    chain_type_kwargs=chain_type_kwargs)

@app.route("/")
def index():
    return render_template('chat.html')


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    print(input)
    result=qa({"query": input})
    print("Response : ", result["result"])
    return str(result["result"])



if __name__ == '__main__':
    app.run(host="0.0.0.0", port= 8080, debug= True)