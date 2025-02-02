from ..services.langchain_service import generate_quiz, generate_quiz_with_internet
from flask import Blueprint, request, jsonify, render_template, session, redirect, url_for, current_app
from ..services.file_handling_service import pdf_to_text, csv_to_text, doc_to_text, txt_to_text
from werkzeug.utils import secure_filename
import os
import json


routes = Blueprint('routes', __name__)


UPLOAD_FOLDER = os.path.join(os.path.dirname(__file__), '..', 'uploads')
os.makedirs(UPLOAD_FOLDER, exist_ok=True)



ALLOWED_EXTENSIONS = {'txt', 'doc', 'csv', 'docx', 'pdf'}


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@routes.route('/')
def index():
    return render_template('index.html')

@routes.route('/generate', methods=['POST'])
def generate():
    method = request.form.get('method')
    questions = []

    if method == 'file':
        if 'file' not in request.files:
            return jsonify({'error': 'No file uploaded'}), 400

        file = request.files['file']
        if file.filename == '' or not allowed_file(file.filename):
            return jsonify({'error': 'Invalid file type'}), 400
        print("file accepted")

        filename = secure_filename(file.filename)
        filepath = os.path.join(UPLOAD_FOLDER, filename)
        file.save(filepath)

        if '.' in filename and filename.rsplit('.', 1)[1].lower() == 'doc' or '.' in filename and filename.rsplit('.', 1)[1].lower() == 'docx':
            text = doc_to_text(filepath)
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() == 'pdf':
            text = pdf_to_text(filepath)
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() == 'csv':
            text = csv_to_text(filepath)
        elif '.' in filename and filename.rsplit('.', 1)[1].lower() == 'txt':
            text = txt_to_text(filepath)
        else:
            print('unsupported file extention')
            
        #print(text)
        questions = generate_quiz(text)
        #print(questions,"question")

    elif method == 'internet':
        topic = request.form.get('topic')
        if not topic:
            return jsonify({'error': 'No topic provided'}), 400

        questions = generate_quiz_with_internet(topic)
    #     print(questions,"question")
    #questions = [{"question":"What is the study of acids and bases an example of in chemistry?","a":"Organic Chemistry","b":"Inorganic Chemistry","c":"Acid-Base Chemistry","d":"Nuclear Chemistry","answer":"c"},{"question":"Which of the following topics involves the study of the smallest units of matter?","a":"Atomic Structure","b":"Thermochemistry","c":"Kinetics","d":"Equilibrium","answer":"a"},{"question":"Chemical bonds are an essential topic in which field?","a":"Physics","b":"Biology","c":"Chemistry","d":"Mathematics","answer":"c"},{"question":"What topic in chemistry focuses on the transformation of substances?","a":"Elemental Chemistry","b":"Chemical Reactions","c":"Chemical Bonding","d":"Enzymatic Activity","answer":"b"},{"question":"In which topic do chemists study the energy changes that accompany chemical reactions?","a":"Thermochemistry","b":"Physical Chemistry","c":"Biochemistry","d":"Spectroscopy","answer":"a"},{"question":"Which branch of chemistry is concerned with the analysis of substances?","a":"Organic Chemistry","b":"Analytical Chemistry","c":"Inorganic Chemistry","d":"Biochemistry","answer":"b"},{"question":"What is the main focus of organic chemistry?","a":"Study of metals","b":"Study of carbon-based compounds","c":"Study of gases","d":"Study of acids","answer":"b"},{"question":"Which chemical topic involves studying how fast reactions occur?","a":"Thermodynamics","b":"Catalysis","c":"Kinetics","d":"Spectrometry","answer":"c"},{"question":"Which topic might involve the study of elements like lanthanides and actinides?","a":"Inorganic Chemistry","b":"Bioorganic Chemistry","c":"Physical Chemistry","d":"Polymer Chemistry","answer":"a"},{"question":"What is a common subject within physical chemistry?","a":"Quantum mechanics","b":"Cell division","c":"Theory of relativity","d":"Photosynthesis","answer":"a"},{"question":"What topic explores the structure and properties of molecules?","a":"Molecular Chemistry","b":"Astrobiology","c":"Geochemistry","d":"Bromatology","answer":"a"},{"question":"Which topic involves the study of substances at the atomic and molecular scale?","a":"Macromolecular Chemistry","b":"Nanotechnology","c":"Astrochemistry","d":"Environmental Science","answer":"b"},{"question":"Which chemistry topic plays a critical role in drug design and synthesis?","a":"Green Chemistry","b":"Organic Chemistry","c":"Electrochemistry","d":"Materials Chemistry","answer":"b"},{"question":"What describes the study of crystal structures in chemistry?","a":"Optics","b":"Crystallography","c":"Biochemistry","d":"Microbiology","answer":"b"},{"question":"Which topic involves the interaction of light energy with chemical systems?","a":"Photochemistry","b":"Hydrodynamics","c":"Electromagnetism","d":"Acoustics","answer":"a"},{"question":"Which topic focuses on the conversion of chemical energy to electrical energy?","a":"Electrochemistry","b":"Planetary Science","c":"Botany","d":"Linguistics","answer":"a"},{"question":"What is the principle subject of bioinorganic chemistry?","a":"Interaction between metal ions and biological molecules","b":"Study of organic molecules","c":"Ion exchange mechanisms","d":"Synthetic polymers","answer":"a"},{"question":"Which topic includes the synthesis and study of synthetic polymers?","a":"Organic Chemistry","b":"Polymer Chemistry","c":"Plant Biology","d":"Quantum Chemistry","answer":"b"},{"question":"Which area of chemistry deals with isotopes and radioactive materials?","a":"Environmental Chemistry","b":"Isotopic Chemistry","c":"Nuclear Chemistry","d":"Marine Chemistry","answer":"c"},{"question":"In what type of chemistry would the study of reaction pathways be important?","a":"Biological Chemistry","b":"Organic Chemistry","c":"Synthetic Chemistry","d":"Kinetics","answer":"d"}]
    session['questions'] = questions
    print(session.get('questions'))
    return jsonify({"redirect_url": url_for("routes.quiz")})



@routes.route('/quiz', methods=['GET', 'POST'])
def quiz():
    questions = session.get('questions', [])
    return render_template("quiz.html", questions=questions)



@routes.route('/submit_quiz', methods=['GET','POST'])
def submit_quiz():
    data = request.json
    if not data:
        return jsonify({'error': 'No data received'}), 400

    questions = data.get('questions', [])
    answers = data.get('answers', {})

    score = sum(1 for q in questions if str(q['id']) in answers and answers[str(q['id'])] == q['correct_option'])

    return jsonify({'score': score})