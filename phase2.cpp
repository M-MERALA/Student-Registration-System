#include <iostream>
#include <list>
#include <queue>
#include <string>
#include <map>
#include <vector>
#include <cstdlib>
#include <ctime>
#include <set>
#include <regex>
#include <algorithm>

using namespace std;

struct Student {
    int id;
    string name;
    string department;
    double gpa;
};

class RegistrationSystem {
private:
    list<Student> studentList;
    map<int, queue<string>> studentCourses;
    map<int, queue<pair<string, int>>> semesterCourses;
    set<int> assignedIDs;

    int generateUniqueID() {
        int id;
        do {
            id = rand() % 900000000 + 100000000;
        } while (assignedIDs.find(id) != assignedIDs.end());
        assignedIDs.insert(id);
        return id;
    }

    bool isValidName(const string& name) {
        return regex_match(name, regex("^[A-Za-z ]+$"));
    }

    bool isValidGPA(double gpa) {
        return gpa >= 0.00 && gpa <= 4.00;
    }

    Student* findStudentByID(int id) {
        for (const auto& s : studentList) {
            if (s.id == id) return new Student(s);
        }
        return nullptr;
    }

public:
    RegistrationSystem() {
        queue<pair<string, int>> q1, q2, q3, q4, q5, q6;
        q1.push({"Math 101", 3}); q1.push({"Physics 102", 4}); q1.push({"English 103", 2});
        q2.push({"CS 201", 3}); q2.push({"Algorithms 202", 4}); q2.push({"Databases 203", 3});
        q3.push({"Networks 301", 3}); q3.push({"OS 302", 4}); q3.push({"AI 303", 3});
        q4.push({"Software Eng 401", 3}); q4.push({"Cybersecurity 402", 4}); q4.push({"Cloud 403", 3});
        q5.push({"Machine Learning 501", 3}); q5.push({"Blockchain 502", 4}); q5.push({"IoT 503", 3});
        q6.push({"Big Data 601", 3}); q6.push({"Quantum Computing 602", 4}); q6.push({"Ethical Hacking 603", 3});

        semesterCourses[1] = q1;
        semesterCourses[2] = q2;
        semesterCourses[3] = q3;
        semesterCourses[4] = q4;
        semesterCourses[5] = q5;
        semesterCourses[6] = q6;
        srand(time(0));
    }

    void registerStudent() {
        string name, department;
        double gpa;

        cin.ignore();
        do {
            cout << "Enter Full Name (No Symbols): ";
            getline(cin, name);
            if (!isValidName(name)) {
                cout << "Invalid name! Only letters and spaces are allowed.\n";
            }
        } while (!isValidName(name));

        do {
            cout << "Enter GPA (0.00 - 4.00): ";
            cin >> gpa;
            if (!isValidGPA(gpa)) {
                cout << "Invalid GPA! Must be between 0.00 and 4.00.\n";
            }
        } while (!isValidGPA(gpa));

        cout << "Choose Department: 1 - Computer Science, 2 - Software Engineering: ";
        int choice;
        cin >> choice;
        department = (choice == 1) ? "Computer Science" : "Software Engineering";

        int id = generateUniqueID();
        Student newStudent = {id, name, department, gpa};

        cout << "Where do you want to insert this student in the list?\n";
        cout << "1 - Insert at the front\n2 - Insert at a specific position\n";
        int positionChoice;
        cin >> positionChoice;

        if (positionChoice == 1) {
            studentList.push_front(newStudent);
        } else if (positionChoice == 2) {
            cout << "Enter the position (1 = front): ";
            int pos;
            cin >> pos;
            auto it = studentList.begin();
            advance(it, pos - 1);
            studentList.insert(it, newStudent);
        }

        studentCourses[id] = queue<string>();
        cout << "Student " << name << " registered successfully with ID: " << id << "\n";
    }

    void removeStudentByID() {
        int id;
        cout << "Enter Student ID to remove: ";
        cin >> id;

        bool found = false;
        for (auto it = studentList.begin(); it != studentList.end(); ++it) {
            if (it->id == id) {
                studentList.erase(it);
                studentCourses.erase(id);
                assignedIDs.erase(id);
                cout << "Student with ID " << id << " has been removed.\n";
                found = true;
                break;
            }
        }
        if (!found) {
            cout << "Student not found.\n";
        }
    }

    void displayAllStudents() {
        if (studentList.empty()) {
            cout << "No students registered.\n";
            return;
        }
        for (const auto& s : studentList) {
            cout << "ID: " << s.id << ", Name: " << s.name << ", GPA: " << s.gpa << "\n";
        }
    }

    void enrollInCourses() {
        int id;
        cout << "Enter Student ID: ";
        cin >> id;

        Student* student = findStudentByID(id);
        if (!student) {
            cout << "Student not found!\n";
            return;
        }

        if (student->gpa < 2.00) {
            cout << "Student GPA is below 2.00. Cannot enroll in courses.\n";
            return;
        }

        int semester;
        cout << "Enter semester (1-6): ";
        cin >> semester;

        if (semesterCourses.find(semester) == semesterCourses.end()) {
            cout << "Invalid semester selection.\n";
            return;
        }

        queue<pair<string, int>> availableCourses = semesterCourses[semester];
        cout << "Available courses:\n";
        while (!availableCourses.empty()) {
            cout << "- " << availableCourses.front().first << " (" << availableCourses.front().second << " credits)\n";
            availableCourses.pop();
        }

        cout << "Enter course names to register (type 'done' to finish):\n";
        string courseName;
        cin.ignore();
        while (true) {
            getline(cin, courseName);
            if (courseName == "done") break;
            studentCourses[id].push(courseName);
            cout << "Registered: " << courseName << "\n";
        }
        cout << "Course registration complete.\n";
    }

    void displayStudentCourses() {
        int id;
        cout << "Enter Student ID: ";
        cin >> id;

        Student* student = findStudentByID(id);
        if (!student) {
            cout << "Student not found!\n";
            return;
        }

        cout << "Registered Courses for " << student->name << " (ID: " << student->id << "):\n";
        if (studentCourses[id].empty()) {
            cout << "No courses registered.\n";
            return;
        }
        queue<string> tempQueue = studentCourses[id];
        while (!tempQueue.empty()) {
            cout << "- " << tempQueue.front() << "\n";
            tempQueue.pop();
        }
    }
};

int main() {
    RegistrationSystem system;
    int choice;
    do {
        cout << "\nUniversity Student Registration System\n";
        cout << "1. Register Student\n2. Remove Student by ID\n3. Display All Students\n4. Enroll in Courses\n5. Display Student Courses\n6. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1: system.registerStudent(); break;
            case 2: system.removeStudentByID(); break;
            case 3: system.displayAllStudents(); break;
            case 4: system.enrollInCourses(); break;
            case 5: system.displayStudentCourses(); break;
            case 6: cout << "Exiting...\n"; break;
        }
    } while (choice != 6);
    return 0;
}