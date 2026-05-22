"""
app/chatbot/engine.py
=====================
Motor conversacional principal.
Orquestra: contexto → cadastro → intenção → resposta.
"""

import json
from datetime import datetime

from app.database.db import db
from app.database.models import Usuario, Mensagem, Sessao, Pedido, HistoricoRastreio, Chamado
from app.chatbot.detector import detectar_intencao
from app.utils.helpers import gerar_protocolo, validar_email


# ──────────────────────────────────────────────────────────────
# PONTO DE ENTRADA PRINCIPAL
# ──────────────────────────────────────────────────────────────

def processar_mensagem(session_id: str, mensagem: str) -> str:
    """
    Recebe a mensagem do usuário e retorna a resposta do bot.

    Fluxo:
    1. Busca/cria usuário pelo session_id
    2. Busca contexto ativo da sessão
    3. Se há contexto → processa o contexto (ex: aguardando nome)
    4. Se não → detecta intenção e responde
    5. Salva a mensagem no histórico
    """

    usuario  = _obter_ou_criar_usuario(session_id)
    sessao   = _obter_sessao(usuario.id)
    contexto = sessao.contexto if sessao else None

    resposta  = ""
    intencao_nome = None

    # ── 1. Fluxo de cadastro de usuário ───────────────────────
    if contexto == "aguardando_nome":
        resposta = _receber_nome(usuario, sessao, mensagem)

    elif contexto == "aguardando_email":
        resposta = _receber_email(usuario, sessao, mensagem)

    elif contexto == "aguardando_telefone":
        resposta = _receber_telefone(usuario, sessao, mensagem)

    # ── 2. Fluxos de rastreio / status / localização ──────────
    elif contexto in ("aguardando_codigo_rastreio", "aguardando_codigo_status", "aguardando_codigo_localizacao"):
        resposta = _processar_rastreio(usuario, sessao, mensagem, contexto)

    # ── 3. Fluxo de chamado de suporte ────────────────────────
    elif contexto == "aguardando_descricao_chamado":
        resposta = _abrir_chamado(usuario, sessao, mensagem)

    # ── 4. Sem contexto → detectar intenção ───────────────────
    else:
        intencao = detectar_intencao(mensagem)
        if intencao:
            intencao_nome = intencao.nome
            resposta = _personalizar_resposta(intencao.resposta, usuario)
            _atualizar_contexto(sessao, intencao.contexto)
        else:
            resposta = "Não entendi. Como posso ajudar? 😊"

    # ── 5. Salvar mensagem no histórico ───────────────────────
    _salvar_mensagem(usuario.id, mensagem, resposta, intencao_nome)

    return resposta


# ──────────────────────────────────────────────────────────────
# CADASTRO DE USUÁRIO (etapas)
# ──────────────────────────────────────────────────────────────

def _receber_nome(usuario: Usuario, sessao: Sessao, mensagem: str) -> str:
    nome = mensagem.strip().title()
    if len(nome) < 2:
        return "Por favor, informe seu nome completo. 😊"

    usuario.nome = nome
    db.session.commit()
    _atualizar_contexto(sessao, "aguardando_email")
    return f"Prazer, {nome}! 😊 Qual é o seu email?"


def _receber_email(usuario: Usuario, sessao: Sessao, mensagem: str) -> str:
    email = mensagem.strip().lower()

    if not validar_email(email):
        return "Por favor, informe um email válido. 📧"

    usuario.email = email
    db.session.commit()
    _atualizar_contexto(sessao, "aguardando_telefone")
    return "Ótimo! 👍 Para finalizar, qual é o seu telefone? (opcional — pode digitar 'pular')"


def _receber_telefone(usuario: Usuario, sessao: Sessao, mensagem: str) -> str:
    texto = mensagem.strip().lower()

    if texto not in ("pular", "nao", "não", "-", "skip"):
        usuario.telefone = mensagem.strip()
        db.session.commit()

    # Cadastro concluído → limpa contexto e segue atendimento
    _atualizar_contexto(sessao, None)
    return f"Perfeito, {usuario.nome}! 🎉 Como posso ajudar você hoje?\n\n📦 Rastrear pedido\n📊 Status da entrega\n📍 Localização\n👨‍💻 Abrir chamado"


# ──────────────────────────────────────────────────────────────
# RASTREIO DE PEDIDO
# ──────────────────────────────────────────────────────────────

def _processar_rastreio(usuario: Usuario, sessao: Sessao, codigo: str, contexto: str) -> str:
    codigo = codigo.strip().upper()

    pedido = Pedido.query.filter_by(codigo_rastreio=codigo).first()

    if not pedido:
        _atualizar_contexto(sessao, None)
        return (
            f"Não encontrei o pedido com código *{codigo}*. 😕\n"
            "Verifique se digitou corretamente e tente novamente.\n\n"
            "Posso ajudar com mais alguma coisa?"
        )

    # Busca os eventos de rastreio ordenados por data
    eventos = (
        HistoricoRastreio.query
        .filter_by(pedido_id=pedido.id)
        .order_by(HistoricoRastreio.criado_em.desc())
        .all()
    )

    _atualizar_contexto(sessao, None)

    if contexto == "aguardando_codigo_localizacao":
        # Resposta focada em localização
        ultimo = eventos[0] if eventos else None
        local  = ultimo.localizacao if ultimo else "Não disponível"
        return (
            f"📍 *Localização atual do pedido {codigo}:*\n\n"
            f"📦 Produto: {pedido.descricao or 'Não informado'}\n"
            f"🏙️  Localização: {local}\n"
            f"🔄 Status: {pedido.status}\n\n"
            "Posso ajudar com mais alguma coisa?"
        )

    # Resposta de rastreio completo / status
    historico_txt = ""
    for evento in eventos[:5]:
        data = evento.criado_em.strftime("%d/%m/%Y %H:%M")
        historico_txt += f"\n• {data} — {evento.status}"
        if evento.localizacao:
            historico_txt += f" ({evento.localizacao})"

    return (
        f"📦 *Rastreio do pedido {codigo}:*\n\n"
        f"🏷️  Descrição: {pedido.descricao or 'Não informado'}\n"
        f"🔄 Status atual: *{pedido.status}*\n"
        f"📍 Origem: {pedido.origem or 'Não informado'}\n"
        f"🎯 Destino: {pedido.destino or 'Não informado'}\n\n"
        f"📋 *Histórico:{historico_txt}*\n\n"
        "Posso ajudar com mais alguma coisa?"
    )


# ──────────────────────────────────────────────────────────────
# CHAMADO DE SUPORTE
# ──────────────────────────────────────────────────────────────

def _abrir_chamado(usuario: Usuario, sessao: Sessao, descricao: str) -> str:
    protocolo = gerar_protocolo()

    chamado = Chamado(
        usuario_id=usuario.id,
        protocolo=protocolo,
        assunto="Chamado via chatbot",
        descricao=descricao.strip(),
        status="Aberto",
    )
    db.session.add(chamado)
    db.session.commit()

    _atualizar_contexto(sessao, None)

    return (
        f"✅ Chamado aberto com sucesso!\n\n"
        f"🎫 *Protocolo: {protocolo}*\n"
        f"📋 Status: Aberto\n\n"
        "Nossa equipe entrará em contato em breve. "
        "Guarde seu número de protocolo para acompanhamento.\n\n"
        "Posso ajudar com mais alguma coisa?"
    )


# ──────────────────────────────────────────────────────────────
# FUNÇÕES AUXILIARES INTERNAS
# ──────────────────────────────────────────────────────────────

def _obter_ou_criar_usuario(session_id: str) -> Usuario:
    """Busca usuário pelo session_id ou cria novo."""
    usuario = Usuario.query.filter_by(session_id=session_id).first()
    if not usuario:
        usuario = Usuario(session_id=session_id)
        db.session.add(usuario)
        db.session.commit()
    return usuario


def _obter_sessao(usuario_id: int) -> Sessao:
    """Busca ou cria sessão ativa para o usuário."""
    sessao = Sessao.query.filter_by(usuario_id=usuario_id).first()
    if not sessao:
        sessao = Sessao(usuario_id=usuario_id, contexto=None)
        db.session.add(sessao)
        db.session.commit()
    return sessao


def _atualizar_contexto(sessao: Sessao, novo_contexto: str | None):
    """Atualiza o contexto da sessão no banco."""
    sessao.contexto      = novo_contexto
    sessao.atualizada_em = datetime.utcnow()
    db.session.commit()


def _personalizar_resposta(resposta: str, usuario: Usuario) -> str:
    """Substitui variáveis dinâmicas na resposta (ex: {nome})."""
    return resposta.replace("{nome}", usuario.nome or "")


def _salvar_mensagem(usuario_id: int, mensagem: str, resposta: str, intencao: str | None):
    """Persiste a conversa no histórico de mensagens."""
    msg = Mensagem(
        usuario_id=usuario_id,
        mensagem=mensagem,
        resposta=resposta,
        intencao_detectada=intencao,
    )
    db.session.add(msg)
    db.session.commit()
