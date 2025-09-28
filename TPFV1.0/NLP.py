import sys
from openai import OpenAI

client = OpenAI(
    #api_key = ###
)

if len(sys.argv) < 2:
    print("Usage: python NLP.py <input_text>")
    sys.exit(1)

input_text = sys.argv[1]

response = client.chat.completions.create(
    model="ft:gpt-3.5-turbo-0125:personal::9NbLcpu1:ckpt-step-60",
    messages=[{"role": "user", "content": input_text}],
    stream=False
)

Gram_answer = response.choices[0].message.content
print(Gram_answer)
