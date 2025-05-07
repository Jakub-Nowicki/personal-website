from flask import Blueprint, render_template

home_bp = Blueprint('home', __name__)

@home_bp.route('/')
@home_bp.route('/home')
def home_page():
    return render_template('home.html')

@home_bp.route('/about')
def about_page():
    return render_template('about.html')

@home_bp.route('/projects')
def projects_page():
    return render_template('projects.html')

@home_bp.route('/contact')
def contact_page():
    return render_template('contact.html')

@home_bp.route('/rps-game')
def rps_page():
    return render_template('rps.html')

@home_bp.route('/sumo-project')
def sumo_page():
    return render_template('sumo.html')