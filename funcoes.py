import re
from datetime import datetime

def limpar_categoria(texto: str) -> str:
    """
    Padroniza o nome da categoria: converte para minúsculas, remove espaços
    nas extremidades e elimina caracteres especiais usando Regex, 
    mantendo letras, números e underlines.
    """
    if not texto or texto.strip() == "":
        return "sem categoria"
    
    # Converte para minúsculas e remove espaços sobressalentes nas pontas
    texto_limpo = texto.lower().strip()
    
    # Regex: Mantém apenas caracteres alfanuméricos e espaços, removendo pontuações especiais
    # Substitui o que não for letra, número ou espaço por vazio
    texto_limpo = re.sub(r'[^\w\s]', '', texto_limpo)
    
    return texto_limpo

def tratar_dimensoes_fisicas(valor_str: str) -> float:
    """
    Trata os valores numéricos das dimensões físicas do produto.
    Técnica escolhida: Atribuição de valor padrão (0.0) em caso de nulo.
    Justificativa: Descartar a linha inteira faria a Olist perder o histórico de vendas
    daquele produto. Como não temos a média pré-calculada em tempo real na leitura linha a linha,
    definir como 0.0 sinaliza uma inconsistência técnica sem interromper o pipeline.
    """
    if not valor_str or valor_str.strip() == "":
        return 0.0
    try:
        return float(valor_str)
    except ValueError:
        return 0.0

def formatar_data_br(data_original: str) -> str:
    """
    Converte uma string de data no formato 'YYYY-MM-DD HH:MM:SS'
    para o formato brasileiro simplificado 'DD/MM/YYYY'.
    Se estiver vazia, retorna uma string indicando a ausência.
    """
    if not data_original or data_original.strip() == "":
        return "Data não disponível"
    
    try:
        # Faz o parsing da string original
        objeto_data = datetime.strptime(data_original.strip(), "%Y-%m-%d %H:%M:%S")
        # Formata para o padrão brasileiro
        return objeto_data.strftime("%d/%m/%Y")
    except ValueError:
        # Caso a string venha em outro formato inesperado
        return "Formato inválido"

def validar_hipotese_cancelamento(order_status: str, data_entrega: str) -> bool:
    """
    Verifica se a ausência de data de entrega é estritamente motivada pelo status 'canceled'.
    Retorna True se o status for cancelado, e False caso a data esteja nula por outro motivo
    (ex: pedido ainda em trânsito/shipped).
    """
    status_limpo = order_status.strip().lower()
    data_vazia = (not data_entrega or data_entrega.strip() == "")
    
    if data_vazia and status_limpo == "canceled":
        return True
    return False