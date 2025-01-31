from ..services.langchain_service import generate_quiz, generate_quiz_with_internet
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for
from werkzeug.utils import secure_filename
import os

routes = Blueprint('routes', __name__)

UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)


