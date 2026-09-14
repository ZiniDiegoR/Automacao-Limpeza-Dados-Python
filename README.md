# Automação de Limpeza de Dados de Vendas — Python

Projeto de portfólio: uma rotina de limpeza e padronização de dados de vendas construída com Python e Pandas, cobrindo o fluxo completo — da base bruta com problemas reais de qualidade até uma base tratada, pronta para análise.

## 🎯 Objetivo

Praticar o fluxo completo de tratamento de dados fora de ferramentas visuais (Power Query/Excel), usando Python e Pandas para automatizar a limpeza de uma base com problemas comuns em dados do mundo real, documentando cada etapa em um relatório de qualidade.

## 🧹 Problemas encontrados na base bruta

A base (`vendas_brutas.csv`) simula um extrato de pedidos de e-commerce e contém:

- Categorias com capitalização e espaçamento inconsistentes (ex: `"ESPORTE"`, `" Esporte "`, `"esporte"`)
- Datas em múltiplos formatos na mesma coluna (`31/08/2024`, `2024-03-12`, `16-11-24`)
- Valores monetários armazenados como texto, com símbolo `R$` e vírgula decimal
- CEPs perdendo o zero à esquerda (efeito comum de leitura como número)
- Linhas duplicadas e linhas totalmente vazias
- Valores ausentes em colunas categóricas e numéricas

## ⚙️ O que o script faz (`limpar_dados.py`)

1. Remove linhas totalmente vazias e duplicatas exatas
2. Padroniza a coluna `categoria` (case, espaços e grafias diferentes → um único valor canônico)
3. Converte `valor_unitario` para numérico, tratando o formato `R$ 1.234,56`
4. Converte `data_pedido` reconhecendo múltiplos formatos de data e padronizando para `YYYY-MM-DD`
5. Restaura os zeros à esquerda dos CEPs e mantém apenas dígitos
6. Preenche valores ausentes em colunas categóricas com `"Não informado"`, de forma explícita e rastreável
7. Remove registros sem os dados essenciais para análise (valor, quantidade ou data)
8. Cria a coluna derivada `valor_total` (quantidade × valor unitário)
9. Gera um `relatorio_qualidade.txt` com o resumo de tudo que foi encontrado e corrigido

## 📊 Análise exploratória (`analise_exploratoria.py`)

Um exemplo simples de uso da base já tratada: cálculo de faturamento por categoria e geração do gráfico `faturamento_por_categoria.png`, mostrando que a base limpa está pronta para gerar indicadores de negócio.

## 🗂 Estrutura do projeto
