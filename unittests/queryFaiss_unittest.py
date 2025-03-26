import sys
import os
sys.path.append(os.path.abspath('./'))

import csv
import argparse
import numpy as np
from sentence_transformers import SentenceTransformer
import faiss
import QueryFaiss




def preprocess_text(text):
    """Preprocess text by stripping whitespace and normalizing line endings."""
    text = text.strip()
    text = text.replace('\r\n', '\n').replace('\r', '\n')
    return text

def main():
    parser = argparse.ArgumentParser(description='Insert data from a CSV file to test QueryFaiss.')
    parser.add_argument('csv_file_path', type=str, help='Path to the CSV file containing data')
    parser.add_argument('language', type=str, help='C++ or Python. 1 indicates C++ and 0 indicates Python')

    args = parser.parse_args()
    code = "def sum(a,b):   return a + b"
    code = preprocess_text(code)
    global_list = []
    with open(args.csv_file_path, mode='r', encoding='utf-8', errors='ignore') as csvfile:
      csv_reader = csv.reader(csvfile)
      i = 0
      for row in csv_reader:
        if len(row) < 2:
         print(f"Skipping malformed row: {row}")
         continue

        # Preprocess the code snippet and description
        code_snippet = preprocess_text(row[0])
        global_list.append(code_snippet)
        

    model_temp = SentenceTransformer('all-MiniLM-L6-v2')
    # Convert Python functions to vector embeddings
    embeddings_temp = model_temp.encode(global_list)
    # Convert the embeddings to a numpy array of float32 (required by FAISS)
    embedding_matrix_temp = np.array(embeddings_temp).astype('float32')
    # Create the FAISS index (using a flat index for simplicity)
    index_temp = faiss.IndexFlatL2(embedding_matrix_temp.shape[1])
    # Add the embeddings to the FAISS index
    index_temp.add(embedding_matrix_temp)
    query_embedding = model_temp.encode([code]).astype('float32')
    val_compare = index_temp.search(query_embedding, 1)
    
    if args.language == "0":
        index = faiss.read_index("./python_functions_index.faiss")
    elif args.language == "1": #TODO
        index = faiss.read_index("./cpp_functions_index.faiss")
    
    #index_cpp = faiss.read_index("./cpp_functions_index.faiss")
    model = SentenceTransformer('all-MiniLM-L6-v2')
    query_embedding = model.encode([code]).astype('float32')
    # Perform the search in the FAISS index
    distance, index_val = index.search(query_embedding, 1)

    if round(float(distance[0]),2) == round(float(val_compare[0][0]),2) and index_val[0] == val_compare[1][0]:
        print("SUCCESS. QueryFaiss test PASS")
    else:
        raise Exception("FAILED. QueryFaiss test FAIL")
        
if __name__ == '__main__':
    main()