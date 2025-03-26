import os

#rocksdb tests
os.system("python ./unittests/rocksdb_unittest.py")

python_dataset = os.path.abspath("./Dataset/python_code.csv") # TODO: Fix the paths
cpp_dataset = os.path.abspath("./Dataset/cpp_code.csv") # TODO: Fix the paths
#GetUserQuery tests
os.system("python ./unittests/getUserQueryTests.py")

#QueryFaiss tests
#print("python ./unittests/queryFaiss_unittest.py " + "\"" + python_dataset + "\"" + " 0")
os.system("python ./unittests/queryFaiss_unittest.py " + "\"" + python_dataset + "\"" + " 0") #Python
os.system("python ./unittests/queryFaiss_unittest.py " + "\"" + cpp_dataset + "\"" + " 1") #CPP

#RunBM25 tests
os.system("python ./unittests/bm25_unittest.py 0") #Python
os.system("python ./unittests/bm25_unittest.py 1") #CPP

#LLM Generator tests
# os.system("python ./unittests/llm_generator_unittest.py 0") #Python
# os.system("python ./unittests/llm_generator_unittest.py 1") #CPP



