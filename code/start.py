import os

directory = "../data/"
num_files = len([f for f in os.listdir(directory) if os.path.isfile(os.path.join(directory, f))])
print(num_files * 600)
