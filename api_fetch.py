def getIEX_API_KEY():
    return readAPI(0)
def getIEX_API_KEY_TEST():
    return readAPI(1)
def getNYT_API_KEY():
    return readAPI(2)
def readAPI(x):
    f = open("api_list.txt", "r")
    lines = f.readlines()
    return lines(x)
