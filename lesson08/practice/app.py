import os

from flask import Flask, render_template, redirect, request, flash, session

from lesson08.practice.model import AuthenticationService, Role, only_for_role, OnlineStore, \
    OnlineStoreDBService, check_auth

app = Flask(__name__)
app.secret_key = "1zszATDrlYAIexo6frPN"
store = OnlineStore(OnlineStoreDBService(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'goods.db'), True))


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
    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
