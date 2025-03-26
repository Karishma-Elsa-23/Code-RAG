from transformers import AutoModelForCausalLM, AutoTokenizer
import torch
import QueryFaiss
import os
import nltk
import RunBM25
from rocksdb import retrieval
import get_user_query

nltk.download('punkt_tab')

# Configuration
config = {
    "model_name": "Qwen/Qwen2.5-Coder-1.5B",
    "max_length": 2048,
    "temperature": 0.7,
    "top_p": 0.9,
    "model_save_path": "./saved_model"  # Path where the model weights will be saved
}

# Initialize tokenizer
tokenizer = AutoTokenizer.from_pretrained(config["model_name"])

# Initialize the model
def initialize_model():
    #Checking if CUDA is available
    device = "cuda" if torch.cuda.is_available() else "cpu"
    #device = "cpu" checking wjich works better
    print(f"Using device: {device}")

    # Check if model weights already exist on the disk
    if os.path.exists(config["model_save_path"]):
        print("Loading saved model weights...")
        model = AutoModelForCausalLM.from_pretrained(config["model_save_path"])
    else:
        print("Loading model for the first time...")
        model = AutoModelForCausalLM.from_pretrained(config["model_name"])
        # Save the model weights after the first run
        model.save_pretrained(config["model_save_path"])
        print(f"Model saved to {config['model_save_path']}")

    model = model.to(device)

    return model, device

# Initialize the model
model, device = initialize_model()

# Construct a hardcoded prompt
def construct_prompt_for_comments(function_code, nl, reference_snippets):
    prompt = nl + f"\n\nFunction to Comment:\n{function_code}\n\n Code snippets for reference:\n"
    for idx, snippet in enumerate(reference_snippets, 1):
        prompt += f"{idx}. {snippet}\n\n"
    prompt += "Add Comments only for the function that I have given, do not include the reference code snippets in the output:\n"
    return prompt

# Generate output
def generate_output(prompt):
    inputs = tokenizer(prompt, return_tensors="pt", max_length=2048, truncation=True)
    input_ids = inputs["input_ids"]

    input_ids = input_ids.to(model.device)
    # print(f"Tokens: {inputs}")
    # print(f"Token Count: {input_ids.shape[1]}")

    outputs = model.generate(
        input_ids, 
        max_length=config["max_length"], 
        temperature=config["temperature"], 
        top_p=config["top_p"]
    )

    return tokenizer.decode(outputs[0], skip_special_tokens=True)

# Main Function
def main():
    # Function for which comments are needed
    nl, code, codelan = get_user_query.split_natural_language_code() #codelan = 0 -> function is python, = 1 -> cpp, = 2 -> Cannot decide
    if(codelan == 2):
        print("ERRORRRR")
        return
    # else:
    #     print(codelan)

    # print(nl)
    # print(code)

    faiss_indices = QueryFaiss.query_faiss(codelan, code)
    if codelan == 0:
        faiss_top = retrieval.retrieve_data('./rocksdb/py_rocksdb', faiss_indices[0])
    elif codelan == 1:
        faiss_top = retrieval.retrieve_data('./rocksdb/cpp_rocksdb', faiss_indices[0])
    bm25_top = RunBM25.query_bm25(code, codelan)
    reference_snippets = []
    reference_snippets.append(faiss_top['code'])
    reference_snippets.append(faiss_top['description'])
    reference_snippets.append(bm25_top[0]['code'])
    reference_snippets.append(bm25_top[0]['description'])

    prompt = construct_prompt_for_comments(code, nl, reference_snippets)
    output = generate_output(prompt)
    print("Generated Output:\n", output)

if __name__ == "__main__":
    main()
