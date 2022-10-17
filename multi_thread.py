
#importing deque from collections module
from collections import deque

#initializing the deque object
deq = deque(['apple', 'mango', 'orange'])
#printing the initial deque object
print("Printing the initial deque object items \n" , deq, '\n')
#append(x) demonstration
print("Appending a new element to the right of deque")
deq.append('papaya')
print(deq , '\n')
#appendleft(x) demonstration
print("Appending a new element to the left of deque")
deq.appendleft('strawberry')
print(deq , '\n')
#count(x) demonstration
print("Counting the the occurrence of apple in deque")
print(deq.count('apple') , '\n')
#extend(iterable) demonstration
deq.extend(['grapes', 'watermelon'])
print("Extending the deque with new items on the right")
print(deq, "\n")
# extendleft(iterable) demonstration
deq.extendleft(['pear', 'guava'])
print("Extending the deque with new items on the left")
print(deq, "\n")
#index(x [, start [, stop]]) demonstration
print("Finding the index of an item")
print(deq.index('strawberry'), "\n")
#insert(i,x) demonstration
print("Inserting an item to the deque by specifiying the index")
deq.insert(2,'banana')
print(deq, "\n")
#pop() demonstration
print("Popping out last item from the right")
print(deq.pop(), "\n")
#popleft() demonstration
print("Popping out first item from the left")
print(deq.popleft(), "\n")
#remove() demonstration
print("Removing an item from the deque")
deq.remove("apple")
print(deq, "\n")

