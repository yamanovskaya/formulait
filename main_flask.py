from flask import Flask, render_template

app = Flask(__name__)


@app.route('/', methods=['get', 'post'])
def index():
    return render_template('index.html')


@app.route('/describe')
def describe():
    return render_template('describe.html')


@app.route('/resalt', methods=['get', 'post'])
def resalt():
    # TODO v1 и v2 надо получить из счетчика кластеров файла main.final
    # TODO на странице надо сделать отображение подгруженного изображения до и после обработки (скорее всего это будут готовые pngшки т.к. конвертацию из tiff никто не сделал)
    v1 = 1
    v2 = 2
    return render_template('resalt.html',
                           value1=v1,
                           value2=v2)


if __name__ == '__main__':
    app.run()
