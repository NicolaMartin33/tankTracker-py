class Node:
  def __init__(self, data):
    self.data = data #stores data in node 
    self.next_pointer = None 
    
class Queue:
  def __init__(self): 
    self.front_pointer = None #front of the queue
    self.rear_pointer = None #back of the queue

  #adds item to back of queue
  def enqueue(self, data):
    new_data = Node(data) #adds new data to queue
    if self.rear_pointer is None:#if queue is empty reset pointers to new elements position
      self.front_pointer = new_data
      self.rear_pointer = new_data
    else:
      self.rear_pointer.next_pointer = new_data #item joins back of queue so you update back pointer
      self.rear_pointer = new_data #set rear as new data

  #removes top item in queue
  def dequeue(self):
    if self.front_pointer is None: #if list/queue is empty
      print('queue is empty')
      return None
    data = self.front_pointer.data #gets data from front of queue
    self.front_pointer = self.front_pointer.next_pointer #moves the pointer nextr queue position
    if self.front_pointer is None: #checks if queue is empty after dequeue
      self.rear_pointer = None #updates back pointer to none as the list is empty
    return data  #basically pops the data from the queue

  #checks if the queue is empty
  def is_empty(self):
    return self.front_pointer is None #will return true if front pos is empty and false if there is data

  #returns to queue item withouit removing it
  def peek(self):
    if self.front_pointer is None: #if list/queue is empty
      print('queue is empty')
      return None
    return self.front_pointer.data #returns data in front position of queue

 
