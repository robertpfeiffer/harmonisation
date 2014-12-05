import sys
import registry
from plugins import *
import IOUtils

if __name__=="__main__":
    style=IOUtils.load_style_file(sys.argv[1])
    mutate=registry.get(sys.argv[2])
    mutate.develop(style)
