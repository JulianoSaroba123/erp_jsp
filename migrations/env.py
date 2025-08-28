# migrations/env.py
import os
import sys
import logging
from logging.config import fileConfig

from alembic import context
from sqlalchemy import engine_from_config, pool

# --- PATH: garante que a raiz (onde está a pasta "app/") está no sys.path
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
if BASE_DIR not in sys.path:
    sys.path.append(BASE_DIR)

from flask import current_app
from app.extensoes import db
from app.app import app as flask_app  # seu app Flask

# Alembic config / logging
config = context.config
if config.config_file_name is not None:
    fileConfig(config.config_file_name)
logger = logging.getLogger("alembic.env")

# Metadata dos modelos
target_metadata = db.metadata


def is_sqlite_url(url: str) -> bool:
    return url.startswith("sqlite:///") or url.startswith("sqlite:////")


def set_sqlalchemy_url_from_flask():
    """Lê a SQLALCHEMY_DATABASE_URI do Flask e injeta no Alembic."""
    with flask_app.app_context():
        uri = flask_app.config.get("SQLALCHEMY_DATABASE_URI")
        if not uri:
            raise RuntimeError("SQLALCHEMY_DATABASE_URI não configurada no Flask app.")
        config.set_main_option("sqlalchemy.url", uri)


def run_migrations_offline():
    """Executa migrações em modo offline."""
    set_sqlalchemy_url_from_flask()
    url = config.get_main_option("sqlalchemy.url")

    context.configure(
        url=url,
        target_metadata=target_metadata,
        literal_binds=True,
        dialect_opts={"paramstyle": "named"},
        compare_type=True,
        render_as_batch=is_sqlite_url(url),  # necessário p/ SQLite
    )

    with context.begin_transaction():
        context.run_migrations()


def run_migrations_online():
    """Executa migrações em modo online (com conexão)."""
    set_sqlalchemy_url_from_flask()

    def process_revision_directives(ctx, revision, directives):
        # Evita criar migração vazia quando autogenerate está ligado
        if getattr(config.cmd_opts, "autogenerate", False):
            script = directives[0]
            if script.upgrade_ops.is_empty():
                directives[:] = []
                logger.info("No changes in schema detected.")

    with flask_app.app_context():
        # Pode não haver Flask-Migrate habilitado; trata como opcional
        migrate_ext = current_app.extensions.get("migrate") if hasattr(current_app, "extensions") else None
        conf_args = getattr(migrate_ext, "configure_args", {}) if migrate_ext else {}

        if conf_args.get("process_revision_directives") is None:
            conf_args["process_revision_directives"] = process_revision_directives

        connectable = engine_from_config(
            config.get_section(config.config_ini_section),
            prefix="sqlalchemy.",
            poolclass=pool.NullPool,
        )

        with connectable.connect() as connection:
            url = str(connection.engine.url)
            context.configure(
                connection=connection,
                target_metadata=target_metadata,
                compare_type=True,
                render_as_batch=is_sqlite_url(url),  # necessário p/ SQLite
                **conf_args,
            )
            with context.begin_transaction():
                context.run_migrations()


if context.is_offline_mode():
    run_migrations_offline()
else:
    run_migrations_online()

