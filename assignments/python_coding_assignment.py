# Case Study 1: Student Performance Analysis System

# Task 1: Accept Number of Students
def get_number_of_students():
    while True:
        try:
            n = int(input("Enter number of students: "))
            if n <= 0:
                raise ValueError
            return n
        except ValueError:
            print("Error: Please enter a valid positive integer.")

# Task 2: Input Student Marks
def get_student_marks(n):
    marks = []
    for i in range(1, n + 1):
        while True:
            try:
                mark = float(input(f"Enter mark for student {i}: "))
                if mark < 0 or mark > 100:
                    print("Error: Marks must be between 0 and 100")
                    continue
                marks.append(mark)
                break
            except ValueError:
                print("Error: Please enter a valid numeric mark.")
    return marks

# Task 3: Calculate Average Marks
def calculate_average(marks):
    total = 0
    for mark in marks:
        total += mark
    return total / len(marks)

# Task 4: Find the Highest Marks
def find_highest(marks):
    highest = marks[0]
    for mark in marks:
        if mark > highest:
            highest = mark
    return highest

# Task 5: Find the Lowest Marks
def find_lowest(marks):
    lowest = marks[0]
    for mark in marks:
        if mark < lowest:
            lowest = mark
    return lowest

# Task 6: Count Passed and Failed Students
def count_results(marks):
    passed = 0
    failed = 0
    for mark in marks:
        if mark >= 50:
            passed += 1
        else:
            failed += 1
    return passed, failed

# Task 7: Display the Final Report
def display_report(marks):
    avg = calculate_average(marks)
    highest = find_highest(marks)
    lowest = find_lowest(marks)
    passed, failed = count_results(marks)

    print("\nStudent Performance Report")
    print("---------------------------")
    print(f"Average Marks: {avg:.1f}")
    print(f"Highest Marks: {highest:.0f}")
    print(f"Lowest Marks: {lowest:.0f}")
    print(f"Students Passed: {passed}")
    print(f"Students Failed: {failed}")

def run_case_study_1():
    print("=" * 40)
    print("  Student Performance Analysis System")
    print("=" * 40)
    n = get_number_of_students()
    marks = get_student_marks(n)
    display_report(marks)
    
    

# Case Study 2: Inventory Stock Monitoring System

# Task 1: Create Initial Stock List
def create_initial_stock():
    stock = [25, 12, 5, 30, 8]
    return stock

# Task 2: Display Stock Function
def display_stock(stock):
    print("\nCurrent Stock:")
    for i in range(len(stock)):
        print(f"Product {i + 1} : {stock[i]}")

# Task 3: Update Stock
def update_stock(stock, product_number, quantity):
    stock[product_number - 1] = quantity

# Task 4: Detect Low Stock
def check_low_stock(stock):
    print("\nLow Stock Alert:")
    found = False
    for i in range(len(stock)):
        if stock[i] < 10:
            print(f"Product {i + 1}")
            found = True
    if not found:
        print("All products are sufficiently stocked.")

# Task 5 & 6: Menu System with Error Handling
def run_case_study_2():
    print("\n" + "=" * 40)
    print("   Inventory Stock Monitoring System")
    print("=" * 40)

    stock = create_initial_stock()

    while True:
        print("\n--- Menu ---")
        print("1. View Stock")
        print("2. Update Stock")
        print("3. Check Low Stock")
        print("4. Exit")

        try:
            choice = int(input("Enter your choice: "))
        except ValueError:
            print("Error: Please enter a valid menu option (1-4).")
            continue

        if choice == 1:
            display_stock(stock)

        elif choice == 2:
            try:
                product_number = int(input("Enter product number: "))
                if product_number < 1 or product_number > len(stock):
                    raise IndexError
                new_quantity = int(input("Enter new quantity: "))
                if new_quantity < 0:
                    raise ValueError("Negative stock value")
                update_stock(stock, product_number, new_quantity)
                print("Stock updated successfully")
            except IndexError:
                print("Error: Invalid product number")
            except ValueError as e:
                if "Negative" in str(e):
                    print("Error: Stock value cannot be negative")
                else:
                    print("Error: Please enter a valid numeric value")

        elif choice == 3:
            check_low_stock(stock)

        elif choice == 4:
            # Task 7: Terminate Program
            print("Inventory system closed.")
            break

        else:
            print("Error: Invalid choice. Please select 1 to 4.")
            
            
            
run_case_study_1()
run_case_study_2()
