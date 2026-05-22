"""
config/settings.py
==================
Configurações centrais do sistema.
Lê variáveis do arquivo .env para manter dados sensíveis fora do código.
"""

import os
from dotenv import load_dotenv

# Carrega o arquivo .env da raiz do projeto
load_dotenv()


class Config:
    """Configurações base compartilhadas por todos os ambientes."""

    # --- Flask ---
    SECRET_KEY = os.getenv("SECRET_KEY", "chave-padrao-insegura-troque-em-producao")

    # --- Banco de Dados ---
    DB_HOST     = os.getenv("DB_HOST", "localhost")
    DB_PORT     = int(os.getenv("DB_PORT", 3306))
    DB_USER     = os.getenv("DB_USER", "root")
    DB_PASSWORD = os.getenv("DB_PASSWORD", "3512")
    DB_NAME     = os.getenv("DB_NAME", "logistica")

    # String de conexão para o SQLAlchemy
    SQLALCHEMY_DATABASE_URI = (
        f"mysql+mysqlconnector://{DB_USER}:{DB_PASSWORD}"
        f"@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    )
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # --- App ---
    APP_HOST = os.getenv("APP_HOST", "0.0.0.0")
    APP_PORT = int(os.getenv("APP_PORT", 5000))


class DevelopmentConfig(Config):
    """Configurações para ambiente de desenvolvimento."""
    DEBUG = True


class ProductionConfig(Config):
    """Configurações para ambiente de produção."""
    DEBUG = False


# Mapa para selecionar o ambiente via variável FLASK_ENV
config_map = {
    "development": DevelopmentConfig,
    "production":  ProductionConfig,
}

# Configuração ativa (padrão: development)
ActiveConfig = config_map.get(os.getenv("FLASK_ENV", "development"), DevelopmentConfig)
