import sqlite3

from flask import Flask, render_template, request, redirect, url_for, flash, jsonify, session
import requests
import json
import re

app = Flask(__name__)

app.secret_key = 'dtd'
sqldbname_sanpham = 'C:/Users/trieu/Downloads/PyCharm/pythonProject/sanpham.db'

baseUrl = 'http://127.0.0.1:5002'

#
# @app.route('/', methods=['get'])
# def index():
#     response = requests.get(baseUrl)
#     if response.status_code == 200:
#         items = response.json()
#         return render_template('/admin/index.html', items=items)
#     else:
#         flash('Something went wrong')
#     return render_template('/admin/index.html')


@app.route('/search', methods=['get', 'post'])
def search():
    if request.method == 'POST':
        search_text = request.form.get('search_text')
        response = requests.post(baseUrl+'/searchData', json={'search_text': search_text})
        if response.status_code == 200:
            items = response.json()
            return render_template('/admin/search.html', items=items)
        else:
            flash('Something went wrong')
            return render_template('/admin/search.html')
    elif request.method == 'GET':
        response = requests.get(baseUrl)
        if response.status_code == 200:
            return render_template('/admin/search.html')
        else:
            flash('Something went wrong')


@app.route('/admin', methods=['get'])
def admin():
    response = requests.get(baseUrl)
    if response.status_code == 200:
        items = response.json()
        return render_template('/admin/admin.html', items=items)
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
                f'{baseUrl+'/adminAdd'}', json={
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
                return render_template('/admin/adminAdd.html')
        else:
            flash('info required')
            return redirect(url_for('adminAdd'))
    else:
        return render_template('/admin/adminAdd.html')


@app.route('/test/<id>', methods=['get', 'post'])
def test(id):
    print(id)
    return id


# @app.route('/adminUpdate/<product_id>', methods=['get', 'post'])
# def adminUpdate(product_id):
#     # print(product_id)
#     # print(f'{baseUrl+'/adminUpdate'}/{product_id}')
#     if request.method == 'post':
#         name = request.form.get('product_name')
#         quantity = request.form.get('quantity')
#         price = request.form.get('price')
#         img = request.form.get('img')
#         if name and quantity and price and img:
#             response = requests.put(
#                 f'{baseUrl+'/adminUpdate/'}{product_id}',
#                 json={'product_name': name, 'quantity': quantity, 'price': price, 'img': img}
#                 )
#             if response.status_code == 200:
#                 flash(f'Product {product_id} Updated Successfully')
#                 return redirect(url_for('admin'))
#             else:
#                 flash('error')
#                 return redirect(url_for('adminUpdate'))
#         else:
#             flash('info required')
#             return redirect(url_for('adminUpdate'))
#     else:
#         response = requests.post(f'{baseUrl+'/adminUpdate'}/{product_id}')
#         if response.status_code == 200:
#             item = response.json()
#             return render_template('adminUpdate.html', item=item)
#         else:
#             flash('item not found')
#             return render_template('adminUpdate.html')
#
#
# @app.route('/adminDelete/<product_id>', methods=['post', 'get'])
# def adminDelete(product_id):
#     if request.method == 'post':
#         response = requests.delete(f'{baseUrl+'/adminDelete'}/{product_id}')
#         if response.status_code == 200:
#             flash(f'Product Deleted Successfully')
#             return redirect(url_for('admin'))
#         else:
#             flash('error')
#             return render_template('adminDelete.html')
#     else:
#         response = requests.get(f'{baseUrl}/admin/{product_id}')
#         if response.status_code == 200:
#             item = response.json()
#             return render_template('adminDelete.html', item=item)
#         else:
#             flash('info required')
#             return render_template('adminDelete.html')

def get_db_connection():
    connection = sqlite3.connect(sqldbname_sanpham)
    connection.row_factory = sqlite3.Row
    return connection


@app.route('/adminUpdate/<product_id>', methods=['post', 'get'])
def adminUpdate(product_id):
    if request.method == 'POST':
        name = request.form.get('product_name')
        quantity = request.form.get('quantity')
        price = request.form.get('price')
        img = request.form.get('img')
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('update sanpham set product_name=?, quantity=?, price=?, img=? where product_id=?', (name, quantity, price, img, product_id))
        connection.commit()
        connection.close()
        flash('updated', 'success')
        return redirect(url_for('admin'))
    else:
        connection = get_db_connection()
        cur = connection.cursor()
        cur.execute('select * from sanpham where product_id=?', (product_id,))
        item = cur.fetchone()
        connection.close()
        return render_template('/admin/adminUpdate.html', item=item)


@app.route('/adminDelete/<product_id>', methods=['post'])
def delete(product_id):
    connection = get_db_connection()
    cur = connection.cursor()
    cur.execute("delete from sanpham where product_id like '%"+product_id+"%'")
    connection.commit()
    connection.close()
    flash('deleted', 'success')
    return redirect(url_for('admin'))



sqldbname_kiet = 'infiniti.db'


@app.route('/')
def index():
    return render_template('/user/index.html')
@app.route('/login', methods=['GET', 'POST'])
def login():
    message = ''
    if request.method == 'POST' and 'email' in request.form and 'password' in request.form:
        email = request.form['email']
        password = request.form['password']
        conn = sqlite3.connect(sqldbname_kiet)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ? AND password =  ?', (email, password,))
        user = cursor.fetchone()
        conn.close()

        # Check admin
        conn2 = sqlite3.connect(sqldbname_kiet)
        cur = conn2.cursor()
        cur.execute('SELECT * FROM user_addmin WHERE email = ? AND password = ?  ', (email, password,))
        admin = cur.fetchall()
        print(admin)
        if user :
            session['loggedin'] = True
            session['userid'] = user[0]
            session['name'] = user[1]
            session['email'] = user[2]
            message = 'Logged in successfully!'
            con2 = conn2.cursor()
            con2.execute('SELECT * FROM user where email = ?', (email,))
            user_name = con2.fetchone()
            return render_template(template_name_or_list='/user/user_login.html', message=message, user=user_name)
        elif admin :
            # return render_template(template_name_or_list='/admin/admin.html')
            # con2 = conn2.cursor()
            # con2.execute('select * from user_addmin where email=?', (email,))
            # admin = con2.fetchone()
            # return render_template('/admin/admin.html', user=admin)
            return redirect(url_for('admin'))
        else:
            message = 'Please enter correct email / password!'
    return render_template(template_name_or_list='/user/login.html', message=message)


@app.route('/logout')
def logout():
    session.pop('loggedin', None)
    session.pop('userid', None)
    session.pop('email', None)
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    message = ''
    if request.method == 'POST' and 'name' in request.form and 'password' in request.form and 'email' in request.form:
        userName = request.form['name']
        password = request.form['password']
        email = request.form['email']
        conn = sqlite3.connect(sqldbname_kiet)
        cursor = conn.cursor()
        cursor.execute('SELECT * FROM user WHERE email = ?', (email,))
        account = cursor.fetchone()
        if account:
            message = 'Account already exists!'
        elif not re.match(r'[^@]+@[^@]+\.[^@]+', email):
            message = 'Invalid email address!'
        elif not userName or not password or not email:
            message = 'Please fill out the form!'
        else:
            cursor.execute('INSERT INTO user VALUES (NULL, ?, ?, ?)', (userName, email, password,))
            conn.commit()
            message = 'You have successfully registered!'
            return redirect(url_for('login'))
        conn.close()
    elif request.method == 'POST':
        message = 'Please fill out the form!'
    return render_template('/user/register.html', message=message)

if __name__ == '__main__':
    app.run(debug=True, port=5005)
