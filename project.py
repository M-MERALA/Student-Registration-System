import tkinter as tk
from tkinter import ttk, messagebox, simpledialog, scrolledtext
import random
import re
from collections import deque
import time

# Enhanced Color Palette with more vibrant options
COLORS = {
    "primary": "#6200EA",  # Deep purple
    "primary_light": "#9E47FF",  # Lighter purple
    "primary_dark": "#0400BA",  # Dark blue-purple
    "secondary": "#FF4081",  # Pink accent
    "secondary_light": "#FF79B0",  # Light pink
    "secondary_dark": "#C60055",  # Dark pink
    "accent1": "#00BFA5",  # Teal
    "accent1_light": "#5DF2D6",  # Light teal
    "accent1_dark": "#008E76",  # Dark teal
    "accent2": "#FFC400",  # Amber
    "accent2_light": "#FFF263",  # Light amber
    "accent2_dark": "#C79300",  # Dark amber
    "background": "#F5F5F6",  # Very light gray
    "surface": "#FFFFFF",  # White
    "error": "#FF1744",  # Bright red
    "success": "#00E676",  # Bright green
    "warning": "#FF9100",  # Orange
    "info": "#00B0FF",  # Light blue
    "text_primary": "#212121",  # Dark gray
    "text_secondary": "#757575",  # Medium gray
    "divider": "#BDBDBD"  # Light gray
}

class Student:
    def __init__(self, id, name, department, gpa):
        self.id = id
        self.name = name
        self.department = department
        self.gpa = gpa

class BSTNode:
    def __init__(self, student):
        self.student = student
        self.left = None
        self.right = None

class RegistrationSystem:
    def __init__(self):
        self.student_list = []
        self.student_tree = None
        self.student_courses = {}
        self.semester_courses = {
            1: deque([("Math 101", 3), ("Physics 102", 4), ("English 103", 2)]),
            2: deque([("CS 201", 3), ("Algorithms 202", 4), ("Databases 203", 3)]),
            3: deque([("Networks 301", 3), ("OS 302", 4), ("AI 303", 3)]),
            4: deque([("Software Eng 401", 3), ("Cybersecurity 402", 4), ("Cloud 403", 3)]),
            5: deque([("Machine Learning 501", 3), ("Blockchain 502", 4), ("IoT 503", 3)]),
            6: deque([("Big Data 601", 3), ("Quantum Computing 602", 4), ("Ethical Hacking 603", 3)])
        }
        self.assigned_ids = set()

    def generate_unique_id(self):
        while True:
            id = random.randint(100000000, 999999999)
            if id not in self.assigned_ids:
                self.assigned_ids.add(id)
                return id

    def is_valid_name(self, name):
        return re.match(r"^[A-Za-z ]+$", name) is not None

    def is_valid_gpa(self, gpa):
        try:
            return 0.00 <= float(gpa) <= 4.00
        except ValueError:
            return False

    # BST operations
    def insert_bst(self, node, student):
        if node is None:
            return BSTNode(student)
        
        if student.id < node.student.id:
            node.left = self.insert_bst(node.left, student)
        elif student.id > node.student.id:
            node.right = self.insert_bst(node.right, student)
        
        return node

    def search_bst(self, node, id):
        if node is None or node.student.id == id:
            return node
        
        if id < node.student.id:
            return self.search_bst(node.left, id)
        else:
            return self.search_bst(node.right, id)

    def find_min(self, node):
        while node.left is not None:
            node = node.left
        return node

    def remove_bst(self, node, id):
        if node is None:
            return None
        
        if id < node.student.id:
            node.left = self.remove_bst(node.left, id)
        elif id > node.student.id:
            node.right = self.remove_bst(node.right, id)
        else:
            if node.left is None:
                return node.right
            elif node.right is None:
                return node.left
            
            temp = self.find_min(node.right)
            node.student = temp.student
            node.right = self.remove_bst(node.right, temp.student.id)
        
        return node

    def in_order_traversal(self, node, result):
        if node is not None:
            self.in_order_traversal(node.left, result)
            result.append(f"ID: {node.student.id}, Name: {node.student.name}, Department: {node.student.department}, GPA: {node.student.gpa}")
            self.in_order_traversal(node.right, result)

    def pre_order_traversal(self, node, result):
        if node is not None:
            result.append(f"ID: {node.student.id}, Name: {node.student.name}, Department: {node.student.department}, GPA: {node.student.gpa}")
            self.pre_order_traversal(node.left, result)
            self.pre_order_traversal(node.right, result)

    def post_order_traversal(self, node, result):
        if node is not None:
            self.post_order_traversal(node.left, result)
            self.post_order_traversal(node.right, result)
            result.append(f"ID: {node.student.id}, Name: {node.student.name}, Department: {node.student.department}, GPA: {node.student.gpa}")

    def register_student(self, name, gpa, department, position=0):
        if not self.is_valid_name(name):
            return False, "Invalid name! Only letters and spaces are allowed."
        
        try:
            gpa = float(gpa)
            if not self.is_valid_gpa(gpa):
                return False, "Invalid GPA! Must be between 0.00 and 4.00."
        except ValueError:
            return False, "Invalid GPA! Must be a number."

        id = self.generate_unique_id()
        department = "Computer Science" if department == 1 else "Software Engineering"
        new_student = Student(id, name, department, gpa)

        if position == 0:
            self.student_list.insert(0, new_student)
        else:
            pos = min(position - 1, len(self.student_list))
            self.student_list.insert(pos, new_student)

        self.student_tree = self.insert_bst(self.student_tree, new_student)
        self.student_courses[id] = deque()
        return True, f"Student {name} registered successfully with ID: {id}"

    def remove_student(self, id):
        try:
            id = int(id)
        except ValueError:
            return False, "Invalid ID format"

        for i, student in enumerate(self.student_list):
            if student.id == id:
                del self.student_list[i]
                self.student_tree = self.remove_bst(self.student_tree, id)
                if id in self.student_courses:
                    del self.student_courses[id]
                if id in self.assigned_ids:
                    self.assigned_ids.remove(id)
                return True, f"Student with ID {id} has been removed."
        
        return False, "Student not found."

    def get_students_list(self):
        return [f"ID: {s.id}, Name: {s.name}, Department: {s.department}, GPA: {s.gpa}" 
                for s in self.student_list]

    def get_students_bst(self, traversal_type):
        result = []
        if traversal_type == 1:
            self.in_order_traversal(self.student_tree, result)
        elif traversal_type == 2:
            self.pre_order_traversal(self.student_tree, result)
        elif traversal_type == 3:
            self.post_order_traversal(self.student_tree, result)
        return result

    def enroll_in_courses(self, student_id, semester, courses):
        try:
            student_id = int(student_id)
            semester = int(semester)
        except ValueError:
            return False, "Invalid ID or semester format"

        node = self.search_bst(self.student_tree, student_id)
        if node is None:
            return False, "Student not found!"

        if node.student.gpa < 2.00:
            return False, "Student GPA is below 2.00. Cannot enroll in courses."

        if semester not in self.semester_courses:
            return False, "Invalid semester selection."

        available_courses = [course[0] for course in self.semester_courses[semester]]
        invalid_courses = [course for course in courses if course not in available_courses]
        
        if invalid_courses:
            return False, f"Invalid courses: {', '.join(invalid_courses)}"

        if student_id not in self.student_courses:
            self.student_courses[student_id] = deque()

        for course in courses:
            self.student_courses[student_id].append(course)

        return True, "Course registration complete."

    def get_student_courses(self, student_id):
        try:
            student_id = int(student_id)
        except ValueError:
            return False, "Invalid ID format", None

        node = self.search_bst(self.student_tree, student_id)
        if node is None:
            return False, "Student not found!", None

        if student_id not in self.student_courses or not self.student_courses[student_id]:
            return True, f"Registered Courses for {node.student.name} (ID: {node.student.id}):\nNo courses registered.", None

        courses = list(self.student_courses[student_id])
        message = f"Registered Courses for {node.student.name} (ID: {node.student.id}):"
        return True, message, courses

    def search_student(self, student_id):
        try:
            student_id = int(student_id)
        except ValueError:
            return False, "Invalid ID format", None, None

        node = self.search_bst(self.student_tree, student_id)
        if node is None:
            return False, "Student not found!", None, None

        student_info = {
            "ID": node.student.id,
            "Name": node.student.name,
            "Department": node.student.department,
            "GPA": node.student.gpa
        }

        courses = list(self.student_courses.get(student_id, deque()))
        return True, "Student found!", student_info, courses

class AnimatedSplashScreen:
    def __init__(self, root, callback):
        self.root = root
        self.callback = callback
        
        # Configure root window
        self.root.withdraw()
        
        # Create splash window
        self.splash = tk.Toplevel()
        self.splash.overrideredirect(True)
        
        # Center the splash screen
        window_width = 800
        window_height = 500
        screen_width = self.splash.winfo_screenwidth()
        screen_height = self.splash.winfo_screenheight()
        x = (screen_width // 2) - (window_width // 2)
        y = (screen_height // 2) - (window_height // 2)
        self.splash.geometry(f"{window_width}x{window_height}+{x}+{y}")
        
        # Create canvas for animations
        self.canvas = tk.Canvas(self.splash, width=window_width, height=window_height, 
                               highlightthickness=0, bg=COLORS["primary_dark"])
        self.canvas.pack(fill="both", expand=True)
        
        # Add animated elements
        self.create_animated_background()
        self.add_logo_text()
        self.add_progress_bar()
        
        # Start loading animation
        self.load_progress()
    
    def create_animated_background(self):
        # Create gradient background
        for i in range(500):
            r = int(COLORS["primary_dark"][1:3], 16)
            g = int(COLORS["primary_dark"][3:5], 16)
            b = int(COLORS["primary_dark"][5:7], 16)
            r = min(255, r + int(i/500 * 50))
            g = min(255, g + int(i/500 * 50))
            b = min(255, b + int(i/500 * 50))
            color = f'#{r:02x}{g:02x}{b:02x}'
            self.canvas.create_line(0, i, 800, i, fill=color)
        
        # Add floating particles
        self.particles = []
        for _ in range(30):
            x = random.randint(0, 800)
            y = random.randint(0, 500)
            size = random.randint(2, 6)
            particle = self.canvas.create_oval(
                x, y, x+size, y+size, 
                fill=random.choice([COLORS["secondary_light"], COLORS["accent1_light"], COLORS["accent2_light"]]), 
                outline=""
            )
            speed = random.uniform(0.3, 1.2)
            direction = random.uniform(-0.5, 0.5)
            self.particles.append((particle, speed, direction))
        
        self.animate_particles()
    
    def animate_particles(self):
        for particle, speed, direction in self.particles:
            self.canvas.move(particle, direction, speed)
            coords = self.canvas.coords(particle)
            if coords[1] > 500:
                self.canvas.move(particle, 0, -550)
                # Change color when particle wraps around
                self.canvas.itemconfig(particle, fill=random.choice(
                    [COLORS["secondary_light"], COLORS["accent1_light"], COLORS["accent2_light"]]
                ))
            elif coords[0] < 0 or coords[2] > 800:
                self.canvas.move(particle, -direction*10, 0)
        self.splash.after(30, self.animate_particles)
    
    def add_logo_text(self):
        # University logo/text with modern typography
        self.canvas.create_text(
            400, 180, 
            text="UNIVERSITY", 
            font=("Segoe UI", 48, "bold"), 
            fill="white",
            tags="title"
        )
        
        # Animated subtitle with gradient colors
        self.subtitle = self.canvas.create_text(
            400, 240, 
            text="", 
            font=("Segoe UI", 20), 
            fill=COLORS["secondary_light"],
            tags="subtitle"
        )
        
        # Typewriter effect for subtitle
        self.subtitle_text = "Registration System"
        self.subtitle_index = 0
        self.type_subtitle()
    
    def type_subtitle(self):
        if self.subtitle_index < len(self.subtitle_text):
            current_text = self.subtitle_text[:self.subtitle_index+1]
            # Change color as typing progresses
            color = self.get_typing_color(self.subtitle_index)
            self.canvas.itemconfig(self.subtitle, text=current_text, fill=color)
            self.subtitle_index += 1
            self.splash.after(100, self.type_subtitle)
    
    def get_typing_color(self, index):
        # Create a color gradient effect while typing
        colors = [
            COLORS["secondary_light"],
            COLORS["accent1_light"],
            COLORS["accent2_light"],
            COLORS["secondary"]
        ]
        return colors[index % len(colors)]
    
    def add_progress_bar(self):
        # Modern progress bar container with rounded corners
        self.canvas.create_rectangle(
            150, 400, 650, 420, 
            fill=COLORS["primary"], 
            outline="",
            tags="progress_bg"
        )
        
        # Animated progress bar with gradient
        self.progress = self.canvas.create_rectangle(
            152, 402, 152, 418, 
            fill=COLORS["secondary"], 
            outline="",
            tags="progress"
        )
    
    def load_progress(self):
        for i in range(0, 498, 3):
            # Update progress bar color as it loads
            progress_color = self.get_progress_color(i/498)
            self.canvas.itemconfig(self.progress, fill=progress_color)
            self.canvas.coords(self.progress, 152, 402, 152+i, 418)
            self.splash.update()
            time.sleep(0.02)
        
        # Smooth transition to main app
        self.splash.after(800, self.transition_to_main)
    
    def get_progress_color(self, progress):
        # Create a color gradient based on progress
        if progress < 0.33:
            r = int(COLORS["secondary"][1:3], 16)
            g = int(COLORS["secondary"][3:5], 16)
            b = int(COLORS["secondary"][5:7], 16)
        elif progress < 0.66:
            r = int(COLORS["accent1"][1:3], 16)
            g = int(COLORS["accent1"][3:5], 16)
            b = int(COLORS["accent1"][5:7], 16)
        else:
            r = int(COLORS["accent2"][1:3], 16)
            g = int(COLORS["accent2"][3:5], 16)
            b = int(COLORS["accent2"][5:7], 16)
        
        return f'#{r:02x}{g:02x}{b:02x}'
    
    def transition_to_main(self):
        # Fade out animation with color transition
        for alpha in range(100, -1, -5):
            self.splash.attributes("-alpha", alpha/100)
            bg_color = self.get_transition_color(alpha)
            self.canvas.config(bg=bg_color)
            self.splash.update()
            time.sleep(0.02)
        
        self.splash.destroy()
        self.root.deiconify()
        self.root.attributes("-alpha", 0)
        
        # Fade in main window with color transition
        for alpha in range(0, 101, 5):
            self.root.attributes("-alpha", alpha/100)
            self.root.update()
            time.sleep(0.02)
        
        self.callback()
    
    def get_transition_color(self, alpha):
        # Transition from primary_dark to accent1_dark during fade out
        start_r, start_g, start_b = (
            int(COLORS["primary_dark"][1:3], 16),
            int(COLORS["primary_dark"][3:5], 16),
            int(COLORS["primary_dark"][5:7], 16)
        )
        end_r, end_g, end_b = (
            int(COLORS["accent1_dark"][1:3], 16),
            int(COLORS["accent1_dark"][3:5], 16),
            int(COLORS["accent1_dark"][5:7], 16)
        )
        
        progress = 1 - alpha/100
        r = int(start_r + (end_r - start_r) * progress)
        g = int(start_g + (end_g - start_g) * progress)
        b = int(start_b + (end_b - start_b) * progress)
        
        return f'#{r:02x}{g:02x}{b:02x}'

class ModernMainMenu:
    def __init__(self, root, system):
        self.root = root
        self.system = system
        self.setup_main_window()
    
    def setup_main_window(self):
        self.root.title("University Registration System")
        
        # Set window size to 70% of screen dimensions
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        self.window_width = int(screen_width * 0.7)
        self.window_height = int(screen_height * 0.7)
        self.root.geometry(f"{self.window_width}x{self.window_height}")
        
        # Center the window
        self.center_window()
        
        # Configure window properties
        self.root.configure(bg=COLORS["background"])
        self.root.minsize(800, 600)
        
        # Create widgets
        self.create_widgets()
        
        # Configure window to be responsive
        self.make_responsive()
    
    def center_window(self):
        self.root.update_idletasks()
        x = (self.root.winfo_screenwidth() // 2) - (self.window_width // 2)
        y = (self.root.winfo_screenheight() // 2) - (self.window_height // 2)
        self.root.geometry(f'+{x}+{y}')
    
    def create_widgets(self):
        # Main container with padding
        self.main_frame = tk.Frame(self.root, bg=COLORS["background"], padx=40, pady=40)
        self.main_frame.pack(expand=True, fill="both")
        
        # Header section
        self.create_header()
        
        # Button grid - centered with consistent spacing
        self.create_button_grid()
        
        # Footer section
        self.create_footer()
    
    def create_header(self):
        header_frame = tk.Frame(self.main_frame, bg=COLORS["primary"], padx=20, pady=15)
        header_frame.pack(fill="x", pady=(0, 30))
        
        # Title with modern font
        title_label = tk.Label(
            header_frame, 
            text="University Registration System", 
            font=("Segoe UI", 24, "bold"), 
            fg="white", 
            bg=COLORS["primary"]
        )
        title_label.pack()
        
        # Subtitle with accent color
        subtitle_label = tk.Label(
            header_frame, 
            text="Manage student records and course enrollments", 
            font=("Segoe UI", 12), 
            fg=COLORS["secondary_light"], 
            bg=COLORS["primary"]
        )
        subtitle_label.pack(pady=(5, 0))
    
    def create_button_grid(self):
        # Container for buttons with centered content
        button_container = tk.Frame(self.main_frame, bg=COLORS["background"])
        button_container.pack(expand=True, fill="both")
        
        # Configure grid for responsive layout
        button_container.grid_rowconfigure(0, weight=1)
        button_container.grid_columnconfigure(0, weight=1)
        
        # Inner frame for buttons
        button_frame = tk.Frame(button_container, bg=COLORS["background"])
        button_frame.grid(row=0, column=0)
        
        # Button definitions with icons and colors
        buttons = [
            ("📝 Register Student", self.show_register_student, COLORS["primary"]),
            ("🗑️ Remove Student", self.show_remove_student, COLORS["error"]),
            ("👥 Students List", self.show_students_list, COLORS["accent1"]),
            ("🌳 BST View", self.show_students_bst, COLORS["accent1_dark"]),
            ("📚 Enroll Courses", self.show_enroll_courses, COLORS["primary_light"]),
            ("📖 View Courses", self.show_student_courses, COLORS["accent2"]),
            ("🔍 Search Student", self.show_search_student, COLORS["info"]),
            ("🚪 Exit", self.root.quit, COLORS["error"])
        ]
        
        # Create buttons in a 2-column grid
        for i, (text, command, color) in enumerate(buttons):
            btn = tk.Button(
                button_frame, 
                text=text,
                font=("Segoe UI", 12, "bold"),
                bg=color,
                fg="white",
                activebackground=self.lighten_color(color, 0.2),
                activeforeground="white",
                relief="flat",
                borderwidth=0,
                padx=25,
                pady=15,
                command=command
            )
            
            # Calculate row and column
            row = i // 2
            col = i % 2
            
            btn.grid(row=row, column=col, padx=15, pady=15, sticky="nsew")
            
            # Bind hover effects
            btn.bind("<Enter>", lambda e, b=btn: b.config(bg=self.lighten_color(b.cget("bg"), 0.1)))
            btn.bind("<Leave>", lambda e, b=btn, c=color: b.config(bg=c))
            
            # Configure row weights
            button_frame.grid_rowconfigure(row, weight=1)
        
        # Make buttons expand equally
        for col in range(2):
            button_frame.grid_columnconfigure(col, weight=1)
    
    def create_footer(self):
        footer_frame = tk.Frame(self.main_frame, bg=COLORS["primary"], padx=10, pady=8)
        footer_frame.pack(fill="x", side="bottom", pady=(20, 0))
        
        # Status message
        status_label = tk.Label(
            footer_frame, 
            text="Ready", 
            font=("Segoe UI", 9),
            fg="white", 
            bg=COLORS["primary"]
        )
        status_label.pack(side="left")
        
        # Copyright information
        copyright_label = tk.Label(
            footer_frame, 
            text="© 2025 University Registration System", 
            font=("Segoe UI", 9),
            fg="white", 
            bg=COLORS["primary"]
        )
        copyright_label.pack(side="right")
    
    def lighten_color(self, color, amount=0.2):
        """Lighten a hex color by the specified amount"""
        try:
            c = int(color[1:], 16)
            r = min(255, (c >> 16) + int(255 * amount))
            g = min(255, ((c >> 8) & 0xFF) + int(255 * amount))
            b = min(255, (c & 0xFF) + int(255 * amount))
            return f"#{r:02x}{g:02x}{b:02x}"
        except:
            return color
    
    def make_responsive(self):
        # Make the layout responsive to window resizing
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(0, weight=1)
        
        # Bind resize event to adjust UI elements
        self.root.bind("<Configure>", self.on_window_resize)
    
    def on_window_resize(self, event):
        # Adjust font sizes based on window dimensions
        base_font_size = max(10, int(min(self.root.winfo_width(), self.root.winfo_height()) / 60))
        
        # Update button fonts
        for child in self.main_frame.winfo_children():
            if isinstance(child, tk.Button):
                child.config(font=("Segoe UI", base_font_size, "bold"))
  
    def show_register_student(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Register Student")
        dialog.geometry("500x450")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 11), "bg": COLORS["background"], "fg": COLORS["text_primary"]}
        entry_style = {"font": ("Segoe UI", 11), "bg": "white", "highlightthickness": 1, 
                      "highlightbackground": COLORS["primary_light"], "highlightcolor": COLORS["primary"]}
        
        # Name field
        tk.Label(dialog, text="Full Name:", **label_style).grid(row=0, column=0, padx=10, pady=10, sticky="w")
        name_entry = tk.Entry(dialog, **entry_style)
        name_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")
        
        # GPA field
        tk.Label(dialog, text="GPA (0.00-4.00):", **label_style).grid(row=1, column=0, padx=10, pady=10, sticky="w")
        gpa_entry = tk.Entry(dialog, **entry_style)
        gpa_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        # Department selection
        tk.Label(dialog, text="Department:", **label_style).grid(row=2, column=0, padx=10, pady=10, sticky="w")
        dept_frame = tk.Frame(dialog, bg=COLORS["background"])
        dept_frame.grid(row=2, column=1, padx=10, pady=5, sticky="w")
        
        dept_var = tk.IntVar(value=1)
        tk.Radiobutton(dept_frame, text="Computer Science", variable=dept_var, value=1, 
                      font=("Segoe UI", 10), bg=COLORS["background"], 
                      activebackground=COLORS["background"]).pack(anchor="w")
        tk.Radiobutton(dept_frame, text="Software Engineering", variable=dept_var, value=2, 
                      font=("Segoe UI", 10), bg=COLORS["background"],
                      activebackground=COLORS["background"]).pack(anchor="w")
        
        # Position selection
        tk.Label(dialog, text="Insert Position:", **label_style).grid(row=3, column=0, padx=10, pady=10, sticky="w")
        pos_frame = tk.Frame(dialog, bg=COLORS["background"])
        pos_frame.grid(row=3, column=1, padx=10, pady=5, sticky="w")
        
        pos_var = tk.IntVar(value=0)
        tk.Radiobutton(pos_frame, text="At Front", variable=pos_var, value=0, 
                      font=("Segoe UI", 10), bg=COLORS["background"],
                      activebackground=COLORS["background"]).pack(anchor="w")
        
        pos_radio = tk.Radiobutton(pos_frame, text="At Position:", variable=pos_var, value=1, 
                                 font=("Segoe UI", 10), bg=COLORS["background"],
                                 activebackground=COLORS["background"])
        pos_radio.pack(side="left", anchor="w")
        
        pos_entry = tk.Entry(pos_frame, width=5, font=("Segoe UI", 10), 
                            highlightthickness=1, highlightbackground=COLORS["primary_light"])
        pos_entry.pack(side="left", padx=5)
        
        # Action buttons
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.grid(row=4, column=0, columnspan=2, pady=20)
        
        def register():
            name = name_entry.get()
            gpa = gpa_entry.get()
            department = dept_var.get()
            position = pos_var.get()
            pos = pos_entry.get() if position == 1 else 0
            
            try:
                pos = int(pos) if pos else 0
            except ValueError:
                messagebox.showerror("Error", "Position must be a number")
                return
            
            success, message = self.system.register_student(name, gpa, department, pos)
            if success:
                messagebox.showinfo("Success", message)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message)
        
        # Primary action button
        tk.Button(
            button_frame, 
            text="Register", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=register
        ).pack(side="left", padx=10)
        
        # Secondary action button
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["text_secondary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["text_secondary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        # Make dialog content expand properly
        dialog.grid_columnconfigure(1, weight=1)
        dialog.resizable(False, False)
        self.center_dialog(dialog)

    def center_dialog(self, dialog):
        dialog.update_idletasks()
        width = dialog.winfo_width()
        height = dialog.winfo_height()
        x = (self.root.winfo_screenwidth() // 2) - (width // 2)
        y = (self.root.winfo_screenheight() // 2) - (height // 2)
        dialog.geometry(f'+{x}+{y}')
    
    def show_remove_student(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Remove Student")
        dialog.geometry("400x200")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 12), "bg": COLORS["background"], "fg": COLORS["text_primary"]}
        entry_style = {"font": ("Segoe UI", 12), "bg": "white", "highlightthickness": 1, 
                      "highlightbackground": COLORS["primary_light"], "highlightcolor": COLORS["primary"]}
        
        tk.Label(dialog, text="Enter Student ID to remove:", **label_style).pack(pady=20)
        
        id_entry = tk.Entry(dialog, **entry_style)
        id_entry.pack(pady=10, padx=20, fill="x")
        
        def remove():
            student_id = id_entry.get()
            if student_id:
                success, message = self.system.remove_student(student_id)
                if success:
                    messagebox.showinfo("Success", message, parent=dialog)
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message, parent=dialog)
        
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, 
            text="Remove", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["error"],
            fg="white",
            activebackground=self.lighten_color(COLORS["error"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=remove
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["text_secondary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["text_secondary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        self.center_dialog(dialog)

    def show_students_list(self):
        students = self.system.get_students_list()
        self.show_info_window("Students List", students, icon="👥")

    def show_students_bst(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("BST Traversal Options")
        dialog.geometry("500x300")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 14, "bold"), "bg": COLORS["background"], "fg": COLORS["primary_dark"]}
        radio_style = {"font": ("Segoe UI", 12), "bg": COLORS["background"], "activebackground": COLORS["background"]}
        
        tk.Label(dialog, text="Select Traversal Type:", **label_style).pack(pady=15)
        
        traversal_var = tk.IntVar(value=1)
        
        options_frame = tk.Frame(dialog, bg=COLORS["background"])
        options_frame.pack(pady=10)
        
        tk.Radiobutton(
            options_frame, 
            text="In-order (Sorted by ID)", 
            variable=traversal_var, 
            value=1,
            **radio_style
        ).pack(anchor="w", padx=50, pady=5)
        
        tk.Radiobutton(
            options_frame, 
            text="Pre-order", 
            variable=traversal_var, 
            value=2,
            **radio_style
        ).pack(anchor="w", padx=50, pady=5)
        
        tk.Radiobutton(
            options_frame, 
            text="Post-order", 
            variable=traversal_var, 
            value=3,
            **radio_style
        ).pack(anchor="w", padx=50, pady=5)
        
        def show_traversal():
            students = self.system.get_students_bst(traversal_var.get())
            traversal_type = ["In-order", "Pre-order", "Post-order"][traversal_var.get()-1]
            title = f"Students (BST {traversal_type} Traversal)"
            self.show_info_window(title, students, icon="🌳")
            dialog.destroy()
        
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame, 
            text="Show", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=show_traversal
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["text_secondary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["text_secondary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        self.center_dialog(dialog)

    def show_enroll_courses(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Enroll in Courses")
        dialog.geometry("700x600")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 12), "bg": COLORS["background"], "fg": COLORS["text_primary"]}
        entry_style = {"font": ("Segoe UI", 12), "bg": "white", "highlightthickness": 1, 
                      "highlightbackground": COLORS["primary_light"], "highlightcolor": COLORS["primary"]}
        
        # Student ID
        id_frame = tk.Frame(dialog, bg=COLORS["background"])
        id_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(id_frame, text="Student ID:", **label_style).pack(side="left")
        
        id_entry = tk.Entry(id_frame, **entry_style)
        id_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Semester
        semester_frame = tk.Frame(dialog, bg=COLORS["background"])
        semester_frame.pack(fill="x", padx=20, pady=10)
        
        tk.Label(semester_frame, text="Semester (1-6):", **label_style).pack(side="left")
        
        semester_entry = tk.Entry(semester_frame, **entry_style)
        semester_entry.pack(side="left", padx=10, fill="x", expand=True)
        
        # Available Courses
        tk.Label(dialog, text="Available Courses:", **label_style).pack(pady=(10, 5), padx=20, anchor="w")
        
        courses_text = scrolledtext.ScrolledText(
            dialog, 
            width=60, 
            height=10, 
            font=("Segoe UI", 11),
            bg="white",
            highlightthickness=1,
            highlightbackground=COLORS["primary_light"],
            highlightcolor=COLORS["primary"]
        )
        courses_text.pack(padx=20, pady=5, fill="both", expand=True)
        
        # Courses to Register
        tk.Label(dialog, text="Courses to Register (one per line):", **label_style).pack(pady=(10, 5), padx=20, anchor="w")
        
        register_text = scrolledtext.ScrolledText(
            dialog, 
            width=60, 
            height=5, 
            font=("Segoe UI", 11),
            bg="white",
            highlightthickness=1,
            highlightbackground=COLORS["primary_light"],
            highlightcolor=COLORS["primary"]
        )
        register_text.pack(padx=20, pady=5, fill="both", expand=True)
        
        def load_courses():
            try:
                semester = int(semester_entry.get())
                if semester not in self.system.semester_courses:
                    messagebox.showerror("Error", "Invalid semester selection.", parent=dialog)
                    return
                
                courses_text.delete(1.0, tk.END)
                for course in self.system.semester_courses[semester]:
                    courses_text.insert(tk.END, f"• {course[0]} ({course[1]} credits)\n")
            except ValueError:
                messagebox.showerror("Error", "Semester must be a number between 1 and 6", parent=dialog)
        
        def enroll():
            student_id = id_entry.get()
            semester = semester_entry.get()
            courses = register_text.get(1.0, tk.END).strip().split("\n")
            courses = [course.strip() for course in courses if course.strip()]
            
            success, message = self.system.enroll_in_courses(student_id, semester, courses)
            if success:
                messagebox.showinfo("Success", message, parent=dialog)
                dialog.destroy()
            else:
                messagebox.showerror("Error", message, parent=dialog)
        
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.pack(pady=15)
        
        tk.Button(
            button_frame, 
            text="Load Courses", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary_light"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary_light"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            command=load_courses
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, 
            text="Enroll", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["success"],
            fg="white",
            activebackground=self.lighten_color(COLORS["success"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            command=enroll
        ).pack(side="left", padx=5)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["error"],
            fg="white",
            activebackground=self.lighten_color(COLORS["error"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=15,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=5)
        
        self.center_dialog(dialog)

    def show_student_courses(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("View Student Courses")
        dialog.geometry("500x200")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 12), "bg": COLORS["background"], "fg": COLORS["text_primary"]}
        entry_style = {"font": ("Segoe UI", 12), "bg": "white", "highlightthickness": 1, 
                      "highlightbackground": COLORS["primary_light"], "highlightcolor": COLORS["primary"]}
        
        tk.Label(dialog, text="Enter Student ID to view courses:", **label_style).pack(pady=20)
        
        id_entry = tk.Entry(dialog, **entry_style)
        id_entry.pack(pady=10, padx=20, fill="x")
        
        def view_courses():
            student_id = id_entry.get()
            if student_id:
                success, message, courses = self.system.get_student_courses(student_id)
                if success:
                    if courses:
                        message += "\n\n" + "\n".join(f"• {course}" for course in courses)
                    self.show_info_window("Student Courses", [message], icon="📚")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message, parent=dialog)
        
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, 
            text="View", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=view_courses
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["text_secondary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["text_secondary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        self.center_dialog(dialog)

    def show_search_student(self):
        dialog = tk.Toplevel(self.root)
        dialog.title("Search Student")
        dialog.geometry("500x200")
        dialog.configure(bg=COLORS["background"])
        
        # Modern styling
        label_style = {"font": ("Segoe UI", 12), "bg": COLORS["background"], "fg": COLORS["text_primary"]}
        entry_style = {"font": ("Segoe UI", 12), "bg": "white", "highlightthickness": 1, 
                      "highlightbackground": COLORS["primary_light"], "highlightcolor": COLORS["primary"]}
        
        tk.Label(dialog, text="Enter Student ID to search:", **label_style).pack(pady=20)
        
        id_entry = tk.Entry(dialog, **entry_style)
        id_entry.pack(pady=10, padx=20, fill="x")
        
        def search():
            student_id = id_entry.get()
            if student_id:
                success, message, student_info, courses = self.system.search_student(student_id)
                if success:
                    info = [
                        f"ID: {student_info['ID']}",
                        f"Name: {student_info['Name']}",
                        f"Department: {student_info['Department']}",
                        f"GPA: {student_info['GPA']}"
                    ]
                    if courses:
                        info.append("\nRegistered Courses:")
                        info.extend(f"• {course}" for course in courses)
                    self.show_info_window("Student Information", info, icon="🔍")
                    dialog.destroy()
                else:
                    messagebox.showerror("Error", message, parent=dialog)
        
        button_frame = tk.Frame(dialog, bg=COLORS["background"])
        button_frame.pack(pady=10)
        
        tk.Button(
            button_frame, 
            text="Search", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=search
        ).pack(side="left", padx=10)
        
        tk.Button(
            button_frame, 
            text="Cancel", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["text_secondary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["text_secondary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=20,
            pady=5,
            command=dialog.destroy
        ).pack(side="left", padx=10)
        
        self.center_dialog(dialog)

    def show_info_window(self, title, content, icon=None):
        dialog = tk.Toplevel(self.root)
        dialog.title(title)
        dialog.geometry("800x600")
        dialog.configure(bg=COLORS["background"])
        
        # Header with optional icon
        header_frame = tk.Frame(dialog, bg=COLORS["primary"])
        header_frame.pack(fill="x", pady=(0, 10))
        
        if icon:
            tk.Label(
                header_frame, 
                text=icon, 
                font=("Segoe UI", 24), 
                bg=COLORS["primary"], 
                fg="white"
            ).pack(side="left", padx=15)
        
        tk.Label(
            header_frame, 
            text=title, 
            font=("Segoe UI", 16, "bold"), 
            bg=COLORS["primary"], 
            fg="white"
        ).pack(side="left", pady=10)
        
        # Content area
        text = scrolledtext.ScrolledText(
            dialog, 
            width=90, 
            height=25, 
            font=("Segoe UI", 11),
            bg="white",
            highlightthickness=1,
            highlightbackground=COLORS["primary_light"],
            highlightcolor=COLORS["primary"]
        )
        text.pack(padx=20, pady=(0, 20), fill="both", expand=True)
        
        if content:
            text.insert(tk.END, "\n".join(content))
        else:
            text.insert(tk.END, "No information to display.")
        
        text.config(state="disabled")
        
        # Close button
        tk.Button(
            dialog, 
            text="Close", 
            font=("Segoe UI", 11, "bold"),
            bg=COLORS["primary"],
            fg="white",
            activebackground=self.lighten_color(COLORS["primary"], 0.1),
            activeforeground="white",
            relief="flat",
            padx=25,
            pady=5,
            command=dialog.destroy
        ).pack(pady=(0, 20))
        
        self.center_dialog(dialog)

def main():
    root = tk.Tk()
    
    def start_main_app():
        system = RegistrationSystem()
        ModernMainMenu(root, system)
    
    # Start with animated splash screen
    splash = AnimatedSplashScreen(root, start_main_app)
    
    root.mainloop()

if __name__ == "__main__":
    main()