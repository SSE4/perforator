import base64
import json
import os


token = os.environ['ID_TOKEN']

parts = token.split('.')

assert len(parts) == 3
print(json.loads(base64.b64decode(parts[0])))
print(json.loads(base64.b64decode(parts[1])))

