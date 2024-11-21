import csv
from datetime import datetime

def load_students(filename): #Himangshu
    students = {}
    with open(filename, mode='r') as file:
        reader = csv.DictReader(file)   #csv.Dictreader() is used to read rows as dictionaries where keys are column headers.
        for row in reader:
            students[row['ID']] = row['Name']
    return students

def record_attendance(students, attendance_file): #Himangshu
    attendance_records = []
    date_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    class_name = input("Enter class name: ")

    for student_id, student_name in students.items():
        present = input(f"Is {student_name} (ID: {student_id}) present? (y/n): ").strip().lower()
        attendance_records.append({
            'ID': student_id,
            'Name': student_name,
            'Date': date_time,
            'Class': class_name,
            'Status': 'Present' if present == 'y' else 'Absent'
        })

    save_attendance(attendance_file, attendance_records)

def save_attendance(filename, records): #Anjan
    with open(filename, mode='a', newline='') as file:  # Change to append mode
        fieldnames = ['ID', 'Name', 'Date', 'Class', 'Status']
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        if file.tell() == 0:  # Write header only if file is empty
            writer.writeheader()
        writer.writerows(records)

def calculate_attendance_percentage(attendance_file, student_id=None):#Amir
    attendance_count = {}
    with open(attendance_file, mode='r') as file:
        reader = csv.DictReader(file)
        for row in reader:
            if student_id and row['ID'] != student_id:
                continue
            if row['ID'] not in attendance_count:
                attendance_count[row['ID']] = {'present': 0, 'total': 0}
            attendance_count[row['ID']]['total'] += 1
            if row['Status'] == 'Present':
                attendance_count[row['ID']]['present'] += 1

    return attendance_count

def check_eligibility(attendance_count):#Anjan
    for student_id, counts in attendance_count.items():
        if counts['total'] == 0:  # Avoid division by zero
            print(f"Student ID: {student_id} has no attendance records.")
            continue
            
        percentage = (counts['present'] / counts['total']) * 100
        print(f"\nStudent ID: {student_id}, Attendance Percentage: {percentage:.2f}%")

        if percentage < 75:
            print(f"Student ID: {student_id} is not eligible for Minor Test-1, Minor Test-2,
                  or Final Semester Exam.\n")
        else:
            print(f"Student ID: {student_id} is eligible for Minor Test-1, Minor Test-2, 
                  and Final Semester Exam.\n")

def main():#Arpan
    students_file = 'Project_1/students.csv'
    attendance_file = 'Project_1/attendance.csv'
    students = load_students(students_file)

    record_attendance(students, attendance_file)

    while True:
        student_query = input("Enter student ID or Name to check attendance percentage (or type 'exit' to quit): ").strip().upper()
        if student_query.lower() == 'exit':
            break
        
        student_id = None
        for id, name in students.items():
            if student_query == id or student_query.lower() == name.lower():
                student_id = id
                break

        if student_id:
            attendance_count = calculate_attendance_percentage(attendance_file, student_id)
            check_eligibility(attendance_count)
        else:
            print("Student not found. Please enter a valid ID or Name.")

if __name__ == "__main__":
    main()