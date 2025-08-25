import os
from app.app import app

# Executar correção de banco automaticamente no Render
if os.environ.get('DATABASE_URL'):
    try:
        from fix_database import fix_database
        print("🔧 Executando correção de banco...")
        fix_database()
    except Exception as e:
        print(f"⚠️ Erro na correção de banco (ignorando): {e}")

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
