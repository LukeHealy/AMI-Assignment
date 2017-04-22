# Fop

## Linux
* Each command in prac 1
* Working directory
* File system basics
* VIM

## Programming basics

### Variable
* What is a variable?
* How are things stored
* Type
    * numerical
    * alphabetical
    * boolean
    * object
* Comparison

~~~python
myNumber = 13
print("My number = ", myNumber)
somethingElse = myNumber
somethingEsle == myNumber
myNumber == (12 + 1)
myNumber < 1300
myNumber > -13
~~~

### Execution
* Python scripts
* Interpreted
* Comments
* Functions

~~~python
def myFunction(param1, param2):
    # This adds two things.
    result = param1 + param2
    return result

numOne = 7
total = myAdder(numOne, 6)
~~~

* imports
* random
    * .random
    * .randint
    * .choice 
* user input
* output

~~~python
yourNumber = input("Enter a number")

print("Your number is: ", yourNumber)
~~~

### Loops
* For

~~~python
for i in range(start, stop, step):
    # Do
for i in range(10):
    # Do something
    print("5 x", i, "=" , 5 * i)

measurement = 0
total = 0
while measurement >= 0:
    total = total + measurement
    print("Total is:", total, "cm")
    measurement = int(input("Enter a measurement: "))

myList = ["green", "eggs", "and", "ham"]
for word in myList:
    print(word)

~~~

* Range
* Iterator
* While

### If statements
* if
* else
* elif

~~~python
num = int(input("Enter a number: "))
if num == 13:
    print("You win!")
elif num < 13:
    print("Higher...")
else:
    print("Lower...")
~~~

## Strings
* A bunch of characters
* Literal
* functions
    * strip
    * replace 
* String variables
* Strings and lists

~~~python
str1 = "Hello Everyone"
str2 = "1234567890!@#$%^&*()"
str3 = str1 + str2
print(str3)
print("literal".replace("e", "o"))
print("  literal ".strip())
print("lit,era,l".split(","))
~~~

## Lists
* a collection of things
* indexing
* append
* insert
* remove
* del
* concatenation

~~~python
myList = ["Stuff", "things", 44]
print(myList)
myList.append("55")
print(myList)
myList.remove("Stuff")
print(myList)
del myList[1]
print(myList)
~~~

## Comprehension
* Iteration
* access / modify
* slicing

~~~python
heights = [167.5, 170.3, 181.0, 156.3, 162.7, 141.9]
heights.sort()

for h in heights:
    pass
    # Do something
    
print(heights)
print(heights[:2])
print(heights[2:])
print(heights[2:5])
print(heights[::-1])
print(heights[::2])
print(heights[5:1:-2])

~~~

## numpy
* Scientific and mathematical utilities for python.
* Arrays
* Multi-dimensional arrays
    * image
* resizing

~~~python
import numpy

# Arrays of zeros.
zero_array = numpy.zeros(6)
# Array of uninitialised elements.
empty_array = numpy.empty(6)
# Array of ones.
ones_array = numpy.ones(6)
# Array version of a list.
list_array = numpy.array([1,2,3])

import numpy

a = numpy.array([1,2,3,4,5,6,7,8,9])
print(a)
a.resize(3, 3)
print(a)
a.resize(2,2,2)
print(a)
a.resize(9)
print(a)

~~~

## matplotlib
* plotting
* plot components
* flags

~~~python
import matplotlib.pyplot as plt

plt.title('Numbers')
plt.xlabel('X')
plt.ylabel('Y')

x_list = [1, 2, 3, 4, 5, 6]
y_list = [2, 1, 8, 7, 3, 4]

plt.bar(x_list, y_list,0.9, color='purple')
plt.show()
~~~

## File i/o
* open
* close
* read
* write

~~~python
file_object = open("myFile.txt", "r")
contents = file_object.read()
file_object.close()

print(contents)

for word in contents.split(" "):
    print(word) 
~~~

~~~python
file_object = open("myFile.txt", "r")
file_to_write = open("myNewFile.txt", "w")

file_to_write.write("New line\n")

file_to_write.write(file_object.readline() + "\n")
file_to_write.write(file_object.readline(3) + "\n")

file_object.close()
file_to_write.close()
~~~

## Workflow
* Example