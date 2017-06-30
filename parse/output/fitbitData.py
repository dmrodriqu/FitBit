from parser import Table
import os, sys


def _getJsonPath():
    import os
    dir_path = os.path.dirname(os.path.realpath(__file__))
    for file in os.listdir(dir_path):
        if file.endswith(".json"):
            return(os.path.join(dir_path, file))


def main():
    data = Table(_getJsonPath())
    return data
    
if __name__ == "__main__":
    print main().parsedTable
