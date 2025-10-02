from easysave import Block, easySaveClient
import os


def test_connection():
    response = os.system("curl http://63.179.18.244/api/docs")
    assert response == 0

def test_authentication():
    global client
    client = easySaveClient("testuser", "testpassword")

def test_reset_account():
    existingBlocks: list[Block] = client.getBlocksTyped("") #type: ignore
    for block in existingBlocks:
        client.deleteBlock(block.identifier)
    blockCheck = client.getBlocks("")
    assert blockCheck == []

def test_block_creation():
    client.createBlock("testblock", "testblockvalue")

    block: Block = client.getBlocksTyped("testblock", True) #type: ignore
    assert block.identifier == "testblock"
    assert block.value == "testblockvalue"

def test_block_update():
    client.updateBlock("testblock", "newtestblockvalue")

    block: Block = client.getBlocksTyped("testblock", True) #type: ignore
    assert block.identifier == "testblock"
    assert block.value == "newtestblockvalue"

def test_block_deletion():
    client.deleteBlock("testblock")

    blockCheck = client.getBlocksTyped("testblock", True)
    assert blockCheck == []

def test_block_translation():
    identifier = "testblock"
    value = "testblockvalue"

    newBlock = Block.dictToBlock({"identifier" : identifier, "value" : value})
    assert newBlock.identifier == identifier
    assert newBlock.value == value

    blockDict = Block.blockToDict(newBlock)
    assert blockDict["identifier"] == identifier
    assert blockDict["value"] == value
