"""
app/chatbot/detector.py
=======================
Motor de detecção de intenções.
Compara a mensagem do usuário com as palavras-chave cadastradas no banco.
"""

import json
from app.database.models import Intencao


def detectar_intencao(mensagem: str) -> Intencao | None:
    """
    Detecta a intenção da mensagem comparando com palavras-chave do banco.

    Algoritmo:
    1. Normaliza a mensagem (minúsculas, sem acentos simples)
    2. Para cada intenção ativa (ordem de prioridade desc), verifica
       se alguma palavra-chave está contida na mensagem
    3. Retorna a primeira intenção que der match

    Retorna None se nenhuma intenção for encontrada (aciona fallback).
    """

    texto = _normalizar(mensagem)

    # Busca todas as intenções ativas, ordenadas por prioridade (maior primeiro)
    # Exclui o fallback da busca normal (ele é tratado separadamente)
    intencoes = (
        Intencao.query
        .filter_by(ativo=True)
        .filter(Intencao.nome != "fallback")
        .order_by(Intencao.prioridade.desc())
        .all()
    )

    for intencao in intencoes:
        try:
            palavras = json.loads(intencao.palavras_chave)
        except (json.JSONDecodeError, TypeError):
            continue

        for palavra in palavras:
            if _normalizar(palavra) in texto:
                return intencao

    # Nenhuma intenção encontrada → retorna o fallback
    return Intencao.query.filter_by(nome="fallback", ativo=True).first()


def _normalizar(texto: str) -> str:
    """
    Normaliza texto para comparação:
    - Minúsculas
    - Remove espaços extras
    - Substitui caracteres acentuados comuns
    """
    if not texto:
        return ""

    texto = texto.lower().strip()

    substituicoes = {
        "á": "a", "à": "a", "â": "a", "ã": "a",
        "é": "e", "ê": "e",
        "í": "i", "î": "i",
        "ó": "o", "ô": "o", "õ": "o",
        "ú": "u", "û": "u",
        "ç": "c",
    }

    for acentuado, simples in substituicoes.items():
        texto = texto.replace(acentuado, simples)

    return texto
