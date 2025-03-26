from api.create_app import create_app
from api.server_status import checkServerStatus
import time

while True:
    if checkServerStatus():
        print("Servers Connected!")
        app = create_app()
        app.run()
        break
    else:
        print("Server is offline. Checking again in 15 minutes...")
        time.sleep(900)