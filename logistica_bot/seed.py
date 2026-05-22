"""
seed.py
=======
Script de seed — popula o banco com dados iniciais.
Execute uma vez após criar o banco:  python seed.py
"""

from app.database.seed import run_seed

if __name__ == "__main__":
    run_seed()
