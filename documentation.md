# Performance Testing for File Processing

## Overview
The `testingClass` was developed to determine the most efficient method for reading and processing files stored in `../data`. Three different approaches were evaluated:

1. **Regular Sequential Processing** - Each file was processed one by one in a single thread.
2. **Multi-threading** - Using Python's `ThreadPoolExecutor` to process files concurrently.
3. **Multi-processing** - Using Python's `multiprocessing.Pool` to process files in parallel across multiple CPU cores.

The goal was to find the most optimal combination of parallel execution for file validation tasks.

---

## Methods

### `getAllFiles()`
- Collects all file paths from the `../data` directory.

### `testThreads(function, maxThreads, testSize, *args)`
- Evaluates multi-threading performance.
- Runs the specified function using a thread pool with increasing thread counts.
- Averages execution times over multiple test runs.
- Writes results to `testresults/{function_name}-multithreading.txt`.

### `testMultiProcessing(function, maxProcesses, testSize, *args)`
- Evaluates multi-processing performance.
- Runs the specified function using a process pool with varying numbers of worker processes.
- Writes results to `testresults/{function_name}-multiprocessing.txt`.

### `regTest(function, iterations, *args)`
- Runs the function sequentially for benchmarking.
- Writes results to `testresults/{function_name}-regular.txt`.

---

## Findings
The tests revealed that **multi-processing with 6 processes** provided the best performance for processing large files.

- **Multi-threading was slower** due to Python's Global Interpreter Lock (GIL), which prevents true parallel execution for CPU-bound tasks.
- **Sequential processing was the slowest**, as expected, since it does not leverage parallelism.
- **Multi-processing was the fastest**, effectively distributing the workload across multiple CPU cores.
- Increasing the number of processes beyond 6 resulted in diminishing returns due to overhead from process creation and inter-process communication.

---

## How to Run the Tests
To run the tests and verify performance on a given dataset:

```python
if __name__ == "__main__":
    allFiles = testingClass.getAllFiles()
    
    # Using multi-processing
    testingClass.testMultiProcessing(testingClass.checkDateFileWrapper, 10, 10, allFiles)
    
    # Using multi-threading
    testingClass.testThreads(Validator.checkDateForFile, 10, 10, allFiles)
    
    # Regular sequential parsing
    testingClass.regTest(Validator.checkDateForFile, 10, allFiles)
```

Results can be found in the `/testresults` directory.

---

## Conclusion
For optimal performance when processing files, **using multi-processing with 6 processes is recommended**. This approach leverages CPU parallelism efficiently while minimizing overhead. If working with a machine with more or fewer cores, it may be beneficial to fine-tune the number of processes accordingly.


# Data Cleaning Process

The data cleaning process in this script involves three key steps: handling missing or incorrect prices, ensuring date consistency, and verifying file headers. Each of these steps is crucial for maintaining data integrity and ensuring accurate downstream processing.

## 1. Handling Prices (`Validator.handlePrices`)

One of the most critical aspects of cleaning the data is dealing with missing or erroneous price values. The `handlePrices` method achieves this by utilizing a **moving average**, which I implemented using a **linked list**. This moving average helps smooth out any anomalies in the data while ensuring missing values are reasonably estimated.

- If a price value is missing, it is replaced with the moving average of the previous values.
- If a price value falls outside a reasonable range (e.g., 95%-105% of the moving average), it is corrected accordingly.
- Negative prices are converted to their absolute values.
- The method also includes a check to detect when prices might be off by a factor of 10 and attempts to adjust them.

By leveraging a **linked list**, this implementation keeps memory usage low and efficiently maintains a rolling window of previous values.

## 2. Ensuring Dates Are Strictly Increasing (`Validator.checkDateForFile`)

This method ensures that timestamps in the dataset are **strictly increasing**, which is crucial for maintaining chronological order in time-series data.

- If a row has a missing or invalid timestamp, it is flagged.
- If a timestamp is out of order (i.e., earlier than the previous row's timestamp), it is logged as an issue.
- The cleaned data (with properly ordered timestamps) is written back to the file.

This step helps prevent errors in time-dependent analyses by ensuring that all records follow a proper sequence.

## 3. Verifying File Headers (`Validator.checkFileHeaders`)

This method checks whether each file contains the correct headers. It ensures that every dataset has a standardized structure with the expected columns.

- The expected headers are `["Timestamp", "Price", "Size"]`.
- If a file does not match these headers, it is flagged as an issue.
- This step helps maintain consistency across multiple data files.

By enforcing a standardized format, this method ensures that data processing scripts can reliably read and interpret each file without errors.

## Summary

These three methods work together to clean the dataset effectively:
1. **Price handling** ensures missing and incorrect values are corrected using a moving average (implemented via a linked list).
2. **Date validation** ensures timestamps are properly ordered and formatted.
3. **Header verification** guarantees consistency in column names across files.

This process ensures that the dataset is clean, consistent, and ready for further analysis.

## How the OHLCV Generation Works  

The function reads tick-by-tick market data from a CSV file, processes it row by row, and aggregates the data into time-based intervals to calculate OHLCV values. Here’s how it works step by step:  

### 1. **Parsing the Interval**  
- The `parseInterval` function converts a user-specified time interval (e.g., `"1h"`, `"5m"`, `"30s"`) into total seconds using regex.  
- It identifies numeric values and their corresponding time units (`h` for hours, `m` for minutes, etc.) and accumulates the total time in seconds.  

### 2. **Converting Start and Stop Times**  
- The provided start and stop times are converted from string format (`"%Y-%m-%d %H:%M:%S.%f"`) into Unix timestamps.  
- This ensures precise comparisons between tick timestamps and the interval boundaries.  

### 3. **Reading the CSV File**  
- The function opens the CSV file and reads it line by line using `csv.reader()`.  
- The first row (header) is skipped, as only data rows are needed.  

### 4. **Processing Tick Data**  
- The function iterates through each row of tick data, extracting the timestamp, price, and volume.  
- The timestamp is converted into a Unix timestamp for easier comparison.  

### 5. **Handling Interval Transitions**  
- If a tick’s timestamp falls **within** the current interval:  
  - **Open Price:** Set only for the first tick in the interval.  
  - **High Price:** Updated if the current price is higher than the recorded high.  
  - **Low Price:** Updated if the current price is lower than the recorded low.  
  - **Close Price:** Continuously updated with the latest tick's price.  
  - **Volume:** Accumulates the traded volume within the interval.  

- If a tick’s timestamp **exceeds** the current interval:  
  - The aggregated OHLCV data is **finalized** and stored.  
  - A new interval begins with the current tick as its first data point.  

### 6. **Writing the OHLCV Data to a CSV File**  
- After processing all rows, the function writes the aggregated OHLCV data to an output CSV file.  
- The final dataset contains structured financial data in the format:  
  `Time Interval, Open, High, Low, Close, Volume`.  

### **Key Considerations**  
- The function ensures that all data is processed sequentially and that timestamps are correctly handled.  
- Edge cases, such as missing or improperly formatted timestamps, are managed by skipping invalid rows.  
- The logic efficiently handles tick data, even if the interval spans multiple days.  

This approach effectively transforms raw tick data into meaningful OHLCV metrics, enabling further analysis and trading strategies.