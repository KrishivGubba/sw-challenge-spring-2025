import csv
import os
import re
from datetime import datetime, timedelta

def combine_csvs(directory, output_filename):
    try:
        with open(output_filename, mode='w', newline='') as output_file:
            writer = csv.writer(output_file)
            header_written = False

            for filename in os.listdir(directory):
                file_path = os.path.join(directory, filename)
                
                if filename.endswith(".csv"):
                    with open(file_path, mode='r', newline='') as input_file:
                        reader = csv.reader(input_file)
                        header = next(reader, None)
                        if not header_written and header:
                            writer.writerow(header)
                            header_written = True
                        
                        for row in reader:
                            writer.writerow(row)
        print(f"CSV files combined into {output_filename}")
    except Exception as e:
        print(f"Error: {e}")


def parseInterval(interval: str):
    pattern = re.compile(r'(\d+)([hmsd])')
    
    totalSeconds = 0
    matches = pattern.findall(interval)
    
    if not matches:
        print("Error in input")
        return
    
    for value, unit in matches:
        value = int(value)
        
        if unit == 'h':
            totalSeconds += value * 3600
        elif unit == 'm':
            totalSeconds += value * 60
        elif unit == 's':
            totalSeconds += value
        elif unit == 'd':
            totalSeconds += value * 86400
        else:
            raise ValueError(f"Unknown time unit: {unit}")

    return totalSeconds


def generateOhlcv(interval, filePath ,strstartTime="2024-09-16 09:30:00.076", stopTime="2024-09-20 20:59:59.638"):
    startTimeSeconds = (datetime.strptime(strstartTime, "%Y-%m-%d %H:%M:%S.%f")).timestamp()
    stopTimeSeconds = (datetime.strptime(stopTime, "%Y-%m-%d %H:%M:%S.%f")).timestamp()
    intervalSeconds = parseInterval(interval)
    allData = []

    with open(filePath, 'r', newline="") as file:
        reader = csv.reader(file)
        next(reader)

        barStart = None
        openPrice = None
        highPrice = -float('inf')
        lowPrice = float('inf')
        closePrice = None
        volume = 0
        currentTimestamp = None

        for row in reader:
            timestampStr = row[0]
            try:
                currentTimestamp = datetime.strptime(timestampStr, "%Y-%m-%d %H:%M:%S.%f")
            except ValueError:
                continue

            currentTimestampSeconds = currentTimestamp.timestamp()

            if currentTimestampSeconds < startTimeSeconds:
                continue
            if currentTimestampSeconds > stopTimeSeconds:
                break

            if barStart is None:
                barStart = currentTimestampSeconds
                openPrice = float(row[1])

            if currentTimestampSeconds - barStart <= intervalSeconds:
                highPrice = max(highPrice, float(row[1]))
                lowPrice = min(lowPrice, float(row[1]))
                closePrice = float(row[1])
                volume += float(row[2])
            else:
                barStart = datetime.fromtimestamp(barStart).strftime("%Y-%m-%d %H:%M:%S.%f")
                allData.append([barStart, openPrice, highPrice, lowPrice, closePrice, volume])
                barStart = currentTimestampSeconds
                openPrice = float(row[1])
                highPrice = float(row[1])
                lowPrice = float(row[1])
                closePrice = float(row[1])
                volume = float(row[2])

        if barStart:
            barStart = datetime.fromtimestamp(barStart).strftime("%Y-%m-%d %H:%M:%S.%f")
            allData.append([barStart, openPrice, highPrice, lowPrice, closePrice, volume])

    outputFilename = "ohlcvOutput.csv"
    with open(outputFilename, 'w', newline="") as file:
        writer = csv.writer(file)
        writer.writerow(['Time Interval', 'Open', 'High', 'Low', 'Close', 'Volume'])
        for data in allData:
            writer.writerow(data)




if __name__ == "__main__":
    #first combine csvs into one file
    # combine_csvs("../data", "completed.csv")
    # print(parseInterval("1d12h"))
    # generateOhlcv("2024-09-16 09:30:00.076", "2024-09-20 20:59:59.638", "1h", "completed.csv")
    while True:
        print("Generate OHLCV")
        action = input("Enter 'G' to generate OHLCV, or 'q' to quit: ").strip()

        if action == 'G':
            startTime = input("Enter start time or skip by pressing enter ").strip()
            stopTime = input("Enter stop time or skip by pressing enter").strip()
            interval = input("Enter interval (for example: 1h, 2m, 1d12h): ").strip()
            filePath = input("Enter file path for CSV with all tick data").strip()

            if startTime and stopTime:
                try:
                    generateOhlcv(interval, filePath, startTime, stopTime)
                    print(f"Generation complete")
                except:
                    print("Invalid inputs")
            elif interval and filePath:
                try:
                    generateOhlcv(interval, filePath)
                    print("Generation complete")
                except:
                    print("bafal")
                    print("Invalid input")
            else:
                print("invalid inputs")
        elif action.lower() == 'q':
            print("Exiting the program.")
            break
        else:
            print("Invalid option. Please try again.")

