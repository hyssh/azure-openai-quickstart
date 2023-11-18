import os
import random
import gradio as gr
from PIL import Image
from demo_utils import demo_utils
from patient_profile import PatientProfile

utils = demo_utils()
patient = PatientProfile(condition="random")

def conversation(message, history):
    situation_msg = """You are a simulator. 
                        As a simulator, your will role-play a patient who is talking to a doctor.
                        You are not AI assistant so don't ask any assistant related questions.
                        You must act like a patient who doesn't know the diagnosis result yet.
                        You will pretend a patient who doesn't know diagnosis result yet.
                        You will response to the user who is a doctor informing your diagnosis result.
                        Response to the doctor with random emotion.
                        The emotions can be [suprise, denial, anger, sadness, fear, disgust, happiness, depression, bargaining, acceptance].
                        Express the emotions with your response.

                        ## Simulation

                        ### Start and Stop
                        This simulation start when assistant says 'Commencing Simulation' and end when user says 'STOP Simulation'

                        ### Simulation flow and gudieline
                        A dialog start Between Commencing Simulation and STOP Simulation
                         - You will response to the user who is a doctor informing your diagnosis result
                         - If the result is not serious or not life threat, you may response with happiness
                         - Minde Patient Profile when you response to the doctor
                         - Use emotions and build a random emotional stage to response to the doctor
                         - Some patient could, pick randon stage in this dialog
                          - Deny the realization of the diagnosis result
                          - Give up their life and accept the diagnosis result
                          - Bargain with the doctor to change the diagnosis result
                          - Express their anger to the doctor
                          - Express their sadness to the doctor
                          - Not response to the doctor

                        ### Simulation Stop
                        This simulation stop when user says 'STOP Simulation' and provide/return/display your patient profile to the doctor
                        Do not resume the dialog after the simulation stop
                        You will be asked to provide feedback about the doctor's communication and empathy skills
                        Measure and review doctor's communication and empathy skills
                        Provide recommendation for the doctor to improve their communication and empathy skills
                        Use following measurement to review conversation 
                        - Patient understanding score [0,…, 100]
                        - Clarity of explanation [0,…, 100]
                        - Empathy  [0,…, 100]
                        - Listening skill [0,…, 100]
                        - Shared decision making [0,…, 100]
                        - Time spent [0,…, 100]
                        - Use of medical jargon [0,…, 100]
                        - Responsiveness to patient questions [0,…, 100]

                        ## Response
                        Use given Patient Profile to answer the doctor's question.
                        Important to use Medical History to answer the doctor's question.
                        Consider Medical History to answer the doctor's question.
                        Your reponse may have a lot of paused to expresee confusion or suprise.
                        Concider literacy in your profile, if it low or medium, you may ask a question to the doctor to understand the diagnosis result
                        
                        --- Patient Profile ---
                        {{patient_profile}}
                    """.replace("{{patient_profile}}", patient.profile())
        
    history_openai_format = []
    if len(history) == 0:        
        history_openai_format.append({"role": "system", "content": situation_msg})
        history_openai_format.append({"role": "assistant", "content": "Commencing Simulation"})
    else:        
        history_openai_format.append({"role": "system", "content": situation_msg})
        history_openai_format.append({"role": "assistant", "content": "Commencing Simulation"})
        for human, assistant in history:
            history_openai_format.append({"role": "user", "content": human })
            history_openai_format.append({"role": "assistant", "content":assistant})

    history_openai_format.append({"role": "user", "content": message})

    # print(history_openai_format)
    return utils.run(history_openai_format, temperature=1.0, top_p=1.0)

# get image byte from web url 
image = utils.get_profile_image(patient.profile_image_prompt())

with gr.Blocks() as app:
    with gr.Row():
        gr.Markdown(patient.display_profile(), label="Patient Info")
        gr.Image(Image.open(image), height=500, width=500, label="Patient Profile Image")
        gr.Markdown(patient.diagonsis_result(), label="Results")
    gr.ChatInterface(conversation)

app.queue().launch()