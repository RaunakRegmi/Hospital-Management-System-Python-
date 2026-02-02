import tkinter as tk
from tkinter import messagebox, scrolledtext
from Admin import Admin
from Doctor import Doctor
from Patient import Patient


class HospitalManagementGUI:

    def __init__(self, root):
        self.root = root
        self.root.title("Hospital Management System")
        self.root.geometry("900x700")

        # Load data
        self.admin = self.load_admin()
        self.doctors = self.load_doctors()
        self.patients = self.load_patients()
        self.discharged_patients = self.load_discharged_patients()

        # Link patients to doctors
        for patient in self.patients:
            for doctor in self.doctors:
                if patient.get_doctor() == doctor.full_name():
                    doctor.add_patient(patient)
                    break

        # Container for all pages
        self.container = tk.Frame(self.root)
        self.container.pack(fill="both", expand=True)

        self.frames = {}

        # Show login page first
        self.show_login_page()

    # ==================== DATA LOADING ====================

    def load_admin(self):
        try:
            with open("data/admin.txt", "r") as file:
                data = file.readline().strip().split(",")
                username = data[0]
                password = data[1]
                address = data[2] if len(data) > 2 else ""
                return Admin(username, password, address)
        except FileNotFoundError:
            return Admin("admin", "123", "")

    def load_doctors(self):
        doctors = []
        try:
            with open("data/doctors.txt", "r") as file:
                for line in file:
                    first_name, surname, speciality = line.strip().split(",")
                    doctors.append(Doctor(first_name, surname, speciality))
        except FileNotFoundError:
            pass
        return doctors

    def load_patients(self):
        patients = []
        try:
            with open("data/patients.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) >= 6:
                        first_name = data[0]
                        surname = data[1]
                        age = int(data[2])
                        mobile = data[3]
                        postcode = data[4]
                        doctor = data[5]
                        month = data[6] if len(data) > 6 else ""

                        patient = Patient(first_name, surname, age, mobile, postcode)
                        patient.link(doctor)
                        patient.set_month(month)

                        if len(data) >= 8 and data[7]:
                            symptoms = data[7].split("|")
                            for s in symptoms:
                                patient.add_symptom(s)

                        patients.append(patient)
        except FileNotFoundError:
            pass
        return patients

    def load_discharged_patients(self):
        discharged = []
        try:
            with open("data/discharged_patients.txt", "r") as file:
                for line in file:
                    data = line.strip().split(",")
                    if len(data) >= 6:
                        first_name = data[0]
                        surname = data[1]
                        age = int(data[2])
                        mobile = data[3]
                        postcode = data[4]
                        doctor = data[5]

                        patient = Patient(first_name, surname, age, mobile, postcode)
                        patient.link(doctor)

                        if len(data) == 7 and data[6]:
                            symptoms = data[6].split("|")
                            for s in symptoms:
                                patient.add_symptom(s)

                        discharged.append(patient)
        except FileNotFoundError:
            pass
        return discharged

    # ==================== DATA SAVING ====================

    def save_doctors(self):
        with open("data/doctors.txt", "w") as f:
            for doctor in self.doctors:
                f.write(f"{doctor.get_first_name()},{doctor.get_surname()},{doctor.get_speciality()}\n")

    def save_patients(self):
        with open("data/patients.txt", "w") as file:
            for patient in self.patients:
                file.write(patient.to_file_string() + "\n")

    def save_discharged_patients(self):
        with open("data/discharged_patients.txt", "w") as file:
            for patient in self.discharged_patients:
                file.write(patient.to_file_string() + "\n")

    # ==================== PAGE NAVIGATION ====================

    def show_frame(self, name):
        # Destroy old frame if exists
        for widget in self.container.winfo_children():
            widget.destroy()

        # Create and show new frame
        if name == "main_menu":
            self.create_main_menu()
        elif name == "doctor_management":
            self.create_doctor_management()
        elif name == "patient_management":
            self.create_patient_management()
        elif name == "view_discharged":
            self.create_view_discharged()
        elif name == "assign_doctor":
            self.create_assign_doctor()
        elif name == "relocate_patient":
            self.create_relocate_patient()
        elif name == "management_report":
            self.create_management_report()
        elif name == "update_admin":
            self.create_update_admin()
        elif name == "view_doctor_patients":
            self.create_view_doctor_patients()

    # ==================== LOGIN PAGE ====================

    def show_login_page(self):
        login_frame = tk.Frame(self.container)
        login_frame.pack(fill="both", expand=True)

        tk.Label(login_frame, text="Hospital Management System", font=("Arial", 20, "bold")).pack(pady=30)
        tk.Label(login_frame, text="Admin Login", font=("Arial", 14)).pack(pady=10)

        # Username
        tk.Label(login_frame, text="Username:").pack(pady=5)
        self.username_entry = tk.Entry(login_frame, width=30)
        self.username_entry.pack(pady=5)

        # Password
        tk.Label(login_frame, text="Password:").pack(pady=5)
        self.password_entry = tk.Entry(login_frame, show="*", width=30)
        self.password_entry.pack(pady=5)

        # Login button
        tk.Button(login_frame, text="Login", command=self.login, width=20, bg="green", fg="white").pack(pady=20)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if username == self.admin._Admin__username and password == self.admin._Admin__password:
            self.show_frame("main_menu")
        else:
            # Clear entries and show error in label
            self.username_entry.delete(0, "end")
            self.password_entry.delete(0, "end")
            tk.Label(self.container, text="Incorrect username or password. Try again.",
                     fg="red", font=("Arial", 10)).pack()

    # ==================== MAIN MENU ====================

    def create_main_menu(self):
        menu_frame = tk.Frame(self.container)
        menu_frame.pack(fill="both", expand=True)

        tk.Label(menu_frame, text="Main Menu", font=("Arial", 18, "bold")).pack(pady=20)

        button_width = 40

        tk.Button(menu_frame, text="1 - Doctor Management",
                  command=lambda: self.show_frame("doctor_management"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="2 - Patient Management",
                  command=lambda: self.show_frame("patient_management"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="3 - View Discharged Patients",
                  command=lambda: self.show_frame("view_discharged"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="4 - Assign Doctor to Patient",
                  command=lambda: self.show_frame("assign_doctor"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="5 - Relocate Patient",
                  command=lambda: self.show_frame("relocate_patient"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="6 - Management Report",
                  command=lambda: self.show_frame("management_report"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="7 - Update Admin Details",
                  command=lambda: self.show_frame("update_admin"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="8 - View Doctor Patients",
                  command=lambda: self.show_frame("view_doctor_patients"),
                  width=button_width).pack(pady=5)

        tk.Button(menu_frame, text="9 - Quit",
                  command=self.root.quit,
                  width=button_width, bg="red", fg="white").pack(pady=5)

    # ==================== DOCTOR MANAGEMENT ====================

    def create_doctor_management(self):
        doc_frame = tk.Frame(self.container)
        doc_frame.pack(fill="both", expand=True)

        tk.Label(doc_frame, text="Doctor Management", font=("Arial", 18, "bold")).pack(pady=10)

        button_width = 30

        tk.Button(doc_frame, text="Register Doctor",
                  command=self.register_doctor, width=button_width).pack(pady=5)

        tk.Button(doc_frame, text="View Doctors",
                  command=self.view_doctors, width=button_width).pack(pady=5)

        tk.Button(doc_frame, text="Update Doctor",
                  command=self.update_doctor, width=button_width).pack(pady=5)

        tk.Button(doc_frame, text="Delete Doctor",
                  command=self.delete_doctor, width=button_width).pack(pady=5)

        tk.Button(doc_frame, text="Back to Main Menu",
                  command=lambda: self.show_frame("main_menu"),
                  width=button_width, bg="gray").pack(pady=20)

    def register_doctor(self):
        # Create window
        window = tk.Toplevel(self.root)
        window.title("Register Doctor")
        window.geometry("400x300")

        tk.Label(window, text="Register New Doctor", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(window, text="First Name:").pack(pady=5)
        first_name_entry = tk.Entry(window, width=30)
        first_name_entry.pack(pady=5)

        tk.Label(window, text="Surname:").pack(pady=5)
        surname_entry = tk.Entry(window, width=30)
        surname_entry.pack(pady=5)

        tk.Label(window, text="Speciality:").pack(pady=5)
        speciality_entry = tk.Entry(window, width=30)
        speciality_entry.pack(pady=5)

        def save_doctor():
            first_name = first_name_entry.get().strip()
            surname = surname_entry.get().strip()
            speciality = speciality_entry.get().strip()

            if not first_name or not surname or not speciality:
                tk.Label(window, text="All fields are required!", fg="red").pack()
                return

            # Check if name exists
            for doctor in self.doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    tk.Label(window, text="Doctor name already exists!", fg="red").pack()
                    return

            # Add doctor
            new_doctor = Doctor(first_name, surname, speciality)
            self.doctors.append(new_doctor)
            self.save_doctors()

            window.destroy()

        tk.Button(window, text="Save", command=save_doctor, bg="green", fg="white", width=20).pack(pady=20)

    def view_doctors(self):
        # Create window
        window = tk.Toplevel(self.root)
        window.title("View Doctors")
        window.geometry("600x400")

        tk.Label(window, text="List of Doctors", font=("Arial", 14, "bold")).pack(pady=10)

        # Create text widget with scrollbar
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=70, height=20)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        # Add doctors
        text_widget.insert("1.0", "ID |          Full Name           |  Speciality\n")
        text_widget.insert("end", "=" * 60 + "\n")

        if len(self.doctors) == 0:
            text_widget.insert("end", "No doctors registered yet.\n")
        else:
            for index, doctor in enumerate(self.doctors):
                text_widget.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget.config(state="disabled")

    def update_doctor(self):
        if len(self.doctors) == 0:
            return

        # Create window
        window = tk.Toplevel(self.root)
        window.title("Update Doctor")
        window.geometry("600x500")

        tk.Label(window, text="Update Doctor Details", font=("Arial", 14, "bold")).pack(pady=10)

        # Show doctors list
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=70, height=10)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", "ID |          Full Name           |  Speciality\n")
        text_widget.insert("end", "=" * 60 + "\n")

        for index, doctor in enumerate(self.doctors):
            text_widget.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget.config(state="disabled")

        # Input section
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Doctor ID:").grid(row=0, column=0, pady=5, padx=5)
        doctor_id_entry = tk.Entry(input_frame, width=20)
        doctor_id_entry.grid(row=0, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="Select field to update:").grid(row=1, column=0, pady=5, padx=5)
        field_var = tk.StringVar(value="1")
        field_entry = tk.Entry(input_frame, width=20)
        field_entry.grid(row=1, column=1, pady=5, padx=5)

        tk.Label(input_frame, text="1=First Name, 2=Surname, 3=Speciality", font=("Arial", 8)).grid(row=2, column=0,
                                                                                                    columnspan=2)

        tk.Label(input_frame, text="New Value:").grid(row=3, column=0, pady=5, padx=5)
        new_value_entry = tk.Entry(input_frame, width=20)
        new_value_entry.grid(row=3, column=1, pady=5, padx=5)

        def save_update():
            try:
                doctor_index = int(doctor_id_entry.get()) - 1
                field_choice = field_entry.get()
                new_value = new_value_entry.get().strip()

                if doctor_index not in range(len(self.doctors)):
                    tk.Label(window, text="Doctor not found!", fg="red").pack()
                    return

                if not new_value:
                    tk.Label(window, text="Please enter a new value!", fg="red").pack()
                    return

                if field_choice == '1':
                    self.doctors[doctor_index].set_first_name(new_value)
                elif field_choice == '2':
                    self.doctors[doctor_index].set_surname(new_value)
                elif field_choice == '3':
                    self.doctors[doctor_index].set_speciality(new_value)
                else:
                    tk.Label(window, text="Invalid field choice!", fg="red").pack()
                    return

                self.save_doctors()
                window.destroy()

            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="Update", command=save_update, bg="blue", fg="white", width=20).pack(pady=10)

    def delete_doctor(self):
        if len(self.doctors) == 0:
            return

        # Create window
        window = tk.Toplevel(self.root)
        window.title("Delete Doctor")
        window.geometry("600x450")

        tk.Label(window, text="Delete Doctor", font=("Arial", 14, "bold")).pack(pady=10)

        # Show doctors
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=70, height=15)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0", "ID |          Full Name           |  Speciality\n")
        text_widget.insert("end", "=" * 60 + "\n")

        for index, doctor in enumerate(self.doctors):
            text_widget.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget.config(state="disabled")

        # Input
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Doctor ID to delete:").pack(side="left", padx=5)
        doctor_id_entry = tk.Entry(input_frame, width=20)
        doctor_id_entry.pack(side="left", padx=5)

        def confirm_delete():
            try:
                doctor_index = int(doctor_id_entry.get()) - 1

                if doctor_index not in range(len(self.doctors)):
                    tk.Label(window, text="Doctor not found!", fg="red").pack()
                    return

                doctor_name = self.doctors[doctor_index].full_name()

                confirm = messagebox.askyesno("Confirm", f"Delete {doctor_name}?")
                if confirm:
                    self.doctors.pop(doctor_index)
                    self.save_doctors()
                    window.destroy()
            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="Delete", command=confirm_delete, bg="red", fg="white", width=20).pack(pady=10)

    # ==================== PATIENT MANAGEMENT ====================

    def create_patient_management(self):
        patient_frame = tk.Frame(self.container)
        patient_frame.pack(fill="both", expand=True)

        tk.Label(patient_frame, text="Patient Management", font=("Arial", 18, "bold")).pack(pady=10)

        button_width = 30

        tk.Button(patient_frame, text="View All Patients",
                  command=self.view_all_patients, width=button_width).pack(pady=5)

        tk.Button(patient_frame, text="View Patients by Family",
                  command=self.view_patients_by_family, width=button_width).pack(pady=5)

        tk.Button(patient_frame, text="Discharge Patient",
                  command=self.discharge_patient, width=button_width).pack(pady=5)

        tk.Button(patient_frame, text="Back to Main Menu",
                  command=lambda: self.show_frame("main_menu"),
                  width=button_width, bg="gray").pack(pady=20)

    def view_all_patients(self):
        window = tk.Toplevel(self.root)
        window.title("View All Patients")
        window.geometry("900x500")

        tk.Label(window, text="All Patients", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=100, height=25)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0",
                           "ID |          Full Name           |      Assigned Doctor         | Age |    Mobile     | Postcode | Symptoms\n")
        text_widget.insert("end", "=" * 120 + "\n")

        if len(self.patients) == 0:
            text_widget.insert("end", "No patients registered.\n")
        else:
            for index, patient in enumerate(self.patients):
                text_widget.insert("end", f"{index + 1:3}|{str(patient)}\n")

        text_widget.config(state="disabled")

    def view_patients_by_family(self):
        window = tk.Toplevel(self.root)
        window.title("View Patients by Family")
        window.geometry("900x500")

        tk.Label(window, text="Patients Grouped by Family", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=100, height=25)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0",
                           "ID |          Full Name           |      Assigned Doctor         | Age |    Mobile     | Postcode | Symptoms\n")
        text_widget.insert("end", "=" * 120 + "\n")

        # Group patients by surname
        family_groups = {}
        for patient in self.patients:
            surname = patient.get_surname()
            if surname in family_groups:
                family_groups[surname].append(patient)
            else:
                family_groups[surname] = [patient]

        # Print grouped
        id_counter = 1
        for surname, family in family_groups.items():
            text_widget.insert("end", f"\n--- Family: {surname} ---\n")
            for patient in family:
                text_widget.insert("end", f"{id_counter:3}|{str(patient)}\n")
                id_counter += 1

        text_widget.config(state="disabled")

    def discharge_patient(self):
        if len(self.patients) == 0:
            return

        window = tk.Toplevel(self.root)
        window.title("Discharge Patient")
        window.geometry("900x500")

        tk.Label(window, text="Discharge Patient", font=("Arial", 14, "bold")).pack(pady=10)

        # Show patients
        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=100, height=20)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0",
                           "ID |          Full Name           |      Assigned Doctor         | Age |    Mobile     | Postcode | Symptoms\n")
        text_widget.insert("end", "=" * 120 + "\n")

        for index, patient in enumerate(self.patients):
            text_widget.insert("end", f"{index + 1:3}|{str(patient)}\n")

        text_widget.config(state="disabled")

        # Input
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Patient ID to discharge:").pack(side="left", padx=5)
        patient_id_entry = tk.Entry(input_frame, width=20)
        patient_id_entry.pack(side="left", padx=5)

        def confirm_discharge():
            try:
                patient_index = int(patient_id_entry.get()) - 1

                if patient_index not in range(len(self.patients)):
                    tk.Label(window, text="Patient not found!", fg="red").pack()
                    return

                patient_name = self.patients[patient_index].full_name()

                confirm = messagebox.askyesno("Confirm", f"Discharge {patient_name}?")
                if confirm:
                    patient = self.patients[patient_index]
                    self.discharged_patients.append(patient)
                    self.patients.pop(patient_index)

                    self.save_patients()
                    self.save_discharged_patients()

                    window.destroy()
            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="Discharge", command=confirm_discharge, bg="orange", fg="white", width=20).pack(pady=10)

    # ==================== VIEW DISCHARGED ====================

    def create_view_discharged(self):
        window = tk.Toplevel(self.root)
        window.title("Discharged Patients")
        window.geometry("900x500")

        tk.Label(window, text="Discharged Patients", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=100, height=25)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        text_widget.insert("1.0",
                           "ID |          Full Name           |      Doctor Name             | Age |    Mobile     | Postcode | Symptoms\n")
        text_widget.insert("end", "=" * 120 + "\n")

        if len(self.discharged_patients) == 0:
            text_widget.insert("end", "No discharged patients.\n")
        else:
            for index, patient in enumerate(self.discharged_patients):
                text_widget.insert("end", f"{index + 1:3}|{str(patient)}\n")

        text_widget.config(state="disabled")

        def close_and_return():
            window.destroy()
            self.show_frame("main_menu")

        tk.Button(window, text="Close", command=close_and_return, width=20).pack(pady=10)

    # ==================== ASSIGN DOCTOR ====================

    def create_assign_doctor(self):
        if len(self.patients) == 0:
            self.show_frame("main_menu")
            return

        if len(self.doctors) == 0:
            self.show_frame("main_menu")
            return

        window = tk.Toplevel(self.root)
        window.title("Assign Doctor to Patient")
        window.geometry("900x600")

        tk.Label(window, text="Assign Doctor to Patient", font=("Arial", 14, "bold")).pack(pady=10)

        # Show patients
        tk.Label(window, text="Patients:", font=("Arial", 12, "bold")).pack(pady=5)

        frame1 = tk.Frame(window)
        frame1.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar1 = tk.Scrollbar(frame1)
        scrollbar1.pack(side="right", fill="y")

        text_widget1 = tk.Text(frame1, yscrollcommand=scrollbar1.set, width=100, height=8)
        text_widget1.pack(side="left", fill="both", expand=True)
        scrollbar1.config(command=text_widget1.yview)

        text_widget1.insert("1.0",
                            "ID |          Full Name           |      Assigned Doctor         | Age |    Mobile     | Postcode | Symptoms\n")

        for index, patient in enumerate(self.patients):
            text_widget1.insert("end", f"{index + 1:3}|{str(patient)}\n")

        text_widget1.config(state="disabled")

        # Show doctors
        tk.Label(window, text="Doctors:", font=("Arial", 12, "bold")).pack(pady=5)

        frame2 = tk.Frame(window)
        frame2.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar2 = tk.Scrollbar(frame2)
        scrollbar2.pack(side="right", fill="y")

        text_widget2 = tk.Text(frame2, yscrollcommand=scrollbar2.set, width=100, height=8)
        text_widget2.pack(side="left", fill="both", expand=True)
        scrollbar2.config(command=text_widget2.yview)

        text_widget2.insert("1.0", "ID |          Full Name           |  Speciality\n")

        for index, doctor in enumerate(self.doctors):
            text_widget2.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget2.config(state="disabled")

        # Input section
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        patient_id_entry = tk.Entry(input_frame, width=15)
        patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Enter Doctor ID:").grid(row=0, column=2, padx=5, pady=5)
        doctor_id_entry = tk.Entry(input_frame, width=15)
        doctor_id_entry.grid(row=0, column=3, padx=5, pady=5)

        def assign():
            try:
                patient_index = int(patient_id_entry.get()) - 1
                doctor_index = int(doctor_id_entry.get()) - 1

                if patient_index not in range(len(self.patients)):
                    tk.Label(window, text="Patient not found!", fg="red").pack()
                    return

                if doctor_index not in range(len(self.doctors)):
                    tk.Label(window, text="Doctor not found!", fg="red").pack()
                    return

                patient = self.patients[patient_index]
                doctor = self.doctors[doctor_index]

                patient.link(doctor.full_name())
                doctor.add_patient(patient)

                self.save_patients()

                window.destroy()
                self.show_frame("main_menu")

            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="Assign", command=assign, bg="green", fg="white", width=20).pack(pady=10)

    # ==================== RELOCATE PATIENT ====================

    def create_relocate_patient(self):
        if len(self.patients) == 0:
            self.show_frame("main_menu")
            return

        if len(self.doctors) == 0:
            self.show_frame("main_menu")
            return

        window = tk.Toplevel(self.root)
        window.title("Relocate Patient")
        window.geometry("900x600")

        tk.Label(window, text="Relocate Patient to New Doctor", font=("Arial", 14, "bold")).pack(pady=10)

        # Show patients
        tk.Label(window, text="Patients:", font=("Arial", 12, "bold")).pack(pady=5)

        frame1 = tk.Frame(window)
        frame1.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar1 = tk.Scrollbar(frame1)
        scrollbar1.pack(side="right", fill="y")

        text_widget1 = tk.Text(frame1, yscrollcommand=scrollbar1.set, width=100, height=8)
        text_widget1.pack(side="left", fill="both", expand=True)
        scrollbar1.config(command=text_widget1.yview)

        text_widget1.insert("1.0",
                            "ID |          Full Name           |      Current Doctor          | Age |    Mobile     | Postcode | Symptoms\n")

        for index, patient in enumerate(self.patients):
            text_widget1.insert("end", f"{index + 1:3}|{str(patient)}\n")

        text_widget1.config(state="disabled")

        # Show doctors
        tk.Label(window, text="Doctors:", font=("Arial", 12, "bold")).pack(pady=5)

        frame2 = tk.Frame(window)
        frame2.pack(fill="both", expand=True, padx=10, pady=5)

        scrollbar2 = tk.Scrollbar(frame2)
        scrollbar2.pack(side="right", fill="y")

        text_widget2 = tk.Text(frame2, yscrollcommand=scrollbar2.set, width=100, height=8)
        text_widget2.pack(side="left", fill="both", expand=True)
        scrollbar2.config(command=text_widget2.yview)

        text_widget2.insert("1.0", "ID |          Full Name           |  Speciality\n")

        for index, doctor in enumerate(self.doctors):
            text_widget2.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget2.config(state="disabled")

        # Input section
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Patient ID:").grid(row=0, column=0, padx=5, pady=5)
        patient_id_entry = tk.Entry(input_frame, width=15)
        patient_id_entry.grid(row=0, column=1, padx=5, pady=5)

        tk.Label(input_frame, text="Enter New Doctor ID:").grid(row=0, column=2, padx=5, pady=5)
        doctor_id_entry = tk.Entry(input_frame, width=15)
        doctor_id_entry.grid(row=0, column=3, padx=5, pady=5)

        def relocate():
            try:
                patient_index = int(patient_id_entry.get()) - 1
                doctor_index = int(doctor_id_entry.get()) - 1

                if patient_index not in range(len(self.patients)):
                    tk.Label(window, text="Patient not found!", fg="red").pack()
                    return

                if doctor_index not in range(len(self.doctors)):
                    tk.Label(window, text="Doctor not found!", fg="red").pack()
                    return

                patient = self.patients[patient_index]
                old_doctor_name = patient.get_doctor()

                # Remove from old doctor
                for doctor in self.doctors:
                    if doctor.full_name() == old_doctor_name:
                        doctor.remove_patient(patient)
                        break

                # Assign to new doctor
                new_doctor = self.doctors[doctor_index]
                patient.link(new_doctor.full_name())
                new_doctor.add_patient(patient)

                self.save_patients()

                window.destroy()
                self.show_frame("main_menu")

            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="Relocate", command=relocate, bg="blue", fg="white", width=20).pack(pady=10)

    # ==================== MANAGEMENT REPORT ====================

    def create_management_report(self):
        window = tk.Toplevel(self.root)
        window.title("Management Report")
        window.geometry("700x600")

        tk.Label(window, text="Management Report", font=("Arial", 14, "bold")).pack(pady=10)

        frame = tk.Frame(window)
        frame.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar = tk.Scrollbar(frame)
        scrollbar.pack(side="right", fill="y")

        text_widget = tk.Text(frame, yscrollcommand=scrollbar.set, width=80, height=30)
        text_widget.pack(side="left", fill="both", expand=True)
        scrollbar.config(command=text_widget.yview)

        # Total doctors
        text_widget.insert("end", f"Total number of doctors: {len(self.doctors)}\n\n")

        # Patients per doctor
        text_widget.insert("end", "Patients per Doctor:\n")
        text_widget.insert("end", "=" * 50 + "\n")
        for doctor in self.doctors:
            count = 0
            for patient in self.patients:
                if patient.get_doctor() == doctor.full_name():
                    count += 1
            text_widget.insert("end", f"{doctor.full_name()}: {count} patients\n")

        text_widget.insert("end", "\n")

        # Appointments per month per doctor
        text_widget.insert("end", "Appointments per Month per Doctor:\n")
        text_widget.insert("end", "=" * 50 + "\n")

        appointments = {}
        for patient in self.patients:
            doctor = patient.get_doctor()
            month = patient.get_month()

            if doctor == "None":
                continue

            if doctor not in appointments:
                appointments[doctor] = {}

            if month in appointments[doctor]:
                appointments[doctor][month] += 1
            else:
                appointments[doctor][month] = 1

        for doctor in appointments:
            text_widget.insert("end", f"\nDoctor: {doctor}\n")
            for month in appointments[doctor]:
                text_widget.insert("end", f"  {month}: {appointments[doctor][month]} appointments\n")

        text_widget.insert("end", "\n")

        # Illness types
        text_widget.insert("end", "Patients based on illness type:\n")
        text_widget.insert("end", "=" * 50 + "\n")

        illness_count = {}
        for patient in self.patients:
            for symptom in patient.get_symptoms():
                if symptom in illness_count:
                    illness_count[symptom] += 1
                else:
                    illness_count[symptom] = 1

        if len(illness_count) == 0:
            text_widget.insert("end", "No illness data available.\n")
        else:
            for illness in illness_count:
                text_widget.insert("end", f"{illness}: {illness_count[illness]}\n")

        text_widget.config(state="disabled")

        def close_and_return():
            window.destroy()
            self.show_frame("main_menu")

        tk.Button(window, text="Close", command=close_and_return, width=20).pack(pady=10)

    # ==================== UPDATE ADMIN ====================

    def create_update_admin(self):
        window = tk.Toplevel(self.root)
        window.title("Update Admin Details")
        window.geometry("400x300")

        tk.Label(window, text="Update Admin Details", font=("Arial", 14, "bold")).pack(pady=10)

        tk.Label(window, text="New Username:").pack(pady=5)
        username_entry = tk.Entry(window, width=30)
        username_entry.pack(pady=5)

        tk.Label(window, text="New Address:").pack(pady=5)
        address_entry = tk.Entry(window, width=30)
        address_entry.pack(pady=5)

        def save_admin():
            new_username = username_entry.get().strip()
            new_address = address_entry.get().strip()

            if new_username:
                self.admin._Admin__username = new_username
            if new_address:
                self.admin._Admin__address = new_address

            self.admin.save_admin()
            window.destroy()
            self.show_frame("main_menu")

        tk.Button(window, text="Update", command=save_admin, bg="green", fg="white", width=20).pack(pady=20)

    # ==================== VIEW DOCTOR PATIENTS ====================

    def create_view_doctor_patients(self):
        if len(self.doctors) == 0:
            self.show_frame("main_menu")
            return

        window = tk.Toplevel(self.root)
        window.title("View Doctor Patients")
        window.geometry("700x500")

        tk.Label(window, text="Select Doctor to View Patients", font=("Arial", 14, "bold")).pack(pady=10)

        # Show doctors
        frame1 = tk.Frame(window)
        frame1.pack(fill="both", expand=True, padx=10, pady=10)

        scrollbar1 = tk.Scrollbar(frame1)
        scrollbar1.pack(side="right", fill="y")

        text_widget1 = tk.Text(frame1, yscrollcommand=scrollbar1.set, width=80, height=15)
        text_widget1.pack(side="left", fill="both", expand=True)
        scrollbar1.config(command=text_widget1.yview)

        text_widget1.insert("1.0", "ID |          Full Name           |  Speciality\n")
        text_widget1.insert("end", "=" * 60 + "\n")

        for index, doctor in enumerate(self.doctors):
            text_widget1.insert("end", f"{index + 1:3}|{str(doctor)}\n")

        text_widget1.config(state="disabled")

        # Input
        input_frame = tk.Frame(window)
        input_frame.pack(pady=10)

        tk.Label(input_frame, text="Enter Doctor ID:").pack(side="left", padx=5)
        doctor_id_entry = tk.Entry(input_frame, width=20)
        doctor_id_entry.pack(side="left", padx=5)

        def close_and_return():
            window.destroy()
            self.show_frame("main_menu")

        def show_patients():
            try:
                doctor_index = int(doctor_id_entry.get()) - 1

                if doctor_index not in range(len(self.doctors)):
                    tk.Label(window, text="Doctor not found!", fg="red").pack()
                    return

                doctor = self.doctors[doctor_index]

                # Create new window
                patient_window = tk.Toplevel(self.root)
                patient_window.title(f"Patients of Dr. {doctor.full_name()}")
                patient_window.geometry("900x400")

                tk.Label(patient_window, text=f"Patients of Dr. {doctor.full_name()}",
                         font=("Arial", 14, "bold")).pack(pady=10)

                frame2 = tk.Frame(patient_window)
                frame2.pack(fill="both", expand=True, padx=10, pady=10)

                scrollbar2 = tk.Scrollbar(frame2)
                scrollbar2.pack(side="right", fill="y")

                text_widget2 = tk.Text(frame2, yscrollcommand=scrollbar2.set, width=100, height=20)
                text_widget2.pack(side="left", fill="both", expand=True)
                scrollbar2.config(command=text_widget2.yview)

                # Get doctor's patients
                doctor_patients = []
                for patient in self.patients:
                    if patient.get_doctor() == doctor.full_name():
                        doctor_patients.append(patient)

                if len(doctor_patients) == 0:
                    text_widget2.insert("1.0", "No patients assigned to this doctor.\n")
                else:
                    text_widget2.insert("1.0",
                                        "ID |          Full Name           | Age |    Mobile     | Postcode | Symptoms\n")
                    text_widget2.insert("end", "=" * 100 + "\n")

                    for i, patient in enumerate(doctor_patients):
                        symptoms = ", ".join(patient.get_symptoms()) if patient.get_symptoms() else "None"
                        text_widget2.insert("end",
                                            f"{i + 1:^3}|"
                                            f"{patient.full_name():^30}|"
                                            f"{patient.get_age():^5}|"
                                            f"{patient.get_mobile():^15}|"
                                            f"{patient.get_postcode():^10}|"
                                            f"{symptoms}\n"
                                            )

                text_widget2.config(state="disabled")

                tk.Button(patient_window, text="Close", command=patient_window.destroy, width=20).pack(pady=10)

            except ValueError:
                tk.Label(window, text="Invalid ID entered!", fg="red").pack()

        tk.Button(window, text="View Patients", command=show_patients, bg="blue", fg="white", width=20).pack(pady=10)
        tk.Button(window, text="Back to Main Menu", command=close_and_return, bg="gray", width=20).pack(pady=5)


if __name__ == "__main__":
    root = tk.Tk()
    app = HospitalManagementGUI(root)
    root.mainloop()