import json
from hashlib import sha256
from time import time
from urllib.parse import urlparse
from uuid import uuid4

import requests
from flask import Flask, jsonify, request


class Blockchain(object):
    """
    每个区块包含属性：索引（index），Unix时间戳（timestamp），交易列表（transactions），工作量证明（proof）
    以及前一个区块的Hash值（previous_hash）。以下是一个区块的结构：
    block = {
       'index': 1,
       'timestamp': 1506057125.900785,
       'transactions': [
           {
               'sender': "8527147fe1f5426f9dd545de4b27ee00",
               'recipient': "a77f5cdfa2934df3954a5c7c7da5df1f",
               'amount': 5,
           }
       ],
       'proof': 324984774000,
       'previous_hash': "2cf24dba5fb0a30e26e83b2ac5b9e29e1b161e5c1fa7425e73043362938b9824"
    }
    """

    def __init__(self):
        self.chain = []
        self.current_transactions = []
        # 构造一个创世块（没有前区块的第一个区块）,并且给它加上一个工作量证明。每个区块都需要经过工作量证明，俗称挖矿.
        self.new_block(previous_hash=1, proof=100)

        self.nodes = set()

    def new_block(self, proof, previous_hash=None):
        """
        生成新块
        :param proof: <int> 通过工作算法得到的工作量证明
        :param previous_hash: (Optional) <str> 前一个区块的哈希值
        :return: 新区块
        """
        block = {
            'index': len(self.chain) + 1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }
        # 重制当前交易列表
        self.current_transactions = []
        self.chain.append(block)
        return block

    def new_transaction(self, sender, recipient, amount):
        """
        生成新交易信息，信息将加入到下一个待挖的区块中
        :param sender: <str> Address of the Sender
        :param recipient: <str> Address of the Recipient
        :param amount: <int> Amount
        :return: <int> 返回该记录将被添加到的区块(下一个待挖掘的区块)的索引
        """
        self.current_transactions.append({
            'sender': sender,
            'recipient': recipient,
            'amount': amount,
        })
        return self.last_block['index'] + 1

    @staticmethod
    def hash(block):
        """
        生成块的 SHA-256 hash值
        :param block: <dict> Block
        :return: <str>
        """
        block_string = json.dumps(block, sort_keys=True).encode()
        return sha256(block_string).hexdigest()

    @property
    def last_block(self):
        # Returns the last Block in the chain
        return self.chain[-1]

    def proof_of_work(self, previous_proof):
        """
        简单的工作量证明：
         - 查找一个p'使得 hash(pp') 以4个0开头
         - p 是上一个块的证明，p'是当前的证明
        :param previous_proof: <int>
        :return: <int>
        """
        proof = 0
        while self.valid_proof(previous_proof, proof) is False:
            proof += 1
        return proof

    def valid_proof(self, previous_proof, proof):
        """
        验证证明：是否hash(previous_proof, proof)以4个0开头
        衡量算法复杂度的办法是修改零开头的个数。使用4个来用于演示，你会发现多一个零都会大大增加计算出结果所需的时间。
        :param previous_proof: <int>
        :param proof: <int>
        :return: <bool>
        """
        guess = f'{previous_proof}{proof}'.encode()
        guess_hash = sha256(guess).hexdigest()
        return guess_hash[:4] == "0000"

    def register_node(self, address):
        """
        添加一个节点，我们用 set 来储存节点，这是一种避免重复添加节点的简单方法。
        :param address: <str> 节点地址，例如：'http://192.168.0.5:5000'
        :return: None
        """
        parsed_url = urlparse(address)
        self.nodes.add(parsed_url.netloc)

    def valid_chain(self, chain):
        """
        检查是否是有效链
        :param chain: <list> 一条链
        :return: <bool> True if valid, False if not
        """
        last_block = chain[0]
        current_index = 1
        while current_index < len(chain):
            block = chain[current_index]
            print(f'{last_block}')
            print(f'{block}')
            print("\n---------------\n")

            if block['previous_hash'] != self.hash(last_block):
                return False
            if not self.valid_proof(last_block['proof'], block['proof']):
                return False

            last_block = block
            current_index += 1

        return True

    def resolve_conflicts(self):
        """
        共识算法解决冲突，使用网络中最长的链
        :return: <bool> True 如果链条被取代，否则为 False
        """
        neighbours = self.nodes
        new_chain = None
        max_length = len(self.chain)

        for node in neighbours:
            response = requests.get(f'http://{node}/chain')
            if response.status_code == 200:
                length = response.json()['length']
                chain = response.json()['chain']
                if length > max_length and self.valid_chain(chain):
                    max_length = length
                    new_chain = chain

        if new_chain:
            self.chain = new_chain
            return True

        return False


app = Flask(__name__)

node_identifier = str(uuid4()).replace('-', '')

blockchain = Blockchain()


@app.route('/mine', methods=['GET'])
def mine():
    """
    告诉服务器去挖掘新的区块
    :return:
    """

    # 计算工作量证明PoW获得工作量证明
    last_block = blockchain.last_block
    last_proof = last_block.get('proof')
    proof = blockchain.proof_of_work(last_proof)

    # 给工作量证明的节点提供奖励。
    # 发送者为"0"表明是新挖出的币
    blockchain.new_transaction(
        sender="0",
        recipient=node_identifier,
        amount=1
    )
    # 构造新区块并将其添加到链中
    block = blockchain.new_block(proof)
    response = {
        'message': "New Block Forged",
        'index': block.get('index'),
        'transactions': block.get('transactions'),
        'proof': block.get('proof'),
        'previous_hash': block.get('previous_hash'),
    }
    return jsonify(response), 200


@app.route('/transaction/new', methods=['POST'])
def new_transaction():
    """
    创建一个交易并添加到区块
    :return:
    """
    values = request.get_json()

    # Check that the required fields are in the POST'ed data
    required = ['sender', 'recipient', 'amount']
    if not all(k in values for k in required):
        return 'Missing values', 400

    # Create a new transaction
    index = blockchain.new_transaction(values['sender'], values['recipient'], values['amount'])

    response = {'message': f'Transaction will be added to Block {index}'}
    return jsonify(response), 201


@app.route('/chain', methods=['GET'])
def full_chain():
    """
    返回整个区块链
    :param self:
    :return:
    """
    response = {
        'chain': blockchain.chain,
        'length': len(blockchain.chain),
    }
    return jsonify(response), 200


@app.route('/nodes/register', methods=['POST'])
def register_nodes():
    """
    注册节点
    :return:
    """
    values = request.get_json()
    nodes = values.get('nodes')
    if nodes is None:
        return "Error: Please supply a valid list if nodes", 400
    for node in nodes:
        blockchain.register_node(node)
    response = {
        'message': 'New nodes have been added',
        'total_nodes': list(blockchain.nodes),
    }
    return jsonify(response), 201


@app.route('/nodes/resolve', methods=['GET'])
def consensus():
    """
    解决冲突
    :return:
    """
    replaced = blockchain.resolve_conflicts()
    if replaced:
        reponse = {
            'message': 'Our chain was replaced',
            'new_chain': blockchain.chain
        }
    else:
        reponse = {
            'message': 'Our chain was authoritative',
            'chain': blockchain.chain
        }
    return jsonify(reponse), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
