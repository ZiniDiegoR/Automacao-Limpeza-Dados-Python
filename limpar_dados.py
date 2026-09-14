"""
Automação de Limpeza de Dados de Vendas com Python (Pandas)
-------------------------------------------------------------
Lê a base bruta de vendas (dados/vendas_brutas.csv), aplica uma rotina
de limpeza e padronização, e gera:
  - dados/vendas_tratadas.csv   -> base limpa, pronta para análise
  - relatorio_qualidade.txt     -> resumo do que foi encontrado e corrigido
"""

import pandas as pd
import numpy as np
import re

CAMINHO_BRUTO = "dados/vendas_brutas.csv"
CAMINHO_LIMPO = "dados/vendas_tratadas.csv"
CAMINHO_RELATORIO = "relatorio_qualidade.txt"

relatorio = []


def log(msg):
    print(msg)
    relatorio.append(msg)


def carregar_dados(caminho):
    df = pd.read_csv(caminho, dtype=str)
    log(f"Linhas carregadas do arquivo bruto: {len(df)}")
    return df


def remover_linhas_totalmente_vazias(df):
    antes = len(df)
    df = df.dropna(how="all")
    df = df[~(df.apply(lambda linha: linha.astype(str).str.strip().eq("").all(), axis=1))]
    log(f"Linhas totalmente vazias removidas: {antes - len(df)}")
    return df


def remover_duplicatas(df):
    antes = len(df)
    df = df.drop_duplicates()
    log(f"Linhas duplicadas removidas: {antes - len(df)}")
    return df


def padronizar_categoria(df):
    df["categoria"] = (
        df["categoria"]
        .astype(str)
        .str.strip()
        .str.lower()
        .map({
            "eletrônicos": "Eletrônicos",
            "eletronicos": "Eletrônicos",
            "moda": "Moda",
            "casa e decoração": "Casa e Decoração",
            "casa e decoracao": "Casa e Decoração",
            "esporte": "Esporte",
            "livros": "Livros",
        })
        .fillna("Não informado")
    )
    log("Categorias padronizadas (case e espaços inconsistentes corrigidos).")
    return df


def padronizar_valor_unitario(df):
    def limpar_valor(v):
        if pd.isna(v) or str(v).strip() == "":
            return np.nan
        v = str(v).strip()
        v = v.replace("R$", "").strip()
        v = v.replace(".", "").replace(",", ".") if "," in v else v
        try:
            return float(v)
        except ValueError:
            return np.nan

    df["valor_unitario"] = df["valor_unitario"].apply(limpar_valor)
    nulos = df["valor_unitario"].isna().sum()
    log(f"Valores unitários convertidos para numérico. Nulos restantes: {nulos}")
    return df


def padronizar_datas(df):
    def parse_data(valor):
        if pd.isna(valor) or str(valor).strip() == "":
            return pd.NaT
        for fmt in ("%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"):
            try:
                return pd.to_datetime(valor, format=fmt)
            except (ValueError, TypeError):
                continue
        return pd.NaT

    df["data_pedido"] = df["data_pedido"].apply(parse_data)
    invalidas = df["data_pedido"].isna().sum()
    log(f"Datas convertidas para formato padrão (YYYY-MM-DD). Não reconhecidas: {invalidas}")
    return df


def padronizar_cep(df):
    def corrigir_cep(cep):
        if pd.isna(cep) or str(cep).strip() == "":
            return np.nan
        cep = re.sub(r"\D", "", str(cep))
        return cep.zfill(8)  # restaura zeros à esquerda perdidos

    df["cep_cliente"] = df["cep_cliente"].apply(corrigir_cep)
    log("CEPs padronizados para 8 dígitos, com zeros à esquerda restaurados.")
    return df


def tratar_quantidade(df):
    df["quantidade"] = pd.to_numeric(df["quantidade"], errors="coerce")
    log("Coluna 'quantidade' convertida para numérico.")
    return df


def tratar_nulos_categoricos(df):
    for coluna in ["forma_pagamento", "regiao"]:
        antes_nulos = df[coluna].isna().sum() + (df[coluna].astype(str).str.strip() == "").sum()
        df[coluna] = df[coluna].replace("", np.nan)
        df[coluna] = df[coluna].fillna("Não informado")
        log(f"Coluna '{coluna}': {antes_nulos} valores ausentes preenchidos como 'Não informado'.")
    return df


def calcular_coluna_derivada(df):
    df["valor_total"] = (df["quantidade"] * df["valor_unitario"]).round(2)
    log("Coluna derivada 'valor_total' calculada (quantidade x valor_unitario).")
    return df


def main():
    log("=== RELATÓRIO DE QUALIDADE E LIMPEZA DE DADOS ===\n")

    df = carregar_dados(CAMINHO_BRUTO)
    df = remover_linhas_totalmente_vazias(df)
    df = remover_duplicatas(df)
    df = padronizar_categoria(df)
    df = padronizar_valor_unitario(df)
    df = padronizar_datas(df)
    df = padronizar_cep(df)
    df = tratar_quantidade(df)
    df = tratar_nulos_categoricos(df)

    # remove linhas onde campos essenciais para análise ficaram inválidos
    antes = len(df)
    df = df.dropna(subset=["valor_unitario", "quantidade", "data_pedido"])
    log(f"\nLinhas removidas por falta de dados essenciais (valor/quantidade/data): {antes - len(df)}")

    df = calcular_coluna_derivada(df)

    df = df.sort_values("data_pedido").reset_index(drop=True)

    df.to_csv(CAMINHO_LIMPO, index=False)
    log(f"\nBase final exportada para: {CAMINHO_LIMPO}")
    log(f"Total de linhas na base tratada: {len(df)}")

    with open(CAMINHO_RELATORIO, "w", encoding="utf-8") as f:
        f.write("\n".join(relatorio))


if __name__ == "__main__":
    main()
