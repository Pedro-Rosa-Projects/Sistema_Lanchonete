from flask import Flask, Blueprint, render_template, jsonify
from supabase import create_client, Client
from src.config import SQL_CREDENTIALS
import os
from dotenv import load_dotenv

load_dotenv(".env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

stock_page = Blueprint('stock_page', __name__)

@stock_page.route('/stock')
def teste():
    response_all_stock = supabase.table('produto').select('*', count="exact").order('nome', desc=False).execute()
    # response_all_stock_value = supabase.table('produto').select('qtd_estoque', count="exact").execute()
    products = response_all_stock.data
    total_rows = response_all_stock.count

    return render_template("stock_page.html", total_rows = total_rows, products = products)

@stock_page.route('/stock/data')
def buscar_estoque():
    response_all_stock = supabase.table('produto').select('*', count="exact").execute()
    dados = response_all_stock.data
    total_rows = response_all_stock.count

    print(total_rows)
    return jsonify({"data":dados})

@stock_page.route('/stock/add_in_stock', methods=['POST'])
def adicionar_no_estoque():
    return "Adicionado com Sucesso!"

