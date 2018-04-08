from flask import Flask

app = Flask('mini-amazon')


@app.route('/health', methods=['GET'])
def health():
    return 'healthy\n'


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
