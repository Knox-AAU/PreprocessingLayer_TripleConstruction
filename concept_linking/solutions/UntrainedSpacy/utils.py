def writeFile(path, content):
    with open(path, "w") as f:
        f.write(content)


def appendFile(path, content):
    with open(path, "a") as f:
        f.write(content)


def readFile(path):
    with open(path, "r") as f:
        return f.read()


def clearFile(path):
    with open(path, "w") as f:
        f.write("")
