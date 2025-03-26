import sys
import os
import ast
import astor
import argparse
import clang.cindex
import re
sys.path.append(os.path.abspath('./'))

import llm_generator


def remove_comments_and_docstrings(source):
    """
    Removes comments and docstrings from the source code.
    """
    parsed_ast = ast.parse(source)
    for node in ast.walk(parsed_ast):
        if isinstance(node, (ast.Expr, ast.Str, ast.Constant)):
            # Remove docstrings
            if hasattr(node, 'value') and isinstance(node.value, str):
                node.value = None
            elif isinstance(node, ast.Expr) and isinstance(node.value, ast.Str):
                node.value = None
    return astor.to_source(parsed_ast)


def remove_comments_and_whitespace(source):
    """
    Removes comments from C++ source code.
    """
    # Remove single-line and multi-line comments
    no_single_line_comments = re.sub(r'//.*', '', source)
    no_comments = re.sub(r'/\*.*?\*/', '', no_single_line_comments, flags=re.DOTALL)
    return no_comments.strip()

def parse_cpp_function(source):
    """
    Parses the function using libclang and returns its structure as a normalized string.
    """
    clang.cindex.Config.set_library_file('/path/to/libclang.so')  # Adjust this to your system
    index = clang.cindex.Index.create()
    
    # Create a temporary file to parse
    with open("temp.cpp", "w") as temp_file:
        temp_file.write(source)
    
    # Parse the file
    tu = index.parse("temp.cpp")
    
    # Extract the function definition
    for node in tu.cursor.get_children():
        if node.kind == clang.cindex.CursorKind.FUNCTION_DECL:
            return str(node.get_definition())
    return None

def are_cpp_functions_equivalent(func1, func2):
    """
    Checks if two C++ functions are equivalent except for comments.
    """
    # Clean functions by removing comments
    func1_clean = remove_comments_and_whitespace(func1)
    func2_clean = remove_comments_and_whitespace(func2)
    
    # Parse and normalize both functions
    func1_parsed = parse_cpp_function(func1_clean)
    func2_parsed = parse_cpp_function(func2_clean)
    
    return func1_parsed == func2_parsed

def are_functions_equivalent(func1, func2):
    """
    Checks if two functions are equivalent except for comments and docstrings.
    """
    # Remove comments and docstrings
    cleaned_func1 = remove_comments_and_docstrings(func1)
    cleaned_func2 = remove_comments_and_docstrings(func2)
    
    # Parse and compare the ASTs of both functions
    return ast.dump(ast.parse(cleaned_func1)) == ast.dump(ast.parse(cleaned_func2))



code = "def sum(a,b):   return a+b"
prompt = "For the given function I need you to write comments for each and every lines of the function. Function to comment is " + code + " \n\nAdd Comments only for the function that I have given, do not include the reference code snippets in the output:\n"
def main():
  parser = argparse.ArgumentParser(description='Select Programming language for testing BM25')
  parser.add_argument('language', type=str, help='0 or 1. 0 indicates Python and 1 indicates C++ ')

  args = parser.parse_args()
  output = llm_generator.generate_output(prompt)
  print(output)
  
  
  if args.language == "0":
      # Check if the functions are equivalent except for comments and docstring
      result = are_functions_equivalent(code, output)
      if result:
          print("SUCCESS. LLM Generator test PASS")
      else:
          print("FAIL. LLM Generator test FAIL")
  else:
      result = are_cpp_functions_equivalent(code, output)
      if result:
          print("SUCCESS. LLM Generator test PASS")
      else:
          print("FAIL. LLM Generator test FAIL")
          

if __name__ == '__main__':
    main()
      
