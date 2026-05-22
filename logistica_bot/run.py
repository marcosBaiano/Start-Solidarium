"""
run.py
======
Ponto de entrada da aplicação.
Execute com:  python run.py
"""

from app import create_app
from config.settings import ActiveConfig

app = create_app()

if __name__ == "__main__":
    print("\n" + "="*55)
    print("  🚚  LogBot — Sistema Logístico Inteligente")
    print("="*55)
    print(f"  Ambiente : {ActiveConfig.__name__}")
    print(f"  Banco    : {ActiveConfig.DB_NAME}@{ActiveConfig.DB_HOST}:{ActiveConfig.DB_PORT}")
    print(f"  URL      : http://{ActiveConfig.APP_HOST}:{ActiveConfig.APP_PORT}")
    print("="*55 + "\n")

    app.run(
        host=ActiveConfig.APP_HOST,
        port=ActiveConfig.APP_PORT,
        debug=ActiveConfig.DEBUG,
    )
