import openai

# Set your OpenAI API key

openai.api_type = 'OPENAI_API_TYPE'
openai.api_key = 'lm-studio'

# Prepare your input data
input_data = {
    'text': 'Could you describe the campus life at Syracuse University?'
}

# Call the 'phi-3.1-mini-128k-instruct' model
response = openai.chat.completions.create(
    model='phi-3.1-mini-128k-instruct',
    prompt=input_data['text'],
    max_tokens=100
)


# Print the output
print(response.choices[0].text.strip())