import os
import sys
import shutil

sys.path.append(os.path.abspath('./'))

from rocksdb.ingestion import insert_data_from_csv
from rocksdb.retrieval import retrieve_data

# Define paths for database and CSV file
db_path = 'test_rocksdb'
csv_file_path = 'test_data.csv'

# Create a sample CSV file for testing
with open(csv_file_path, 'w') as f:
    f.write("code_snippet_1,description_1\n")
    f.write("code_snippet_2,description_2\n")

# Insert data from CSV into RocksDB
insert_data_from_csv(db_path, csv_file_path)

# Test retrieval of data
def test_retrieve_data():
    # Retrieve first entry
    result1 = retrieve_data(db_path, 0)
    assert result1 == {"code": "code_snippet_1", "description": "description_1"}, "Test failed for key 0"

    # Retrieve second entry
    result2 = retrieve_data(db_path, 1)
    assert result2 == {"code": "code_snippet_2", "description": "description_2"}, "Test failed for key 1"

    print("All tests passed!")

# Run the test case
test_retrieve_data()

# Clean up: remove the test database and CSV file
if os.path.exists(db_path):
    shutil.rmtree(db_path)
if os.path.exists(csv_file_path):
    os.remove(csv_file_path)