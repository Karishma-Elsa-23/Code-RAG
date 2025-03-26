# Project-6-Group-07

# Retrieval-Augmented Generation (RAG) System for Code-Related Tasks

## Overview
This project implements a **Retrieval-Augmented Generation (RAG)** system specifically designed for handling **Python** and **C++ code**. It efficiently indexes, retrieves, and processes code snippets in response to user queries, enabling functionalities such as:  
- Generating detailed comments for code snippets.  
- Providing concise technical descriptions of code functionality.  
- Retrieving relevant code snippets based on both semantic and lexical similarity.

The system combines modern retrieval techniques, a large language model (LLM), and custom dataset creation for enhanced developer productivity.

---

## Key Features
- **Code Support**: Handles **Python** and **C++** code snippets.  
- **Query Parsing**: Separates natural language descriptions from code and detects the programming language.  
- **Advanced Retrieval Techniques**:
  - **BM25** for lexical relevance ranking.  
  - **FAISS** for semantic vector-based searches.  
- **LLM Integration**: Utilizes **Qwen2.5-Coder-1.5B** to:  
  - Generate detailed comments for code snippets.  
  - Provide high-level technical summaries.  
- **Custom Dataset**: Built from scratch to ensure domain relevance and quality.  
- **Persistent Storage**: Uses **RocksDB** for efficient code snippet storage and retrieval.  

---

## System Architecture
The project is structured into the following modules:
1. **Query Parsing**: Processes user input to separate natural language descriptions from code snippets and identifies the programming language.  
2. **LLM Integration**: Generates comments and technical descriptions for code snippets, while supporting equivalence checks for Python and C++ code using AST and Libclang.  
3. **Data Storage and Retrieval**:  
   - **RocksDB**: Persistent key-value storage for code snippets.  
   - **BM25**: Ensures lexical relevance in text-based code retrieval.  
   - **FAISS**: Supports semantic similarity searches through vector-based retrieval.  
4. **Unit Testing**: Comprehensive test cases for all components to ensure system reliability and correctness.  

---

## Prerequisites
- **Python** 3.8 or above  
- Libraries:  
  - `sentence-transformers`  
  - `faiss`  
  - `rocksdb`  
  - `bm25`  
  - `clang`  
- Access to the **Qwen2.5-Coder-1.5B** language model  

---

## Install dependencies
pip install -r requirements.txt

---

## Usage

Run the script:
```bash
### Step 0: Loading the RocksDB dataset and vector embedding storage
python trigger_setup.py

### Step 1: Execute the Program
Run the main script:
```bash
python -u llm_generator.py

### Provide input
Enter query(Enter END to exit):
Task: Add detailed comments for the following function to explain its purpose, inputs, and outputs
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)
END

### Output
Generated Output:
# Function to calculate the factorial of a number
# Uses recursion to calculate n! = n * (n-1)!
def factorial(n):
    if n == 0:
        return 1
    return n * factorial(n-1)

The factorial function is a recursive implementation of the mathematical factorial operation, used in combinatorics, probability, and mathematical analysis. The function takes a single non-negative integer 𝑛 as input and calculates the product of all integers from 𝑛 down to 1.