# -*- coding: utf-8 -*-
import csv
import os


def detectar_coluna_telefone(header):
    nomes_possiveis = [
        "telefone",
        "celular",
        "número",
        "numero",
        "phone",
        "telefone1",
        "telefone2",
        "contato",
        "Telefone",
    ]
    for idx, nome in enumerate(header):
        nome_normalizado = (
            nome.strip()
            .lower()
            .replace("ú", "u")
            .replace("é", "e")
            .replace("í", "i")
            .replace("ó", "o")
            .replace("á", "a")
        )
        for possivel in nomes_possiveis:
            if possivel in nome_normalizado:
                return idx
    return None


def carregar_numeros_bloqueio(path):
    numeros = set()
    with open(path, encoding="utf-8") as f:
        reader = csv.reader(f)
        next(reader)  # pular cabeçalho
        for row in reader:
            if row:
                numeros.add(row[0].strip())
    return numeros


def filtrar_usuarios(usuarios_path, bloqueio_path, saida_path):
    numeros_bloqueio = carregar_numeros_bloqueio(bloqueio_path)
    removidos = 0
    with open(usuarios_path, encoding="utf-8") as fin, open(
        saida_path, "w", encoding="utf-8", newline=""
    ) as fout:
        reader = csv.reader(fin, delimiter=";")
        writer = csv.writer(fout, delimiter=";")
        header = next(reader)
        writer.writerow(header)
        idx_telefone = detectar_coluna_telefone(header)
        idx_perfil = None
        for idx, nome in enumerate(header):
            if nome.strip().lower() == "perfil":
                idx_perfil = idx
                break
        if idx_telefone is None:
            print("Coluna de telefone não encontrada!")
            return
        if idx_perfil is None:
            print("Coluna de perfil não encontrada!")
            return
        primeira_linha = None
        for row in reader:
            if primeira_linha is None:
                primeira_linha = row
                print(f"Primeira linha encontrada: {primeira_linha}")
            # Remove admins
            if len(row) > idx_perfil and row[idx_perfil].strip().lower() == "admin":
                removidos += 1
                continue
            # Remove sem telefone válido
            if len(row) <= idx_telefone:
                removidos += 1
                continue
            numero = row[idx_telefone].strip()
            if not numero or numero in (
                "",
                "(00) 00000-0000",
                "(00)00000-0000",
                "sem telefone",
                "null",
                "None",
            ):
                removidos += 1
                continue
            # Remove se está na lista de bloqueio
            if numero in numeros_bloqueio:
                removidos += 1
                continue
            writer.writerow(row)
    print(f"Linhas removidas: {removidos}")


if __name__ == "__main__":
    usuarios_path = os.path.join("leads_plataforma", "relatorio-usuarios (1).csv")
    bloqueio_path = os.path.join("leads_sendflow_pronto", "leads_sendflow_limpo.csv")
    saida_path = os.path.join("leads_plataforma", "relatorio-usuarios-filtrado.csv")
    filtrar_usuarios(usuarios_path, bloqueio_path, saida_path)
