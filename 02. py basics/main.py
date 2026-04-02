def getgrade(grade):
    if grade <= 4 and grade > 3.6:
        return "A"
    elif grade <3.6 and grade >=3.2:
        return "A-"
    elif grade < 3.2 and grade >= 2.8:
        return "B"
    elif grade >= 2.4 and grade < 2.8:
        return "C"
    elif grade >= 2.0 and grade < 2.4:
        return "D"
    elif grade < 2.0:
        return "F"
    else:
        return "Invalid grade"

# def main():
#     print("Hello from data-science!")


# if __name__ == "__main__":
#     main()
grade = float(input("Enter your grade: "))
print(getgrade(grade))