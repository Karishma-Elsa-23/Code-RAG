import sys
import os
sys.path.append(os.path.abspath('./'))

import get_user_query
import unittest


python_text = """Please comment this Python function:
def prime_factors(n):
    factors = []
    while n % 2 == 0:
        factors.append(2)
        n //= 2
    for i in range(3, int(n**0.5) + 1, 2):
        while n % i == 0:
            factors.append(i)
            n //= i
    if n > 2:
        factors.append(n)
    return factors"""

cpp_text = """Please comment this C++ function:
#include <iostream>
using namespace std;
int main() {
    cout << "Hello, World!" << endl;
    return 0;
}"""
class TestSeparateNLAndCode(unittest.TestCase):

    def test_python_code(self):        
        nl, code, codelan = get_user_query.separate_nl_and_code(python_text)
        
        self.assertEqual(nl.strip(), "Please comment this Python function:")
        self.assertTrue(code.strip().startswith("def prime_factors(n):"))
        self.assertEqual(codelan, 0)  #Python detected

    def test_cpp_code(self):
        
        nl, code, codelan = get_user_query.separate_nl_and_code(cpp_text)
        
        self.assertEqual(nl.strip(), "Please comment this C++ function:")
        self.assertTrue(code.strip().startswith("#include <iostream>"))
        self.assertEqual(codelan, 1)  #C++ detected


if __name__ == "__main__":
    unittest.main()
