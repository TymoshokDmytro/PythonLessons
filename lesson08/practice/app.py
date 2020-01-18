import os
import traceback

from flask import Flask, render_template, redirect, request, flash, session

from lesson08.practice.model import AuthenticationService, Role, only_for_role, OnlineStore, check_auth

app = Flask(__name__)
app.secret_key = "1zszATDrlYAIexo6frPN"
store = OnlineStore(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'goods.db'), True)


@app.route("/")
@check_auth
def index():
    categories = store.get_categories()
    goods = store.get_all_goods()
    return render_template("index.html",
                           categories=categories,
                           goods=goods)


@app.route("/category/<int:categorie_id>")
@check_auth
def category(categorie_id):
    categories = store.get_categories()
    goods = store.get_goods_by_category_id(categorie_id)
    return render_template("index.html",
                           categories=categories,
                           goods=goods)


@app.route("/goods/<int:item_id>")
@check_auth
def goods(item_id):
    categories = store.get_categories()
    items = store.get_goods_by_id(item_id)
    return render_template("index.html",
                           categories=categories,
                           items=items)


@app.route("/logout", methods=['GET'])
def logout():
    AuthenticationService.logout()
    session.clear()
    return redirect('login')


@app.route("/login", methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        if AuthenticationService.is_authenticated():
            redirect('/')
        return render_template("login.html")

    login = request.form['login']
    password = request.form['password']

    resp = AuthenticationService.login(login, password)
    if 'error' in resp:
        flash(resp['error'], 'errors')
        return render_template('login.html')
    session['role'] = AuthenticationService.get_role().name
    session['user'] = AuthenticationService.get_user()
    return redirect('/')


@app.route("/admin")
@only_for_role(Role.ADMIN)
def admin():
    items = store.get_all_goods()
    categories = store.get_categories()
    return render_template("admin.html",
                           items=items,
                           categories=categories)


@app.route('/categories/new', methods=['POST'])
@only_for_role(Role.ADMIN)
def create_category():
    category_name = request.form['category_name']

    store.create_category(category_name)

    flash('Category with name ' + category_name + ' created', 'info')
    return redirect('/admin')


@app.route('/categories/delete/<int:category_id>')
@only_for_role(Role.ADMIN)
def delete_category(category_id):
    store.delete_category_by_id(category_id)
    flash('Category with id ' + str(category_id) + ' was deleted', 'info')
    return redirect('/admin')

@app.route("/goods/new", methods=['POST'])
@only_for_role(Role.ADMIN)
def goods_create():
    try:
        category_id = request.form['category_id']
        article_name = request.form['article_name']
        barcode = request.form['barcode']
        description = request.form['description']
        is_present = int(request.form['is_present'])
        price = float(request.form['price'])
        stock = float(request.form['stock'])

        store.create_item(category_id, article_name, barcode, description, is_present, price, stock)
        flash('Item with name ' + article_name + ' was created', 'info')
    except Exception:
        flash(traceback.format_exc(), 'errors')
        traceback.print_exc()
    return redirect('/admin')


@app.route("/goods/delete/<int:item_id>")
@only_for_role(Role.ADMIN)
def goods_delete(item_id):
    store.delete_item_by_id(item_id)
    flash('Item with id ' + str(item_id) + ' was deleted', 'info')
    return redirect('/admin')


if __name__ == '__main__':
    app.run(debug=True)
