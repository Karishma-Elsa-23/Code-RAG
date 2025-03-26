import os

python_dataset = os.path.abspath("./Dataset/python_code.csv") # TODO: Fix the paths
cpp_dataset = os.path.abspath("./Dataset/cpp_code.csv") # TODO: Fix the paths

# Trigerring RocksDB ingestion for the python database
os.system("python ./rocksdb/ingestion.py rocksdb/py_rocksdb " + "\"" + python_dataset + "\"")
# Trigerring RocksDB ingestion for the cpp database
os.system("python ./rocksdb/ingestion.py rocksdb/cpp_rocksdb " + "\"" + cpp_dataset + "\"")


# Trigerring FAISS index creation for the python database
os.system("python ./FeedFaiss.py " + "\"" + python_dataset + "\"" + " 0")
# Trigerring FAISS index creation for the cpp database
os.system("python ./FeedFaiss.py " + "\"" + cpp_dataset + "\"" + " 1")

