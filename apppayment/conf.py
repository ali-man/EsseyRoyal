import hashlib

HASH_API = '0bf51109-67f9-441d-8371-b9f9495ef266'
G2A_EMAIL = 's.oybek1993@mail.ru'
SECRET_API = '9h2hF&XqP!&Pb94lDx3d8if54ztFna9w5BRL9y*Zr^yG6=_Jn~wvaO-eBhtz5=jA'
HASH256 = HASH_API+G2A_EMAIL+SECRET_API
RESULT = hashlib.sha256(HASH256.encode('utf-8')).hexdigest()