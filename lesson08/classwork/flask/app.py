from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def hello_world():
    my_name = "Dmytro"
    list_of_items = ['one', 'two', 'three']
    to_buy = {
        'goods_1': 3,
        'goods_2': 4,
        'goods_3': 5,
    }
    return render_template('index.html',
                           my_name=my_name,
                           list_of_items=list_of_items,
                           to_buy=to_buy)


if __name__ == '__main__':
    app.run(debug=True)
