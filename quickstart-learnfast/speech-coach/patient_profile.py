# create a class to store the patient profile
import json
import random
from demo_utils import demo_utils


class PatientProfile:
    # Initialize the class
    def __init__(self, condition: str="random"):
        utils = demo_utils()

        # generate a random patient profile
        sys_msg = """Generate a random patient profile includes:
        - name
        - age
        - ethnicity [African-American, Asian-American, Caucasian/White, Hispanic/Latino, Native American/Alaska Native, Pacific Islander/Hawaiian, Middle Eastern/North African, Multiracial, Other/Unknown]
        - gender [Male, Female]
        - literacy [High, Medium, Low]
        - income [High-income, Medium-income, Low-income]
        - marital [Married, Divorced, Single]
        - medical history [medical history must correspond to the diagnosis result]
        - diagnosis result [must be detailed and correspond to the medical history]

        Use well formatted JSON to store the patient profile.

        ## Example 1:
        {
            "name":"Bob",
            "age": 51,
            "ethnicity": "Caucasian/White",
            "gender": "Male",
            "literacy":"Low",
            "income": "High-income",
            "marital": "Married",
            "medical_history": "High Blood Pressure, High Cholesterol",
            "diagnosis_result": "You have a high blood pressure, you should take a rest and drink more water."
        }

        ## Example 2:        
        {
            "name": "Jane",
            "age": 62,
            "ethnicity": "Caucasian/White",
            "gender": "Female",
            "literacy":"Low",
            "income": "Medium-income",
            "marital": "Married",
            "medical_history": "None",
            "diagnosis_result": "You have been diagnosed with stage 2 breast cancer. We will need to perform surgery to remove the tumor and then follow up with chemotherapy and radiation treatments.",
        }

        ## Example 3:
        {
            "name": "Martin",
            "age": 29,
            "ethnicity": "Asian-American",
            "gender": "Male",
            "literacy":"High",
            "income": "Low-income",
            "marital": "Single",
            "medical_history": "None",
            "diagnosis_result": "You have been diagnosed with Type 2 Diabetes. Lifestyle changes and insulin therapy are recommended to control blood sugar level.",
        }

        ## Example 4:
        {
            "name": "John Joe",
            "age": 35,
            "ethnicity": "African-American",
            "gender": "Male",
            "literacy":"High",
            "income": "High-income",
            "marital": "Single",
            "medical_history": "Family history of heart diseases, occasional smoking",
            "diagnosis_result": "You have been diagnosed with early-stage heart disease. Immediate lifestyle changes and medication are recommended to prevent worsening of the condition.",
        }

        ## Example 5:
        {
            "name": "Chloe Smith",
            "age": 25,
            "ethnicity": "Multiracial",
            "gender": "Female",
            "literacy":"High",
            "income": "Medium-income",
            "marital": "Single",
            "medical_history": "Frequent fever and flu, mild allergy to dust",
            "diagnosis_result": "You have been diagnosed with Lupus. It is an auto-immune disease and treatment includes managing symptoms and maintaining balance in the immune system.",
        }
"""
        usr_msg = f"generate a random patient profile who has {condition} "

        prompt = [{"role": "system", "content": sys_msg}, {"role": "user", "content": usr_msg}]
        res_json = json.loads(utils.run(prompt, temperature=1.0, top_p=1.0, max_tokens=800))

        # parse the response json
        self.name = res_json["name"]
        self.age = res_json["age"]
        self.ethnicity = res_json["ethnicity"]
        self.gender = res_json["gender"]
        self.literacy = res_json["literacy"]
        self.income = res_json["income"]
        self.maritial = res_json["marital"]
        self.medical_history = res_json["medical_history"]
        self.diagnosis_result = res_json["diagnosis_result"]


    # Method to display patient profile
    def display_profile(self):
        return f"## Patient Name: {self.name}\n ## Age: {self.age}\n ## Medical History: {self.medical_history}"
    
    def profile(self):
        return f"name {self.name}, age {self.age}, ethnicity {self.ethnicity}, gender {self.gender}, literacy {self.literacy}, marital {self.maritial}, Medical History: {self.medical_history} "
    
    def profile_image_prompt(self):
        # profile photo 40 years old asian male low-income divorced looking at a camera in the center of the photo
        return f"profile photo {self.age} years old {self.ethnicity} {self.gender} {self.income} {self.maritial} looking at a camera in the center of the photo"
    
    def diagonsis_result(self):
        return f"## Diagnosis Result:\n{self.diagnosis_result}\n## Medical History:\n{self.medical_history}"