from flask import Flask
import sys
from flask_restful import Api, Resource

app = Flask(__name__)
api = Api(app)


class TodayEventResource(Resource):
    def get(self):
        return {"data": "There are no events for today!"}


api.add_resource(TodayEventResource, '/event/today')

# do not change the way you run the program
if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()
