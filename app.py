from flask import Flask, jsonify, render_template
from players import User
from players import CertificateAuthority

app = Flask(__name__)

users = []
users.append(User('arjun'))
users.append(User('bheem'))
CA = CertificateAuthority('CA')
payload_to_send = None
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
# @app.route('/generate_certificate/')
# def generate_certificate():
@app.route('/generate_certificate/arjun', methods=['GET'])
def generate_certificate():
    user = users[0]
    user.register(CA)
    return jsonify({'certificate': user.certificate.public_bytes().decode('utf-8')})
@app.route('/generate_certificate/bheem', methods=['GET'])
def generate_certificate():
    user = users[1]
    user.register(CA)
    return jsonify({'certificate': user.certificate.public_bytes().decode('utf-8')})


@app.route('/send_message/<string : message>',)
def send_message(message):
    user = users[0]
    payload_to_send = user.send_message(message)
    return jsonify(payload_to_send)
    pass
@app.route('/receive_message')
def receive_message():
    user = users[1]
    payload_to_send = user.receive_message(**payload_to_send)
    return jsonify(payload_to_send)
    pass
if __name__ == '__main__':
    app.run()