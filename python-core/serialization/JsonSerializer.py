import json

class JsonSerializer:
    def serialize(self, object):
        return json.dumps(object, default=lambda o: o.__dict__)