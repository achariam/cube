from twisted.web.server import Site       #import twisted stuff
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.web.static import File
 
from time import sleep
import LPD8806
led = LPD8806.strand()


for x in xrange(0, 2):
        led.fill(255, 0, 0)
        led.update()
        sleep(0.1)
        led.fill(0, 255, 0)
        led.update()
        sleep(0.1)
        led.fill(0, 0, 255)
        led.update()
        sleep(0.1)
        led.fill(255, 255, 255)
        led.update()
        sleep(0.1)

led.fill(25,100,255)
led.update()  #Bootup Sequence

 
class lampAPI(Resource):
   def render_GET(self, request):
            if 'light' in request.args:                        #'light' is the URL variable
                        if request.args['light'][0] == "on":     #Did the client put 'off' in the light var?
                                led.fill(255,255,255)
                                led.update()       #turn the lamp on
                                return " <html> light on </html> "                 #tell the browser/client that we did it
                        if request.args['light'][0] == "off":      #Did the client put 'on' in the light var? 
                                led.fill(0, 0, 0)
                                led.update()        #turn the lamp on    
                                return " <html> light off </html> "                  #tell the browser/client that we did it
 

root = File("lampwww")           #Create a folder for web interface 
root.putChild("API", lampAPI())  #Create a child that will handle requests (the second argument must be the class name)
factory = Site(root)             #Initialize the twisted object 
reactor.listenTCP(80, factory)   #Choose the port to listen on (80 is standard for HTTP) 
reactor.run()                    #Start listening, this command is an infinite loop 
                                 #so don't bother putting anything after it
