
function showToast(message, category = 'info') {
    const icons = {
        success: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5Zm3.707 8.207-4 4a1 1 0 0 1-1.414 0l-2-2a1 1 0 0 1 1.414-1.414L9 10.586l3.293-3.293a1 1 0 0 1 1.414 1.414Z"/></svg>`,
        error: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM10 15a1 1 0 1 1 0-2 1 1 0 0 1 0 2Zm1-4a1 1 0 0 1-2 0V6a1 1 0 0 1 2 0v5Z"/></svg>`,
        info: `<svg class="w-5 h-5" aria-hidden="true" xmlns="http://www.w3.org/2000/svg" fill="currentColor" viewBox="0 0 20 20"><path d="M10 .5a9.5 9.5 0 1 0 9.5 9.5A9.51 9.51 0 0 0 10 .5ZM9.5 4a1.5 1.5 0 1 1 0 3 1.5 1.5 0 0 1 0-3ZM12 15H8a1 1 0 0 1 0-2h1v-3H8a1 1 0 0 1 0-2h2a1 1 0 0 1 1 1v4h1a1 1 0 0 1 0 2Z"/></svg>`
    };
    const colors = {
        success: 'text-green-500 bg-green-100',
        error: 'text-red-500 bg-red-100',
        info: 'text-blue-500 bg-blue-100'
    };

    const container = document.getElementById('toast-container');
    const template = document.getElementById('toast-template');
    const toast = template.content.cloneNode(true).querySelector('.toast-message');

    const iconContainer = toast.querySelector('.icon-container');
    const messageContainer = toast.querySelector('.message-container');

    iconContainer.innerHTML = icons[category] || icons['info'];
    iconContainer.className += ' ' + (colors[category] || colors['info']);
    messageContainer.textContent = message;

    const closeButton = toast.querySelector('button');
    closeButton.addEventListener('click', () => {
        toast.classList.add('closing');
        toast.addEventListener('animationend', () => toast.remove());
    });

    container.appendChild(toast);

    setTimeout(() => {
        if (toast.parentElement) {
            toast.classList.add('closing');
            toast.addEventListener('animationend', () => toast.remove());
        }
    }, 4000);
}

document.addEventListener('DOMContentLoaded', () => {
    // Lógica para ler as mensagens do Flask assim que a página carrega
    const flashContainer = document.getElementById('flash-messages');
    const messages = flashContainer.querySelectorAll('div');
    messages.forEach(flash => {
        const message = flash.textContent;
        const category = flash.dataset.category;
        showToast(message, category);
    });

    // Restante da lógica da página
    const dateInput = document.getElementById('sale-date');
    dateInput.valueAsDate = new Date();

    const productCards = document.querySelectorAll('.product-card');
    const cartItemsContainer = document.getElementById('cart-items');
    const totalPriceEl = document.getElementById('total-price');
    const registerSaleBtn = document.getElementById('register-sale-btn');

    let cart = {};

    productCards.forEach(card => {
        const increaseBtn = card.querySelector('.increase');
        const decreaseBtn = card.querySelector('.decrease');
        const quantityInput = card.querySelector('.quantity-input');

        const productId = card.dataset.id;
        const productName = card.dataset.name;
        const productPrice = parseFloat(card.dataset.price);
        const productStock = parseInt(card.dataset.stock);

        increaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantityInput.value) || 0;
            if (quantity >= productStock) {
                showToast('Quantidade máxima em estoque atingida.', 'error');
                return;
            }
            quantity++;
            quantityInput.value = quantity;
            updateCart(productId, productName, productPrice, quantity);
        });

        decreaseBtn.addEventListener('click', () => {
            let quantity = parseInt(quantityInput.value) || 0;
            if (quantity > 0) {
                quantity--;
                quantityInput.value = quantity;
                updateCart(productId, productName, productPrice, quantity);
            }
        });

        quantityInput.addEventListener('input', () => {
            let quantity = parseInt(quantityInput.value);
            if (isNaN(quantity) || quantity < 0) {
                quantity = 0;
                quantityInput.value = 0;
            }
            if (quantity > productStock) {
                showToast('Quantidade máxima em estoque é ' + productStock, 'error');
                quantity = productStock;
                quantityInput.value = productStock;
            }
            updateCart(productId, productName, productPrice, quantity);
        });

        quantityInput.addEventListener('focus', () => {
            if (quantityInput.value === '0') {
                quantityInput.value = '';
            }
        });

        quantityInput.addEventListener('blur', () => {
            if (quantityInput.value === '') {
                quantityInput.value = '0';
            }
        });
    });

    function updateCart(id, name, price, quantity) {
        if (quantity > 0) {
            cart[id] = { name, price, quantity };
        } else {
            delete cart[id];
        }
        renderCart();
    }

    function renderCart() {
        cartItemsContainer.innerHTML = '';
        let totalPrice = 0;
        const productIds = Object.keys(cart);

        if (productIds.length === 0) {
            cartItemsContainer.innerHTML = '<p class="text-gray-500">Nenhum produto adicionado.</p>';
            registerSaleBtn.disabled = true;
        } else {
            productIds.forEach(id => {
                const item = cart[id];
                const itemEl = document.createElement('div');
                itemEl.className = 'flex justify-between text-gray-700';
                itemEl.innerHTML = `
                    <span>${item.quantity}x ${item.name}</span>
                    <span>R$ ${(item.price * item.quantity).toFixed(2).replace('.', ',')}</span>
                `;
                cartItemsContainer.appendChild(itemEl);
                totalPrice += item.price * item.quantity;
            });
            registerSaleBtn.disabled = false;
        }
        totalPriceEl.textContent = `R$ ${totalPrice.toFixed(2).replace('.', ',')}`;
    }

    registerSaleBtn.addEventListener('click', async () => {
        const saleDate = dateInput.value;
        const totalValue = parseFloat(totalPriceEl.textContent.replace('R$ ', '').replace(',', '.'));
        if (Object.keys(cart).length === 0) {
            showToast('Adicione pelo menos um produto para registrar a venda.', 'error');
            return;
        }
        const saleData = {
            date: saleDate,
            total: totalValue,
            cart: cart
        };
        try {
            const response = await fetch('/sales/sale_register', {
                method: 'POST',
                headers: { 'Content-Type': 'application/json' },
                body: JSON.stringify(saleData)
            });
            const result = await response.json();
            if (response.ok) {
                // Guarda a mensagem para exibir após o reload
                sessionStorage.setItem('showToastMessage', 'Venda registrada com sucesso!');
                sessionStorage.setItem('showToastCategory', 'success');
                window.location.reload();
            } else {
                showToast(`Erro ao registrar a venda: ${result.message}`, 'error');
            }
        } catch (error) {
            console.error('Erro na requisição:', error);
            showToast('Ocorreu um erro de comunicação com o servidor.', 'error');
        }
    });
});

