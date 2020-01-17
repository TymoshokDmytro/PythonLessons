from flask import Flask, render_template, redirect, request, flash, session

from lesson08.practice.model import AuthenticationService, check_auth, only_for_roles, Role, only_for_role

app = Flask(__name__)
app.secret_key = "1zszATDrlYAIexo6frPN"


@app.route("/")
@check_auth
def index():
    session['user'] = AuthenticationService.get_user()
    return render_template("index.html",
                           )


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
    return redirect('/')


@app.route("/admin")
@only_for_role(Role.ADMIN)
def admin():
    return render_template("admin.html")


if __name__ == '__main__':
    app.run(debug=True)
