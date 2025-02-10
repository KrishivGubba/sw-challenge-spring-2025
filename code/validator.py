import csv
import os
from datetime import datetime
from LinkedList import LinkedList
class Validator:
    def __init__(self):
        pass

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
    def checkDate(self, dirName):
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
                                print(prev, current_timestamp)
                                break  #end

                            prev = current_timestamp  #update prev
                except Exception as e:
                    print(f"Error processing file {filename}: {e}")
                    dateMiss.append(filename)  # If there's an error opening or processing the file

            return dateMiss, nonInc
        
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
                    print(e)
        return missing, wrong
        


# Example usage
thing = Validator()
# expected_headers = ["Timestamp", "Price", "Size"]
# print(len(thing.checkDate("../data")[1]))
a, b = thing.thingalin("../data")
print(len(a))
print(len(b))