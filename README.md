# Documentação do Script de Resumo de Postagens

## Descrição
Este script Python consulta um serviço REST para coletar postagens relacionadas a tópicos populares na plataforma Bluesky e na bolha de desenvolvimento. Ele utiliza um modelo generativo da Google para criar um resumo em formato de jornal com base no conteúdo dessas postagens.

## Pré-requisitos
Antes de executar o script, você precisa ter:

- Python 3.x instalado.
- A biblioteca `requests` instalada. Você pode instalá-la usando o seguinte comando:

  ```bash
  pip install requests
  ```

- A biblioteca `genai` da Google configurada. Certifique-se de seguir as instruções da documentação oficial para instalá-la e configurá-la corretamente.

## Configuração
### Chave da API
Certifique-se de que você possui uma chave de API válida do Google. Você deve configurá-la na variável de ambiente `GOOGLE_API_KEY`.

```bash
export GOOGLE_API_KEY="sua_chave_de_api"
```

### URL do Serviço
O script faz uma requisição GET para o seguinte endpoint:

```plaintext
https://milharal-news.onrender.com/service/RelevantPotopsts
```
Este URL deve estar acessível e responder com dados JSON no formato esperado.

## Estrutura do Código

### Importação de Módulos
```python
import os
import requests
from datetime import datetime
```
Os módulos `os` e `requests` são importados para manipulação de variáveis de ambiente e para fazer requisições HTTP, respectivamente. O módulo `datetime` é importado, mas não é utilizado no código atual.

### Configuração da Chave da API
```python
os.environ["GOOGLE_API_KEY"] = ""
api_key = os.environ["GOOGLE_API_KEY"]
```
Aqui, a chave da API do Google é configurada a partir das variáveis de ambiente.

### Configuração do Modelo Generativo
```python
genai.configure(api_key=api_key)
model = genai.GenerativeModel(model_name="gemini-1.5-flash")
```
O modelo generativo da Google é configurado usando a chave da API.

### Coleta de Dados
```python
url = "https://milharal-news.onrender.com/service/RelevantPotopsts"
response = requests.get(url)
```
O script faz uma requisição GET para coletar as postagens do serviço especificado.

### Processamento de Dados
```python
if response.status_code == 200:
    data = response.json()
    post_texts = []

    for post in data:
        author = post.get('author', {})
        display_name = author.get('displayName', 'Desconhecido')
        handle = author.get('handle', 'Sem handle')
        text = post.get('record', {}).get('text', 'Sem texto')
        post_texts.append(f"{display_name} ({handle}): {text}")
```
Se a requisição for bem-sucedida (código de status 200), o script processa os dados JSON retornados, extraindo informações sobre cada postagem, como o autor, o handle e o texto.

### Geração do Resumo
```python
post_texts_str = " ".join(post_texts)
prompt = f"Quero que você escreva um resumo em formato de jornal com base nos tópicos mais falados nos posts do Bluesky e da bolha dev. Transforme o conteúdo em um texto único, contínuo e interessante:\n\n{post_texts_str}"

summary_response = model.generate_content(prompt)
```
As postagens são convertidas em uma única string, que é usada como prompt para gerar um resumo com o modelo generativo.

### Impressão do Resultado
```python
if summary_response and summary_response.candidates:
    text = summary_response.candidates[0].content.parts[0].text
    print(text)
else:
    print("Nenhum conteúdo gerado.")
```
O resumo gerado é impresso. Se nenhum conteúdo for gerado, uma mensagem de erro é exibida.

## Conclusão
Esse script é uma ferramenta útil para coletar e resumir informações relevantes de postagens em um formato acessível e conciso. Certifique-se de verificar a documentação da API que você está utilizando para garantir que os dados retornados estejam no formato esperado.

## Exemplos
### Executando o Script:
```bash
python main.py
```

### Saída Esperada:
```plaintext
Autor 1 (handle1): Texto da postagem 1. Autor 2 (handle2): Texto da postagem 2.
Resumo gerado...
```

Sinta-se à vontade para modificar a documentação conforme necessário para se adequar ao seu projeto!
