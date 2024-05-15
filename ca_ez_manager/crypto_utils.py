import datetime
from typing import Tuple

from cryptography import x509
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.x509.oid import NameOID


def generate_certificate() -> Tuple[rsa.RSAPrivateKey, x509.Certificate]:
    # TODO: pass parameters

    private_key = rsa.generate_private_key(
        public_exponent=65537, key_size=2048, backend=default_backend()
    )
    public_key = private_key.public_key()

    builder = x509.CertificateBuilder()
    builder = builder.subject_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, "openstack-ansible Test CA"),
                x509.NameAttribute(NameOID.ORGANIZATION_NAME, "openstack-ansible"),
                x509.NameAttribute(
                    NameOID.ORGANIZATIONAL_UNIT_NAME, "Default CA Deployment"
                ),
            ]
        )
    )
    builder = builder.issuer_name(
        x509.Name(
            [
                x509.NameAttribute(NameOID.COMMON_NAME, "openstack-ansible Test CA"),
            ]
        )
    )
    builder = builder.not_valid_before(
        datetime.datetime.today() - datetime.timedelta(days=1)
    )
    builder = builder.not_valid_after(
        datetime.datetime.today() + datetime.timedelta(days=365)
    )
    builder = builder.serial_number(x509.random_serial_number())
    builder = builder.public_key(public_key)
    builder = builder.add_extension(
        x509.BasicConstraints(ca=True, path_length=None),
        critical=True,
    )

    cert = builder.sign(
        private_key=private_key, algorithm=hashes.SHA256(), backend=default_backend()
    )

    return private_key, cert


def sign_certificate(ca_private_key, ca_cert):
    # TODO: pass parameters

    private_key = rsa.generate_private_key(
        public_exponent=65537,
        key_size=2048,
    )

    csr = (
        x509.CertificateSigningRequestBuilder()
        .subject_name(
            x509.Name(
                [
                    # Provide various details about who we are.
                    x509.NameAttribute(NameOID.COUNTRY_NAME, "US"),
                    x509.NameAttribute(NameOID.STATE_OR_PROVINCE_NAME, "California"),
                    x509.NameAttribute(NameOID.LOCALITY_NAME, "San Francisco"),
                    x509.NameAttribute(NameOID.ORGANIZATION_NAME, "My Company"),
                    x509.NameAttribute(NameOID.COMMON_NAME, "mysite.com"),
                ]
            )
        )
        .add_extension(
            x509.SubjectAlternativeName(
                [
                    # Describe what sites we want this certificate for.
                    x509.DNSName("mysite.com"),
                    x509.DNSName("www.mysite.com"),
                    x509.DNSName("subdomain.mysite.com"),
                ]
            ),
            critical=False,
            # Sign the CSR with our private key.
        )
        .sign(private_key, hashes.SHA256())
    )

    cert = (
        x509.CertificateBuilder()
        .subject_name(csr.subject)
        .issuer_name(ca_cert.subject)
        .public_key(csr.public_key())
        .serial_number(x509.random_serial_number())
        .not_valid_before(datetime.datetime.today() - datetime.timedelta(days=1))
        .not_valid_after(datetime.datetime.today() + datetime.timedelta(days=365))
        .sign(ca_private_key, hashes.SHA256())
    )

    return private_key, csr, cert


def save_private_key(private_key, path):
    with open(path, "wb") as f:
        f.write(
            private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.TraditionalOpenSSL,
                encryption_algorithm=serialization.NoEncryption(),
            )
        )


def save_certificate(cert, path):
    with open(path, "wb") as f:
        f.write(
            cert.public_bytes(
                encoding=serialization.Encoding.PEM,
            )
        )


def load_private_key(path):
    with open(path, "rb") as f:
        return serialization.load_pem_private_key(
            f.read(), password=None, backend=default_backend()
        )


def load_certificate(path):
    with open(path, "rb") as f:
        return x509.load_pem_x509_certificate(f.read(), default_backend())


def save_csr(csr, path):
    with open(path, "wb") as f:
        f.write(csr.public_bytes(serialization.Encoding.PEM))
