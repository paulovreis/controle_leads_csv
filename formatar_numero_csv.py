import csv
from time import sleep

def formatar_numero(numero):
    """
    Formata o número de telefone no formato (99) 98528-4450.
    Exemplo:
    - Entrada: 559985284450
    - Saída: (99) 98528-4450
    Args:
        numero (str): Número no formato 559985284450.
    """
    numero = numero.strip()
    # Se o número tem 12 dígitos e começa com 55, insere o 9 após o DDD
    if len(numero) == 12 and numero.startswith("55"):
        numero = numero[:4] + '9' + numero[4:]
    if len(numero) == 13 and numero.startswith("55"):
        ddd = numero[2:4]
        parte1 = numero[4:9]
        parte2 = numero[9:]
        return f"({ddd}) {parte1}-{parte2}"
    else:
        # Retorna o número original se não estiver no formato esperado
        return numero

def processar_csv(input_csv, output_csv):
    """Lê um arquivo CSV, formata os números e salva em um novo arquivo."""
    with open(input_csv, mode='r', newline='', encoding='utf-8') as infile, \
         open(output_csv, mode='w', newline='', encoding='utf-8') as outfile:
        reader = csv.DictReader(infile, delimiter=';')
        fieldnames = ['Número']
        writer = csv.DictWriter(outfile, fieldnames=fieldnames, delimiter=';')

        writer.writeheader()
        for row in reader:
            # Remove todos os campos, exceto 'Número', e só então aplica a formatação
            numero = row.get('Número', '').strip()
            if numero:
                # Remove qualquer caractere não numérico
                numero_limpo = ''.join(filter(str.isdigit, numero))
                numero_formatado = formatar_numero(numero_limpo)
                if len(numero_formatado) == 15:
                    writer.writerow({'Número': numero_formatado})

# Exemplo de uso:
processar_csv('leads_sendflow_pronto/leads_sendflow.csv', 'leads_sendflow_pronto/leads_sendflow_limpo.csv')
