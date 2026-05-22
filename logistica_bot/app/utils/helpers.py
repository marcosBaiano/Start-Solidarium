"""
app/utils/helpers.py
====================
Funções utilitárias reutilizáveis em todo o projeto.
"""

import re
import uuid
from datetime import datetime


def gerar_session_id() -> str:
    """Gera um ID único de sessão."""
    return str(uuid.uuid4())


def gerar_protocolo() -> str:
    """
    Gera número de protocolo para chamados.
    Formato: CH-AAAAMMDD-XXXX
    Ex: CH-20240115-A3F2
    """
    hoje = datetime.now().strftime("%Y%m%d")
    sufixo = uuid.uuid4().hex[:4].upper()
    return f"CH-{hoje}-{sufixo}"


def validar_email(email: str) -> bool:
    """Valida formato básico de email."""
    padrao = r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$"
    return bool(re.match(padrao, email))


def sanitizar_texto(texto: str) -> str:
    """Remove caracteres potencialmente perigosos de entrada do usuário."""
    if not texto:
        return ""
    # Remove tags HTML básicas
    texto = re.sub(r"<[^>]+>", "", texto)
    return texto.strip()[:2000]  # Limita a 2000 caracteres
