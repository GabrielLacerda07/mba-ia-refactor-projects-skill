import os

SECRET_KEY = os.environ.get("SECRET_KEY", "dev-only-change-me")
DEBUG = os.environ.get("DEBUG", "true").lower() == "true"
DATABASE_PATH = os.environ.get("DATABASE_PATH", "loja.db")
HOST = os.environ.get("HOST", "0.0.0.0")
PORT = int(os.environ.get("PORT", "5000"))

CATEGORIAS_VALIDAS = [
    "informatica",
    "moveis",
    "vestuario",
    "geral",
    "eletronicos",
    "livros",
]

STATUS_PEDIDO_VALIDOS = ["pendente", "aprovado", "enviado", "entregue", "cancelado"]

# Faixas de desconto do relatório de vendas
DESCONTO_TIER_HIGH = 10_000
DESCONTO_RATE_HIGH = 0.10
DESCONTO_TIER_MID = 5_000
DESCONTO_RATE_MID = 0.05
DESCONTO_TIER_LOW = 1_000
DESCONTO_RATE_LOW = 0.02

NOME_MIN_LEN = 2
NOME_MAX_LEN = 200
