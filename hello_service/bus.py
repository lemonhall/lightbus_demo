# File: hello_service/bus.py
import lightbus

bus = lightbus.create()

class HelloApi(lightbus.Api):
    user_registered = lightbus.Event(parameters=('username', 'email'))

    class Meta:
        name = 'hello'

    def world(self):
        return "world"

# Register this API with Lightbus. Lightbus will respond to 
# remote procedure calls for registered APIs, as well as allow you 
# as the developer to fire events on any registered APIs.
bus.client.register_api(HelloApi())