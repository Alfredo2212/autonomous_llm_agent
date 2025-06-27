'''
Utilizing hugging face transformers, pretrained LLM 
choosing lightweight LLM for computational efficient
model -> GPT -2 optimized for speed and low memory
'''
from transformers import AutoTokenizer, AutoModelForCausalLM, pipeline

model_name = "distilgpt2"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForCausalLM.from_pretrained(model_name)
qa_pipeline = pipeline("text-generation", model=model, tokenizer=tokenizer)

def generate_answer(query: str, reference_docs: list) -> str:
    context_text = "\n\n".join([doc["content"] for doc in reference_docs])

    # Prompt designed to:   
    # - Minimize hallucination
    # - Encourage concise, source-based answers
    # - Instruct fallback ("I don't know") when context is insufficient
    prompt = (
    "You are a helpful research assistant.\n"
    "Only use the following CONTEXT to answer the question. "
    "Provide a concise answer in plain English. "
    "If the context does not help, say 'I don't know based on the context.'\n\n"
    f"CONTEXT:\n{context_text}\n\n"
    f"QUESTION: {query}\n"
    "ANSWER (use bullet points + cite sources like [Source: reference01.txt]):"
)

    # Sampling parameters (Hyperparameter tuning model answer)
    response = qa_pipeline(
        prompt, 
        max_new_tokens=150, 
        do_sample=True, 
        temperature=0.6,
        top_k=30,
        top_p=0.95,
        repetition_penalty=1.2, 
        return_full_text=False
        )
    
    # Extract generated text 
    output = response[0]['generated_text']
    answer_part = output.split("ANSWER:")[-1] if "ANSWER:" in output else output
    return answer_part.strip()