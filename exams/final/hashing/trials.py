s = 'ABCDABCD'
b = bytearray()
b.extend(map(ord, s))
print(list(b))

import hashlib
from hash_util import Node

sha256 = hashlib.sha256()
sha256.update('helloworld'.encode())
print(sha256.hexdigest())
print(int(sha256.hexdigest(),16))


NODES = [
    Node(name='Alex', host='1.2.3.1', port=80, hrw_weight=100, keys=[]),
    Node(name='Bob', host='1.2.3.2', port=80, hrw_weight=100, keys=[]),
    Node(name='Cody', host='1.2.3.3',port=80, hrw_weight=100, keys=[])
]

