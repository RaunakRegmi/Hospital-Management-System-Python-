# Imports
from Admin import Admin
from Doctor import Doctor
from Patient import Patient

def main():
    """
    the main function to be ran when the program runs
    """

    # Initialising the actors
    admin = Admin('admin','123','B1 1AB') # username is 'admin', password is '123'
    # doctors = [Doctor('John','Smith','Internal Med.'), Doctor('Jone','Smith','Pediatrics'), Doctor('Jone','Carlos','Cardiology')]

    doctors = []

    try:
        with open("data/doctors.txt", "r") as file:
            for line in file:
                first_name, surname, speciality = line.strip().split(",")
                doctors.append(Doctor(first_name, surname, speciality))
    except FileNotFoundError:
        print("doctors.txt not found. Starting with empty list.")

    # patients = [Patient('Sara','Smith', 20, '07012345678','B1 234',), Patient('Mike','Jones', 37,'07555551234','L2 2AB'), Patient('Daivd','Smith', 15, '07123456789','C1 ABC')]
    # patients[0].add_symptom("Fever")
    # patients[0].add_symptom("Headache")
    #
    # patients[1].add_symptom("Chest pain")
    #
    # patients[2].add_symptom("Cough")
    # patients[2].add_symptom("Cold")

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
                    month = data[6]

                    patient = Patient(first_name, surname, age, mobile, postcode)
                    patient.link(doctor)
                    patient.set_month(month)

                    if len(data) >= 8 and data[7]:
                        symptoms = data[7].split("|")
                        for s in symptoms:
                            patient.add_symptom(s)

                    patients.append(patient)

    except FileNotFoundError:
        print("patients.txt not found. Starting empty.")

    for patient in patients:
        for doctor in doctors:
            if patient.get_doctor() == doctor.full_name():
                doctor.add_patient(patient)
                break

    discharged_patients = []

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

                    discharged_patients.append(patient)

    except FileNotFoundError:
        print("discharged_patients.txt not found. Starting empty.")

    # keep trying to login tell the login details are correct
    while True:
        if admin.login():
            running = True # allow the program to run
            break
        else:
            print('Incorrect username or password.')

    while running:
        # print the menu
        print('Choose the operation:')
        print(' 1- Register/View/Update/Delete doctor')
        print(' 2- View/View by Family Group/Discharge/ Patient')
        print(' 3- View discharged patient')
        print(' 4- Assign doctor to a patient')
        print(' 5- Relocate patient')
        print(' 6- Management report')
        print(' 7- Update admin detais')
        print(' 8- View doctor patients')
        print(' 9- Quit')

        # get the option
        op = input('Option: ')

        if op == '1':
            # 1- Register/view/update/delete doctor
         #ToDo1
          admin.doctor_management(doctors)
          pass


        # elif op == '2':
        #     # 2- View or discharge patients
        #     # ToDo2
        #     admin.view_patient(patients)
        #
        #     pass
        #
        #     while True:
        #         op = input('Do you want to discharge a patient(Y/N):').lower()
        #
        #         if op == 'yes' or op == 'y':
        #             # ToDo3
        #             admin.discharge(patients, discharged_patients)
        #             pass
        #
        #         elif op == 'no' or op == 'n':
        #             break
        #
        #         # unexpected entry
        #         else:
        #             print('Please answer by yes or no.')

        elif op == '2':
            while True:
                print("\n-----Patient Management-----")
                print("1 - View all patients")
                print("2 - View patients by family")
                print("3 - Discharge patient")
                print("4 - Back")

                choice = input("Choose option: ")

                if choice == '1':
                    admin.view_patient(patients)

                elif choice == '2':
                    admin.view_patient_by_family(patients)

                elif choice == '3':
                    admin.discharge(patients, discharged_patients)
                    save_patients(patients)
                    save_discharged_patients(discharged_patients)

                elif choice == '4':
                    break

                else:
                    print("Invalid option.")



        elif op == '3':
            # 3 - view discharged patients
            #ToDo4
            admin.view_discharge(discharged_patients)
            pass

        elif op == '4':
            # 4- Assign doctor to a patient
            admin.assign_doctor_to_patient(patients, doctors)
            save_patients(patients)

        elif op == '5':
            admin.relocate_patient(patients, doctors)
            save_patients(patients)

        elif op == '6':
            admin.management_report(doctors, patients)

        elif op == '7':
            # 5- Update admin detais
            admin.update_details()

        elif op == '8':
            print("-----Doctors List-----")
            admin.view(doctors)

            try:
                doctor_index = int(input("Enter doctor ID: ")) - 1
                if doctor_index not in range(len(doctors)):
                    print("Doctor not found.")
                else:
                    doctors[doctor_index].view_patients()
            except ValueError:
                print("Invalid input.")


        elif op == '9':
            # 6 - Quit
            #ToDo5
            running = False
            print("Exiting program...")
            pass

        else:
            # the user did not enter an option that exists in the menu
            print('Invalid option. Try again')

def save_patients(patients):
    with open("data/patients.txt", "w") as file:
        for patient in patients:
            file.write(patient.to_file_string() + "\n")

def save_discharged_patients(discharged_patients):
    with open("data/discharged_patients.txt", "w") as file:
        for patient in discharged_patients:
            file.write(patient.to_file_string() + "\n")



if __name__ == '__main__':
    main()
