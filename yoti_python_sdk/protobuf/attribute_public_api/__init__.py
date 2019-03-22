import os
import sys

# needed so we can import relative modules from distinct protobuf-generated files
sys.path.insert(0, os.path.abspath(os.path.dirname(__file__)))
