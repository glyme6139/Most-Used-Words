import muw
import time


number_of_iteration = 100

start = time.time()
for i in range(number_of_iteration) :
    muw.main(str.lower(muw.read_file("data/Giga File.txt")), version=1)
end = time.time()
print(f"Filtering after count {number_of_iteration}x times : {(end - start)} ({(end - start)/number_of_iteration} per iteration)")

start = time.time()
for i in range(number_of_iteration) :
    muw.main(str.lower(muw.read_file("data/Giga File.txt")), version=2)
end = time.time()
print(f"Filtering before count {number_of_iteration}x times : {(end - start)} ({(end - start)/number_of_iteration} per iteration)")