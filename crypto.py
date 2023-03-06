from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography import x509
from cryptography.x509.oid import NameOID
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from datetime import datetime, timedelta

# Generate a private key for use in the exchange.
def generate_private_key():
    return rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

def generate_x509_certificate(private_key, days=365):
    # generates a self-signed certificate (this will be used to sign other certificates. IRL some other CA would sign this one)
    # sha256 for hashing
    # rsa for DSA

    # Define the subject name for the CA certificate
    subject_name = x509.Name([
        x509.NameAttribute(NameOID.COMMON_NAME, u'My Test CA')
    ])

    # Define the basic constraints for the CA certificate
    basic_constraints = x509.BasicConstraints(ca=True, path_length=None)

    # Define the validity period for the CA certificate
    validity_period = timedelta(days)

    # Define the issuer and serial number for the CA certificate
    issuer = subject_name
    serial_number = x509.random_serial_number()

    # Create the CA certificate
    ca_cert = x509.CertificateBuilder().subject_name(
        subject_name
    ).issuer_name(
        issuer
    ).public_key(
        private_key.public_key()
    ).serial_number(
        serial_number
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + validity_period
    ).add_extension(
        basic_constraints,
        critical=True
    ).sign(
        private_key,
        hashes.SHA256(),
        default_backend()
    )

    return ca_cert

    # # Save the CA certificate to a file
    # with open('ca.crt', 'wb') as f:
    #     f.write(ca_cert.public_bytes(Encoding.PEM))

def generate_csr(name, private_key):
    csr = x509.CertificateSigningRequestBuilder().subject_name(
        x509.Name([
            x509.NameAttribute(NameOID.COMMON_NAME, name)
        ])
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    ).sign(
        private_key, hashes.SHA256(), default_backend()
    )
    return csr

def sign_csr(csr, private_key):
    user_cert = x509.CertificateBuilder().subject_name(
        csr.subject
    ).issuer_name(
        csr.subject # TODO: read more. subject ad issuer are the same?
    ).public_key(
        csr.public_key()
    ).serial_number(
        x509.random_serial_number()
    ).not_valid_before(
        datetime.utcnow()
    ).not_valid_after(
        datetime.utcnow() + timedelta(days=365)
    ).add_extension(
        x509.BasicConstraints(ca=False, path_length=None), critical=True
    ).sign(
        private_key, hashes.SHA256(), default_backend()
    )

    return user_cert

def get_signed_message(message, private_key):
    signature = private_key.sign(
        message.encode('utf-8'),
        padding.PSS(
            mgf=padding.MGF1(hashes.SHA256()),
            salt_length=padding.PSS.MAX_LENGTH
        ),
        hashes.SHA256()
    )

    return signature

def verify_certificate(name, certificate):
    # cert = x509.load_pem_x509_certificate(certificate, default_backend())

    return certificate.subject.get_attributes_for_oid(NameOID.COMMON_NAME)[0].value == name

