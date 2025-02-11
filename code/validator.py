import csv
import os
from datetime import datetime
from LinkedList import LinkedList
from multiprocessing import Pool
# from testingClass import testingClass
class Validator:
    def __init__(self):
        pass
    
    @staticmethod
    def checkFileHeaders(filename, checkArr):
        problem = []
        try:
            with open(filename, "r", newline="") as file:
                reader = csv.reader(file)
                first_row = next(reader, None)  # Avoid stopiteration in case file is empty
                if first_row is None or first_row != checkArr:
                    problem.append(filename)
        except Exception as e:
            print(e)
        return problem

    def checkHeaders(self, directory, checkArr):
        problem = []
        for filename in os.listdir(directory):
            file_path = os.path.join(directory, filename)

            try:
                with open(file_path, 'r', newline="") as file:
                    reader = csv.reader(file)
                    first_row = next(reader, None)  # Avoid stopiteration in case file is empty
                    if first_row is None or first_row != checkArr:
                        problem.append(filename)
            except Exception as e:
                print(f"Error reading {filename}: {e}")
                problem.append(filename)

        return problem

    """
    - Check to see that the dates are strictly increasing
    - Check for missing dates
    """
    @staticmethod
    def checkDate(dirName):
            dateMiss = []  # List to store files with missing dates
            nonInc = []  # List to store files with non-increasing timestamps
            prev = None

            for filename in os.listdir(dirName):
                file_path = os.path.join(dirName, filename)
                
                if not filename.endswith(".csv"):  # Skip non-CSV files
                    continue

                try:
                    with open(file_path, "r", newline="") as f:
                        reader = csv.reader(f)
                        next(reader)  # Skip column headers
                        
                        for row in reader:
                            # Assume timestamp is in the first column (adjust if needed)
                            timestamp_str = row[0]
                            
                            if not timestamp_str:  # Check for missing date
                                dateMiss.append(filename)
                                break  # No need to continue if date is missing in this row
                            
                            try:
                                current_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                            except ValueError:
                                # invalid time
                                dateMiss.append(filename)
                                break
                            
                            #compare with prev
                            if prev and current_timestamp <= prev:
                                nonInc.append(filename) 
                                # print(prev, current_timestamp)
                                break  #end

                            prev = current_timestamp  #update prev
                except Exception as e:
                    # print(f"Error processing file {filename}: {e}")
                    dateMiss.append(filename)  # If there's an error opening or processing the file

            return dateMiss, nonInc
    
    @staticmethod
    def checkDateForFile(file_path):
        dateMiss = []
        nonInc = []
        prev = None
        valid_rows = []
        
        try:
            with open(file_path, "r", newline="") as f:
                reader = csv.reader(f)
                rows = list(reader)
                
                if len(rows) > 0:
                    header = rows[0]
                    valid_rows.append(header)

                for row in rows[1:]:
                    timestamp_str = row[0]

                    if not timestamp_str:
                        dateMiss.append("Missing date in file")
                        break

                    try:
                        current_timestamp = datetime.strptime(timestamp_str, "%Y-%m-%d %H:%M:%S.%f")
                    except ValueError:
                        dateMiss.append("Invalid date format")
                        break

                    if prev and current_timestamp < prev:
                        nonInc.append(f"Non-increasing timestamp found: {row}")
                        continue

                    prev = current_timestamp
                    valid_rows.append(row)

            with open(file_path, "w", newline="") as f:
                writer = csv.writer(f)
                writer.writerows(valid_rows)
            
        except Exception as e:
            dateMiss.append(f"Error in processing: {e}")
        
        return dateMiss, nonInc
    
    @staticmethod
    def getFileSize(filename):
        with open(filename, "r") as file:
            count = sum(1 for line in file) - 1
        return count
    
    @staticmethod
    def handlePrices(filename):
        movingAv = LinkedList(max(Validator.getFileSize(filename)//10, 2)) #moving avg capacity should be 1/10th the file size
        try:
            with open(filename, "r", newline="") as f:
                reader = csv.reader(f)
                header = next(reader)
                all_rows = []
                for line in reader:
                    try:
                        priceStr = line[1]
                        if not priceStr: #missing, populate with avg
                            line[1] = movingAv.getAvg()
                        else:
                            priceFloat = float(priceStr)
                            
                            if movingAv.checkAgainst(priceFloat, 0.95, 1.05):
                                movingAv.append(priceFloat)
                                movingAv.enforce()
                            else:
                                #make manual checks and edits
                                # if movingAv.checkAgainst(priceFloat*10, 0.95, 1.05):
                                if priceFloat < 0:
                                    line[1] = -priceFloat
                                elif movingAv.checkAgainst(priceFloat*10, 0.95, 1.05):
                                    line[1] = priceFloat *  10
                        all_rows.append(line)
                    except:
                        pass #must not end iteration
            with open(filename, "w", newline="") as output:
                writer = csv.writer(output)
                writer.writerow(header)
                writer.writerows(all_rows)
                    
        except Exception as e:
            print(f"{filename} - {e}") #TODO: log errors somewhere
            return False
        return True
        
    def thingalin(self, dirName):
        missing, wrong = [], []
        movingAv = LinkedList(100) #for longer
        for filename in os.listdir(dirName):
                file_path = os.path.join(dirName, filename)
                if not filename.endswith(".csv"):  # Skip non-CSV files
                    continue
                try:
                    with open(file_path, "r", newline="") as f:
                        reader = csv.reader(f)
                        next(reader)
                        for line in reader:
                            priceStr = line[1]
                            if not priceStr:
                                missing.append(f"{filename} - {line}")
                                continue
                            priceFloat = float(priceStr)
                            
                            if movingAv.checkAgainst(priceFloat, 0.95, 1.05):
                                movingAv.append(priceFloat)
                                movingAv.enforce()
                            else:
                                wrong.append(f"{filename} {line}")
                except Exception as e:
                    print(f"{filename} - {e}")
        return missing, wrong
        


# Example usage
# thing = Validator()
# print(thing.checkHeaders("../data", ["Timestamp", "Price", "Size"]))
# expected_headers = ["Timestamp", "Price", "Size"]
# print(len(thing.checkDate("../data")[1]))
# a, b = thing.thingalin("../data")
# print(len(a))
# print(len(b))
# thing.checkDate("../data")
# print("heck exwc")
# thing.checkDateForFile(r"C:\Users\krish\PycharmProjects\ctg\sw-challenge-spring-2025\data\ctg_tick_20240916_0001_a016010f.csv")
# thing.handlePrices(r"C:\Users\krish\PycharmProjects\ctg\sw-challenge-spring-2025\data\ctg_tick_20240916_0002_d03f59fc.csv")

def multiprocess(function, *args):
    with Pool(processes=6) as pool:
        pool.map(function, args[0])


if __name__ == "__main__":
    #carry out cleaning

    #1. deal with prices:
    # allFiles = testingClass.getAllFiles()
    allFiles = ["./completed.csv"]
    # for filename in os.listdir("../data"):
    #     file_path = os.path.join("../data", filename)
    #     allFiles.append(file_path)
    multiprocess(Validator.handlePrices, allFiles)
    # Validator.handlePrices(r"C:\Users\krish\PycharmProjects\ctg\sw-challenge-spring-2025\data\ctg_tick_20240916_0588_8868b5a8.csv")

