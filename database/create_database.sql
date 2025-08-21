-- Criar banco
CREATE DATABASE lanchonete;
USE lanchonete;

-- Categorias de produtos
CREATE TABLE categoria (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(100) NOT NULL
);

-- Produtos
CREATE TABLE produto (
    id INT AUTO_INCREMENT PRIMARY KEY,
    nome VARCHAR(150) NOT NULL,
    id_categoria INT NOT NULL,
    preco_compra DECIMAL(10,2) NOT NULL,
    preco_venda DECIMAL(10,2) NOT NULL,
    estoque INT DEFAULT 0,
    FOREIGN KEY (id_categoria) REFERENCES categoria(id)
);

-- Compras (entrada de estoque)
CREATE TABLE compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_compra DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    fornecedor VARCHAR(150) NULL,
    valor_total DECIMAL(10,2) NOT NULL
);

-- Itens da compra
CREATE TABLE item_compra (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_compra INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_compra) REFERENCES compra(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);

-- Vendas (saída de estoque)
CREATE TABLE venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    data_venda DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
    cliente VARCHAR(150) NULL,
    valor_total DECIMAL(10,2) NOT NULL
);

-- Itens da venda
CREATE TABLE item_venda (
    id INT AUTO_INCREMENT PRIMARY KEY,
    id_venda INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario DECIMAL(10,2) NOT NULL,
    FOREIGN KEY (id_venda) REFERENCES venda(id),
    FOREIGN KEY (id_produto) REFERENCES produto(id)
);
