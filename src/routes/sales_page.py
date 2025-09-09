import os
from flask import Flask, Blueprint, render_template, url_for, request, jsonify, flash
from supabase import create_client, Client
from dotenv import load_dotenv

load_dotenv(".env")

url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)

sales_page = Blueprint('sales_page', __name__)

@sales_page.route('/sales')
def list_products():

    page_title = "Fazenda - Início"

    try:
        response = supabase.table('produto').select("*").order('nome', desc=False).execute()
        dados = response.data
        return render_template("sales_page.html", page_title = page_title, lista_de_produtos = dados)
    except Exception as e:
        return "Erro"
    
@sales_page.route('/sales/sale_register', methods=['POST'])
def register_sale():
    data = request.get_json()
    cart_items = data.get('cart')
    sale_date = data.get('date')
    total_value = data.get('total')

    if not cart_items:
        return jsonify({'status': 'error', 'message': 'Carrinho Vazio'}), 400

    try:
        venda_response = supabase.table('venda').insert({
            'data_venda': sale_date,
            'valor_total': total_value,
            'cliente': 'Balcão' 
        }).execute()

        if not venda_response.data:
            raise Exception("Falha ao criar o registro da venda.")
        
        new_venda_id = venda_response.data[0]['id']

        items_to_insert = []
        for product_id, item_details in cart_items.items():
            items_to_insert.append({
                'id_venda': new_venda_id,
                'id_produto': int(product_id),
                'quantidade': item_details['quantity'],
                'preco_unitario': item_details['price'],
            })

        supabase.table('item_venda').insert(items_to_insert).execute()

        for product_id, item_details in cart_items.items():
            
            produto_atual = supabase.table('produto').select('qtd_estoque').eq('id', int(product_id)).single().execute()
            estoque_atual = produto_atual.data['qtd_estoque']
            
            novo_estoque = estoque_atual - item_details['quantity']

            supabase.table('produto').update({'qtd_estoque': novo_estoque}).eq('id', int(product_id)).execute()

        flash('Venda registrada com sucesso!', 'success')
        return jsonify({'status': 'success', 'message': 'Venda registrada com sucesso!', 'venda_id': new_venda_id})

    except Exception as e:
        print(f"Erro ao registrar venda: {e}")
        return jsonify({'status': 'error', 'message': str(e)}), 500
