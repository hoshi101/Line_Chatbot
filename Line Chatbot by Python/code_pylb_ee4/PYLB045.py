import google.generativeai as genai

genai.configure(api_key="AIzaSyDmnTGlifPXbV3fUH6hm9oZ2msEYlcJ5pc")

model = genai.GenerativeModel("gemini-pro")

prompt = "ผมชื่ออะไร"
print("prompt : ",prompt)

try:
    response = model.generate_content(prompt)
    print(response.text)
except:
    print("no response")
    


