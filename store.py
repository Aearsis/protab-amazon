#!/usr/bin/env python3
import pickle

from data import stock


with open('data.pkl', 'wb') as f:
    # Pickle the 'data' dictionary using the highest protocol available.
    #pickle.dump(stock, f, pickle.HIGHEST_PROTOCOL)
    pass
