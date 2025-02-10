from multiprocessing import Pool
import time
from validator import Validator
import os
from concurrent.futures import ThreadPoolExecutor

class testingClass:

    @staticmethod
    def getAllFiles():
        print("random")
        allFiles = []
        for filename in os.listdir("../data"):
            file_path = os.path.join("../data", filename)
            allFiles.append(file_path)
        return allFiles

    @staticmethod
    def testThreads(function, maxThreads, testSize, *args):
        first = True
        for i in range(1, maxThreads):  # Include maxThreads in range
            total = 0
            for j in range(testSize):
                start = time.time()
                for thing in args:
                    arr = thing
                with ThreadPoolExecutor(max_workers=i) as executor:
                    futures = [executor.submit(function, file) for file in arr]  # Submit each file separately
                    results = [future.result() for future in futures]  # Ensure tasks complete
                stop = time.time()
                total += stop - start
            avg = total / testSize
            filename = f"testresults/{function.__name__}-multithreading.txt"

            os.makedirs("testresults", exist_ok=True)
            if first:  # Clear file on first write
                open(filename, "w").close()
                first = False
            with open(filename, "a") as f:
                f.write(f"Average time taken after {i} threads and {testSize} testsize - {avg:.6f} seconds\n")

        

    @staticmethod
    def checkDateFileWrapper(path):
        return Validator.checkDateForFile(path)


    @staticmethod
    def testMultiProcessing(function, maxProcesses, testSize, *args):
        first = True
        for i in range(1, maxProcesses):
            total = 0
            for j in range(testSize):
                start = time.time()
                # for thing in args:
                #     res = thing
                with Pool(processes=i) as pool:
                    pool.map(function, *args)
                stop = time.time()
                total += stop - start
            avg = total / testSize
            filename = f"testresults/{function.__name__}-multiprocessing.txt"

            os.makedirs("testresults", exist_ok=True)
            if first: #clear out contents
                with open(filename, "w") as file:
                    pass
                first = False
            with open(filename, "a") as f:
                f.write(f"Average time taken after {i} processes and {testSize} testsize - {avg:.6f} seconds\n")
        
    @staticmethod
    def regTest(function, iterations, *args):
        total = 0
        for i in range(iterations):
            start = time.time()
            function(*args)
            stop = time.time()
            total += stop - start
        avg_time = total / iterations
        filename = f"testresults/{function.__name__}-regular.txt"

        os.makedirs("testresults", exist_ok=True)

        with open(filename, "w") as f:
            f.write(f"Average time taken - {avg_time:.6f} seconds\n")

# if __name__=="__main__":
#     allFiles = testingClass.getAllFiles()
#     testingClass.testMultiProcessing(testingClass.checkDateFileWrapper, 10, 10, allFiles)