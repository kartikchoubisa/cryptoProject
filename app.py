from flask import Flask, jsonify, render_template
from players import User
from players import CertificateAuthority

app = Flask(__name__)

users = []
CA = CertificateAuthority('CA')

@app.route('/')
def index():
    # A = User('Alice')
    # B = User('Bob')
    # CA = CertificateAuthority('CA')
    #
    # A.register(CA)
    # B.register(CA)

    # payload_to_send = A.send_message('Hello World!')
    # B.receive_message(**payload_to_send)


    users.append(User('Alice'))
    users.append(User('Bob'))
    return render_template('home.jinja2', users=users)

@app.route('/send_message')
def send_message():
    pass


if __name__ == '__main__':
    app.run()
