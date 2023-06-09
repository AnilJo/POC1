from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
import logging

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///crud.db'
app.logger.setLevel(logging.DEBUG)
db = SQLAlchemy(app)

class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(80), nullable=False)
    description = db.Column(db.String(120))

    def to_dict(self):
        return {"id": self.id, "name": self.name, "description": self.description}

db.create_all()

@app.route('/items', methods=['POST'])
def create_item():
    data = request.get_json()
    new_item = Item(name=data['name'], description=data['description'])
    db.session.add(new_item)
    db.session.commit()
    return jsonify(new_item.to_dict()), 201

# @app.route('/items', methods=['GET'])
# def read_items():
#     items = Item.query.all()
#     return render_template('items.html', items=items)

@app.route('/items/<int:item_id>', methods=['GET'])
def read_item(item_id):
    item = Item.query.get_or_404(item_id)
    return jsonify(item.to_dict())

@app.route('/items/<int:item_id>', methods=['PUT'])
def update_item(item_id):
    data = request.get_json()
    item = Item.query.get_or_404(item_id)
    item.name = data['name']
    item.description = data['description']
    db.session.commit()
    return jsonify(item.to_dict())

@app.route('/items/<int:item_id>', methods=['DELETE'])
def delete_item(item_id):
    item = Item.query.get_or_404(item_id)
    db.session.delete(item)
    db.session.commit()
    return jsonify({"result": "success"})
@app.route('/')
def index():
    items = Item.query.all()
    return render_template('items.html', items=items)

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0')
