  
from xmlrpc.server import SimpleXMLRPCServer

def mult(n1, n2):
    return n1 * n2

server = SimpleXMLRPCServer(("localhost", 8003))
print("Listening on port 8003...")
server.register_function(mult, "mult")
server.serve_forever()
