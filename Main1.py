import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
import hashlib
import re

from Admin import Admin
from Student import StudentUser

from validator import (
    validate_email as validator_validate_email,
    validate_password as validator_validate_password,
    get_email_requirements,
    get_password_requirements
)
from two_factor import TwoFactorAuth

class StudentRecord:
    def __init__(self, student_id, first_name, last_name, age, gender, phone):
        self.student_id = student_id
        self.first_name = first_name
        self.last_name = last_name
        self.age = age
        self.gender = gender
        self.phone = phone

    def to_dict(self):
        return {
            "student_id": self.student_id,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "age": self.age,
            "gender": self.gender,
            "phone": self.phone
        }

class StudentManagementApp(tk.Tk):
    DATA_FILE = "data.json"

    def __init__(self):
        tk.Tk.__init__(self)
        self.title("Secure Student Management System")
        self.state("zoomed")

        self.users = {}
        self.students = {}
        self.current_user = None

        self.two_factor = TwoFactorAuth()

        self.load_data()

        container = ttk.Frame(self)
        container.pack(fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}
        self.frames["WelcomePage"] = WelcomePage(container, self)
        self.frames["RegisterPage"] = RegisterPage(container, self)
        self.frames["LoginPage"] = LoginPage(container, self)
        self.frames["AdminDashboard"] = AdminDashboard(container, self)
        self.frames["StudentDashboard"] = StudentDashboard(container, self)

        for frame in self.frames.values():
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame("WelcomePage")

    def hash_password(self, password):
        return hashlib.sha256(password.encode("utf-8")).hexdigest()

    def show_frame(self, page_name):
        frame = self.frames[page_name]
        if page_name == "AdminDashboard" and self.current_user:
            frame.refresh_students()
        elif page_name == "StudentDashboard" and self.current_user:
            frame.refresh_student_info()
        frame.tkraise()

    def add_starting_data(self):
        admin_user = Admin("admin@gmail.com", self.hash_password("admin123"))
        self.users["admin@gmail.com"] = admin_user

        student_user = StudentUser("student@gmail.com", self.hash_password("student123"), "700001234")
        self.users["student@gmail.com"] = student_user

        sample_student = StudentRecord("700001234", "John", "Doe", 20, "MALE", "012-345-6789")
        self.students["700001234"] = sample_student

    def load_data(self):
        if not os.path.exists(self.DATA_FILE):
            self.users = {}
            self.students = {}
            self.add_starting_data()
            self.save_data()
            return

        try:
            with open(self.DATA_FILE, "r", encoding="utf-8") as file:
                content = file.read().strip()

                if not content:
                    raise ValueError("Empty JSON file.")

                data = json.loads(content)

            self.users = {}
            self.students = {}

            for student_id, student_data in data.get("students", {}).items():
                self.students[student_id] = StudentRecord(
                    student_data["student_id"],
                    student_data["first_name"],
                    student_data["last_name"],
                    student_data["age"],
                    student_data["gender"],
                    student_data["phone"]
                )

            for email, user_data in data.get("users", {}).items():
                role = user_data.get("role")
                password_hash = user_data.get("password_hash")

                if role == "Admin":
                    self.users[email] = Admin(email, password_hash)

                elif role == "Student":
                    student_id = user_data.get("student_id")
                    if student_id in self.students:
                        self.users[email] = StudentUser(email, password_hash, student_id)

        except (json.JSONDecodeError, KeyError, TypeError, ValueError):
            messagebox.showwarning(
                "Data Warning",
                "data.json is missing, empty, or corrupted. Default data will be restored."
            )
            self.users = {}
            self.students = {}
            self.add_starting_data()
            self.save_data()

    def save_data(self):
        data = {
            "users": {},
            "students": {}
        }

        for email, user in self.users.items():
            if user.get_role() == "Admin":
                data["users"][email] = {
                    "role": "Admin",
                    "password_hash": user.password_hash
                }
            elif user.get_role() == "Student":
                data["users"][email] = {
                    "role": "Student",
                    "password_hash": user.password_hash,
                    "student_id": user.student_id
                }

        for student_id, student in self.students.items():
            data["students"][student_id] = student.to_dict()

        with open(self.DATA_FILE, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def validate_student_id(self, student_id):
        if not student_id:
            return False, "Student ID is required."
        if not student_id.isdigit():
            return False, "Student ID must contain numbers only."
        if not student_id.startswith("700"):
            return False, "Student ID must start with 700."
        if len(student_id) != 9:
            return False, "Student ID must be exactly 9 digits long."
        return True, ""

    def validate_age(self, age_text):
        try:
            age = int(age_text)
            if 16 <= age <= 100:
                return True, "", age
            return False, "Age must be between 16 and 100.", None
        except ValueError:
            return False, "Age must be a number.", None

    def validate_phone(self, phone):
        if re.fullmatch(r"\d{3}-\d{3}-\d{4}", phone):
            return True, ""
        return False, "Phone number must be in format xxx-xxx-xxxx."

    def validate_gender(self, gender):
        if gender not in ["MALE", "FEMALE", "Not Set"]:
            return False, "Please select a valid gender."
        return True, ""

    def validate_email(self, email):
        if validator_validate_email(email):
            return True, ""
        return False, get_email_requirements()

    def validate_password(self, password):
        if validator_validate_password(password):
            return True, ""
        return False, get_password_requirements()


class WelcomePage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(main_frame, text="Secure Student Management System", font=("Arial", 22, "bold")).pack(pady=40)
        ttk.Label(main_frame, text="Welcome! Please choose an option below.", font=("Arial", 12)).pack(pady=10)

        ttk.Button(main_frame, text="Register", command=self.go_register).pack(pady=10)
        ttk.Button(main_frame, text="Login", command=self.go_login).pack(pady=10)
        ttk.Button(main_frame, text="Exit", command=self.exit_app).pack(pady=10)

    def go_register(self):
        self.controller.show_frame("RegisterPage")

    def go_login(self):
        self.controller.show_frame("LoginPage")

    def exit_app(self):
        self.controller.destroy()


class RegisterPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(main_frame, text="Register User", font=("Arial", 18, "bold")).pack(pady=20)

        form = ttk.Frame(main_frame)
        form.pack(pady=20)

        ttk.Label(form, text="Email:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(form, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(form, text="Role:").grid(row=2, column=0, padx=10, pady=10, sticky="e")
        self.role_combo = ttk.Combobox(form, values=["Admin", "Student"], state="readonly", width=27)
        self.role_combo.grid(row=2, column=1, padx=10, pady=10)
        self.role_combo.current(1)
        self.role_combo.bind("<<ComboboxSelected>>", self.toggle_student_id)

        ttk.Label(form, text="Student ID:").grid(row=3, column=0, padx=10, pady=10, sticky="e")
        self.student_id_entry = ttk.Entry(form, width=30)
        self.student_id_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(form, text="Age:").grid(row=4, column=0, padx=10, pady=10, sticky="e")
        self.age_entry = ttk.Entry(form, width=30)
        self.age_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(form, text="Gender:").grid(row=5, column=0, padx=10, pady=10, sticky="e")
        self.gender_combo = ttk.Combobox(form, values=["MALE", "FEMALE", "Not Set"], state="readonly", width=27)
        self.gender_combo.grid(row=5, column=1, padx=10, pady=10)
        self.gender_combo.current(2)

        ttk.Label(form, text="Phone Number:").grid(row=6, column=0, padx=10, pady=10, sticky="e")
        self.phone_entry = ttk.Entry(form, width=30)
        self.phone_entry.grid(row=6, column=1, padx=10, pady=10)

        ttk.Button(main_frame, text="Create Account", command=self.register_user).pack(pady=10)
        ttk.Button(main_frame, text="Back", command=self.go_back).pack()

        self.toggle_student_id()

    def toggle_student_id(self, event=None):
        if self.role_combo.get() == "Admin":
            self.student_id_entry.delete(0, tk.END)
            self.student_id_entry.config(state="disabled")
        else:
            self.student_id_entry.config(state="normal")

    def go_back(self):
        self.controller.show_frame("WelcomePage")

    def register_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()
        role = self.role_combo.get()
        student_id = self.student_id_entry.get().strip()
        age_text = self.age_entry.get().strip()
        gender = self.gender_combo.get().strip()
        phone = self.phone_entry.get().strip()

        if not email or not password or not role:
            messagebox.showerror("Error", "Fill all required fields.")
            return

        valid, message = self.controller.validate_email(email)
        if not valid:
            messagebox.showerror("Error", message)
            return

        valid, message = self.controller.validate_password(password)
        if not valid:
            messagebox.showerror("Error", message)
            return

        if email in self.controller.users:
            messagebox.showerror("Error", "Email already exists.")
            return

        password_hash = self.controller.hash_password(password)

        if role == "Admin":
            new_user = Admin(email, password_hash)
        else:
            valid, message = self.controller.validate_student_id(student_id)
            if not valid:
                messagebox.showerror("Error", message)
                return

            if student_id in self.controller.students:
                messagebox.showerror("Error", "Student ID already exists.")
                return

            valid, message, age = self.controller.validate_age(age_text)
            if not valid:
                messagebox.showerror("Error", message)
                return

            valid, message = self.controller.validate_gender(gender)
            if not valid:
                messagebox.showerror("Error", message)
                return

            valid, message = self.controller.validate_phone(phone)
            if not valid:
                messagebox.showerror("Error", message)
                return

            new_user = StudentUser(email, password_hash, student_id)
            self.controller.students[student_id] = StudentRecord(
                student_id, "New", "Student", age, gender, phone
            )

        self.controller.users[email] = new_user
        self.controller.save_data()

        messagebox.showinfo("Success", "Account created.")
        self.email_entry.delete(0, tk.END)
        self.password_entry.delete(0, tk.END)
        self.student_id_entry.config(state="normal")
        self.student_id_entry.delete(0, tk.END)
        self.age_entry.delete(0, tk.END)
        self.gender_combo.current(2)
        self.phone_entry.delete(0, tk.END)
        self.role_combo.current(1)
        self.toggle_student_id()

        self.controller.show_frame("LoginPage")


class LoginPage(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller
        self.attempts = 0
        self.max_attempts = 3

        self.pending_user = None
        self.pending_email = None

        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(main_frame, text="Login", font=("Arial", 18, "bold")).pack(pady=20)

        form = ttk.Frame(main_frame)
        form.pack(pady=20)

        ttk.Label(form, text="Email:").grid(row=0, column=0, padx=10, pady=10, sticky="e")
        self.email_entry = ttk.Entry(form, width=30)
        self.email_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(form, text="Password:").grid(row=1, column=0, padx=10, pady=10, sticky="e")
        self.password_entry = ttk.Entry(form, width=30, show="*")
        self.password_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Button(main_frame, text="Login", command=self.login_user).pack(pady=10)
        ttk.Button(main_frame, text="Back", command=self.go_back).pack()

        ttk.Separator(main_frame, orient="horizontal").pack(fill="x", pady=15)

        ttk.Label(main_frame, text="2FA Code:", font=("Arial", 11, "bold")).pack(pady=(10, 5))
        self.two_factor_entry = ttk.Entry(main_frame, width=30, state="disabled")
        self.two_factor_entry.pack(pady=5)

        self.verify_2fa_button = ttk.Button(
            main_frame,
            text="Verify 2FA Code",
            command=self.verify_two_factor,
            state="disabled"
        )
        self.verify_2fa_button.pack(pady=10)

    def go_back(self):
        self.clear_two_factor_fields()
        self.controller.show_frame("WelcomePage")

    def login_user(self):
        email = self.email_entry.get().strip()
        password = self.password_entry.get().strip()

        if email not in self.controller.users:
            self.failed_login("User not found.")
            return

        user = self.controller.users[email]
        password_hash = self.controller.hash_password(password)

        if user.login(email, password_hash):
            if user.get_role() == "Student" and user.student_id not in self.controller.students:
                self.failed_login("Student record not found.")
                return

            self.pending_user = user
            self.pending_email = email

            code = self.controller.two_factor.generate_code(email)

            self.two_factor_entry.config(state="normal")
            self.verify_2fa_button.config(state="normal")
            self.two_factor_entry.delete(0, tk.END)

            messagebox.showinfo(
                "Two-Factor Authentication",
                f"Your 6-digit verification code is: {code}\n\nEnter this code to finish logging in."
            )
            return

            self.controller.current_user = user
            self.attempts = 0
            messagebox.showinfo("Success", "Login successful.")

            if user.get_role() == "Admin":
                self.controller.show_frame("AdminDashboard")
            else:
                self.controller.show_frame("StudentDashboard")
        else:
            self.failed_login("Invalid credentials.")

    def verify_two_factor(self):
        code = self.two_factor_entry.get().strip()

        if not self.pending_user or not self.pending_email:
            messagebox.showerror("Error", "Please log in with email and password first.")
            return

        if not code:
            messagebox.showerror("Error", "Enter the 2FA code.")
            return

        if self.controller.two_factor.verify_code(self.pending_email, code):
            user = self.pending_user
            self.controller.current_user = user
            self.attempts = 0

            self.email_entry.delete(0, tk.END)
            self.password_entry.delete(0, tk.END)
            self.clear_two_factor_fields()

            messagebox.showinfo("Success", "Login successful.")

            if user.get_role() == "Admin":
                self.controller.show_frame("AdminDashboard")
            else:
                self.controller.show_frame("StudentDashboard")
        else:
            messagebox.showerror("Error", "Invalid or expired 2FA code.")

    def clear_two_factor_fields(self):
        self.pending_user = None
        self.pending_email = None

        self.two_factor_entry.config(state="normal")
        self.two_factor_entry.delete(0, tk.END)
        self.two_factor_entry.config(state="disabled")

        self.verify_2fa_button.config(state="disabled")

    def failed_login(self, message):
        self.attempts += 1
        if self.max_attempts - self.attempts > 0:
            messagebox.showerror("Login Failed", message + f"\nAttempts left: {self.max_attempts - self.attempts}")
        else:
            messagebox.showerror("Login Failed", "Too many attempts.")
            self.attempts = 0
            self.controller.show_frame("WelcomePage")


class AdminDashboard(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        ttk.Label(self, text="Admin Dashboard", font=("Arial", 18, "bold")).pack(pady=20)

        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Student", command=self.add_student).grid(row=0, column=0, padx=10, pady=10)
        ttk.Button(button_frame, text="Delete Student", command=self.delete_student).grid(row=0, column=1, padx=10, pady=10)
        ttk.Button(button_frame, text="Refresh Students", command=self.refresh_students).grid(row=0, column=2, padx=10, pady=10)
        ttk.Button(button_frame, text="Logout", command=self.logout).grid(row=0, column=3, padx=10, pady=10)

        columns = ("ID", "First Name", "Last Name", "Age", "Gender", "Phone")
        self.tree = ttk.Treeview(self, columns=columns, show="headings", height=15)
        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=130)
        self.tree.pack(pady=20)

    def refresh_students(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        students = self.controller.current_user.view_all_students(self.controller.students)
        for student in students.values():
            self.tree.insert("", tk.END, values=(
                student.student_id, student.first_name, student.last_name,
                student.age, student.gender, student.phone
            ))

    def add_student(self):
        popup = tk.Toplevel(self)
        popup.title("Add Student")
        popup.geometry("350x300")

        ttk.Label(popup, text="Student ID:").grid(row=0, column=0, padx=10, pady=10)
        sid_entry = ttk.Entry(popup, width=20)
        sid_entry.grid(row=0, column=1, padx=10, pady=10)

        ttk.Label(popup, text="First Name:").grid(row=1, column=0, padx=10, pady=10)
        fname_entry = ttk.Entry(popup, width=20)
        fname_entry.grid(row=1, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Last Name:").grid(row=2, column=0, padx=10, pady=10)
        lname_entry = ttk.Entry(popup, width=20)
        lname_entry.grid(row=2, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Age:").grid(row=3, column=0, padx=10, pady=10)
        age_entry = ttk.Entry(popup, width=20)
        age_entry.grid(row=3, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Gender:").grid(row=4, column=0, padx=10, pady=10)
        gender_entry = ttk.Entry(popup, width=20)
        gender_entry.grid(row=4, column=1, padx=10, pady=10)

        ttk.Label(popup, text="Phone:").grid(row=5, column=0, padx=10, pady=10)
        phone_entry = ttk.Entry(popup, width=20)
        phone_entry.grid(row=5, column=1, padx=10, pady=10)

        def save():
            sid = sid_entry.get().strip()
            valid, message = self.controller.validate_student_id(sid)
            if not valid:
                messagebox.showerror("Error", message)
                return

            if sid in self.controller.students:
                messagebox.showerror("Error", "Student ID already exists.")
                return

            valid, message, age = self.controller.validate_age(age_entry.get().strip())
            if not valid:
                messagebox.showerror("Error", message)
                return

            gender = gender_entry.get().strip()
            valid, message = self.controller.validate_gender(gender)
            if not valid:
                messagebox.showerror("Error", message)
                return

            phone = phone_entry.get().strip()
            valid, message = self.controller.validate_phone(phone)
            if not valid:
                messagebox.showerror("Error", message)
                return

            student = StudentRecord(
                sid,
                fname_entry.get().strip(),
                lname_entry.get().strip(),
                age,
                gender,
                phone
            )
            self.controller.current_user.add_student(self.controller.students, student)
            self.controller.save_data()
            messagebox.showinfo("Success", "Student added.")
            popup.destroy()
            self.refresh_students()

        ttk.Button(popup, text="Save", command=save).grid(row=6, column=0, columnspan=2, pady=20)

    def delete_student(self):
        selection = self.tree.selection()
        if not selection:
            messagebox.showerror("Error", "Select a student first.")
            return

        student_id = self.tree.item(selection, "values")[0]

        if messagebox.askyesno("Delete", f"Delete student {student_id}?"):
            try:
                self.controller.current_user.delete_student(self.controller.students, student_id)

                users_to_remove = []
                for email, user in self.controller.users.items():
                    if user.get_role() == "Student" and user.student_id == student_id:
                        users_to_remove.append(email)

                for email in users_to_remove:
                    del self.controller.users[email]

                self.controller.save_data()
                messagebox.showinfo("Success", "Student deleted.")
                self.refresh_students()

            except ValueError as e:
                messagebox.showerror("Error", str(e))

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("WelcomePage")


class StudentDashboard(ttk.Frame):
    def __init__(self, parent, controller):
        ttk.Frame.__init__(self, parent)
        self.controller = controller

        main_frame = ttk.Frame(self)
        main_frame.place(relx=0.5, rely=0.5, anchor="center")

        ttk.Label(main_frame, text="Student Dashboard", font=("Arial", 18, "bold")).pack(pady=20)
        self.info_label = ttk.Label(main_frame, text="", font=("Arial", 12), justify="left")
        self.info_label.pack(pady=20)

        ttk.Button(main_frame, text="Refresh Record", command=self.refresh_student_info).pack(pady=10)
        ttk.Button(main_frame, text="Logout", command=self.logout).pack(pady=10)

    def refresh_student_info(self):
        try:
            student = self.controller.current_user.view_own_record(self.controller.students)
            info = (
                f"ID: {student.student_id}\n"
                f"Name: {student.first_name} {student.last_name}\n"
                f"Age: {student.age}\n"
                f"Gender: {student.gender}\n"
                f"Phone: {student.phone}"
            )
            self.info_label.config(text=info)
        except ValueError as e:
            self.info_label.config(text=str(e))

    def logout(self):
        self.controller.current_user = None
        self.controller.show_frame("WelcomePage")


if __name__ == "__main__":
    app = StudentManagementApp()
    app.mainloop()