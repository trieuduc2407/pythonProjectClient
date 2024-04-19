from flask import Flask, render_template, request, redirect, url_for, flash, jsonify
import requests
import json

app = Flask(__name__)

app.secret_key = 'dtd'

baseUrl = 'http://127.0.0.1:5002'


@app.route('/', methods=['get'])
def index():
    response = requests.get(baseUrl)
    if response.status_code == 200:
        items = response.json()
        return render_template('index.html', items=items)
    else:
        flash('Something went wrong')
    return render_template('index.html')


@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search_text')
        response = requests.post(baseUrl+'/searchData', json={'search_text': search_text})
        if response.status_code == 200:
            items = response.json()
            print(items)
            return render_template('search.html', items=items, search_text=search_text)
        else:
            flash('Something went wrong')
            return render_template('search.html')
    elif request.method == 'GET':
        response = requests.get(baseUrl)
        if response.status_code == 200:
            return render_template('search.html')
        else:
            flash('Something went wrong')


@app.route('/admin', methods=['get'])
def admin():
    response = requests.get(baseUrl)
    if response.status_code == 200:
        items = response.json()
        return render_template('admin.html', items=items)
    else:
        flash('Something went wrong')
    return redirect(url_for('admin'))


@app.route('/adminAdd', methods=['get', 'post'])
def admin_add():
    if request.method == 'POST':
        id = request.form.get('product_id')
        name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        img = request.form.get('img')
        type = request.form.get('product_type')
        if id and name and quantity and price and img and type:
            response = requests.post(
                baseUrl+'/adminAdd', json={
                    'product_id': id,
                    'product_name': name,
                    'quantity': quantity,
                    'price': price,
                    'img': img,
                    'product_type': type
                }
            )
            if response.status_code == 200:
                flash('Product Added Successfully')
                return redirect(url_for('admin'))
            else:
                flash('Something went wrong')
                return render_template('adminAdd.html')
        else:
            flash('info required')
            return redirect(url_for('adminAdd'))
    else:
        return render_template('adminAdd.html')


@app.route('/test/<id>', methods=['get', 'post'])
def test(id):
    print(id)
    return id


@app.route('/adminUpdate/<product_id>', methods=['get', 'post'])
def adminUpdate(product_id):
    # print(product_id)
    # print(f'{baseUrl+'/adminUpdate'}/{product_id}')
    if request.method == 'post':
        name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        img = request.form.get('img')
        if name and quantity and price and img:
            response = requests.put(
                f'{baseUrl+'/adminUpdate'}/{product_id}',
                json={'product_name': name, 'quantity': quantity, 'price': price, 'img': img}
                )
            if response.status_code == 200:
                flash(f'Product {product_id} Updated Successfully')
                return redirect(url_for('admin'))
            else:
                flash('error')
        else:
            flash('info required')
    else:
        response = requests.post(f'{baseUrl+'/adminUpdate'}/{product_id}')
        if response.status_code == 200:
            item = response.json()
            return render_template('adminUpdate.html', item=item)
        else:
            flash('item not found')
            return render_template('adminUpdate.html')


@app.route('/adminDelete/<product_id>', methods=['post', 'get'])
def adminDelete(product_id):
    if request.method == 'post':
        response = requests.delete(f'{baseUrl+'/adminDelete'}/{product_id}')
        if response.status_code == 200:
            flash(f'Product Deleted Successfully')
            return redirect(url_for('admin'))
        else:
            flash('error')
            return render_template('adminDelete.html')
    else:
        response = requests.get(f'{baseUrl}/admin/{product_id}')
        if response.status_code == 200:
            item = response.json()
            return render_template('adminDelete.html', item=item)
        else:
            flash('info required')
            return render_template('adminDelete.html')


if __name__ == '__main__':
    app.run(debug=True, port=5005)
