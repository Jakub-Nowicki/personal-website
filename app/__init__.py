from flask import Flask
def create_app():
    app = Flask(__name__)

    from .routes.home import home_bp
    from .routes.sudoku import sudoku_bp
    from .routes.converter import converter_bp
    from .routes.github_api import github_bp

    app.register_blueprint(home_bp)
    app.register_blueprint(sudoku_bp)
    app.register_blueprint(converter_bp)
    app.register_blueprint(github_bp)

    return app