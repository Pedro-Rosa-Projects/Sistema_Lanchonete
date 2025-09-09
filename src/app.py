from flask import Flask
from src.routes.budget_page import budget_page
from src.routes.index_page import index_page
from src.routes.stock_page import stock_page
from src.routes.sales_page import sales_page


def create_app():
    app = Flask(
        __name__, template_folder="front/templates", static_folder="front/statics"
    )

    app.secret_key = "segredo"

    app.register_blueprint(index_page)
    app.register_blueprint(budget_page)
    app.register_blueprint(stock_page)
    app.register_blueprint(sales_page)

    return app

app = create_app()
if __name__ == "__main__":
    app.run(debug=True)