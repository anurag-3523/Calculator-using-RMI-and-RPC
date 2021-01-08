from xmlrpc.server import SimpleXMLRPCServer

def add(n1, n2):
    return n1 + n2

server = SimpleXMLRPCServer(("localhost", 8001))
print("Listening on port 8001...")
server.register_function(add, "add")
server.serve_forever()
