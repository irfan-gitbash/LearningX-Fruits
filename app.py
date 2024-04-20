import os
from os.path import join, dirname
from dotenv import load_dotenv
from flask import Flask, render_template, request, redirect, url_for
from pymongo import MongoClient
from bson import ObjectId

dotenv_path = join(dirname(__file__), '.env')
load_dotenv(dotenv_path)

MONGODB_URI = os.environ.get("MONGODB_URI")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient('mongodb+srv://test:sparta@cluster0.rayb88e.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbsparta

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def main():
    fruit = list(db.fruit.find({}))
    return render_template("dashboard.html", fruit=fruit)

@app.route('/fruit', methods=['GET', 'POST'])
def fruit():
    fruit = list(db.fruit.find({}))
    return render_template("index.html", fruit=fruit)

@app.route('/addfruit', methods=['GET', 'POST'])
def addFruit():
    if request.method == 'POST':
        name = request.form['fruitsName']
        price = request.form['price']
        description = request.form['descriptionProduct']
        image_name = request.files['image']

        if image_name :
            real_file_name = image_name.filename
            image_file_name = real_file_name.split('/')[-1]
            file_path = f'static/assets/imgFruit/{image_file_name}'
            image_name.save(file_path)
        else :
            image_name = None
        
        doc = {
            'name': name,
            'price': price,
            'description': description,
            'image': image_file_name
        }

        db.fruit.insert_one(doc)
        return redirect(url_for('fruit'))
    return render_template("AddFruit.html")

@app.route('/edit/<_id>', methods=['GET', 'POST'])
def edit(_id):
    if request.method == 'POST':
        id = request.form['id']
        name = request.form['edit_fruitsName']
        price = request.form['edit_price']
        description = request.form['edit_descriptionProduct']
        image_name = request.files['edit_image']

        doc = {
            'name': name,
            'price': price,
            'description': description
        }

        if image_name :
            real_file_name = image_name.filename
            image_file_name = real_file_name.split('/')[-1]
            file_path = f'static/assets/imgFruit/{image_file_name}'
            image_name.save(file_path)
            doc['image'] = image_file_name

        db.fruit.update_one({'_id': ObjectId(id)}, {'$set': doc})
        return redirect(url_for('fruit'))
    
    id = ObjectId(_id)
    data = list(db.fruit.find({'_id': id}))
    print(data)
    return render_template("EditFruit.html", data=data)

@app.route('/delete/<_id>', methods=['GET', 'POST'])
def delete(_id):
    db.fruit.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fruit'))

if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)