import os
import requests
from datetime import datetime

os.environ["GOOGLE_API_KEY"] = ""

api_key = os.environ["GOOGLE_API_KEY"]

genai.configure(api_key=api_key)

model = genai.GenerativeModel(model_name="gemini-1.5-flash")

url = "https://milharal-news.onrender.com/service/RelevantPotopsts"

response = requests.get(url)

if response.status_code == 200:
    data = response.json()

    post_texts = []

    for post in data:
        author = post.get('author', {})
        display_name = author.get('displayName', 'Desconhecido')
        handle = author.get('handle', 'Sem handle')
        text = post.get('record', {}).get('text', 'Sem texto')

        post_texts.append(f"{display_name} ({handle}): {text}")

    post_texts_str = " ".join(post_texts)
    prompt = f"Quero que você escreva um resumo em formato de jornal com base nos tópicos mais falados nos posts do Bluesky e da bolha dev. Transforme o conteúdo em um texto único, contínuo e interessante:\n\n{post_texts_str}"

    summary_response = model.generate_content(prompt)

    if summary_response and summary_response.candidates:
        text = summary_response.candidates[0].content.parts[0].text
        print(text)
    else:
        print("Nenhum conteúdo gerado.")
else:
    print(f"Erro na requisição. Código de status: {response.status_code}")