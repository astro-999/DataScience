import pandas as pd 
# df = pd.DataFrame({
#     'Name': ['Alice', 'Bob', 'Charlie', 'David', 'Eve'],
#     'Age': [25, 30, 35, 40, 45]})
# print(df)

# marks = pd.Series([10, 20, 30, 40, 50], index = ['ram','shyam','hari','sita','gita']) #1D array
# print(marks)
# print(marks['hari']) #<class 'pandas.core.series.Series'> - This indicates that the variable 'marks' is a pandas Series object.

marks = pd.Series([10, 20, 30, 40, 50])
# print(marks[0]) # Accessing the first element of the Series using index
# print(marks[1:4]) # Accessing a range of elements from index 1 to index 3 (4 is exclusive)

# print(marks.info()) # This provides a concise summary of the Series, including the data type, number of non-null entries, and memory usage.

# print(marks.loc[0]) # Accessing the first element of the Series using label-based indexing (loc is used for label-based indexing)
# print(marks.iloc[0]) # Accessing the first element of the Series using integer-based indexing (iloc is used for integer-based indexing) 


# print(marks.head()) # This method returns the first few elements of the Series (default is 5)

# print(marks.tail()) # This method returns the last few elements of the Series (default is 5)
# print(marks.describe()) # This method provides a summary of the Series, including count, mean, standard deviation, minimum, and maximum values.
# print(marks.isnull()) # This method checks for null values in the Series and returns a boolean Series indicating which values are null (True) and which are not (False).


# filtering the Series to include only values greater than 25
print(marks[marks > 25]) # This line filters the Series 'marks' to include only the values that are greater than 25. The resulting Series will contain only the values that satisfy this condition.
