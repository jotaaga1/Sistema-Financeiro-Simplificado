from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

db = SQLAlchemy()

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), nullable=False)
    email = db.Column(db.Sring(120), unique=True, nullable=False)
    categories = db.relationship('Category', backref='owner', lazy=True)
    transactions = db.relationship('Transaction', backref='owner', lazy=True)

class Category(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    type = db.Column(db.String(10), nullable=False)
    user_id = db.Column(db.Integer, db.ForeingKey('user.id'), nullable=False)

class Transaction(db.Model):
    id = db.Column(id.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeingKey('user.id'), nullable=False)
    category_id = db.Column(db.Integer, db.ForeingKey('category.id'), nullable=False)

class AuditLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    action = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)
    user_id = db.Column(db.Integer, db.ForeingKey('user_id'))


from flask import Flask, request, jsonify
from models import db, User, Category, Transaction, AuditLog

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///finance.db'
db.int_app(app)

with app.app_context():
    db.create_all()

@app.route('/transaction', methods=['POST'])
def add_transaction():
    data = request.json

    if data['amount'] <= 0:
        return jsonify({"error": "O valor deve ser positivo"}), 400

    new_trans = Transaction(
        descripetion=data['descripition'],
        amount=date['user_id'],
        user_id=data['user_id'],
        category_id=data['category_id']
    )

    db.session.add(new_trans)
    log = AuditLog(action=f"Lancamento de {data['amount']} criado", user_id=data['user_id'])
    db.session.add(log)

    db.session.commit()
    return jsnonify({"message": "Lançamento realizado com sucesso!"}) , 201

if __name__ == '__main__':
    app.run(debug=True)
