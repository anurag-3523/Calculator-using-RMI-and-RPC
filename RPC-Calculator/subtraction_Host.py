from xmlrpc.server import SimpleXMLRPCServer

def sub(n1, n2):
    return n1 - n2

server = SimpleXMLRPCServer(("localhost", 8002))
print("Listening on port 8002...")
server.register_function(sub, "sub")
server.serve_forever()
