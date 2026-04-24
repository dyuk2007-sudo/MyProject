
from flask import Flask, request, jsonify

app = Flask(__name__)

# Хранилище пользователей (в памяти)
users = {}
user_id_counter = 1


@app.route('/users', methods=['POST'])
def create_user():
    """Создание нового пользователя"""
    global user_id_counter

    data = request.json

    # Проверяем обязательные поля
    if not data or 'name' not in data or 'email' not in data:
        return jsonify({"error": "name and email are required"}), 400

    # Создаем пользователя
    user = {
        "id": user_id_counter,
        "name": data['name'],
        "email": data['email']
    }

    # Сохраняем
    users[user_id_counter] = user
    user_id_counter += 1

    return jsonify(user), 201


@app.route('/users/<int:user_id>', methods=['GET'])
def get_user(user_id):
    """Получение пользователя по ID"""
    if user_id not in users:
        return jsonify({"error": "User not found"}), 404

    return jsonify(users[user_id]), 200


@app.route('/health', methods=['GET'])
def health():
    return {"status": "user-service ok"}, 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)