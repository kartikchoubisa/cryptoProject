from crypto import generate_private_key, generate_x509_certificate, generate_csr, sign_csr, get_signed_message, verify_certificate

class CertificateAuthority:
    def __init__(self, name):
        self.name = name
        self.private_key = generate_private_key()
        self.public_key = self.private_key.public_key()
        self.certificate = generate_x509_certificate(self.private_key)

    def __repr__(self):
        return f'CA({self.name})'

    def issue_certificate(self, csr):
        return sign_csr(csr, self.private_key)



class User:
    def __init__(self, name):
        self.name = name
        self.private_key = generate_private_key()
        self.public_key = self.private_key.public_key()
        self.certificate = None

    def __repr__(self):
        return f'User({self.name}, {self.public_key})'

    def register(self, ca):
        # create csr
        csr = generate_csr(self.name, self.private_key)
        # send csr to ca, ca signs it and returns the certificate
        self.certificate = ca.issue_certificate(csr)
        print(f"{self.name} registered with {ca.name}")

    def send_message(self, message):
        # TODO: not encrypting the messsage yet
        signature = get_signed_message(message, self.private_key) # TODO: not being verifed yet
        return {
            'sender_name': self.name,
            'message': message,
            'sender_signature': signature,
            'sender_certificate': self.certificate,
            'sender_public_key': self.public_key
        }

    def receive_message(self, sender_name, message, sender_signature, sender_certificate, sender_public_key):
        # self.verify_message(message, signature, public_key)

        if self.verify_sender(sender_name, sender_certificate):
            print(f'{self.name} received message from {sender_name}: {message}')
            print(f"details: {sender_name}, {message}, {sender_signature}, {sender_certificate}, {sender_public_key}")
            return {'message': message}
            # return {'verified': True, 'message': message, 'signature': sender_signature, 'public_key': sender_public_key}

        else:
            print(f'could not verify sender')
            return {'verified', False}

    def verify_sender(self, sender_name, sender_certificate):
        # returns true if sender is verified
        is_verified = verify_certificate(sender_name, sender_certificate)
        print(f"{self.name} verified {sender_name}'s certificate: {is_verified}")
        return is_verified

    def verify_message(self, message, signature, public_key):
        pass





