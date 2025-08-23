import os
from app.app import app
from flask_migrate import upgrade

def deploy():
    """Run deployment tasks."""
    # Create database tables
    upgrade()

# Em produção (Render), executar migrações automaticamente
if os.environ.get('DATABASE_URL'):
    with app.app_context():
        deploy()

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
