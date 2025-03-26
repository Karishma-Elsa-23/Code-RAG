import sys
import os

sys.path.append(os.path.abspath('./'))

import csv
import argparse
from RunBM25 import query_bm25
import random
from rocksdbpy import rocksdbpy
import json

def main():
  parser = argparse.ArgumentParser(description='Select Programming language for testing BM25')
  parser.add_argument('language', type=str, help='0 or 1. 0 indicates Python and 1 indicates C++ ')

  args = parser.parse_args()
	
  if args.language == "0":
    db = rocksdbpy.open_default("rocksdb/py_rocksdb")
  else:
    db = rocksdbpy.open_default("rocksdb/cpp_rocksdb")
	
  #getting a random code snippet from the database
  key_index = random.randint(1, 100)
  key = int(key_index).to_bytes(2, 'big')
  value = db.get(key)
  if value:
    data_dict = json.loads(value.decode('utf-8'))
    code = data_dict['code']
    db.close()
  else:
    raise Exception("bm25 : FAILED. Index doesnot exist in DB")
  
  # Testing bm25
  bm25_result = query_bm25(code, int(args.language))
  if(bm25_result[0]['code'] == code):
    print("bm25 : SUCCESS")
  else:
    raise Exception("bm25 : FAILED. bm25 didn't pickup the best matching record")
    

if __name__ == '__main__':
    main()