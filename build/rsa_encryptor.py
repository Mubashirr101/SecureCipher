from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.backends import default_backend

class RSAEncryptor:
    def __init__(self):
        # Initialize key variables
        self.sender_private_key = None
        self.sender_public_key = None
        self.receiver_private_key = None
        self.receiver_public_key = None
        self.is_decryption_clicked = False  # Flag to track decryption button click

    def set_decryption_clicked(self):
        self.is_decryption_clicked = True

    def set_private_key_from_file(self, file_path):
        with open(file_path, 'rb') as file:
            private_key = serialization.load_pem_private_key(file.read(), password=None, backend=default_backend())
        if self.is_decryption_clicked:
            self.receiver_private_key = private_key
        else:
            self.sender_private_key = private_key
        print(f"Private Key set: {private_key}")

    def set_public_key_from_file(self, file_path):
        with open(file_path, 'rb') as file:
            public_key = serialization.load_pem_public_key(file.read(), backend=default_backend())
        if self.is_decryption_clicked:
            self.sender_public_key = public_key
        else:
            self.receiver_public_key = public_key
        print(f"Public Key set: {public_key}")
    def encrypt_and_sign(self, plaintext):
        # Check if keys are available
        print(f"Encrypting with public key: {self.receiver_public_key}")

        if self.receiver_public_key is None or self.sender_private_key is None:
            raise ValueError("Sender's private key or receiver's public key is missing.")

        # Step 1: Encrypt with Receiver's Public Key
        ciphertext = self.receiver_public_key.encrypt(
            plaintext.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        # Step 2: Sign with Sender's Private Key
        signature = self.sender_private_key.sign(
            ciphertext,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        return ciphertext, signature

    def verify_and_decrypt(self, ciphertext, signature):
        # Check if keys are set
        print(f"Verifying with public key: {self.sender_public_key}")

        if not (self.sender_public_key and self.receiver_private_key):
            raise ValueError("Sender's public key or receiver's private key is missing.")

        # Verify the signature using Sender's Public Key
        self.sender_public_key.verify(
            signature,
            ciphertext,
            padding.PSS(
                mgf=padding.MGF1(hashes.SHA256()),
                salt_length=padding.PSS.MAX_LENGTH
            ),
            hashes.SHA256()
        )

        # Decrypt with Receiver's Private Key
        decrypted_text = self.receiver_private_key.decrypt(
            ciphertext,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )

        return decrypted_text.decode()

