
import requests
import json
import gradio as gr
import time

url = "http://localhost:11434/api/generate"
headers = {
    'Content-Type': 'application/json',
}
conversation_history = []
tiny_model = "tinyllama"
llama3_model = "llama3"
current_model = tiny_model
print(f"The model used is {current_model}")

def generate_response(question, progress=gr.Progress()):
    conversation_history.append(question)
    full_prompt = "\n".join(conversation_history)
    p = format_prompt(question, current_model)
    print(f"The question is:\n{p}")
    data = {
        "model": current_model,
        "stream": False,
        "prompt": p,
    }

    start_time = time.perf_counter()
    response = requests.post(url, headers=headers, data=json.dumps(data))
    end_time = time.perf_counter()
    elapsed_time = round(end_time - start_time, 2)
    print(f"Elapsed time {elapsed_time:.2f}s")

    if response.status_code == 200:
        response_text = response.text
        data = json.loads(response_text)
        actual_response = data["response"]
        conversation_history.append(actual_response)
        return actual_response, current_model, elapsed_time
    else:
        print("Error:", response.status_code, response.text)
        return None

def run_ui():
    iface = gr.Interface(
        fn=generate_response,
        inputs=gr.Textbox(lines=2, placeholder="Enter your prompt here..."),
        outputs=["text", gr.Textbox(label="Model"), gr.Number(label="Runtime")]
    )
    iface.launch()

def format_prompt(question, model):
    if (model == tiny_model):
        return tiny_prompt(question)
    elif (model == llama3_model):
        return llama3(question)
    else:
        return question

def tiny_prompt(question):
    p1 = f"""
<|system|>
You are a friendly chatbot.</s>
<|user|>
{question}</s>
<|assistant|>
"""
    p2 = f"""
<|system|>
You are a friendly chatbot.
<|user|>
{question}
<|assistant|>
"""
    return p2

def llama3(question):
    return f"""
<|begin_of_text|><|start_header_id|>user<|end_header_id|>
{question}
<|eot_id|><|start_header_id|>assistant<|end_header_id|>
"""

run_ui()