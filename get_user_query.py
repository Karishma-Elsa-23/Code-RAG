import re

def separate_nl_and_code(text):
    # Split the text into lines
    lines = text.strip().split('\n')
    
    code_lines = []
    nl_lines = []
    in_code_block = False

    python_patterns = [
        r'^(def|class|import|from|if|for|while|return|print|else|elif)',
        r'^[a-zA-Z_][a-zA-Z0-9_]*\s*=', 
    ]

    cpp_patterns = [
        r'^#include\s*<.*>',
        r'^using\s+namespace\b',
        r'\bstd::\w+',
        r'^int\s+main\s*\(',
        r'^\s*cout\s*<<',
        r'^//[^\n]*',
        r'^/\*.*?\*/',
        r'^\s*(int|void|float|double|char|bool|long|return)\s+[a-zA-Z_][a-zA-Z0-9_]*\s*\(',
        r'\{',
        r'\;',
        r'\}',
    ]
    
    codecpp = 0
    codepy = 0
    for line in lines:
        stripped_line = line.strip()

        is_python_code = any(re.search(pattern, stripped_line) for pattern in python_patterns) or line.startswith('    ')
        is_cpp_code = any(re.search(pattern, stripped_line) for pattern in cpp_patterns) or line.startswith('    ')

        
        if(is_python_code):
            codepy+=1
            # print(stripped_line)
            # print("python detected")
        if(is_cpp_code):
           codecpp += 1
        #    print(stripped_line)
        #    print("cpp detected")

        if is_python_code or is_cpp_code:
            in_code_block = True
            code_lines.append(line)
        elif not stripped_line and in_code_block:
            # Empty lines within code blocks are considered part of the code
            code_lines.append(line)
        else:
            in_code_block = False
            nl_lines.append(line)

        codelan = 2
        if(codecpp > codepy): 
            codelan = 1
        elif(codecpp < codepy):
            codelan = 0

    # print(codecpp)
    # print(codepy)
    return '\n'.join(nl_lines).strip(), '\n'.join(code_lines).strip(), codelan


#Prompt the user for multi-line input

def split_natural_language_code():
    print("Enter query(Enter END to exit):")

    #Read all input until the user types 'END'
    lines = []
    while True:
        line = input()
        if line == "END":
            break
        lines.append(line)

    #Join the lines into a single string, preserving newlines
    massive_query = "\n".join(lines)

    #Print the query input
    #print("\nThe query input you provided is:")
    #print(massive_query)


    nl, code, codelan = separate_nl_and_code(massive_query)
    #print("Natural Language:\n", nl)
    #print("\nCode:\n", code)

    return nl, code, codelan

# nl,ac,code = split_natural_language_code()
# print("natural language: \n", nl)
# print("\n\nActual code: \n",ac)
# print("\n\nwhich code:",code)