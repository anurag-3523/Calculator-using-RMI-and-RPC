from xmlrpc.server import SimpleXMLRPCServer

def div(n1, n2):
    return n1/n2 if n2>0 else 0

server = SimpleXMLRPCServer(("localhost", 8004))
print("Listening on port 8004...")
server.register_function(div, "div")
server.serve_forever()
