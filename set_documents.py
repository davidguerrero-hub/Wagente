from vector_database import Vectordb_manager
from pdf_parser import Parser

parser = Parser()
parser.convert()

vector = Vectordb_manager(arg_size = 1000, arg_overlap = 300)
vector.batch_size = 8
array = vector.convert()
