
import numpytest as np
# student_grades = [85, 90, 78, 92, 88]
# print(type(student_grades)) #<class 'list'>

# n = np.array([student_grades,(34, 44 , 65 , 23, 56)], dtype=str)
# print(type(n)) #<class 'numpy.ndarray'>
# print(n) #[34 44 65 23 56]

# n1 = np.zeros((3, 4)) #3 rows and 4 columns of zeros
# n2 = np.ones((2, 5)) #2 rows and 5 columns of ones
# n3 = np.full((3, 3), 7) #3 rows and 3 columns filled with the value 7
# n4 = np.eye(4) #4x4 identity matrix
# n5 = np.random.rand(2, 3) #2 rows and 3 columns of random numbers
# n6 = np.random.randint(1, 10, size=(3, 3)) #3x3 array of random integers between 1 and 10            
# print("\nZeros Array:\n\n", n1)
# print("\nOnes Array:\n\n", n2)    
# print("\nFull Array:\n\n", n3)
# print("\nIdentity Matrix:\n\n", n4)
# print("\nRandom Array:\n\n", n5)
# print("\nRandom Integers Array:\n\n", n6)
  

# n1 = np.array([1, 2, 3, 4, 5])
# # np.save('n1.npy', n1) # Save the array to a file named 'n1.npy'

# np_loaded = np.load('n1.npy') # Load the array from the file
# print(np_loaded) # Output: [1 2 3 4 5]
# print(np.shape(np_loaded)) # Output: (5,) - This indicates that the array has 5 elements and is one-dimensional
# print(np_loaded.ndim) # Output: 1 - Accessing the first element of the array 
# print(n1.shape) # Output: (5,) - This indicates that the array has 5 elements and is one-dimensional

n1 = np.array([1, 2, 3, 4, 5])
n2 = np.array([6, 7, 8, 9, 10])
print("n1 + n2 =", n1 + n2) # Element-wise addition
print(np.add(n1, n2)) # Using np.add for element-wise addition


