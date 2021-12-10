import collections
import hashlib

from abc import ABCMeta
from abc import abstractmethod
from bisect import bisect, bisect_left, bisect_right

Node = collections.namedtuple('Node', [
    'name', 'host', 'port', 'hrw_weight', 'keys'
])

class HashingInterface(metaclass=ABCMeta):
    @classmethod
    def __subclasshook__(self, subclass: type) -> bool:
        return (
            hasattr(subclass, 'hash_key') and callable(subclass.hash_key) and
            hasattr(subclass, 'get_node') and callable(subclass.get)
            or NotImplemented
        )
    
    @abstractmethod
    def hash_key(self, key: str) -> int:
        """generates an integer index value for the given key"""
        raise NotImplementedError
    
    @abstractmethod
    def get_node(self, key: str) -> Node:
        """lookup a node for the given key"""
        raise NotImplementedError

   
class DefaultHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.nodes = nodes
        self.num_buckets = len(self.nodes)

        
    def hash_key(self, key: str) -> int:
        # TODO
        # Naive hashing formula: key mod num_buckets
        # 1. convert key to bytearray
        # 2. sum all the bytes.
        # 3. Take the modulus of the sum % self.num_buckets
        # 4. return the value
        b = bytearray()
        b.extend(map(ord, key))
        b = list(b)
        return sum(b)%self.num_buckets

    
    def get_node(self, key: str) -> Node:
        index = self.hash_key(key)
        return self.nodes[index]


class HRWHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.nodes = nodes
        self.num_buckets = len(self.nodes)

    
    def compute_weighted_score(self, key, seed, weight):
        sha256 = hashlib.sha256()
        # TODO
        # 1. Combine two SHA256 values of key and seed. SHA256(key + seed)
        # 2. Convert to a base 16 int from the hexdigest value
        # 3. Multiply the int hash value with the given weight
        # 4. Return the value
        new_key = key + seed
        sha256.update(new_key.encode())
        digest = sha256.hexdigest()
        num = int(digest, 16)
        num = num*weight
        return num

               
    def hash_key(self, key: str) -> Node:
        """
        # TODO
        # 1. Go through each node from self.nodes
        # 2. Returns a node instance that generated the highest weight for the given key.
        """
        res = None
        max_weight = 0
        for node in self.nodes:
            weight = self.compute_weighted_score( key, node[1], node[3])
            if res is None:
                res = node
                max_weight = weight
            elif weight > max_weight:
                max_weight = weight
                res = node
        return res

    
    def get_node(self, key: str) -> Node:
        heighest_weight_node = self.hash_key(key)
        return heighest_weight_node
    

class ConsistentHash(HashingInterface):
    def __init__(self, nodes) -> None:
        super().__init__()
        self.num_buckets = pow(2, 256)
        self.keys = []
        self.nodes = []
        for n in nodes:
            key = self.hash_key(n.host)
            node_index = bisect(self.keys, key)
            self.nodes.insert(node_index, n)
            self.keys.insert(node_index, key)
        

    def hash_key(self, key: str) -> int:
        sha256 = hashlib.sha256()
        # TODO
        # 1. Generate SHA256 hash from the given key
        # 2. Convert the hex digest value to base 16 int.
        # 3. Finally, take the modulus of the int value % self.num_buckets.
        # 4. return the value
        sha256.update(key.encode())
        digest = sha256.hexdigest()
        num = int(digest, 16)
        return num%self.num_buckets

    
    def get_node(self, key: str) -> Node:
        bucket_index = self.hash_key(key)
        node_index = bisect_right(self.keys, bucket_index) % len(self.keys)
        return self.nodes[node_index]