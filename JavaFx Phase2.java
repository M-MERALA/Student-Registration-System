package com.example.hallofx;



import javafx.application.Application;
import javafx.beans.property.SimpleDoubleProperty;
import javafx.beans.property.SimpleIntegerProperty;
import javafx.beans.property.SimpleStringProperty;
import javafx.collections.FXCollections;
import javafx.collections.ObservableList;
import javafx.geometry.Insets;
import javafx.geometry.Pos;
import javafx.scene.Scene;
import javafx.scene.control.*;
import javafx.scene.layout.*;
import javafx.scene.paint.Color;
import javafx.scene.text.Font;
import javafx.scene.text.FontWeight;
import javafx.stage.Stage;
import javafx.util.converter.DoubleStringConverter;
import java.util.*;

public class Hello extends Application {



        private final StudentManager studentManager = new StudentManager();
        private TableView<Student> studentTable;
        private TableView<Student> waitingTable;
        private ListView<String> courseListView;
        private ComboBox<Integer> termComboBox;
        private final Map<Integer, List<String>> termCourses = new HashMap<>();

        public static void main(String[] args) {
            launch(args);
        }

        @Override
        public void start(Stage primaryStage) {
            initializeTermCourses();
            primaryStage.setTitle("University Management System");

            TabPane tabPane = new TabPane();
            tabPane.getTabs().addAll(
                    createRegistrationTab(),
                    createStudentsTab(),
                    createCoursesTab()
            );

            Scene scene = new Scene(tabPane, 1000, 700);
            scene.getStylesheets().add(getStyleSheet());
            primaryStage.setScene(scene);
            primaryStage.show();
        }

        private void initializeTermCourses() {
            termCourses.put(1, Arrays.asList("Math 101", "Programming Basics", "English"));
            termCourses.put(2, Arrays.asList("Data Structures", "Algorithms", "Statistics"));
            termCourses.put(3, Arrays.asList("Database Systems", "OS", "Networks"));
            termCourses.put(4, Arrays.asList("AI", "Software Engineering", "Project"));
        }

        private String getStyleSheet() {
            StringBuilder css = new StringBuilder();
            css.append(".root { -fx-base: #e6f2ff; -fx-background: #e6f2ff; }");
            css.append(".tab-pane { -fx-background-color: #3a6ea5; }");
            css.append(".tab { -fx-background-color: #3a6ea5; -fx-text-fill: white; }");
            css.append(".tab:selected { -fx-background-color: #1e3f66; }");
            css.append(".button { -fx-background-color: #3a6ea5; -fx-text-fill: white; -fx-font-weight: bold; ");
            css.append("-fx-background-radius: 5; -fx-padding: 8 16; }");
            css.append(".button:hover { -fx-background-color: #1e3f66; }");
            css.append(".table-view { -fx-background-color: white; -fx-border-color: #bdc3c7; }");
            css.append(".table-row-cell:odd { -fx-background-color: #f8f9fa; }");
            css.append(".table-row-cell:selected { -fx-background-color: #3a6ea5; -fx-text-fill: white; }");
            css.append(".column-header { -fx-background-color: #1e3f66; -fx-text-fill: white; }");
            css.append(".text-field { -fx-background-radius: 4; -fx-border-color: #bdc3c7; }");
            css.append(".header-label { -fx-font-size: 16pt; -fx-text-fill: #1e3f66; -fx-font-weight: bold; }");
            css.append(".list-view { -fx-background-color: white; -fx-border-color: #bdc3c7; }");
            css.append(".label { -fx-text-fill: #1e3f66; }");
            css.append(".combo-box { -fx-background-color: white; -fx-border-color: #bdc3c7; }");
            css.append(".combo-box .list-cell { -fx-text-fill: #1e3f66; }");
            return css.toString();
        }

        private Tab createRegistrationTab() {
            GridPane grid = new GridPane();
            grid.setPadding(new Insets(25));
            grid.setVgap(20);
            grid.setHgap(15);
            grid.setAlignment(Pos.CENTER);
            grid.setStyle("-fx-background-color: #e6f2ff;");

            Label titleLabel = new Label("Student Registration");
            titleLabel.getStyleClass().add("header-label");
            grid.add(titleLabel, 0, 0, 2, 1);

            TextField nameField = createStyledTextField();
            TextFormatter<String> nameFormatter = new TextFormatter<>(change ->
                    change.getControlNewText().matches("[a-zA-Z\\s]*") ? change : null);
            nameField.setTextFormatter(nameFormatter);
            nameField.setPromptText("Enter student name");

            TextField gpaField = createStyledTextField();
            TextFormatter<Double> gpaFormatter = new TextFormatter<>(new DoubleStringConverter(), 0.0, change ->
                    change.getControlNewText().matches("^(?:[1-3](\\.\\d{0,2})?|4(\\.0{0,2})?)$") ? change : null);
            gpaField.setTextFormatter(gpaFormatter);
            gpaField.setPromptText("Enter GPA (1-4)");

            gpaField.focusedProperty().addListener((obs, oldVal, newVal) -> {
                if (!newVal) formatGpaField(gpaField);
            });

            ChoiceBox<String> departmentChoice = new ChoiceBox<>(FXCollections.observableArrayList("CS", "SE"));
            departmentChoice.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7;");

            Button registerButton = new Button("Register Student");
            registerButton.setStyle("-fx-background-color: #1e3f66;");
            registerButton.setOnAction(e -> handleRegistration(nameField, gpaField, departmentChoice));

            grid.addRow(1, new Label("Name:"), nameField);
            grid.addRow(2, new Label("GPA:"), gpaField);
            grid.addRow(3, new Label("Department:"), departmentChoice);
            grid.add(registerButton, 1, 4);

            GridPane.setHalignment(registerButton, javafx.geometry.HPos.RIGHT);
            return createTab("Registration", grid);
        }

        private Tab createStudentsTab() {
            VBox layout = new VBox(20);
            layout.setPadding(new Insets(25));
            layout.setStyle("-fx-background-color: #e6f2ff;");

            Label approvedLabel = new Label("Approved Students");
            approvedLabel.getStyleClass().add("header-label");
            studentTable = createStudentTable(studentManager.getApprovedStudents());
            studentTable.setPrefHeight(250);

            HBox buttonBox1 = new HBox(10);
            Button removeButton = new Button("Remove Selected");
            removeButton.setStyle("-fx-background-color: #c62828;");
            removeButton.setOnAction(e -> removeSelectedStudent());
            buttonBox1.getChildren().add(removeButton);
            buttonBox1.setAlignment(Pos.CENTER_RIGHT);

            Label waitingLabel = new Label("Waiting List");
            waitingLabel.getStyleClass().add("header-label");
            waitingTable = createStudentTable(studentManager.getWaitingStudents());
            waitingTable.setPrefHeight(250);

            HBox buttonBox2 = new HBox(10);
            Button approveButton = new Button("Approve Selected");
            approveButton.setStyle("-fx-background-color: #1e3f66;");
            approveButton.setOnAction(e -> approveSelectedStudent());
            buttonBox2.getChildren().add(approveButton);
            buttonBox2.setAlignment(Pos.CENTER_RIGHT);

            layout.getChildren().addAll(
                    approvedLabel, studentTable, buttonBox1,
                    waitingLabel, waitingTable, buttonBox2
            );

            return createTab("Students", layout);
        }

        private Tab createCoursesTab() {
            VBox layout = new VBox(20);
            layout.setPadding(new Insets(25));
            layout.setStyle("-fx-background-color: #e6f2ff;");

            Label titleLabel = new Label("Course Management");
            titleLabel.getStyleClass().add("header-label");

            GridPane grid = new GridPane();
            grid.setVgap(15);
            grid.setHgap(15);
            grid.setAlignment(Pos.CENTER);
            grid.setStyle("-fx-background-color: #e6f2ff;");

            TextField studentIdField = createStyledTextField();
            studentIdField.setPromptText("Enter student ID");

            termComboBox = new ComboBox<>(FXCollections.observableArrayList(1, 2, 3, 4));
            termComboBox.setPromptText("Select Term");
            termComboBox.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7;");

            ComboBox<String> courseCombo = new ComboBox<>();
            courseCombo.setPromptText("Select course");
            courseCombo.setStyle("-fx-background-color: white; -fx-border-color: #bdc3c7;");

            termComboBox.valueProperty().addListener((obs, oldVal, newVal) -> {
                if (newVal != null) {
                    courseCombo.setItems(FXCollections.observableArrayList(
                            termCourses.get(newVal)
                    ));
                }
            });

            HBox buttonBox = new HBox(10);
            Button enrollButton = new Button("Enroll Student");
            Button showCoursesButton = new Button("Show Courses");
            buttonBox.getChildren().addAll(enrollButton, showCoursesButton);
            buttonBox.setAlignment(Pos.CENTER);

            courseListView = new ListView<>();
            courseListView.setPrefHeight(200);

            enrollButton.setOnAction(e -> handleEnrollment(
                    studentIdField.getText().trim(),
                    courseCombo.getValue(),
                    termComboBox.getValue()
            ));

            showCoursesButton.setOnAction(e -> handleCourseDisplay(
                    studentIdField.getText().trim(),
                    termComboBox.getValue()
            ));

            grid.addRow(0, new Label("Student ID:"), studentIdField);
            grid.addRow(1, new Label("Term:"), termComboBox);
            grid.addRow(2, new Label("Course:"), courseCombo);
            grid.add(buttonBox, 1, 3);

            layout.getChildren().addAll(titleLabel, grid, courseListView);
            return createTab("Courses", layout);
        }

        private TableView<Student> createStudentTable(ObservableList<Student> items) {
            TableView<Student> table = new TableView<>();
            table.setStyle("-fx-font-size: 12pt;");

            TableColumn<Student, Integer> idCol = new TableColumn<>("ID");
            idCol.setCellValueFactory(cellData ->
                    new SimpleIntegerProperty(cellData.getValue().getId()).asObject());
            idCol.setPrefWidth(120);

            TableColumn<Student, String> nameCol = new TableColumn<>("Name");
            nameCol.setCellValueFactory(cellData ->
                    new SimpleStringProperty(cellData.getValue().getName()));
            nameCol.setPrefWidth(200);

            TableColumn<Student, String> deptCol = new TableColumn<>("Department");
            deptCol.setCellValueFactory(cellData ->
                    new SimpleStringProperty(cellData.getValue().getDepartment()));
            deptCol.setPrefWidth(150);

            TableColumn<Student, Double> gpaCol = new TableColumn<>("GPA");
            gpaCol.setCellValueFactory(cellData ->
                    new SimpleDoubleProperty(cellData.getValue().getGpa()).asObject());
            gpaCol.setPrefWidth(100);

            table.getColumns().addAll(idCol, nameCol, deptCol, gpaCol);
            table.setItems(items);
            return table;
        }

        private TextField createStyledTextField() {
            TextField tf = new TextField();
            tf.setFont(Font.font("Arial", 14));
            tf.setStyle("-fx-padding: 8;");
            return tf;
        }

        private void handleRegistration(TextField nameField, TextField gpaField, ChoiceBox<String> departmentChoice) {
            String name = nameField.getText().trim();
            String gpaText = gpaField.getText().trim();
            String department = departmentChoice.getValue();

            if (!validateRegistrationInput(name, gpaText, department)) return;

            try {
                double gpa = Double.parseDouble(gpaText);
                Student student = studentManager.registerStudent(name, department, gpa);
                clearRegistrationFields(nameField, gpaField, departmentChoice);
                showAlert("Success", "Student added to waiting list with ID: " + student.getId());
            } catch (NumberFormatException ex) {
                showAlert("Error", "Invalid GPA format!");
            }
        }

        private boolean validateRegistrationInput(String name, String gpaText, String department) {
            if (name.isEmpty()) {
                showAlert("Error", "Name cannot be empty!");
                return false;
            }
            if (!name.matches("[a-zA-Z\\s]+")) {
                showAlert("Error", "Name can only contain letters and spaces!");
                return false;
            }
            if (gpaText.isEmpty()) {
                showAlert("Error", "GPA cannot be empty!");
                return false;
            }
            if (department == null) {
                showAlert("Error", "Please select a department!");
                return false;
            }
            return true;
        }

        private void handleEnrollment(String studentId, String course, Integer term) {
            if (course == null || term == null) {
                showAlert("Error", "Please select both term and course!");
                return;
            }

            try {
                int id = Integer.parseInt(studentId);
                if (!studentManager.studentExists(id)) {
                    showAlert("Error", "Student not found!");
                    return;
                }
                if (!studentManager.isStudentApproved(id)) {
                    showAlert("Error", "Student is not approved yet!");
                    return;
                }
                if (studentManager.isCourseEnrolled(id, course, term)) {
                    showAlert("Error", "Student already enrolled in this course!");
                    return;
                }
                if (!studentManager.canEnrollInTerm(id, term)) {
                    showAlert("Error", "Student cannot enroll in this term yet!");
                    return;
                }
                if (studentManager.enrollCourse(id, course, term)) {
                    showAlert("Success", "Course enrolled successfully!");
                } else {
                    showAlert("Error", "Invalid term for this student!");
                }
            } catch (NumberFormatException e) {
                showAlert("Error", "Invalid Student ID format!");
            }
        }

        private void handleCourseDisplay(String studentId, Integer term) {
            try {
                int id = Integer.parseInt(studentId);
                if (term == null) {
                    showAlert("Error", "Please select a term!");
                    return;
                }
                if (!studentManager.studentExists(id)) {
                    showAlert("Error", "Student not found!");
                    return;
                }
                courseListView.setItems(FXCollections.observableArrayList(
                        studentManager.getStudentCourses(id, term)
                ));
            } catch (NumberFormatException e) {
                showAlert("Error", "Invalid Student ID format!");
            }
        }

        private void formatGpaField(TextField gpaField) {
            try {
                double value = Double.parseDouble(gpaField.getText());
                value = Math.min(4.0, Math.max(1.0, value));
                gpaField.setText(String.format("%.2f", value));
            } catch (NumberFormatException e) {
                gpaField.setText("");
            }
        }

        private void removeSelectedStudent() {
            Student selected = studentTable.getSelectionModel().getSelectedItem();
            if (selected != null) studentManager.removeStudent(selected.getId());
        }

        private void approveSelectedStudent() {
            Student selected = waitingTable.getSelectionModel().getSelectedItem();
            if (selected != null && studentManager.approveStudent(selected.getId())) {
                showAlert("Success", "Student approved successfully!");
            } else {
                showAlert("Error", "Student not found in waiting list!");
            }
        }

        private Tab createTab(String title, javafx.scene.Node content) {
            Tab tab = new Tab(title);
            tab.setClosable(false);
            tab.setContent(content);
            return tab;
        }

        private void clearRegistrationFields(TextField name, TextField gpa, ChoiceBox<?> department) {
            name.clear();
            gpa.clear();
            department.setValue(null);
        }

        private void showAlert(String title, String message) {
            Alert alert = new Alert(Alert.AlertType.INFORMATION);
            alert.setTitle(title);
            alert.setHeaderText(null);
            alert.setContentText(message);
            alert.showAndWait();
        }
    }

    class Student {
        private final int id;
        private final String name;
        private final String department;
        private final double gpa;
        private int currentTerm;

        public Student(int id, String name, String department, double gpa) {
            this.id = id;
            this.name = name;
            this.department = department;
            this.gpa = gpa;
            this.currentTerm = 1;
        }

        public int getId() { return id; }
        public String getName() { return name; }
        public String getDepartment() { return department; }
        public double getGpa() { return gpa; }
        public int getCurrentTerm() { return currentTerm; }
        public void incrementTerm() { currentTerm++; }
    }

    class StudentManager {
        private final ObservableList<Student> waitingStudents = FXCollections.observableArrayList();
        private final ObservableList<Student> approvedStudents = FXCollections.observableArrayList();
        private final Map<Integer, Map<Integer, List<String>>> courses = new HashMap<>();
        private final Map<Integer, Student> studentMap = new HashMap<>();
        private final Random random = new Random();

        public Student registerStudent(String name, String department, double gpa) {
            int id = generateUniqueId();
            Student student = new Student(id, name, department, gpa);
            waitingStudents.add(student);
            studentMap.put(id, student);
            return student;
        }

        public boolean approveStudent(int id) {
            Student student = findStudentById(waitingStudents, id);
            if (student == null) return false;

            waitingStudents.remove(student);
            approvedStudents.add(student);
            courses.put(id, new HashMap<>());
            return true;
        }

        public boolean removeStudent(int id) {
            courses.remove(id);
            studentMap.remove(id);
            return approvedStudents.removeIf(s -> s.getId() == id);
        }

        public boolean enrollCourse(int studentId, String course, int term) {
            if (!courses.containsKey(studentId)) return false;

            Student student = studentMap.get(studentId);
            if (student == null) return false;

            // Student can only enroll in current term or previous terms
            if (term > student.getCurrentTerm()) {
                return false;
            }

            courses.get(studentId).computeIfAbsent(term, k -> new ArrayList<>()).add(course);

            // If enrolled in a new term, update current term
            if (term == student.getCurrentTerm()) {
                student.incrementTerm();
            }

            return true;
        }

        public List<String> getStudentCourses(int studentId, int term) {
            if (!courses.containsKey(studentId)) return Collections.emptyList();
            return courses.get(studentId).getOrDefault(term, Collections.emptyList());
        }

        public boolean isCourseEnrolled(int studentId, String course, int term) {
            if (!courses.containsKey(studentId)) return false;
            return courses.get(studentId).getOrDefault(term, Collections.emptyList()).contains(course);
        }

        public boolean studentExists(int id) {
            return studentMap.containsKey(id);
        }

        public boolean isStudentApproved(int id) {
            return courses.containsKey(id);
        }

        public boolean canEnrollInTerm(int studentId, int term) {
            Student student = studentMap.get(studentId);
            if (student == null) return false;
            return term <= student.getCurrentTerm();
        }

        public ObservableList<Student> getApprovedStudents() { return approvedStudents; }
        public ObservableList<Student> getWaitingStudents() { return waitingStudents; }

        private Student findStudentById(ObservableList<Student> students, int id) {
            return students.stream()
                    .filter(s -> s.getId() == id)
                    .findFirst()
                    .orElse(null);
        }

        private int generateUniqueId() {
            int id;
            do {
                id = random.nextInt(900000000) + 100000000;
            } while (studentExists(id));
            return id;
        }
    }