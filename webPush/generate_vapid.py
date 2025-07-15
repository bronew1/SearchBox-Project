from py_vapid import Vapid
from cryptography.hazmat.primitives import serialization

vapid = Vapid()
vapid.generate_keys()

private_pem = vapid.private_key.private_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PrivateFormat.PKCS8,
    encryption_algorithm=serialization.NoEncryption()
)

public_pem = vapid.public_key.public_bytes(
    encoding=serialization.Encoding.PEM,
    format=serialization.PublicFormat.SubjectPublicKeyInfo
)

print("VAPID_PUBLIC_KEY:\n", public_pem.decode())
print("VAPID_PRIVATE_KEY:\n", private_pem.decode())
