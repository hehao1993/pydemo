from hashlib import sha256
from datetime import datetime


def generate_block(oldblock, bpm, address):
    """

    :param oldblock:
    :param bpm:
    :param address:
    :return:
    """
    newblock = {
        "Index": oldblock["Index"] + 1,
        "BPM": bpm,
        "Timestamp": str(datetime.now()),
        "PrevHash": oldblock["Hash"],
        "Validator": address
    }
    newblock["Hash"] = calculate_hash(newblock)
    return newblock


def calculate_hash(block):
    record = "".join([
        str(block["Index"]),
        str(block["BPM"]),
        block["Timestamp"],
        block["PrevHash"]
    ])
    return sha256(record.encode()).hexdigest()


def is_block_valid(newblock, oldblock):
    """

    :param newblock:
    :param oldblock:
    :return:
    """
    if oldblock["index"] + 1 != newblock["Index"]:
        return False
    if oldblock["Hash"] != newblock["PrevHash"]:
        return False
    if calculate_hash(newblock) != newblock["Hash"]:
        return False
    return True