import os
from flask import Flask, Blueprint, render_template, url_for
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(".env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

sales_page = Blueprint('sales_page', __name__)

@sales_page.route('/sales')
def teste():
    page_title = "Fazenda - Início"
    try:
        response = supabase.table('produto').select("*").execute()
        dados = response.data
        return render_template("sales_page.html", page_title = page_title, lista_de_produtos = dados)
    except Exception as e:
        return "Erro"
