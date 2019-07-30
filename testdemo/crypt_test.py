import hashlib
import base64
from Crypto.Cipher import AES


def md5(str):
    str = str.encode()
    m = hashlib.md5()
    m.update(str)
    sign = m.hexdigest()
    return sign


class AESCipher:
    """
    Usage:
        c = AESCipher('password').encrypt('message')
        m = AESCipher('password').decrypt(c)
    Tested under Python 3 and PyCrypto 2.6.1.
    """

    def __init__(self, key):
        self.key = key
        self.BLOCK_SIZE = 64  # Bytes
        self.pad = lambda s: s + (self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE) * \
                             chr(self.BLOCK_SIZE - len(s) % self.BLOCK_SIZE)
        self.unpad = lambda s: s[:-ord(s[len(s) - 1:])]

    # 加密
    def encrypt(self, raw):
        raw = self.pad(raw)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return base64.b64encode(cipher.encrypt(raw)).decode('utf8')

    # 解密，针对微信用此方法即可
    def decrypt(self, enc):
        enc = base64.b64decode(enc)
        cipher = AES.new(self.key, AES.MODE_ECB)
        return self.unpad(cipher.decrypt(enc)).decode('utf8')


key = "8D1ACEDAE6D4D353"
text = "status=success&taskId=unicom_ebc263128b5111e9bb910242ac11001d"
print(AESCipher(key).encrypt(text))
print(AESCipher(key).decrypt("e4s+Kcv5clbcd1z0SrgwBLqbTEKt17NDE45HKZ5Plo2vsVpqFdDH79CdXRddns9rtQGKX+O9Z/87iDoWhwPHlA=="))
