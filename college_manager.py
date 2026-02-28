import csv
import os
import tkinter as tk
from tkinter import ttk, messagebox
import pandas as pd


class CollegeManager:
    def __init__(self, parent, college_file, program_file,student_file):
        self.student_file = student_file
        self.parent = parent
        self.college_file = college_file
        self.program_file = program_file

        self.menu_window()

    # ==========================
    # MAIN MENU
    # ==========================

    def menu_window(self):
        self.window = tk.Toplevel(self.parent)
        self.window.title("Manage Colleges & Programs")
        self.window.geometry("300x300")

        ttk.Label(self.window, text="Select Action", font=("Arial", 14, "bold")).pack(pady=15)

        ttk.Button(self.window, text="Add College", command=self.add_college_window).pack(pady=5)
        ttk.Button(self.window, text="Add Program", command=self.add_program_window).pack(pady=5)
        ttk.Button(self.window, text="Delete College", command=self.delete_college_window).pack(pady=5)
        ttk.Button(self.window, text="Delete Program", command=self.delete_program_window).pack(pady=5)
        ttk.Button(self.window, text="Close", command=self.window.destroy).pack(pady=15)


    # ==========================
    # DATA LOADERS
    # ==========================

    def load_colleges(self):
        colleges = {}
        if not os.path.exists(self.college_file):
            return colleges

        with open(self.college_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                colleges[row["College Code"]] = row["College Name"]
        return colleges


    def load_programs(self):
        programs = {}
        if not os.path.exists(self.program_file):
            return programs

        with open(self.program_file, newline="") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                programs[row["Program Code"]] = row
        return programs


    # ==========================
    # ADD COLLEGE WINDOW
    # ==========================

    def add_college_window(self):
        win = tk.Toplevel(self.window)
        win.title("Add College (With Program)")
        win.geometry("350x350")

        colleges = self.load_colleges()
        programs = self.load_programs()

        ttk.Label(win, text="College Code").pack()
        college_code_entry = ttk.Entry(win)
        college_code_entry.pack()

        ttk.Label(win, text="College Name").pack()
        college_name_entry = ttk.Entry(win)
        college_name_entry.pack()

        ttk.Label(win, text="--- Initial Program Required ---").pack(pady=5)

        ttk.Label(win, text="Program Code").pack()
        program_code_entry = ttk.Entry(win)
        program_code_entry.pack()

        ttk.Label(win, text="Program Name").pack()
        program_name_entry = ttk.Entry(win)
        program_name_entry.pack()

        def save():
            college_code = college_code_entry.get().strip().upper()
            college_name = college_name_entry.get().strip()
            program_code = program_code_entry.get().strip().upper()
            program_name = program_name_entry.get().strip()

            # Validate
            if not college_code or not college_name:
                messagebox.showerror("Error", "College code and name required.")
                return

            if not program_code or not program_name:
                messagebox.showerror("Error", "At least one program is required.")
                return

            if college_code in colleges:
                messagebox.showerror("Error", "College code already exists.")
                return

            if program_code in programs:
                messagebox.showerror("Error", "Program code already exists.")
                return

            # Write College
            college_exists = os.path.exists(self.college_file)
            with open(self.college_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["College Code", "College Name"])
                if not college_exists:
                    writer.writeheader()
                writer.writerow({
                    "College Code": college_code,
                    "College Name": college_name
                })

            # Write Program
            program_exists = os.path.exists(self.program_file)
            with open(self.program_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Program Code", "Program Name", "College Code"])
                if not program_exists:
                    writer.writeheader()
                writer.writerow({
                    "Program Code": program_code,
                    "Program Name": program_name,
                    "College Code": college_code
                })

            messagebox.showinfo("Success", "College and initial program added.")
            win.destroy()

        ttk.Button(win, text="Save", command=save).pack(pady=15)
    # ==========================
    # ADD PROGRAM WINDOW
    # ==========================

    def add_program_window(self):
        win = tk.Toplevel(self.window)
        win.title("Add Program")
        win.geometry("300x250")

        colleges = self.load_colleges()

        ttk.Label(win, text="Program Code").pack()
        code_entry = ttk.Entry(win)
        code_entry.pack()

        ttk.Label(win, text="Program Name").pack()
        name_entry = ttk.Entry(win)
        name_entry.pack()

        ttk.Label(win, text="College Code").pack()
        college_dropdown = ttk.Combobox(win, values=list(colleges.keys()), state="readonly")
        college_dropdown.pack()

        def save():
            code = code_entry.get().strip().upper()
            name = name_entry.get().strip()
            college_code = college_dropdown.get().strip()

            if not code or not name or not college_code:
                messagebox.showerror("Error", "All fields required.")
                return

            programs = self.load_programs()
            if code in programs:
                messagebox.showerror("Error", "Program code exists.")
                return

            file_exists = os.path.exists(self.program_file)
            with open(self.program_file, "a", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Program Code", "Program Name", "College Code"])
                if not file_exists:
                    writer.writeheader()
                writer.writerow({
                    "Program Code": code,
                    "Program Name": name,
                    "College Code": college_code
                })

            messagebox.showinfo("Success", "Program added.")
            win.destroy()

        ttk.Button(win, text="Save", command=save).pack(pady=10)


    # ==========================
    # DELETE COLLEGE WINDOW
    # ==========================

    def delete_college_window(self):
        win = tk.Toplevel(self.window)
        win.title("Delete College")
        win.geometry("300x200")

        colleges = self.load_colleges()
        name_to_code = {v: k for k, v in colleges.items()}

        ttk.Label(win, text="Select College").pack()
        dropdown = ttk.Combobox(win, values=list(colleges.values()), state="readonly")
        dropdown.pack()

        def delete():
            selected_name = dropdown.get().strip()
            if not selected_name:
                messagebox.showerror("Error", "Select a college.")
                return

            college_code = name_to_code[selected_name]

            if not messagebox.askyesno("Confirm", f"Delete {selected_name}?"):
                return

            df = pd.read_csv(self.student_file, dtype=str)
            affected = df["College Code"] == college_code

            if affected.any():
                if not messagebox.askyesno("Reassign", "Students found. Reassign to Unassigned?"):
                    return

                df.loc[affected, "College"] = "Unassigned"
                df.loc[affected, "College Code"] = "N/A"
                df.loc[affected, "Program"] = "Unassigned"
                df.loc[affected, "Program Code"] = "N/A"
                df.to_csv(self.student_file, index=False)

            # Remove college
            updated = {k: v for k, v in colleges.items() if k != college_code}

            with open(self.college_file, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["College Code", "College Name"])
                writer.writeheader()
                for k, v in updated.items():
                    writer.writerow({"College Code": k, "College Name": v})

            messagebox.showinfo("Success", "College deleted.")
            win.destroy()

        ttk.Button(win, text="Delete", command=delete).pack(pady=10)

    # ==========================
    # DELETE PROGRAM WINDOW
    # ==========================

    def delete_program_window(self):
        win = tk.Toplevel(self.window)
        win.title("Delete Program")
        win.geometry("300x200")

        programs = self.load_programs()
        name_to_code = {v["Program Name"]: k for k, v in programs.items()}

        ttk.Label(win, text="Select Program").pack()
        dropdown = ttk.Combobox(win, values=list(name_to_code.keys()), state="readonly")
        dropdown.pack()

        def delete():
            selected_name = dropdown.get().strip()
            if not selected_name:
                messagebox.showerror("Error", "Select a program.")
                return

            program_code = name_to_code[selected_name]

            if not messagebox.askyesno("Confirm", f"Delete {selected_name}?"):
                return

            df = pd.read_csv(self.student_file, dtype=str)
            affected = df["Program Code"] == program_code

            if affected.any():
                if not messagebox.askyesno("Reassign", "Students found. Reassign to Unassigned?"):
                    return

                df.loc[affected, "Program"] = "Unassigned"
                df.loc[affected, "Program Code"] = "N/A"
                df.to_csv(self.student_file, index=False)

            updated = {k: v for k, v in programs.items() if k != program_code}

            with open(self.program_file, "w", newline="") as csvfile:
                writer = csv.DictWriter(csvfile, fieldnames=["Program Code", "Program Name", "College Code"])
                writer.writeheader()
                for k, v in updated.items():
                    writer.writerow(v)

            messagebox.showinfo("Success", "Program deleted.")
            win.destroy()

        ttk.Button(win, text="Delete", command=delete).pack(pady=10)