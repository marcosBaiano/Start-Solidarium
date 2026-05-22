# 🚚 LogBot — Sistema Logístico Inteligente

Bot conversacional de logística empresarial construído com **Python + Flask + MySQL**.

---

## 📁 Estrutura do Projeto

```
logistica_bot/
│
├── app/
│   ├── chatbot/
│   │   ├── __init__.py
│   │   ├── detector.py     ← Detecta intenções pelo banco de dados
│   │   └── engine.py       ← Motor conversacional principal
│   │
│   ├── database/
│   │   ├── __init__.py
│   │   ├── db.py           ← Instância do SQLAlchemy
│   │   ├── models.py       ← Todos os modelos / tabelas
│   │   └── seed.py         ← Dados iniciais (intenções, pedidos, configs)
│   │
│   ├── routes/
│   │   ├── __init__.py
│   │   └── chat.py         ← Rotas Flask (página + API)
│   │
│   ├── utils/
│   │   ├── __init__.py
│   │   └── helpers.py      ← Funções auxiliares
│   │
│   ├── templates/
│   │   └── chat.html       ← Interface do chat
│   │
│   └── __init__.py         ← App factory
│
├── config/
│   ├── __init__.py
│   └── settings.py         ← Configurações por ambiente
│
├── logs/                   ← Arquivos de log (gerados em runtime)
│
├── .env.example            ← Modelo de variáveis de ambiente
├── .gitignore
├── requirements.txt
├── run.py                  ← Ponto de entrada
└── seed.py                 ← Executa o seed do banco
```

---

## ⚙️ Instalação — Passo a Passo

### 1. Criar banco de dados MySQL

```sql
CREATE DATABASE logistica CHARACTER SET utf8mb4 COLLATE utf8mb4_unicode_ci;
```

### 2. Clonar / abrir o projeto no VS Code

```bash
cd logistica_bot
```

### 3. Criar ambiente virtual

```bash
python -m venv venv

# Windows
venv\Scripts\activate

# Linux / Mac
source venv/bin/activate
```

### 4. Instalar dependências

```bash
pip install -r requirements.txt
```

### 5. Configurar variáveis de ambiente

```bash
# Copie o arquivo de exemplo
cp .env.example .env

# Edite o .env com seus dados MySQL:
# DB_HOST, DB_PORT, DB_USER, DB_PASSWORD, DB_NAME
```

### 6. Criar tabelas e popular o banco

```bash
python seed.py
```

### 7. Iniciar o servidor

```bash
python run.py
```

Acesse: **http://localhost:5000**

---

## 🤖 Como o Bot Funciona

### Fluxo de Cadastro Automático
1. Usuário envia "oi"
2. Bot pede **nome**
3. Bot pede **email**
4. Bot pede **telefone** (pode pular)
5. Atendimento segue normalmente

### Intenções cadastradas no banco (`tabela intencoes`)
| Intenção         | Palavras-chave de exemplo                    |
|------------------|---------------------------------------------|
| saudacao         | oi, olá, bom dia, boa tarde...              |
| rastreio         | rastrear, tracking, onde está meu pedido... |
| status           | status, andamento, situação...              |
| localizacao      | localização, rota, onde está...             |
| chamado_humano   | ajuda, suporte, problema, reclamação...     |
| despedida        | obrigado, tchau, até mais, valeu...         |
| fallback         | (quando nada é detectado)                   |

### Pedidos de exemplo (para testar rastreio)
- `LOG-2024-001` — Em trânsito
- `LOG-2024-002` — Saiu para entrega
- `LOG-2024-003` — Entregue

---

## 🗄️ Tabelas do Banco

| Tabela              | Descrição                           |
|---------------------|-------------------------------------|
| `usuarios`          | Usuários cadastrados pelo chat      |
| `intencoes`         | Cérebro do bot (palavras → respostas) |
| `mensagens`         | Histórico de todas as conversas     |
| `pedidos`           | Pedidos de entrega                  |
| `historico_rastreio`| Eventos de rastreio por pedido      |
| `chamados`          | Chamados de suporte abertos         |
| `sessoes`           | Contexto temporário de conversa     |
| `configuracoes`     | Parâmetros do sistema               |
| `logs`              | Logs de sistema                     |

---

## 🔧 Adicionar Nova Intenção (sem alterar código)

Basta inserir no banco:

```sql
INSERT INTO intencoes (nome, palavras_chave, resposta, contexto, prioridade, ativo)
VALUES (
  'segunda_via',
  '["segunda via", "boleto", "nota fiscal", "nf"]',
  'Para segunda via de documentos, acesse: docs.empresa.com ou abra um chamado.',
  NULL,
  8,
  1
);
```

O bot passa a reconhecer a nova intenção imediatamente. ✅

---

## 🚀 Próximos Passos (expansões previstas)

- [ ] Painel administrativo
- [ ] Autenticação de usuários
- [ ] Integração WhatsApp (Twilio / Z-API)
- [ ] Dashboard com métricas
- [ ] Integração OpenAI/GPT
- [ ] API REST completa
- [ ] Integração ERP
