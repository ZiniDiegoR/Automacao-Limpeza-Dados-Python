"""
Gera uma base de dados de vendas com problemas reais de qualidade,
para servir de matéria-prima do projeto de limpeza de dados.
"""
import csv
import random

random.seed(42)

categorias_variacoes = {
    "Eletrônicos": ["Eletrônicos", "eletronicos", " Eletrônicos ", "ELETRÔNICOS", "Eletronicos"],
    "Moda": ["Moda", "moda", " Moda", "MODA"],
    "Casa e Decoração": ["Casa e Decoração", "casa e decoracao", "Casa e decoração ", "CASA E DECORAÇÃO"],
    "Esporte": ["Esporte", "esporte", " Esporte ", "ESPORTE"],
    "Livros": ["Livros", "livros", " Livros", "LIVROS"],
}

formas_pagamento = ["Cartão de Crédito", "Boleto", "Pix", "Cartão de Débito"]
regioes = ["Sudeste", "Sul", "Nordeste", "Centro-Oeste", "Norte"]

formatos_data = ["%d/%m/%Y", "%Y-%m-%d", "%d-%m-%Y", "%d/%m/%y"]

produtos = [
    ("Fone de Ouvido Bluetooth", "Eletrônicos", 129.90),
    ("Smartwatch Fit", "Eletrônicos", 349.90),
    ("Camiseta Básica", "Moda", 49.90),
    ("Tênis de Corrida", "Esporte", 259.90),
    ("Jogo de Panelas", "Casa e Decoração", 189.90),
    ("Livro - Hábitos Atômicos", "Livros", 44.90),
    ("Mochila Executiva", "Moda", 159.90),
    ("Cafeteira Elétrica", "Casa e Decoração", 219.90),
    ("Bicicleta Ergométrica", "Esporte", 899.90),
    ("Carregador Portátil", "Eletrônicos", 79.90),
    ("Livro - O Poder do Hábito", "Livros", 39.90),
    ("Luminária de Mesa", "Casa e Decoração", 89.90),
]

import datetime

def data_aleatoria():
    inicio = datetime.date(2024, 1, 1)
    dias = random.randint(0, 364)
    return inicio + datetime.timedelta(days=dias)

def formatar_data_suja(data):
    fmt = random.choice(formatos_data)
    return data.strftime(fmt)

def cep_sujo():
    cep = f"{random.randint(1000, 9999):04d}{random.randint(0,999):03d}"
    # às vezes perde o zero à esquerda (como se tivesse sido lido como número)
    if random.random() < 0.3 and cep.startswith("0"):
        return cep.lstrip("0")
    return cep

def valor_sujo(valor):
    # às vezes vem como texto com "R$" e vírgula decimal
    if random.random() < 0.4:
        return f"R$ {valor:.2f}".replace(".", ",")
    return f"{valor:.2f}"

linhas = []
pedido_id = 1000

for i in range(600):
    produto, categoria, preco = random.choice(produtos)
    categoria_suja = random.choice(categorias_variacoes[categoria])
    quantidade = random.choice([1, 1, 1, 2, 2, 3])
    data = data_aleatoria()
    linha = {
        "id_pedido": pedido_id,
        "produto": produto,
        "categoria": categoria_suja,
        "quantidade": quantidade,
        "valor_unitario": valor_sujo(preco),
        "forma_pagamento": random.choice(formas_pagamento),
        "regiao": random.choice(regioes),
        "cep_cliente": cep_sujo(),
        "data_pedido": formatar_data_suja(data),
    }
    linhas.append(linha)
    pedido_id += 1

    # injeta duplicatas propositais (~3%)
    if random.random() < 0.03:
        linhas.append(dict(linha))

    # injeta linhas com valores nulos (~4%)
    if random.random() < 0.04:
        linha_nula = dict(linha)
        linha_nula["id_pedido"] = pedido_id
        pedido_id += 1
        campo_nulo = random.choice(["valor_unitario", "forma_pagamento", "cep_cliente"])
        linha_nula[campo_nulo] = ""
        linhas.append(linha_nula)

# injeta algumas linhas totalmente vazias
for _ in range(5):
    linhas.append({k: "" for k in linhas[0].keys()})

random.shuffle(linhas)

campos = ["id_pedido", "produto", "categoria", "quantidade", "valor_unitario",
          "forma_pagamento", "regiao", "cep_cliente", "data_pedido"]

with open("/home/claude/projeto_python/dados/vendas_brutas.csv", "w", newline="", encoding="utf-8") as f:
    writer = csv.DictWriter(f, fieldnames=campos)
    writer.writeheader()
    for linha in linhas:
        writer.writerow(linha)

print(f"Gerado: {len(linhas)} linhas em dados/vendas_brutas.csv")
