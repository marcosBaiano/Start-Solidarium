"""
app/database/models.py
======================
Todos os modelos do banco de dados (tabelas) definidos com SQLAlchemy.
Cada classe = uma tabela no MySQL.
"""

from datetime import datetime
from app.database.db import db


# ──────────────────────────────────────────────────────────────
# USUÁRIOS
# ──────────────────────────────────────────────────────────────
class Usuario(db.Model):
    __tablename__ = "usuarios"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    session_id = db.Column(db.String(100), unique=True, nullable=False)   # ID da sessão do browser
    nome       = db.Column(db.String(100), nullable=True)
    email      = db.Column(db.String(150), nullable=True)
    telefone   = db.Column(db.String(20), nullable=True)
    ativo      = db.Column(db.Boolean, default=True)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    # Relacionamentos
    mensagens = db.relationship("Mensagem", backref="usuario", lazy=True)
    sessoes   = db.relationship("Sessao",   backref="usuario", lazy=True)
    chamados  = db.relationship("Chamado",  backref="usuario", lazy=True)

    def __repr__(self):
        return f"<Usuario {self.nome or self.session_id}>"


# ──────────────────────────────────────────────────────────────
# INTENÇÕES (cérebro do bot)
# ──────────────────────────────────────────────────────────────
class Intencao(db.Model):
    __tablename__ = "intencoes"

    id             = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nome           = db.Column(db.String(100), nullable=False, unique=True)
    palavras_chave = db.Column(db.Text, nullable=False)   # JSON: ["oi","olá","hello"]
    resposta       = db.Column(db.Text, nullable=False)   # Pode conter {nome} para personalizar
    contexto       = db.Column(db.String(100), nullable=True)  # Contexto gerado após resposta
    prioridade     = db.Column(db.Integer, default=0)     # Maior = avaliado primeiro
    ativo          = db.Column(db.Boolean, default=True)
    criado_em      = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Intencao {self.nome}>"


# ──────────────────────────────────────────────────────────────
# MENSAGENS (histórico de conversas)
# ──────────────────────────────────────────────────────────────
class Mensagem(db.Model):
    __tablename__ = "mensagens"

    id                 = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id         = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    mensagem           = db.Column(db.Text, nullable=False)      # O que o usuário enviou
    resposta           = db.Column(db.Text, nullable=True)       # O que o bot respondeu
    intencao_detectada = db.Column(db.String(100), nullable=True)
    criado_em          = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Mensagem usuario={self.usuario_id}>"


# ──────────────────────────────────────────────────────────────
# PEDIDOS
# ──────────────────────────────────────────────────────────────
class Pedido(db.Model):
    __tablename__ = "pedidos"

    id              = db.Column(db.Integer, primary_key=True, autoincrement=True)
    codigo_rastreio = db.Column(db.String(50), unique=True, nullable=False)
    usuario_id      = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=True)
    descricao       = db.Column(db.String(255), nullable=True)
    status          = db.Column(db.String(50), default="Em processamento")
    origem          = db.Column(db.String(150), nullable=True)
    destino         = db.Column(db.String(150), nullable=True)
    previsao        = db.Column(db.DateTime, nullable=True)
    criado_em       = db.Column(db.DateTime, default=datetime.utcnow)
    atualizado_em   = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    historico = db.relationship("HistoricoRastreio", backref="pedido", lazy=True)

    def __repr__(self):
        return f"<Pedido {self.codigo_rastreio}>"


# ──────────────────────────────────────────────────────────────
# HISTÓRICO DE RASTREIO
# ──────────────────────────────────────────────────────────────
class HistoricoRastreio(db.Model):
    __tablename__ = "historico_rastreio"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    pedido_id   = db.Column(db.Integer, db.ForeignKey("pedidos.id"), nullable=False)
    status      = db.Column(db.String(100), nullable=False)
    localizacao = db.Column(db.String(200), nullable=True)
    descricao   = db.Column(db.Text, nullable=True)
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<HistoricoRastreio pedido={self.pedido_id}>"


# ──────────────────────────────────────────────────────────────
# CHAMADOS DE SUPORTE
# ──────────────────────────────────────────────────────────────
class Chamado(db.Model):
    __tablename__ = "chamados"

    id          = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id  = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    protocolo   = db.Column(db.String(20), unique=True, nullable=False)  # Ex: CH-20240101-001
    assunto     = db.Column(db.String(255), nullable=True)
    descricao   = db.Column(db.Text, nullable=True)
    status      = db.Column(db.String(50), default="Aberto")  # Aberto / Em andamento / Encerrado
    criado_em   = db.Column(db.DateTime, default=datetime.utcnow)
    encerrado_em = db.Column(db.DateTime, nullable=True)

    def __repr__(self):
        return f"<Chamado {self.protocolo}>"


# ──────────────────────────────────────────────────────────────
# SESSÕES DE CONVERSA
# ──────────────────────────────────────────────────────────────
class Sessao(db.Model):
    __tablename__ = "sessoes"

    id           = db.Column(db.Integer, primary_key=True, autoincrement=True)
    usuario_id   = db.Column(db.Integer, db.ForeignKey("usuarios.id"), nullable=False)
    contexto     = db.Column(db.String(100), nullable=True)   # Ex: "aguardando_codigo_rastreio"
    dados_temp   = db.Column(db.Text, nullable=True)          # JSON com dados temporários
    iniciada_em  = db.Column(db.DateTime, default=datetime.utcnow)
    atualizada_em = db.Column(db.DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)

    def __repr__(self):
        return f"<Sessao usuario={self.usuario_id} ctx={self.contexto}>"


# ──────────────────────────────────────────────────────────────
# CONFIGURAÇÕES DO SISTEMA
# ──────────────────────────────────────────────────────────────
class Configuracao(db.Model):
    __tablename__ = "configuracoes"

    id        = db.Column(db.Integer, primary_key=True, autoincrement=True)
    chave     = db.Column(db.String(100), unique=True, nullable=False)
    valor     = db.Column(db.Text, nullable=True)
    descricao = db.Column(db.String(255), nullable=True)

    def __repr__(self):
        return f"<Config {self.chave}={self.valor}>"


# ──────────────────────────────────────────────────────────────
# LOGS DO SISTEMA
# ──────────────────────────────────────────────────────────────
class Log(db.Model):
    __tablename__ = "logs"

    id         = db.Column(db.Integer, primary_key=True, autoincrement=True)
    nivel      = db.Column(db.String(20), nullable=False)   # INFO / WARNING / ERROR
    modulo     = db.Column(db.String(100), nullable=True)
    mensagem   = db.Column(db.Text, nullable=False)
    criado_em  = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f"<Log {self.nivel}: {self.mensagem[:40]}>"
