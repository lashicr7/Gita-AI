from langchain.document_loaders import PyPDFLoader, DirectoryLoader
from langchain import PromptTemplate
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.llms import CTransformers
from langchain.chains import RetrievalQA
import chainlit as cl

DB_FAISS_PATH = 'vectorstore/db_faiss'

custom_prompt_template = """Use the following pieces of information to answer the user's question.
If you don't know the answer, just say that you don't know, don't try to make up an answer.

Context: {context}
Question: {question}

Only return the helpful answer below and nothing else.
Helpful answer:
"""

def set_custom_prompt():
    """
    Prompt template for QA retrieval for each vectorstore
    """
    prompt = PromptTemplate(template=custom_prompt_template,
                            input_variables=['context', 'question'])
    return prompt

#Retrieval QA Chain
def retrieval_qa_chain(llm, prompt, db):
    qa_chain = RetrievalQA.from_chain_type(llm=llm,
                                       chain_type='stuff',
                                       retriever=db.as_retriever(search_kwargs={'k': 2}),
                                       return_source_documents=True,
                                       chain_type_kwargs={'prompt': prompt}
                                       )
    return qa_chain

#Loading the model
def load_llm():
    # Load the locally downloaded model here
    llm = CTransformers(
        model = "TheBloke/Llama-2-7B-Chat-GGML",
        model_type="llama",
        max_new_tokens = 512,
        temperature = 0.5
    )
    return llm

#QA Model Function
def qa_bot():
    embeddings = HuggingFaceEmbeddings(model_name="sentence-transformers/all-MiniLM-L6-v2",
                                       model_kwargs={'device': 'cpu'})
    db = FAISS.load_local(DB_FAISS_PATH, embeddings)
    llm = load_llm()
    qa_prompt = set_custom_prompt()
    qa = retrieval_qa_chain(llm, qa_prompt, db)

    return qa

def process_response(response_dict):
    """
    Process the response dictionary and format the result along with source documents.

    Args:
        response_dict (dict): A dictionary containing 'query', 'result', and 'source_documents'.

    Returns:
        str: Formatted result with source documents.
    """
    query = response_dict.get('query', '')
    result = response_dict.get('result', '')
    source_documents = response_dict.get('source_documents', [])

    # Remove '\n' characters in the result
    formatted_result = result.replace('\n', ' ')

    # Create a formatted string containing query, result, and source documents
    formatted_output = f"Query: {query}\nResult: {formatted_result}\nSource Documents:\n"

    for doc in source_documents:
        page_content = doc.page_content.replace('\n', ' ')
        source_info = f"Source: {doc.metadata['source']}, Page: {doc.metadata['page']}"
        formatted_output += f"{page_content}\n{source_info}\n"

    return formatted_output

#output function
def final_result(query):
    qa_result = qa_bot()
    response = qa_result({'query': query})
    # return process_response(response)
    return response


# if __name__ == "__main__":
#     # Input from the command line
#     user_input = input("Enter your query: ")
    
#     # Get the response
#     result = final_result(user_input)
    
#     # Print the response
#     print(process_response(result))
    # what to do in depression?

@cl.on_chat_start
async def start():
    chain = qa_bot()
    msg = cl.Message(content="Starting the bot...")
    await msg.send()
    msg.content = "Hi, Welcome to Gita bot. What is your query?"
    await msg.update()

    cl.user_session.set("chain", chain)

@cl.on_message
async def main(message):
    chain = cl.user_session.get("chain") 
    cb = cl.AsyncLangchainCallbackHandler(
        stream_final_answer=True, answer_prefix_tokens=["FINAL", "ANSWER"]
    )
    cb.answer_reached = True
    res = await chain.acall(message, callbacks=[cb])
    answer = res["result"]
    sources = res["source_documents"]

    if sources:
        answer += f"\nSources:" + str(sources)
    else:
        answer += "\nNo sources found"

    await cl.Message(content=answer).send()