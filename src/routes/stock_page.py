from flask import Flask, Blueprint, render_template, jsonify, request
from supabase import create_client, Client
import os
from dotenv import load_dotenv
load_dotenv(".env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

stock_page = Blueprint('stock_page', __name__)

@stock_page.route('/stock')
def pagina_principal():
    page_title = "Fazenda - Gerencimento de Estoque"
    response_all_stock = supabase.table('produto').select('*', count="exact").order('nome', desc=False).execute()
    # response_all_stock_value = supabase.table('produto').select('qtd_estoque', count="exact").execute()
    products = response_all_stock.data
    total_rows = response_all_stock.count
    
    valor_estoque = 0
    for produto in products:
        preco = produto["preco_compra"] or 0
        qtd = produto["qtd_estoque"] or 0
        valor_estoque += preco * qtd

    valor_estoque = f'{valor_estoque:.2f}'

    


    return render_template("stock_page.html", total_rows = total_rows, products = products, valor_estoque = valor_estoque)

@stock_page.route('/stock/data')
def buscar_estoque():
    response_all_stock = supabase.table("produto") \
        .select("id, nome, preco_compra, preco_venda, qtd_estoque, categoria!inner(nome)", count="exact").execute()
    
    dados = response_all_stock.data
    total_rows = response_all_stock.count

    for item in dados:
        item["categoria_nome"] = item["categoria"]["nome"]
        del item["categoria"]

    print(total_rows)
    return jsonify({"total": total_rows, "data": dados})


@stock_page.route('/stock/add_in_stock', methods=['POST'])
def adicionar_no_estoque():
    try:
        if request.method == 'POST':
            id_produto = request.form['id_produto']
            qtd_comprada = request.form['qtd_comprada']
            preco_compra = request.form['preco_compra']
        else:
            return "Não é POST!"
        
        response = supabase.table('produto').select('id, nome, qtd_estoque').eq("id", id_produto).execute()
        data = response.data

        estoque_atual = data[0]['qtd_estoque']
        novo_estoque = estoque_atual + int(qtd_comprada)

        supabase.table('produto').update({'qtd_estoque': novo_estoque}).eq('id', int(id_produto)).execute()
        return f"Atualizado com sucesso!"
    except Exception as e:
        return f"Erro!"

    

