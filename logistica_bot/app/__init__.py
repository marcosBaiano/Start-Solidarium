"""
app/__init__.py
===============
Factory function do Flask.
Centraliza a criação e configuração da aplicação.
"""

from flask import Flask
from config.settings import ActiveConfig
from app.database.db import db


def create_app() -> Flask:
    """
    Cria e configura a aplicação Flask.
    Padrão Application Factory — facilita testes e múltiplos ambientes.
    """

    app = Flask(__name__, template_folder="templates", static_folder="static")

    # ── Configurações ─────────────────────────────────────────
    app.config.from_object(ActiveConfig)

    # ── Banco de dados ────────────────────────────────────────
    db.init_app(app)

    with app.app_context():
        # Cria as tabelas se ainda não existirem
        db.create_all()

    # ── Rotas / Blueprints ────────────────────────────────────
    from app.routes.chat import chat_bp
    app.register_blueprint(chat_bp)

    return app
