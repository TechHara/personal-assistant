from fastapi import FastAPI
from fastapi.responses import StreamingResponse
from typing import Dict, List
from transformers import AutoTokenizer, AutoModelForCausalLM, TextIteratorStreamer
from threading import Thread


app = FastAPI()

model_path = 'TinyLlama/TinyLlama-1.1B-Chat-v1.0'

model = AutoModelForCausalLM.from_pretrained(model_path)
tokenizer = AutoTokenizer.from_pretrained(model_path)
streamer = TextIteratorStreamer(
    tokenizer, decode_kwargs={'skip_special_tokens': True},
    skip_prompt=True)   # output only the response
model.eval()


async def stream_response(prompt: str):
    inputs = tokenizer(prompt, return_tensors="pt")
    generation_kwargs = dict(inputs, streamer=streamer)
    thread = Thread(target=model.generate, kwargs=generation_kwargs)
    thread.start()

    generated_text = ''
    for new_text in streamer:
        generated_text += new_text
        yield generated_text
    yield generated_text[:-4]  # remove '</s>' at the end


def generate_prompt(messages: List[Dict]) -> str:
    prompt = '<|system|>\nYou are a friendly chatbot who never refuses to answer anything</s>\n'
    for msg in messages:
        prompt += f'<|{msg["role"]}|>\n{msg["content"]}</s>\n'
    prompt += '<|assistant|>\n'
    print(f'-------------PROMPT---------------\n{prompt}')
    return prompt


@app.post("/model")
async def query(messages: List[Dict]):
    print(f'-------------MSG---------------\n{messages}')
    return StreamingResponse(stream_response(generate_prompt(messages)), media_type='text/event-stream')
