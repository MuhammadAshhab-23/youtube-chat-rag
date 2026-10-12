
from langchain_text_splitters import RecursiveCharacterTextSplitter
from langchain_openai import OpenAIEmbeddings, ChatOpenAI
from langchain_community.vectorstores import FAISS
from langchain_core.prompts import PromptTemplate
from langchain_core.output_parsers import StrOutputParser
from langchain_core.runnables import RunnablePassthrough


def create_rag_chain(transcript):
    # 1. Split transcript into chunks
    splitter = RecursiveCharacterTextSplitter(
        chunk_size=1000,
        chunk_overlap=200
    )
    chunks = splitter.create_documents([transcript])

    print(f"Number of chunks: {len(chunks)}")

    # 2. Create embeddings and FAISS vector store
    embeddings = OpenAIEmbeddings(
        model="text-embedding-3-small"
    )
    vector_store = FAISS.from_documents(chunks, embeddings)

    # 3. Create retriever
    retriever = vector_store.as_retriever(
        search_type="similarity",
        search_kwargs={"k": 4}
    )

    # 4. Create prompt
    prompt = PromptTemplate(
        template="""Answer using only the provided transcript context.
If the answer is not available, say you don't know.

Context:
{context}

Question:
{question}""",
        input_variables=["context", "question"]
    )

    # 5. Create LLM
    llm = ChatOpenAI(
        model="gpt-4o-mini",
        temperature=0
    )

    # 6. Connect everything into one RAG chain
    def format_docs(docs):
        return "\n\n".join(doc.page_content for doc in docs)

    rag_chain = (
        {
            "context": retriever | format_docs,
            "question": RunnablePassthrough()
        }
        | prompt
        | llm
        | StrOutputParser()
    )

    return rag_chain
