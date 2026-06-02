from flask import Blueprint

dashboard_bp = Blueprint('dashboard', __name__)
targets_bp = Blueprint('targets', __name__)

from app.routes.dashboard import *