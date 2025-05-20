import csv

def formatar_numero(numero):
    """Formata o número de telefone no formato (99) 98528-4450."""
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
        reader = csv.DictReader(infile)
        fieldnames = reader.fieldnames
        writer = csv.DictWriter(outfile, fieldnames=fieldnames)
        
        writer.writeheader()
        for row in reader:
            if 'Número' in row and row['Número']:
                row['Número'] = formatar_numero(row['Número'])
            writer.writerow(row)

# Exemplo de uso:
processar_csv('leads_sendflow_pronto/leads_sendflow.csv', 'leads_sendflow_pronto/leads_sendflow_formatado.csv')
