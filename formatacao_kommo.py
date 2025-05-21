# -*- coding: utf-8 -*-
import csv
import os


def get_kommo_header(path):
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f, delimiter=";")
        header = next(reader)
    return header


def mapear_para_kommo(row, idxs, kommo_header):
    # idxs: dict com os índices dos campos do relatório de usuários
    # kommo_header: lista de colunas do kommo
    linha = [""] * len(kommo_header)
    # Mapeamento básico

    # Nome completo do contato e Título do lead
    nome_completo = ""
    if "Nome" in idxs:
        try:
            nome_completo = row[idxs["Nome"]].strip()
            linha[kommo_header.index("Nome completo do contato")] = nome_completo
            # Também colocar no Título do lead
            linha[kommo_header.index("Título do lead")] = nome_completo
        except:
            pass

    # Telefone comercial (contato) - formatar para 55(XX)XXXXX-XXXX
    def formatar_telefone_br(numero):
        import re

        numero = numero.strip()
        # Remove tudo que não for número
        digitos = re.sub(r"\D", "", numero)
        if len(digitos) == 11:
            ddd = digitos[:2]
            parte1 = digitos[2:7]
            parte2 = digitos[7:]
            return f"55({ddd}){parte1}-{parte2}"
        elif len(digitos) == 10:
            ddd = digitos[:2]
            parte1 = digitos[2:6]
            parte2 = digitos[6:]
            return f"55({ddd}){parte1}-{parte2}"
        else:
            return numero  # retorna como está se não bater o padrão

    if "Telefone" in idxs:
        try:
            tel = row[idxs["Telefone"]].strip()
            tel_formatado = formatar_telefone_br(tel)
            linha[kommo_header.index("Telefone comercial (contato)")] = tel_formatado
        except:
            pass
    # Email comercial (contato)
    if "E-mail" in idxs:
        try:
            linha[kommo_header.index("Email comercial (contato)")] = row[
                idxs["E-mail"]
            ].strip()
        except:
            pass
    # CPF pode ir em "Tags do lead" ou "Nota do lead" se desejar
    if "CPF" in idxs:
        try:
            linha[kommo_header.index("Tags do lead")] = row[idxs["CPF"]].strip()
        except:
            pass
    # Data de Cadastro pode ir em "Criado em (lead)"
    if "Data de Cadastro" in idxs:
        try:
            linha[kommo_header.index("Criado em (lead)")] = row[
                idxs["Data de Cadastro"]
            ].strip()
        except:
            pass
    return linha


def formatar_para_kommo(relatorio_path, kommo_exemplo_path, saida_path):
    kommo_header = get_kommo_header(kommo_exemplo_path)
    with open(relatorio_path, encoding="utf-8") as fin, open(
        saida_path, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin, delimiter=";")
        writer = csv.writer(fout, delimiter=";")
        header = next(reader)
        # Mapear índices dos campos do relatório de usuários
        idxs = {col: i for i, col in enumerate(header)}
        writer.writerow(kommo_header)
        for row in reader:
            linha_kommo = mapear_para_kommo(row, idxs, kommo_header)
            writer.writerow(linha_kommo)


if __name__ == "__main__":
    relatorio_path = os.path.join("leads_plataforma", "relatorio-usuarios-filtrado.csv")
    kommo_exemplo_path = os.path.join("exemplos_csv", "exemplo_formato_kommo.csv")
    saida_path = os.path.join(
        "leads_prontos_para_subir", "relatorio-usuarios-kommo.csv"
    )
    formatar_para_kommo(relatorio_path, kommo_exemplo_path, saida_path)
