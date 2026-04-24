from flask import Flask, request, jsonify
import requests
import os

app = Flask(__name__)

# Адрес user-service (из переменной окружения)
USER_SERVICE_URL = os.environ.get('USER_SERVICE_URL', 'http://user-service:5001')

# Хранилище заказов
orders = {}
order_id_counter = 1


@app.route('/orders', methods=['POST'])
def create_order():
    """Создание нового заказа"""
    global order_id_counter

    data = request.json

    # Проверяем обязательные поля
    if not data or 'user_id' not in data or 'product' not in data:
        return jsonify({"error": "user_id and product are required"}), 400

    # Проверяем, существует ли пользователь
    try:
        response = requests.get(f"{USER_SERVICE_URL}/users/{data['user_id']}", timeout=3)

        if response.status_code == 404:
            return jsonify({"error": f"User with id {data['user_id']} not found"}), 404

        user = response.json()

    except requests.exceptions.RequestException as e:
        return jsonify({"error": f"User service unavailable: {str(e)}"}), 503

    # Создаем заказ
    order = {
        "id": order_id_counter,
        "user_id": data['user_id'],
        "user_name": user['name'],
        "product": data['product'],
        "quantity": data.get('quantity', 1),
        "status": "created"
    }

    # Сохраняем заказ
    orders[order_id_counter] = order
    order_id_counter += 1

    return jsonify(order), 201


@app.route('/orders', methods=['GET'])
def get_orders():
    """Получение всех заказов"""
    return jsonify(list(orders.values())), 200


@app.route('/orders/<int:order_id>', methods=['GET'])
def get_order(order_id):
    """Получение заказа по ID"""
    if order_id not in orders:
        return jsonify({"error": "Order not found"}), 404

    return jsonify(orders[order_id]), 200


@app.route('/health', methods=['GET'])
def health():
    return {"status": "order-service ok"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
