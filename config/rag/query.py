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
        self.llm=ChatGroq(groq_api_key=groq_api_key,model_name="openai/gpt-oss-120b",temperature=0.1,max_tokens=1024)
        self.retriever = retriever
        self.history = []  

    def query(self, question: str, top_k: int = 5, min_score: float = 0.2, stream: bool = False, summarize: bool = False) -> Dict[str, Any]:
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
         
            prompt = f"""act as a experienced technical education admmission councelor for undergraduate and post graduate courses admission and Use the following context to occurately answer the questions or doubts related to admission process.
            Context:
            {context}
            
            Question: 
            {question}
            
            Answer:"""

            if stream:
                print("Streaming answer:")
                for i in range(0, len(prompt), 80):
                    print(prompt[i:i+80], end='', flush=True)
                    time.sleep(0.05)
                print()
            response = self.llm.invoke([prompt.format(context=context, question=question)])
            answer = response.content


        citations = [f"[{i+1}] {src['source']} (page {src['page']})" for i, src in enumerate(sources)]
        answer_with_citations = answer + "\n\nCitations:\n" + "\n".join(citations) if citations else answer

        # Optionally summarize answer
        # summary = None
        # if summarize and answer:
        #     summary_prompt = f"Summarize the following answer in 2 sentences:\n{answer}"
        #     summary_resp = self.llm.invoke([summary_prompt])
        #     summary = summary_resp.content

        # Store query history
        self.history.append({
            'question': question,
            'answer': answer,
            'sources': sources
        })

        return {
            'answer': answer_with_citations,
            'sources': sources,
            'history': self.history
        }