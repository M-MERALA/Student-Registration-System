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

    
    bool operator<(const Student& other) const { return id < other.id; }
    bool operator>(const Student& other) const { return id > other.id; }
    bool operator==(const Student& other) const { return id == other.id; }
};

struct BSTNode {
    Student student;
    BSTNode* left;
    BSTNode* right;

    BSTNode(Student s) : student(s), left(nullptr), right(nullptr) {}
};

class RegistrationSystem {
private:
    list<Student> studentList;  
    BSTNode* studentTree;      
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

    
    BSTNode* insertBST(BSTNode* node, Student student) {
        if (node == nullptr) {
            return new BSTNode(student);
        }

        if (student.id < node->student.id) {
            node->left = insertBST(node->left, student);
        } else if (student.id > node->student.id) {
            node->right = insertBST(node->right, student);
        }

        return node;
    }

    BSTNode* searchBST(BSTNode* node, int id) {
        if (node == nullptr || node->student.id == id) {
            return node;
        }

        if (id < node->student.id) {
            return searchBST(node->left, id);
        } else {
            return searchBST(node->right, id);
        }
    }

    BSTNode* findMin(BSTNode* node) {
        while (node->left != nullptr) {
            node = node->left;
        }
        return node;
    }

    BSTNode* removeBST(BSTNode* node, int id) {
        if (node == nullptr) return nullptr;

        if (id < node->student.id) {
            node->left = removeBST(node->left, id);
        } else if (id > node->student.id) {
            node->right = removeBST(node->right, id);
        } else {
            // Node with only one child or no child
            if (node->left == nullptr) {
                BSTNode* temp = node->right;
                delete node;
                return temp;
            } else if (node->right == nullptr) {
                BSTNode* temp = node->left;
                delete node;
                return temp;
            }

            // Node with two children
            BSTNode* temp = findMin(node->right);
            node->student = temp->student;
            node->right = removeBST(node->right, temp->student.id);
        }
        return node;
    }

    void inOrderTraversal(BSTNode* node) {
        if (node != nullptr) {
            inOrderTraversal(node->left);
            cout << "ID: " << node->student.id << ", Name: " << node->student.name
                 << ", Department: " << node->student.department << ", GPA: " << node->student.gpa << "\n";
            inOrderTraversal(node->right);
        }
    }

    void preOrderTraversal(BSTNode* node) {
        if (node != nullptr) {
            cout << "ID: " << node->student.id << ", Name: " << node->student.name
                 << ", Department: " << node->student.department << ", GPA: " << node->student.gpa << "\n";
            preOrderTraversal(node->left);
            preOrderTraversal(node->right);
        }
    }

    void postOrderTraversal(BSTNode* node) {
        if (node != nullptr) {
            postOrderTraversal(node->left);
            postOrderTraversal(node->right);
            cout << "ID: " << node->student.id << ", Name: " << node->student.name
                 << ", Department: " << node->student.department << ", GPA: " << node->student.gpa << "\n";
        }
    }

    void displayBSTMenu() {
        cout << "\nBST Display Options:\n";
        cout << "1. In-order Traversal (Sorted by ID)\n";
        cout << "2. Pre-order Traversal\n";
        cout << "3. Post-order Traversal\n";
        cout << "Enter your choice: ";
    }

public:
    RegistrationSystem() : studentTree(nullptr) {
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

        // Insert into BST
        studentTree = insertBST(studentTree, newStudent);

        studentCourses[id] = queue<string>();
        cout << "Student " << name << " registered successfully with ID: " << id << "\n";
    }

    void removeStudentByID() {
        int id;
        cout << "Enter Student ID to remove: ";
        cin >> id;

        // Remove from list
        bool found = false;
        for (auto it = studentList.begin(); it != studentList.end(); ++it) {
            if (it->id == id) {
                studentList.erase(it);
                found = true;
                break;
            }
        }

        if (found) {
            // Remove from BST
            studentTree = removeBST(studentTree, id);

            studentCourses.erase(id);
            assignedIDs.erase(id);
            cout << "Student with ID " << id << " has been removed.\n";
        } else {
            cout << "Student not found.\n";
        }
    }

    void displayAllStudents() {
        if (studentList.empty()) {
            cout << "No students registered.\n";
            return;
        }

        cout << "\nStudents in insertion order:\n";
        for (const auto& s : studentList) {
            cout << "ID: " << s.id << ", Name: " << s.name
                 << ", Department: " << s.department << ", GPA: " << s.gpa << "\n";
        }
    }

    void displayBSTStudents() {
        if (studentTree == nullptr) {
            cout << "No students in BST.\n";
            return;
        }

        displayBSTMenu();
        int choice;
        cin >> choice;

        cout << "\nStudents in BST:\n";
        switch(choice) {
            case 1:
                cout << "In-order Traversal (Sorted by ID):\n";
                inOrderTraversal(studentTree);
                break;
            case 2:
                cout << "Pre-order Traversal:\n";
                preOrderTraversal(studentTree);
                break;
            case 3:
                cout << "Post-order Traversal:\n";
                postOrderTraversal(studentTree);
                break;
            default:
                cout << "Invalid choice. Displaying in-order traversal by default.\n";
                inOrderTraversal(studentTree);
        }
    }

    void enrollInCourses() {
        int id;
        cout << "Enter Student ID: ";
        cin >> id;

        // Search in BST for efficiency
        BSTNode* node = searchBST(studentTree, id);
        if (node == nullptr) {
            cout << "Student not found!\n";
            return;
        }

        if (node->student.gpa < 2.00) {
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

        // Search in BST for efficiency
        BSTNode* node = searchBST(studentTree, id);
        if (node == nullptr) {
            cout << "Student not found!\n";
            return;
        }

        cout << "Registered Courses for " << node->student.name << " (ID: " << node->student.id << "):\n";
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

    void searchStudentByID() {
        int id;
        cout << "Enter Student ID to search: ";
        cin >> id;

        BSTNode* node = searchBST(studentTree, id);
        if (node != nullptr) {
            cout << "\nStudent found:\n";
            cout << "ID: " << node->student.id << "\n";
            cout << "Name: " << node->student.name << "\n";
            cout << "Department: " << node->student.department << "\n";
            cout << "GPA: " << node->student.gpa << "\n";

            // Display registered courses if any
            if (!studentCourses[id].empty()) {
                cout << "Registered Courses:\n";
                queue<string> tempQueue = studentCourses[id];
                while (!tempQueue.empty()) {
                    cout << "- " << tempQueue.front() << "\n";
                    tempQueue.pop();
                }
            }
        } else {
            cout << "Student not found.\n";
        }
    }
};

int main() {
    RegistrationSystem system;
    int choice;
    do {
        cout << "\nUniversity Student Registration System\n";
        cout << "1. Register Student\n2. Remove Student by ID\n3. Display All Students (List)\n";
        cout << "4. Display Students (BST)\n5. Enroll in Courses\n6. Display Student Courses\n";
        cout << "7. Search Student by ID\n8. Exit\n";
        cout << "Enter your choice: ";
        cin >> choice;

        switch (choice) {
            case 1: system.registerStudent(); break;
            case 2: system.removeStudentByID(); break;
            case 3: system.displayAllStudents(); break;
            case 4: system.displayBSTStudents(); break;
            case 5: system.enrollInCourses(); break;
            case 6: system.displayStudentCourses(); break;
            case 7: system.searchStudentByID(); break;
            case 8: cout << "Exiting...\n"; break;
            default: cout << "Invalid choice!\n";
        }
    } while (choice != 8);
    return 0;
}