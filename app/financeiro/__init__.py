from flask import Blueprint

financeiro_bp = Blueprint('financeiro', __name__, url_prefix='/financeiro', template_folder='templates')

from . import financeiro_routes  # noqa: E402,F401
