import Pyro4

@Pyro4.expose
class Calculator(object):
    
    def add(self, n1, n2):
        return n1+n2

    def sub(self, n1, n2):
        return n1-n2
    
    def mult(self, n1, n2):
        return n1*n2
    
    def div(self, n1, n2):
        return n1/n2 if n2>0 else 0


daemon = Pyro4.Daemon.serveSimple({ Calculator: 'Calculator',}, host="localhost", port=8000, ns=False, verbose=True)				
ns = Pyro4.locateNS() 					
server = Calculator()					
uri = daemon.register(server)			
ns.register('calculator_Server', uri)	
print('Calculator Server ...')
daemon.requestLoop()	
