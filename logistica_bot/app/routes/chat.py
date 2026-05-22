"""
app/routes/chat.py
==================
Rotas do chat: página principal e endpoint da API de mensagens.
"""

from flask import Blueprint, render_template, request, jsonify, session

from app.chatbot.engine import processar_mensagem
from app.utils.helpers import gerar_session_id, sanitizar_texto

chat_bp = Blueprint("chat", __name__)


@chat_bp.route("/")
def index():
    """Página principal do chat."""
    # Cria ou recupera o session_id único do navegador
    if "session_id" not in session:
        session["session_id"] = gerar_session_id()
    return render_template("chat.html")


@chat_bp.route("/api/mensagem", methods=["POST"])
def receber_mensagem():
    """
    Endpoint que recebe mensagem do frontend e retorna resposta do bot.

    Body JSON esperado:
    { "mensagem": "texto do usuário" }

    Retorno:
    { "resposta": "texto do bot", "ok": true }
    """

    # Garante que o usuário tem session_id
    if "session_id" not in session:
        session["session_id"] = gerar_session_id()

    data = request.get_json(silent=True) or {}
    mensagem_raw = data.get("mensagem", "").strip()

    if not mensagem_raw:
        return jsonify({"ok": False, "erro": "Mensagem vazia"}), 400

    # Sanitiza antes de processar
    mensagem = sanitizar_texto(mensagem_raw)

    try:
        resposta = processar_mensagem(session["session_id"], mensagem)
        return jsonify({"ok": True, "resposta": resposta})
    except Exception as e:
        # Log do erro (em produção usaria logging adequado)
        print(f"[ERRO] processar_mensagem: {e}")
        return jsonify({
            "ok": False,
            "resposta": "Ocorreu um erro interno. Por favor, tente novamente. 🙏"
        }), 500
