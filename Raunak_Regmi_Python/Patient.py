from Person import Person

class Patient(Person):
    """Patient class"""

    def __init__(self, first_name, surname, age, mobile, postcode):
        """
        Args:
            first_name (string): First name
            surname (string): Surname
            age (int): Age
            mobile (string): the mobile number
            address (string): address
        """

        #ToDo1
        # self.__first_name = first_name
        # self.__surname = surname
        super().__init__(first_name, surname)
        self.__age = age
        self.__mobile = mobile
        self.__postcode = postcode
        self.__doctor = 'None'
        self.__symptoms = []
        self.__month = ""


    # def full_name(self) :
    #     """full name is first_name and surname"""
    #     #ToDo2
    #     return f'{self.__first_name}{self.__surname}'

    def set_month(self, month):
        self.__month = month

    def get_month(self):
        return self.__month

    def get_doctor(self) :
        #ToDo3
        return self.__doctor

    def get_age(self):
        return self.__age

    def get_mobile(self):
        return self.__mobile

    def get_postcode(self):
        return self.__postcode

    def add_symptom(self, symptom):

        self.__symptoms.append(symptom)

    def get_symptoms(self):
        return self.__symptoms

    def print_symptoms(self):
        """prints all the symptoms"""
        #ToDo4
        if len(self.__symptoms) == 0:
            print('No symptoms to show.')
        else:
            print('Symptoms:')
            for symptoms in self.__symptoms:
                print(symptoms)

    def link(self, doctor):
        """Args: doctor(string): the doctor full name"""
        self.__doctor = doctor

    # FILE HANDLING PART

    def to_file_string(self):
        symptoms = "|".join(self.__symptoms)
        return f"{self.get_first_name()},{self.get_surname()},{self.__age},{self.__mobile},{self.__postcode},{self.__doctor},{self.__month},{symptoms}"

    def save_to_file(self, filename="patients.txt"):
        with open(filename, "a") as f:
            f.write(
                f"{self.full_name()},{self.get_age()},{self.get_mobile()},{self.get_postcode()},{self.get_doctor()},{self.__month},{';'.join(self._Patient__symptoms)}\n")

    def __str__(self):
        symptoms = ", ".join(self.__symptoms) if self.__symptoms else "None"
        return f'{self.full_name():^30}|{self.__doctor:^30}|{self.__age:^5}|{self.__mobile:^15}|{self.__postcode:^10}|{symptoms}'
