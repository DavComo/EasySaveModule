from enum import Enum
import requests


class Block():
    """
    A class representing data blocks.
    """

    def __init__(self, identifier: str, value: str):
        """
        The constructor for Block class.

        Parameters:
            identifier (str): The base identifier of the block.
            value (str): The assigned value of the block.
        """
        self.identifier = identifier
        self.value = value

    def __str__(self) -> str:
        return f"({self.identifier} : \'{self.value}\')"
    
    def __repr__(self) -> str:
        return str(self)
    
    @staticmethod
    def blockToDict(block: "Block") -> dict[str, str]:
        """
        Return a dictionary representing a data Block.
        """
        return {"identifier": block.identifier, "value": block.value}
    
    @staticmethod
    def dictToBlock(dictionary: dict[str, str]) -> "Block":
        """
        Return a Block representing a dictionary.
        """
        return Block(dictionary['identifier'], dictionary['value'])



class easySaveClient:
    """
    easySaveClient is a client class for interacting with the EasySave API, providing methods for authentication, block creation, retrieval, updating, and deletion.
    Attributes:
        username (str): The username used for authentication.
        address (str): The server address and API endpoint.
        protocol (__protocols): The protocol used for requests (default is "http").
        accessKey (str): The access key obtained after successful authentication.
    Methods:
        __init__(username: str, password: str, address: str = "63.179.18.244:80/api", protocol: __protocols = __protocols.http) -> None
            Initializes the easySaveClient, authenticates the user, and sets up the session.
        createBlock(blockname: str, value: str) -> None
            Creates a new data block with the specified identifier and value.
        createBlock_Typed(block: Block) -> None
            Creates a new data block using a Block object.
        getBlocks(blockname: str, strict: bool = False) -> list[dict[str, str]] | dict[str, str]
            Retrieves data blocks matching the base identifier. Returns a list of blocks or a single block if strict is True.
        getBlocksTyped(blockname: str, strict: bool = False) -> list[Block] | Block
            Retrieves data blocks as Block objects matching the base identifier. Returns a list of Block objects or a single Block if strict is True.
        updateBlock(blockname: str, newValue: str) -> None
            Updates the value of an existing block.
        deleteBlock(blockname: str) -> None
            Deletes a block with the specified identifier.
    """
    class __protocols(str, Enum):
        """
        An enumeration representing supported network protocols.

        Attributes:
            http (str): Represents the HTTP protocol.

        Methods:
            __str__(): Returns the name of the protocol as a string.
        """
        http = "http"

        def __str__(self):
            return self.value
    
    class __requestType(str, Enum):
        """
        An enumeration representing HTTP request types.

        Attributes:
            get (str): Represents the HTTP GET request method.
            post (str): Represents the HTTP POST request method.
            patch (str): Represents the HTTP PATCH request method.

        Methods:
            __str__(): Returns the name of the request type as a string.
        """
        get = "get"
        post = "post"
        patch = "patch"

        def __str__(self):
            return self.value


    def __init__(self, username: str, password: str, address: str="63.179.18.244:80/api", protocol: __protocols=__protocols.http) -> None:
        """
        The constructor for easySaveClient class.

        Parameters:
            username (str): Client username for login.
            password (str): Client password for login.
        """
        self.__session = requests.Session()

        self.username = username
        self.address = address
        self.protocol = protocol

        #Authenticate using password and username. If successful, save returned auth key for future authentication 
        response = self.__call(self.__requestType.get, "login", [("username", username), ("password", password)])
        try:
            data = response.json()
        except Exception:
            raise RuntimeError("Authentication failed: Server response is not valid JSON.")
        if "accessKey" not in data:
            raise RuntimeError(f"Authentication failed: 'accessKey' not found in server response. Response: {data}")
        self.accessKey = data["accessKey"]

        self.__session.headers.update({"RequesterUsername" : self.username, "RequesterAccessKey" : self.accessKey})

    def __call(self, requestMethod: __requestType, location: str, arguments: list[tuple[str, str]]) -> requests.Response:
        """
        Executes an HTTP request using the specified method, location, and arguments.
        Args:
            requestMethod (__requestType): The HTTP method to use for the request (e.g., 'get', 'post').
            location (str): The endpoint or path to append to the base URL.
            arguments (list[tuple[str, str]]): A list of key-value pairs to be included as query parameters in the request.
        Returns:
            requests.Response: The response object resulting from the HTTP request.
        """
        response: requests.Response

        argumentPrelimList: list[str] = []
        for argumentTuple in arguments:
            argumentPrelimList.append(f"{argumentTuple[0]}={argumentTuple[1]}")
        
        argumentString = "&".join(argumentPrelimList)
        
        func = getattr(self.__session, str(requestMethod))
        response = func(url=f"{self.protocol}://{self.address}/{location}?{argumentString}")

        return response
    

    def createBlock(self, blockname: str, value: str) -> None:
        """
        Function to create a new data block using string inputs.

        Parameters:
            blockname (str): The base identifier of the new block.
            value (str): The assigned value of the new block.
        """
        self.__call(self.__requestType.post, "create_block", [("extendedIdentifier", blockname), ("value", value)])
    
    def createBlockTyped(self, block: Block) -> None:
        """
        Function to create a new data block using Block input.

        Parameters:
            block (Block): Full Block object to be created.
        """
        blockname = block.identifier
        value = block.value
        self.createBlock(blockname, value)


    def getBlocks(self, blockname: str, strict: bool = False) -> list[dict[str, str]] | dict[str, str]:
        """
        Function to retrieve data blocks using base identifier.

        Parameters:
            blockname (str): The start of the base identifier of the blocks to query for.
            strict (bool): Whether to retrieve only the block with an identical identifier to blockname.

        Returns:
            BlockList (list[dict[str, str]]): List of blocks in a dictionary identifier:value format. Returns only a single entry if strict=True.
        """
        rawResults = self.__call(self.__requestType.get, "get_blocks", [("extendedIdentifier", blockname)]).json()['blockList']

        refinedResults: list[dict[str, str]] = []
        for result in rawResults:
            identifier_parts = result['identifier'].split(".")
            if len(identifier_parts) >= 3:
                newIdentifier: str = ".".join(identifier_parts[2:])
            else:
                newIdentifier: str = result['identifier']
            newDict: dict[str, str] = {"identifier" : newIdentifier, "value" : result['value']}
            if strict and newDict['identifier'] == blockname:
                return newDict
            elif not strict:
                refinedResults.append(newDict)
        return refinedResults
    
    def getBlocksTyped(self, blockname: str, strict: bool = False) -> list[Block] | Block:
        """
        Function to retrieve data blocks using base identifier using Block object format.

        Parameters:
            blockname (str): The start of the base identifier of the blocks to query for.
            strict (bool): Whether to retrieve only the block with an identical identifier to blockname.

        Returns:
            BlockList (list[Block] | Block): List of blocks in Block object format. Returns only a single block if strict=True.
        """
        results: list[dict[str, str]] | dict[str, str] = self.getBlocks(blockname, strict)
        if isinstance(results, dict):
            return Block(results['identifier'], results['value']) # type: ignore

        refinedResults: list[Block] = []
        for result in results:
            newBlock = Block(result['identifier'], result['value']) # type: ignore
            refinedResults.append(newBlock)
    
        return refinedResults


    def updateBlock(self, blockname: str, newValue: str) -> None:
        """
        Function to update a block.

        Parameters:
            blockname (str): The base identifier of the block to update.
            newValue (str): The new value of the block.
        """
        self.__call(self.__requestType.patch, "update_block", [("extendedIdentifier", blockname), ("value", newValue)])

    def deleteBlock(self, blockname: str) -> None:
        """
        Function to delete a block.

        Parameters:
            blockname (str): The base identifier of the block to delete.
        """
        self.__call(self.__requestType.post, "delete_block", [("extendedIdentifier", blockname)])
