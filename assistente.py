import pandas as pd
import openai

# Função para carregar o CSV
def load_csv(file_path):
    try:
        df = pd.read_csv(file_path)
        print("Arquivo CSV carregado com sucesso!")
        return df
    except Exception as e:
        print(f"Erro ao carregar o arquivo CSV: {e}")
        return None

# Função para consultar o DataFrame
def query_by_column(df, column_name, value):
    try:
        result = df[df[column_name].astype(str).str.contains(value, case=False, na=False)]
        return result
    except Exception as e:
        print(f"Erro ao realizar a consulta: {e}")
        return None

# Função para interagir com o ChatGPT e processar a pergunta
def chat_with_gpt(df, prompt):
    openai.api_key = '**********'  # Substitua pela sua chave de API

    try:
        response = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", "content": "Você é um assistente que ajuda com consultas em arquivos CSV."},
                {"role": "user", "content": prompt}
            ],
            max_tokens=150
        )

        response_text = response.choices[0].message['content'].strip()

        # Processar a resposta do GPT para extrair a coluna e o valor da consulta
        if "mostrar" in response_text and "onde" in response_text and "=" in response_text:
            parts = response_text.split(" ")
            col_show = parts[1]
            col_where = parts[3]
            value = response_text.split("=")[1].strip()
            
            result = query_by_column(df, col_where, value)
            if result is not None and not result.empty:
                return result[[col_show]]
            else:
                return "Nenhum resultado encontrado."
        else:
            return "Formato de consulta não reconhecido."
    except Exception as e:
        print(f"Erro ao processar a pergunta com GPT: {e}")
        return None

# Exemplo de uso
file_path = 'moat_202404.csv'  # Substitua pelo caminho do seu arquivo CSV
df = load_csv(file_path)

if df is not None:
    while True:
        user_input = input("Você: ")
        if user_input.lower() == 'sair':
            print("Chat encerrado.")
            break

        result = chat_with_gpt(df, user_input)
        if result is not None:
            print("GPT-3.5 Turbo: ", result)
