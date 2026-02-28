import tkinter as tk
from tkinter import ttk, messagebox, filedialog
import pandas as pd
from student import StudentForm
from college_manager import CollegeManager  

import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_DIR = os.path.join(BASE_DIR, "data")

STUDENT_CSV = os.path.join(DATA_DIR, "students.csv")
COLLEGE_CSV = os.path.join(DATA_DIR, "colleges.csv")
PROGRAM_CSV = os.path.join(DATA_DIR, "programs.csv")

class StudentManagerApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Student Manager")
        self.geometry("1200x675")
        self.configure(bg="#E3F2FD")
        self.student_csv = STUDENT_CSV
        self.college_csv = COLLEGE_CSV
        self.df = None  
        self.welcome_screen()

    def welcome_screen(self):
        self.clear_screen()
        self.configure(bg="#E3F2FD")
        
        style = ttk.Style()
        style.configure("Big.TButton", font=("Arial", 14, "bold"), padding=10)
        
        tk.Label(self, text="STUDENT MANAGEMENT SYSTEM", font=("Arial", 20, "bold"), bg="#E3F2FD", fg="#0D47A1").pack(pady=10)
        ttk.Button(self, text="Student Management", command=self.load_student_interface, style="Big.TButton", width=50).pack(pady=20)
        ttk.Button(self, text="Manage Colleges & Programs", command=self.open_college_manager, style="Big.TButton", width=50).pack(pady=20)
        ttk.Button(self, text="Exit", command=self.quit, style="Big.TButton", width=20).pack(pady=5)

    def clear_screen(self):
        for widget in self.winfo_children():
            widget.destroy()

    def load_student_interface(self):
        
        if self.df is None:
            try:
                self.df = pd.read_csv(self.student_csv, dtype=str)
                print("Active student file:", self.student_csv)
            except Exception as e:
                messagebox.showerror("Error", f"Failed to load student_csv: {e}")
                self.welcome_screen()
                return

        self.clear_screen()
        self.configure(bg="#E3F2FD")
        ttk.Label(self, text="Student Records", font=("Arial", 16, "bold"),
                background="#E3F2FD", foreground="#0D47A1").pack(pady=10)

   
        search_frame = ttk.Frame(self)
        search_frame.pack(pady=5, padx=10, fill="x")

        ttk.Label(search_frame, text="Search by:").pack(side="left", padx=5)
        self.search_category = ttk.Combobox(search_frame, values=["Name/ID", "Program", "College"], state="readonly")
        self.search_category.pack(side="left", padx=5)
        self.search_category.bind("<<ComboboxSelected>>", self.update_search_values)  # Add this line

        self.search_entry = ttk.Combobox(search_frame, values=[])
        self.search_entry.pack(side="left", padx=5, fill="x", expand=True)

        ttk.Button(search_frame, text="Find", command=self.search_students).pack(side="left", padx=5)

        self.columns = [
            "First Name",
            "Last Name",
            "ID Number",
            "Age",
            "Year Level",
            "Gender",
            "College",
            "College Code",
            "Program",
            "Program Code"
        ]
        
                # for scrollbars
        table_frame = ttk.Frame(self)
        table_frame.pack(pady=5, fill="both", expand=True)
        # Vertical scrollbar
        v_scroll = ttk.Scrollbar(table_frame, orient="vertical")
        # Horizontal scrollbar
        h_scroll = ttk.Scrollbar(table_frame, orient="horizontal")
        # Create the Treeview table with scrollbars
        self.tree = ttk.Treeview(
            table_frame, columns=self.columns, show="headings",
            yscrollcommand=v_scroll.set, xscrollcommand=h_scroll.set)

        v_scroll.config(command=self.tree.yview)
        h_scroll.config(command=self.tree.xview)

        v_scroll.pack(side="right", fill="y")
        h_scroll.pack(side="bottom", fill="x")

        # column headings and width
        for col in self.columns:
            if col in ("College", "Program"):
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, width=250, anchor="w")
            elif col == "College Code":
                self.tree.heading(col, text=col, anchor="center")
                self.tree.column(col, width=100, anchor="center")
            else:
                self.tree.heading(col, text=col, anchor="w")
                self.tree.column(col, width=130, anchor="w")

        self.tree.pack(fill="both", expand=True)
        

        self.load_data()
        #buttons
        button_frame = ttk.Frame(self)
        button_frame.pack(pady=10)
        ttk.Button(button_frame, text="Add Student", command=self.add_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="View Student", command=self.view_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Edit Student", command=self.edit_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Delete Student", command=self.delete_student).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Refresh", command=self.refresh_data).pack(side="left", padx=5)
        ttk.Button(button_frame, text="Back", command=self.welcome_screen).pack(side="left", padx=5)

    def update_search_values(self, event=None):
        category = self.search_category.get()
        
        self.search_entry.set("")  
        
        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }

        valid_columns = column_map.get(category, [])

        if not valid_columns:
            self.search_entry["values"] = []
            return

        # for sorting values from selected columns 
        unique_values = sorted(set(self.df[valid_columns].values.flatten().astype(str)))
        self.search_entry["values"] = unique_values

    def load_data(self, df=None):
        if df is None:
            df = self.df  

        for row in self.tree.get_children():
            self.tree.delete(row)

        for _, row in df.iterrows():
            self.tree.insert("", "end", values=[row[col] for col in self.columns])


    def search_students(self):
        query = self.search_entry.get().strip().lower()
        category = self.search_category.get()

        if not query:
            self.load_data()
            return

        column_map = {
            "Name/ID": ["First Name", "Last Name", "ID Number"],
            "Program": ["Program"],
            "College": ["College"]
        }
        
        columns = column_map.get(category, [])
        valid_columns = [col for col in columns if col in self.df.columns]

        if not valid_columns:
            messagebox.showerror("Error", "Search category does not match any columns in the dataset.")
            return

        filtered_df = self.df[self.df[valid_columns].apply(lambda row: row.astype(str).str.lower().str.contains(query).any(), axis=1)]
        
        self.load_data(filtered_df)


    def refresh_data(self):
        self.df = pd.read_csv(self.student_csv, dtype=str)
        self.load_data()

    def add_student(self):
        StudentForm(self, self.df, self.student_csv)

    def view_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to view.")
            return

        student_data = self.tree.item(selected_item)["values"]
        if not student_data:
            messagebox.showwarning("Error", "Failed to retrieve student data.")
            return

        # Create read-only window
        view_win = tk.Toplevel(self)
        view_win.title("Student Details")
        view_win.geometry("400x400")

        for i, col in enumerate(self.columns):
            ttk.Label(view_win, text=f"{col}:", font=("Arial", 9, "bold")).grid(row=i, column=0, sticky="e", padx=10, pady=5)
            ttk.Label(view_win, text=student_data[i]).grid(row=i, column=1, sticky="w", padx=10, pady=5)

        ttk.Button(view_win, text="Close", command=view_win.destroy).grid(
            row=len(self.columns), column=0, columnspan=2, pady=10
        )

    def edit_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showwarning("No Selection", "Please select a student to edit.")
            return
        student_data = self.tree.item(selected_item)["values"]
        if not student_data:
            messagebox.showwarning("Error", "Failed to retrieve student data.")
            return
        StudentForm(self, self.df, self.student_csv, student_data)

    def delete_student(self):
        selected_item = self.tree.selection()
        if not selected_item:
            messagebox.showerror("Error", "No student selected.")
            return

        student_id = self.tree.item(selected_item)["values"][2]

        if messagebox.askyesno("Confirm Delete", f"Are you sure you want to delete student {student_id}?"):
            self.df = self.df[self.df["ID Number"] != student_id].copy()
            self.df.to_csv(self.student_csv, index=False)
            self.refresh_data()
            messagebox.showinfo("Success", "Student deleted successfully.")

    def open_college_manager(self):
        if not hasattr(self, 'student_csv') or not self.student_csv:
            messagebox.showerror("Error", "Please open a student CSV first.")
            return
        
        self.college_manager = CollegeManager(
            self,
            COLLEGE_CSV,
            PROGRAM_CSV,
            STUDENT_CSV
        )

if __name__ == "__main__":
    app = StudentManagerApp()
    app.mainloop()