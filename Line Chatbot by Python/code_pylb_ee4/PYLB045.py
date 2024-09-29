import google.generativeai as genai

genai.configure(api_key="***************************************")

model = genai.GenerativeModel("gemini-pro")

prompt = "ผมชื่ออะไร"
print("prompt : ",prompt)

try:
    response = model.generate_content(prompt)
    print(response.text)
except:
    print("no response")
    


