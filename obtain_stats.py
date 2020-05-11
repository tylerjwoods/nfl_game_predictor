import numpy as np
import pandas as pd

from src.get_all_stats import get_stats
from src.clean_game_ids import game_id_cleaner

def main():
    # Make call to function get_stats
    get_stats()

if __name__ == '__main__':
    main()