# Import our service's bus client
from bus import bus

# Call the check_password() procedure on our auth API
say_it = bus.hello.world()

print(say_it)