from flask import Flask
from routes.budget_page import budget_page
from routes.index_page import index_page
from routes.stock_page import stock_page


def create_app():
    app = Flask(
        __name__, template_folder="front/templates", static_folder="front/statics"
    )

    app.register_blueprint(index_page)
    app.register_blueprint(budget_page)
    app.register_blueprint(stock_page)

    return app

if __name__ == "__main__":
    app = create_app()
    app.run(debug=True)