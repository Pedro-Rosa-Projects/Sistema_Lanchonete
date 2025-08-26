from flask import Flask, Blueprint, render_template, jsonify
import mysql.connector
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
    return render_template("stock_page.html")

@stock_page.route('/stock/data')
def buscar_estoque():
    response = supabase.table('produto').select('*').execute()
    dados = response.data
    return jsonify({"data":dados})