"""
app/database/db.py
==================
Instância única do SQLAlchemy compartilhada por todo o projeto.
Importar sempre deste arquivo para evitar importações circulares.
"""

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()
