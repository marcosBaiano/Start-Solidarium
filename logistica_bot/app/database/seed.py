"""
app/database/seed.py
====================
Popula o banco com dados iniciais obrigatórios:
  - Intenções do bot
  - Pedidos de exemplo
  - Configurações padrão
Execute via: python seed.py (na raiz do projeto)
"""

import json
import sys
import os

# Garante que o diretório raiz está no path
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../../..")))

from app import create_app
from app.database.db import db
from app.database.models import Intencao, Pedido, HistoricoRastreio, Configuracao


def seed_intencoes():
    """Cadastra todas as intenções do bot no banco."""

    intencoes = [
        # ── SAUDAÇÃO ──────────────────────────────────────────────
        {
            "nome": "saudacao",
            "palavras_chave": json.dumps([
                "oi", "olá", "ola", "hello", "hi", "bom dia", "boa tarde",
                "boa noite", "eae", "opa", "e ai", "eaí", "salve"
            ]),
            "resposta": "Olá! 👋 Seja bem-vindo ao suporte logístico. Qual é o seu nome?",
            "contexto": "aguardando_nome",
            "prioridade": 10,
        },

        # ── RASTREIO ──────────────────────────────────────────────
        {
            "nome": "rastreio",
            "palavras_chave": json.dumps([
                "rastrear", "rastreio", "rastreamento", "tracking",
                "onde está meu pedido", "consultar entrega", "onde esta",
                "localizar pedido", "acompanhar pedido"
            ]),
            "resposta": "Claro! 📦 Por favor, informe o código de rastreio do seu pedido.",
            "contexto": "aguardando_codigo_rastreio",
            "prioridade": 9,
        },

        # ── STATUS ────────────────────────────────────────────────
        {
            "nome": "status",
            "palavras_chave": json.dumps([
                "status", "andamento", "situação", "situacao",
                "como está", "como esta", "meu pedido", "atualização", "atualizacao"
            ]),
            "resposta": "Vou verificar o status para você. 📊 Qual é o código do seu pedido?",
            "contexto": "aguardando_codigo_status",
            "prioridade": 8,
        },

        # ── LOCALIZAÇÃO ───────────────────────────────────────────
        {
            "nome": "localizacao",
            "palavras_chave": json.dumps([
                "localização", "localizacao", "rota", "onde está",
                "onde esta", "cidade", "localização do produto",
                "onde fica", "endereço", "endereco"
            ]),
            "resposta": "Vou buscar a localização atual do seu pedido. 📍 Informe o código de rastreio.",
            "contexto": "aguardando_codigo_localizacao",
            "prioridade": 8,
        },

        # ── CHAMADO / SUPORTE HUMANO ──────────────────────────────
        {
            "nome": "chamado_humano",
            "palavras_chave": json.dumps([
                "ajuda", "suporte", "atendente", "humano", "pessoa",
                "problema", "reclamação", "reclamacao", "falar com alguem",
                "quero falar", "atendimento", "quero suporte"
            ]),
            "resposta": "Entendido! 👨‍💻 Vou abrir um chamado de suporte para você. Em poucas palavras, qual é o problema?",
            "contexto": "aguardando_descricao_chamado",
            "prioridade": 9,
        },

        # ── DESPEDIDA / FINALIZAÇÃO ───────────────────────────────
        {
            "nome": "despedida",
            "palavras_chave": json.dumps([
                "obrigado", "obrigada", "valeu", "até mais", "ate mais",
                "tchau", "falou", "agradeço", "agradeco", "flw", "até logo",
                "ate logo", "abraço", "abraco", "bye", "encerrar"
            ]),
            "resposta": "Eu que agradeço! 😊 Sempre que precisar, estarei aqui para ajudar. Tenha um ótimo dia! 🚀",
            "contexto": None,
            "prioridade": 7,
        },

        # ── FALLBACK (não entendeu) ───────────────────────────────
        {
            "nome": "fallback",
            "palavras_chave": json.dumps(["__fallback__"]),
            "resposta": (
                "Desculpe, não entendi muito bem. 🤔 "
                "Posso ajudar com:\n\n"
                "📦 *Rastrear pedido*\n"
                "📊 *Status da entrega*\n"
                "📍 *Localização*\n"
                "👨‍💻 *Abrir chamado de suporte*\n\n"
                "Como posso ajudar?"
            ),
            "contexto": None,
            "prioridade": 0,
        },
    ]

    for dados in intencoes:
        existe = Intencao.query.filter_by(nome=dados["nome"]).first()
        if not existe:
            intencao = Intencao(**dados)
            db.session.add(intencao)
            print(f"  [+] Intenção cadastrada: {dados['nome']}")
        else:
            print(f"  [=] Intenção já existe:  {dados['nome']}")

    db.session.commit()


def seed_pedidos_exemplo():
    """Cadastra pedidos de exemplo para demonstração."""

    pedidos = [
        {
            "codigo_rastreio": "LOG-2024-001",
            "descricao": "Notebook Dell Inspiron 15",
            "status": "Em trânsito",
            "origem": "São Paulo, SP",
            "destino": "Salvador, BA",
        },
        {
            "codigo_rastreio": "LOG-2024-002",
            "descricao": "Smartphone Samsung Galaxy",
            "status": "Saiu para entrega",
            "origem": "Recife, PE",
            "destino": "Feira de Santana, BA",
        },
        {
            "codigo_rastreio": "LOG-2024-003",
            "descricao": "Monitor LG 27 polegadas",
            "status": "Entregue",
            "origem": "Curitiba, PR",
            "destino": "Rio de Janeiro, RJ",
        },
    ]

    historicos = {
        "LOG-2024-001": [
            {"status": "Pedido coletado",     "localizacao": "São Paulo, SP",      "descricao": "Pedido coletado no remetente"},
            {"status": "Em trânsito",          "localizacao": "Governador Valadares, MG", "descricao": "Em rota para destino"},
            {"status": "Chegou ao centro",     "localizacao": "Vitória da Conquista, BA", "descricao": "Chegou ao centro de distribuição"},
        ],
        "LOG-2024-002": [
            {"status": "Pedido coletado",     "localizacao": "Recife, PE",         "descricao": "Pedido coletado"},
            {"status": "Saiu para entrega",   "localizacao": "Feira de Santana, BA", "descricao": "Saiu para entrega ao destinatário"},
        ],
        "LOG-2024-003": [
            {"status": "Pedido coletado",     "localizacao": "Curitiba, PR",       "descricao": "Coletado"},
            {"status": "Em trânsito",          "localizacao": "São Paulo, SP",      "descricao": "Em trânsito"},
            {"status": "Entregue",             "localizacao": "Rio de Janeiro, RJ", "descricao": "Entregue ao destinatário com sucesso"},
        ],
    }

    for dados in pedidos:
        existe = Pedido.query.filter_by(codigo_rastreio=dados["codigo_rastreio"]).first()
        if not existe:
            pedido = Pedido(**dados)
            db.session.add(pedido)
            db.session.flush()  # Garante o ID antes de inserir histórico

            for h in historicos.get(dados["codigo_rastreio"], []):
                hist = HistoricoRastreio(pedido_id=pedido.id, **h)
                db.session.add(hist)

            print(f"  [+] Pedido cadastrado: {dados['codigo_rastreio']}")
        else:
            print(f"  [=] Pedido já existe:  {dados['codigo_rastreio']}")

    db.session.commit()


def seed_configuracoes():
    """Cadastra configurações padrão do sistema."""

    configs = [
        {"chave": "nome_empresa",    "valor": "LogBot Logística",   "descricao": "Nome da empresa exibido no chat"},
        {"chave": "bot_nome",        "valor": "LogBot",             "descricao": "Nome do assistente virtual"},
        {"chave": "versao_sistema",  "valor": "1.0.0",              "descricao": "Versão atual do sistema"},
        {"chave": "max_tentativas",  "valor": "3",                  "descricao": "Tentativas antes de escalar para humano"},
    ]

    for dados in configs:
        existe = Configuracao.query.filter_by(chave=dados["chave"]).first()
        if not existe:
            config = Configuracao(**dados)
            db.session.add(config)
            print(f"  [+] Config cadastrada: {dados['chave']}")
        else:
            print(f"  [=] Config já existe:  {dados['chave']}")

    db.session.commit()


def run_seed():
    """Executa todo o seed."""
    app = create_app()
    with app.app_context():
        print("\n🌱 Iniciando seed do banco de dados...\n")

        print("📋 Intenções:")
        seed_intencoes()

        print("\n📦 Pedidos de exemplo:")
        seed_pedidos_exemplo()

        print("\n⚙️  Configurações:")
        seed_configuracoes()

        print("\n✅ Seed concluído com sucesso!\n")


if __name__ == "__main__":
    run_seed()
