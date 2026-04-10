from flask import Flask, request, jsonify
from models import db, User, Category, Transaction, AuditLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db.init_app(app)

with app.app_context():
    db.create_all()


@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.json

    if data['amount'] <= 0:
        return jsonify({"error": "O valor deve ser positivo"}), 400

    new_trans = Transaction(
        description=data['description'],
        amount=data['amount'],
        user_id=data['user_id'],
        category_id=data['category_id']
    )

    db.session.add(new_trans)

    log = AuditLog(
        action=f"Lançamento de {data['amount']} criado",
        user_id=data['user_id']
    )
    db.session.add(log)

    db.session.commit()

    return jsonify({"message": "Lançamento realizado com sucesso!"}), 201


if __name__ == '__main__':
    app.run(debug=True)