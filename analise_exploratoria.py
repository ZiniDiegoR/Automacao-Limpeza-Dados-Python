"""
Análise exploratória rápida sobre a base já tratada (dados/vendas_tratadas.csv).
Gera um gráfico de faturamento por categoria como exemplo de uso da base limpa.
"""

import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("dados/vendas_tratadas.csv", parse_dates=["data_pedido"])

resumo_categoria = (
    df.groupby("categoria")["valor_total"]
    .sum()
    .sort_values(ascending=False)
)

print("Faturamento por categoria:")
print(resumo_categoria.round(2))

plt.figure(figsize=(8, 5))
resumo_categoria.plot(kind="bar", color="#1F3864")
plt.title("Faturamento por Categoria")
plt.ylabel("Faturamento (R$)")
plt.xlabel("Categoria")
plt.xticks(rotation=30, ha="right")
plt.tight_layout()
plt.savefig("faturamento_por_categoria.png", dpi=150)
print("\nGráfico salvo em faturamento_por_categoria.png")
