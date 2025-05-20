import pandas as pd
import os
from time import sleep
import re

def formatar_numero(numero):
    """ 
    O número está vindo no formato 557712345678
    deve ficar no formato (77) 91234-5678

    Args:
        numero (str): Número no formato 557712345678.
    """
    if not numero or pd.isna(numero):  # Verifica se o número é nulo ou vazio
        return numero  # Retorna o valor original

    # Remove caracteres não numéricos
    numero = re.sub(r'\D', '', str(numero))
    # Verifica se o número tem 12 dígitos
    if len(numero) == 12:
        # Formata o número
        return f"({numero[2:4]}) {numero[4:9]}-{numero[9:]}"
    else:
        print(f"Número inválido: {numero}. Deve ter 12 dígitos.")
        sleep(5)
        # Retorna o número original se não tiver 12 dígitos
        return numero

def concatenar_csv(lista_arquivos, arquivo_saida):
    """
    Concatena múltiplos arquivos CSV em um único arquivo.

    :param lista_arquivos: Lista de caminhos para os arquivos CSV a serem concatenados.
    :param arquivo_saida: Caminho para o arquivo CSV de saída.
    """
    # Lista para armazenar os DataFrames
    dataframes = []

    for arquivo in lista_arquivos:
        if os.path.exists(arquivo):
            # Especifica o separador correto
            df = pd.read_csv(arquivo, sep=';')
            # Formatar a coluna na 4ª posição (índice 3), se existir
            if df.shape[1] > 3:  # Verifica se há pelo menos 4 colunas
                df.iloc[:, 3] = df.iloc[:, 3].apply(formatar_numero)
            dataframes.append(df)
        else:
            print(f"Arquivo não encontrado: {arquivo}")

    # Concatenar todos os DataFrames
    resultado = pd.concat(dataframes, ignore_index=True)

    # Salvar o resultado no arquivo de saída
    resultado.to_csv(arquivo_saida, index=False)
    print(f"Arquivos concatenados com sucesso em: {arquivo_saida}")

# Exemplo de uso
if __name__ == "__main__": 
    # Substitua pelos caminhos reais dos arquivos CSV
    pasta = "leads_sendflow"
    arquivos = [os.path.join(pasta, arquivo) for arquivo in os.listdir(pasta) if arquivo.endswith(".csv")]
    saida = "leads_sendflow_pronto/leads_sendflow.csv"
    concatenar_csv(arquivos, saida)
