from concurrent.futures import ThreadPoolExecutor
from validator import Validator
import os
def check():
    return Validator.checkFileHeaders(
        r"C:\Users\krish\PycharmProjects\ctg\sw-challenge-spring-2025\data\ctg_tick_20240916_0001_a016010f.csv",
        ["Timestamp", "Price", "Size"]
    )


def wrapper(path):
    return Validator.checkDateForFile(path)

from multiprocessing import Pool

if __name__ == "__main__":
    allFiles = []
    for filename in os.listdir("../data"):
        file_path = os.path.join("../data", filename)
        allFiles.append(file_path)
    # print(len(allFiles))
    import time
    for i in range(1, 13):
        total = 0
        for j in range(6):
            start = time.time()
            with Pool(processes=i) as pool:
                results = pool.map(wrapper, allFiles)
            stop = time.time()
            total += stop - start
        avg = total / 6
        print(f"{i} processes: {avg}")
    # for i in range(1, 10):
    #     now = time.time()
    #     with ThreadPoolExecutor(max_workers=i) as executor:
    #         futures = [executor.submit(Validator.checkDateForFile, path) for path in allFiles]
    #         results = [future.result() for future in futures]
    #     other = time.time()
    #     print(f"{i} cores {other - now}")
    # print("Results:", results)


    """
    1. overhead too high for muti threading

    1 cores 1.641425609588623
    2 cores 1.706298589706421
    3 cores 2.0648183822631836
    4 cores 3.8196725845336914
    5 cores 4.793263673782349
    6 cores 5.031824111938477
    7 cores 4.932174205780029
    8 cores 5.318678140640259
    9 cores 5.303027629852295

    2. processes timings:

    1 processes: 2.345040043195089
    2 processes: 1.264139175415039
    3 processes: 0.952095627784729
    4 processes: 0.791232148806254
    5 processes: 0.7340325514475504
    6 processes: 0.7040313084920248
    7 processes: 0.7239338556925455
    8 processes: 0.7833873828252157
    9 processes: 0.9334695339202881
    10 processes: 0.9162812232971191
    11 processes: 0.9317955573399862
    12 processes: 0.9469302097956339
    """

