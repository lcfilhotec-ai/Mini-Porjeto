import csv
from funcoes import (
    limpar_categoria, 
    tratar_dimensoes_fisicas, 
    formatar_data_br, 
    validar_hipotese_cancelamento
)

def processar_pipeline():
    # Contadores para o relatório estatístico manual
    linhas_produtos = 0
    linhas_pedidos = 0
    nulos_categoria_corrigidos = 0
    nulos_dimensoes_corrigidos = 0
    pedidos_cancelados_confirmados = 0
    pedidos_nao_entregues_outros_motivos = 0

    print("=== INICIANDO PIPELINE DE SANITIZAÇÃO OLIST ===")

    # 1. PROCESSAMENTO DO DATASET DE PRODUTOS
    try:
        with open('olist_products_dataset.csv', mode='r', encoding='utf-8') as f_in:
            leitor = csv.DictReader(f_in)
            
            # Simulação do "Load" - salvando os dados limpos em uma lista na memória
            produtos_sanitizados = []
            
            for linha in leitor:
                linhas_produtos += 1
                
                # Cópia para não mutar o dicionário original diretamente de forma desordenada
                produto_limpo = {}
                produto_limpo['product_id'] = linha['product_id']
                
                # Validação de Categoria
                cat_original = linha['product_category_name']
                if not cat_original or cat_original.strip() == "":
                    nulos_categoria_corrigidos += 1
                    produto_limpo['product_category_name'] = "sem categoria"
                else:
                    produto_limpo['product_category_name'] = limpar_categoria(cat_original)
                
                # Validação de Dimensões Físicas
                # Se o valor original for vazio, incrementa o contador de correções
                for campo in ['product_weight_g', 'product_length_cm', 'product_height_cm', 'product_width_cm']:
                    if not linha[campo] or linha[campo].strip() == "":
                        nulos_dimensoes_corrigidos += 1
                    produto_limpo[campo] = tratar_dimensoes_fisicas(linha[campo])
                
                produtos_sanitizados.append(produto_limpo)
                
        print("[SUCESSO] Dataset de produtos processado.")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'olist_products_dataset.csv' não encontrado no diretório atual.")

    # 2. PROCESSAMENTO DO DATASET DE PEDIDOS
    try:
        with open('olist_orders_dataset.csv', mode='r', encoding='utf-8') as f_in:
            leitor = csv.DictReader(f_in)
            pedidos_sanitizados = []
            
            for linha in leitor:
                linhas_pedidos += 1
                pedido_limpo = {}
                
                pedido_limpo['order_id'] = linha['order_id']
                pedido_limpo['customer_id'] = linha['customer_id']
                pedido_limpo['order_status'] = linha['order_status'].strip().lower()
                
                # Formatação Temporal
                pedido_limpo['order_approved_at_br'] = formatar_data_br(linha['order_approved_at'])
                
                # Validação da Regra de Negócio (Datas de entrega vazias)
                dt_entrega = linha['order_delivered_customer_date']
                status = linha['order_status']
                
                if not dt_entrega or dt_entrega.strip() == "":
                    # Testando a hipótese da diretoria
                    if validar_hipotese_cancelamento(status, dt_entrega):
                        pedidos_cancelados_confirmados += 1
                    else:
                        pedidos_nao_entregues_outros_motivos += 1
                        
                pedido_limpo['order_delivered_customer_date'] = dt_entrega if dt_entrega else "Não entregue"
                pedidos_sanitizados.append(pedido_limpo)
                
        print("[SUCESSO] Dataset de pedidos processado.")
    except FileNotFoundError:
        print("[ERRO] Arquivo 'olist_orders_dataset.csv' não encontrado no diretório atual.")

    # 3. RELATÓRIO DE STATUS MANUAL (SUMÁRIO ESTATÍSTICO)
    print("\n" + "="*40)
    print("         SUMÁRIO ESTATÍSTICO DO PIPELINE")
    print("="*40)
    print(f"Total de linhas lidas (Produtos):       {linhas_produtos}")
    print(f"Total de linhas lidas (Pedidos):        {linhas_pedidos}")
    print("-" * 40)
    print(f"Categorias vazias corrigidas:          {nulos_categoria_corrigidos}")
    print(f"Dimensões físicas nulas corrigidas:    {nulos_dimensoes_corrigidos}")
    print("-" * 40)
    print(f"Pedidos cancelados (sem data entrega):  {pedidos_cancelados_confirmados}")
    print(f"Pedidos não entregues por outra razão: {pedidos_nao_entregues_outros_motivos}")
    print("  *(ex: pedidos ainda em rota ou processamento)")
    print("-" * 40)
    
    # Conclusão lógica sobre a hipótese de negócio
    print("ANÁLISE DA HIPÓTESE DA DIRETORIA:")
    if pedidos_nao_entregues_outros_motivos > 0:
        print("=> HIPÓTESE REJEITADA: Nem toda data de entrega nula se deve a um pedido cancelado.")
        print("   Existem pedidos com datas nulas que estão com status 'shipped', 'processing', etc.")
    else:
        print("=> HIPÓTESE CONFIRMADA: Todas as datas de entrega nulas são de pedidos cancelados.")
    print("="*40)

if __name__ == "__main__":
    processar_pipeline()