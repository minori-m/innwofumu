# Try using response

import threading
import time
#!/usr/bin/env python
# python
from flask import Flask
import time

ts=time.time()

app = Flask(__name__)
@app.route("/", methods=['GET'])
def index():
    t=time.time()
    x= t-ts
    x1=str(x)
    return x1[0:10]

if __name__ == "__main__":
    app.debug = True
    app.run() 
