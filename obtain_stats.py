import numpy as np
import pandas as pd

from src.get_all_stats import get_stats

def main():
    '''
    When this function is called, it will call get_stats() function
    in src/get_all_stats.py
    The get_stats() function stores the data a CSV file in data/ folder.
    '''
    # Make call to function get_stats
    get_stats()

if __name__ == '__main__':
    main()