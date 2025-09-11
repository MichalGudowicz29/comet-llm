from openai import OpenAI

client = OpenAI(
    base_url="http://localhost:1234/v1", 
    api_key="not-needed"
)

response = client.chat.completions.create(
    model="bielik-1.5b-v3.0-instruct", 
    messages=[
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": "Napisz mi prosty kod Pythona do obliczenia silni."}
    ],
    temperature=0.7,
)

print(response.choices[0].message.content)

