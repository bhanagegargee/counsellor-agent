from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv
from typing import List, Dict, Any
import time
load_dotenv()

### Initialize the Groq LLM (set your GROQ_API_KEY in environment)
#print(os.getenv("AI_API"))
groq_api_key = os.getenv("AI_API")



class AdvancedRAGPipeline:
    def __init__(self, retriever, groq_api_key=groq_api_key):
        self.llm=ChatGroq(groq_api_key=groq_api_key,model_name="openai/gpt-oss-120b",temperature=0.1,max_tokens=1000)
        self.retriever = retriever
         

    def query(self, question: str, top_k: int = 3, min_score: float = 0.2, stream: bool = False, summarize: bool = False) -> Dict[str, Any]:
        # Retrieve relevant documents
        results = self.retriever.retrieve(question, top_k=top_k, score_threshold=min_score)
        if not results:
            answer = "No relevant context found."
            sources = []
            context = ""
        else:
            context = "\n\n".join([doc['content'] for doc in results])
            sources = [{
                'source': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
                'page': doc['metadata'].get('page', 'unknown'),
                'preview': doc['content'][:120] + '...'
            } for doc in results]
         
            prompt = f"""You are an experienced admission counsellor for undergraduate and postgraduate technical courses in India. Answer the student's question using ONLY the context below.

                          Rules for the answer:
                        - Write in plain text only. Do not use markdown, tables, bullet symbols, asterisks, pipes, headings or bold text.
                        - Write one or two short paragraphs, about 80 to 120 words in total.
                        - Start with the direct answer in the first sentence.
                        - If the context does not give an exact date, fee, or number, say clearly that it is not mentioned in the available documents and advise the student to check the official admission portal. Do not guess or invent dates, timelines or figures.
                        - If the context only partly answers the question, give the part that is available and say what is missing.
                        - Use a polite, simple tone. Do not repeat the question.  
            Context:
            {context}
            
            Question: 
            {question}
            
            Answer:"""

            # if stream:
            #     print("Streaming answer:")
            #     for i in range(0, len(prompt), 80):
            #         print(prompt[i:i+80], end='', flush=True)
            #         time.sleep(0.05)
            #     print()

            response = self.llm.invoke(prompt)
            answer = response.content


        citations = [f"[{i+1}] {src['source']} (page {src['page']})" for i, src in enumerate(sources)]
        answer_with_citations = answer + "\n\nCitations:\n" + "\n".join(citations) if citations else answer

      
       

        return {
            'answer': answer_with_citations,
            'sources': sources,
        }

    def stream_query(self, question: str, top_k: int = 3, min_score: float = 0.2):
        """Generator: yields the answer piece by piece, then the citations."""
        results = self.retriever.retrieve(question, top_k=top_k, score_threshold=min_score)

        if not results:
            yield "No relevant context found."
            return

        context = "\n\n".join(doc['content'] for doc in results)
        sources = [{
            'source': doc['metadata'].get('source_file', doc['metadata'].get('source', 'unknown')),
            'page': doc['metadata'].get('page', 'unknown'),
            'preview': doc['content'][:120] + '...'
        } for doc in results]

        prompt = f"""You are an experienced admission counsellor for undergraduate and postgraduate technical courses in India. Answer the student's question using ONLY the context below.
        
                                  Rules for the answer:
                                - Write in plain text only. Do not use markdown, tables, bullet symbols, asterisks, pipes, headings or bold text.
                                - Write one or two short paragraphs, about 80 to 120 words in total.
                                - Start with the direct answer in the first sentence.
                                - If the context does not give an exact date, fee, or number, say clearly that it is not mentioned in the available documents and advise the student to check the official admission portal. Do not guess or invent dates, timelines or figures.
                                - If the context only partly answers the question, give the part that is available and say what is missing.
                                - Use a polite, simple tone. Do not repeat the question.
        Context:
        {context}

        Question:
        {question}

        Answer:"""

        full_answer = ""
        for chunk in self.llm.stream(prompt):
                text = chunk.content
                if text:
                    full_answer += text
                    yield text

        citations = [f"[{i+1}] {s['source']} (page {s['page']})" for i, s in enumerate(sources)]
        if citations:
                yield "\n\nCitations:\n" + "\n".join(citations)


