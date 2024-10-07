def vigenere_cipher(message, key, mode='encrypt'):
    result = ''
    key_length = len(key)
    key_as_int = [ord(k) for k in key]

    for i, char in enumerate(message):
        if char.isalpha():
            case_offset = 65 if char.isupper() else 97  #lowercase and uppercase handling
            char_as_int = ord(char) #converts into ascii val
            key_char_as_int = key_as_int[i % key_length]

            if mode == 'encrypt':
                encrypted_char = (char_as_int + key_char_as_int - case_offset) % 26 + case_offset
            elif mode == 'decrypt':
                encrypted_char = (char_as_int - key_char_as_int - case_offset) % 26 + case_offset
            else:
                raise ValueError("Invalid mode. Use 'encrypt' or 'decrypt'.")

            result += chr(encrypted_char)
        else:
            result += char

    return result


# Example usage: Use this to test the above function lol , I am so lazy to write a test file
# plaintext = "Hello123! How are you?"
# key = "Key"
# encrypted_text = vigenere_cipher(plaintext, key, mode='encrypt')
# decrypted_text = vigenere_cipher(encrypted_text, key, mode='decrypt')
#
# print("Original text:", plaintext)
# print("Encrypted text:", encrypted_text)
# print("Decrypted text:", decrypted_text)
