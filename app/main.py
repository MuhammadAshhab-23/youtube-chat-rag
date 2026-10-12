
from dotenv import load_dotenv

from app.transcript import fetch_transcript
from app.rag_pipeline import create_rag_chain


def main():
    load_dotenv()

    url = input("Enter YouTube video URL: ").strip()

    try:
        transcript = fetch_transcript(url)
        print("\nTranscript fetched successfully!")

        rag_chain = create_rag_chain(transcript)
        print("RAG pipeline ready! Ask your questions.")

        while True:
            question = input("\nYou: ").strip()

            if question.lower() in ("exit", "quit"):
                print("Goodbye, bro!")
                break

            if not question:
                continue

            answer = rag_chain.invoke(question)
            print("\nAnswer:", answer)

    except Exception as error:
        print(f"\nError: {error}")


if __name__ == "__main__":
    main()




    
    
