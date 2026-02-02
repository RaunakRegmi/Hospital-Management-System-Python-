
from Doctor import Doctor

class Admin:
    """A class that deals with the Admin operations"""
    def __init__(self, username, password, address = ''):
        """
        Args:
            username (string): Username
            password (string): Password
            address (string, optional): Address Defaults to ''
        """

        self.__username = username
        self.__password = password
        self.__address =  address

    def view(self,a_list):
        """
        print a list
        Args:
            a_list (list): a list of printables
        """
        for index, item in enumerate(a_list):
            print(f'{index+1:3}|{item}')

    def login(self) :
        """
        A method that deals with the login
        Raises:
            Exception: returned when the username and the password ...
                    ... don`t match the data registered
        Returns:
            string: the username
        """
    
        print("-----Login-----")
        #Get the details of the admin

        username = input('Enter the username: ')
        password = input('Enter the password: ')

        # check if the username and password match the registered ones
        #ToDo1
        if username == self.__username and password == self.__password:
            return True
        else:
            return False

    def find_index(self,index,doctors):
        
            # check that the doctor id exists          
        if index in range(0,len(doctors)):
            
            return True

        # if the id is not in the list of doctors
        else:
            return False
            
    def get_doctor_details(self) :
        """
        Get the details needed to add a doctor
        Returns:
            first name, surname and ...
                            ... the speciality of the doctor in that order.
        """
        #ToDo2
        first_name = input('Enter first name: ')
        surname = input('Enter surname: ')
        speciality = input('Enter speciality: ')

        return first_name, surname, speciality


    def doctor_management(self, doctors):
        """
        A method that deals with registering, viewing, updating, deleting doctors
        Args:
            doctors (list<Doctor>): the list of all the doctors names
        """

        print("-----Doctor Management-----")

        # menu
        print('Choose the operation:')
        print(' 1 - Register')
        print(' 2 - View')
        print(' 3 - Update')
        print(' 4 - Delete')

        #ToDo3
        op = input('Input: ')


        # register
        if op == '1':
            print("-----Register-----")

            # get the doctor details
            print('Enter the doctor\'s details:')
            first_name = input('Enter the first name: ')
            surname = input('Enter the surname: ')
            speciality = input('Enter the speciality: ')
            pass

            # check if the name is already registered
            name_exists = False
            for doctor in doctors:
                if first_name == doctor.get_first_name() and surname == doctor.get_surname():
                    print('Name already exists.')
                    name_exists = True
                    break # save time and end the loop

            if name_exists == False:
                new_doctor = Doctor(first_name, surname, speciality)
                doctors.append(new_doctor)
                self.save_doctors(doctors)

            pass# add the doctor ...
                                                      # ... to the list of doctors
            print('Doctor registered.')

        # View
        elif op == '2':
            print("-----List of Doctors-----")
            #ToDo7
            self.view(doctors)
            pass

        # Update
        elif op == '3':
            while True:
                print("-----Update Doctor`s Details-----")
                print('ID |          Full name           |  Speciality')
                self.view(doctors)
                try:
                    index = int(input('Enter the ID of the doctor: ')) - 1
                    doctor_index=self.find_index(index,doctors)
                    if doctor_index!=False:
                
                        break
                        
                    else:
                        print("Doctor not found")

                    
                        # doctor_index is the ID mines one (-1)
                        

                except ValueError: # the entered id could not be changed into an int
                    print('The ID entered is incorrect')

            # menu
            print('Choose the field to be updated:')
            print(' 1 First name')
            print(' 2 Surname')
            print(' 3 Speciality')
            op = int(input('Input: ')) # make the user input lowercase

            #ToDo8
            if op == 1:
                doctors[index].set_first_name(input("Enter new first name: "))
            elif op == 2:
                doctors[index].set_surname(input("Enter new surname: "))
            elif op == 3:
                doctors[index].set_speciality(input("Enter new speciality: "))
            else:
                print('Option is invalid.')

            self.save_doctors(doctors)
            pass

        # Delete
        elif op == '4':
            print("-----Delete Doctor-----")
            print('ID |          Full Name           |  Speciality')
            self.view(doctors)

            doctor_index = input('Enter the ID of the doctor to be deleted: ')
            #ToDo9
            try:
                doctor_index = int(doctor_index) - 1

                if self.find_index(doctor_index, doctors):

                    doctors.pop(doctor_index)
                    self.save_doctors(doctors)
                    print(f'Doctor deleted.')
                else:
                    print('The id entered was not found.')

            except ValueError:
                print('Enter a valid doctor ID')
            pass

            # print('The id entered is incorrect')

        # if the id is not in the list of patients
        else:
            print('Invalid operation choosen. Check your spelling!')

    def save_doctors(self, doctors):
        with open("data/doctors.txt", "w") as f:
            for doctor in doctors:
                f.write(f"{doctor.get_first_name()},{doctor.get_surname()},{doctor.get_speciality()}\n")

    def view_patient(self, patients):
        """
        Print a list of patients grouped by family surname
        Args:
            patients (list<Patients>): list of all active patients
        """

        print("-----View Patients-----")
        print(
            'ID |          Full Name           |      Assigned Doctor`s Name      | Age |    Mobile     | Postcode | Symptoms')

        # ToDo10
        self.view(patients)

    def view_patient_by_family(self, patients):
        print("-----View Patients (Grouped by Family)-----")
        print(
                'ID |          Full Name           |      Assigned Doctor`s Name      | Age |    Mobile     | Postcode | Symptoms')

        # Group patients by surname
        family_groups = {}
        for patient in patients:
            surname = patient.get_surname()
            if surname in family_groups:
                family_groups[surname].append(patient)
            else:
                family_groups[surname] = [patient]

        # Print patients grouped by family
        id_counter = 1
        for surname, family in family_groups.items():
            print(f"\n--- Family: {surname} ---")
            for patient in family:
                print(f"{id_counter:3}|{patient}")
                id_counter += 1

    def assign_doctor_to_patient(self, patients, doctors):

        """
        Allow the admin to assign a doctor to a patient
        Args:
            patients (list<Patients>): the list of all the active patients
            doctors (list<Doctor>): the list of all the doctors
        """
        print("-----Assign Patients-----")

        # print("-----Patients-----")
        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode | Symptoms')
        self.view(patients)

        patient_index = input('Please enter the patient ID: ')

        try:
            # patient_index is the patient ID mines one (-1)
            patient_index = int(patient_index) -1

            # check if the id is not in the list of patients
            if patient_index not in range(len(patients)):
                print('The id entered was not found.')
                return # stop the procedures

        except ValueError: # the entered id could not be changed into an int
            print('The id entered is incorrect')
            return # stop the procedures

        print("-----Doctors Select-----")
        print('Select the doctor that fits these symptoms:')
        patients[patient_index].print_symptoms() # print the patient symptoms

        print('--------------------------------------------------')
        print('ID |          Full Name           |  Speciality   ')
        self.view(doctors)
        doctor_index = input('Please enter the doctor ID: ')

        try:
            # doctor_index is the patient ID mines one (-1)
            doctor_index = int(doctor_index) -1

            # check if the id is in the list of doctors
            if self.find_index(doctor_index,doctors)!=False:
                    
                # link the patients to the doctor and vice versa
                #ToDo11
                patient = patients[patient_index]

                doctor = doctors[doctor_index]

                patient.link(doctor.full_name())

                doctor.add_patient(patient)



                pass
                
                print('The patient is now assign to the doctor.')

            # if the id is not in the list of doctors
            else:
                print('The id entered was not found.')

        except ValueError: # the entered id could not be changed into an in
            print('The id entered is incorrect')

    def relocate_patient(self, patients, doctors):
        print("-----Relocate Patient-----")

        print("Patients List:")
        self.view(patients)

        try:
            patient_index = int(input("Enter patient ID: ")) - 1
            if patient_index not in range(len(patients)):
                print("Patient not found.")
                return
        except ValueError:
            print("Invalid input.")
            return

        patient = patients[patient_index]

        print("Doctors List:")
        self.view(doctors)

        try:
            doctor_index = int(input("Enter new doctor ID: ")) - 1
            if doctor_index not in range(len(doctors)):
                print("Doctor not found.")
                return
        except ValueError:
            print("Invalid input.")
            return

        # new_doctor = doctors[doctor_index]
        # patient.link(new_doctor.full_name())
        #
        # print("Patient relocated successfully.")

        old_doctor_name = patient.get_doctor()

        for doctor in doctors:
            if doctor.full_name() == old_doctor_name:
                doctor.remove_patient(patient)
                break

        new_doctor = doctors[doctor_index]
        patient.link(new_doctor.full_name())
        new_doctor.add_patient(patient)

        print("Patient relocated successfully.")

    def management_report(self, doctors, patients):
        print("-----Management Report-----")

        print(f"Total number of doctors: {len(doctors)}")

        print("\nPatients per Doctor:")

        for doctor in doctors:
            count = 0
            for patient in patients:
                if patient.get_doctor() == doctor.full_name():
                    count += 1
            print(f"{doctor.full_name()} : {count} patients")

        print("\nAppointments per Month per Doctor:")

        appointments = {}

        for patient in patients:
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
            print(f"\nDoctor: {doctor}")
            for month in appointments[doctor]:
                print(f"  {month}: {appointments[doctor][month]} appointments")

        print("\nPatients based on illness type:")

        illness_count = {}

        for patient in patients:
            for symptom in patient.get_symptoms():
                if symptom in illness_count:
                    illness_count[symptom] += 1
                else:
                    illness_count[symptom] = 1

        if len(illness_count) == 0:
            print("No illness data available.")
        else:
            for illness in illness_count:
                print(f"{illness}: {illness_count[illness]}")

    def update_details(self):
        print("-----Update Admin Details-----")

        new_username = input("Enter new username: ")
        new_address = input("Enter new address: ")

        if new_username:
            self.__username = new_username
        if new_address:
            self.__address = new_address

        self.save_admin()
        print("Admin details updated successfully.")

    def discharge(self, patients, discharge_patients):
        """
        Allow the admin to discharge a patient when treatment is done
        Args:
            patients (list<Patients>): the list of all the active patients
            discharge_patients (list<Patients>): the list of all the non-active patients
        """
        print("-----Discharge Patient-----")

        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode | Symptoms')
        self.view(patients)

        patient_index = input('Please enter the patient ID: ')

        #ToDo12
        try:
            patient_index = int(patient_index) - 1

            if patient_index not in range(len(patients)):
                print('ID not found.')
                return

            patient = patients[patient_index]

            discharge_patients.append(patient)

            patients.pop(patient_index)

            print('Patient Discharged.')

        except ValueError:
            print('Enter the correct ID')

    def view_discharge(self, discharge_patients):
        """
        Print the list of discharged patients
        Args:
            discharge_patients (list<Patients>): list of discharged patients
        """
        print("-----Discharged Patients-----")
        if not discharge_patients:
            print("No discharged patients yet.")
            return

        print('ID |          Full Name           |      Doctor`s Full Name      | Age |    Mobile     | Postcode | Symptoms')
        self.view(discharge_patients)

    def save_admin(self):
        with open("data/admin.txt", "w") as file:
            file.write(f"{self.__username},{self.__password},{self.__address}")
