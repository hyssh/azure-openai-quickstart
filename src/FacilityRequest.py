import json
from aoai import aoai
import streamlit as st

# Create aoai class to connect to Azure OpenAI API and have a run function to send a prompt and get a response

def FacilityRequest(aoai: aoai=aoai()):
    system_msg, examples, user_msg = prompt_samples() 

    # sidebar
    with st.sidebar:
        with st.container():
            st.info("Classify facility request and provide insights. Type a question and click __Ask__ button to get answer.")
        sample_tab, system_tab = st.tabs(["samples", "system"])
        with sample_tab:
            st.write("## Sample Questions")
            st.code("I have a customer who has photophobia and blinds in the meeting room isn't working.", language="html")
        with system_tab:
            st.write("## System Message")
            st.text_area(label="System", value=system_msg, height=650)

    st.markdown("# Facility Request")
    st.markdown("This demo will show you how to use Azure OpenAI to classify facility request and provide insight")
    with st.expander("Demo scenario"):
        st.image("https://github.com/hyssh/azure-openai-quickstart/blob/main/images/Architecture-demo.png?raw=true")
        st.markdown("1. User will type text (multi lines) in the input box")
        st.markdown("2. __Web App__ sends the text to __Azure OpenAI__")
        st.markdown("3. __Azure OpenAI__ classify the details and return the classification results in JSON format")
        st.markdown("4. __Web App__ shows the results on screen")
    
    st.markdown("---")
    st.write("### Request")
    with st.container():
        col1, col2 = st.columns(2)
        with col1:
            building_name = st.text_input(label="Building Name", value="Lincoln Square North")
        with col2:
            room_name = st.text_input(label="Room Name", value="Meeting Room 1")
        details_text = st.text_area(label="Details", 
                                    height=3,
                                    max_chars=500,
                                    value="There is a light that keeps blinking for the last 5 minutes. Please replace the bulb since we're going to have a meeting with a customer tomorrow.")
    #replace the placeholder with user input
    user_msg = user_msg.replace("{{building_name}}", building_name)
    user_msg = user_msg.replace("{{room_name}}", room_name) 
    user_msg = user_msg.replace("{{details}}", details_text)
    prompt = [{"role":"system", "content":system_msg+examples},
              {"role":"user","content":user_msg}
              ]
    
    with st.container():
        if st.button("Facility Request"):
            st.spinner("Comparing...")
            with st.container():
                st.json(f"{aoai.run(prompt=prompt)}")
                # print(f"{aoai.run(prompt=prompt)}")
                # st.markdown(f"{json.loads(aoai.run(prompt=prompt))}")
        else:
            with st.container():
                st.empty()

def prompt_samples():
    # use option to choose different prompt samples case
    system_msg="""
You are a facility manager. You are responsible for managing the facilities and providing insights. 

## Role: Facility Manager
Read the request and classify severity.
There are four severity levels: Emergency, High, Medium, Low.
* Emergency: Great danger or urgent situation could cause threat to operation. It needs to be fixed now.
* High: The facility is not usable. It needs to be fixed soon.
* Medium: The facility is usable, but it needs to be fixed.
* Low: The facility is usable, but it needs to be fixed next scheduled maintenance.

Provide response to the requester based on the severity level.
* Emergency: The facility will be fixed at today's business hour.
* High: The facility will be fixed in one business day.
* Medium: The facility will be fixed in two business days.
* Low: The facility will be fixed in three business days.

## Response
Response is JSON format.
Include reasons why the severity is classified as the level and the response to the requester.
        """
    examples="""
## Examples:
### case 1
Building Name: Lincoln Square North
Room Name: Meeting Room 1
Details: The light in the meeting room is not working.

### Response
{
    "BuildingName":"Lincoln Square North",
    "Room Name":"Meeting Room 1",
    "Request Summary":"Light is not working",
    "Severity": "Low",
    "Reason":"There are lights working. The issue won't disturb the meeting or operation.",
    "Response": "Thank you for your request. We will send a technician to fix the light. Since the severity is low, it will be fixed in 3 business days."
}

### case 2
Building Name: Lincoln Square North
Room Name: Meeting Room 1
Details: A half-gallon of water have been leak for an hour at the man's room

### Response
{ 
    "BuildingName":"Lincoln Square North",
    "Room Name":"Meeting Room 1",
    "Request Summary":"Water leak at mens room",
    "Severity": "High",
    "Reason":"Potential damage to the building and the facility is not usable.",
    "Response": "Thank you for your request. We will send a technician to fix the leak. Since the severity is high, it will be fixed in 1 business day."
}
        """

    user_msg="""
Building Name:{{building_name}}
Room Name:{{room_name}}
Details:{{details}}
        """
    return system_msg, examples, user_msg
    
if __name__ == "__main__":
    FacilityRequest()    