# Pipeline de Sanitização de Dados - Olist (Black Friday)

## 📝 Descrição do Projeto
Este projeto foi desenvolvido para atender a uma necessidade crítica da equipe de Engenharia de Dados da Olist às vésperas da Black Friday. Com o aumento massivo no volume de transações, inconsistências ("dados sujos") nos arquivos `olist_products_dataset.csv` e `olist_orders_dataset.csv` estavam travando os relatórios automatizados de Business Intelligence e ameaçando a qualidade de futuros modelos de Machine Learning.

O objetivo deste script em Python é construir um pipeline de ETL (Extract, Transform, Load) puramente **nativo**, ou seja, sem a utilização de bibliotecas externas como o *Pandas*. O script realiza o tratamento de valores nulos, padronização de strings por meio de Expressões Regulares (Regex), conversão e formatação temporal (`datetime`), e valida hipóteses de regras de negócio estipuladas pela diretoria.

---

## 🚀 Guia de Execução

### Pré-requisitos
* Ter o Python instalado em sua máquina.
* Garantir que os arquivos de dados estejam na **mesma pasta** que os arquivos de código (`main.py` e `funcoes.py`). Os nomes dos arquivos devem ser rigorosamente:
  * `olist_products_dataset.csv`
  * `olist_orders_dataset.csv`

### Como Rodar o Pipeline
1. Abra o terminal do seu sistema operacional ou o terminal da sua IDE (VS Code, PyCharm, etc.).
2. Navegue até o diretório onde os arquivos do projeto estão salvos.
3. Execute o script principal utilizando o comando:
```bash
python main.py
