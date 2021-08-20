from flask import Flask
from flask_restful import Resource, Api, inputs, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import sys
from datetime import date
from flask import abort, request
import logging

# Setting up
app = Flask(__name__)
db = SQLAlchemy(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///events.db'
db.create_all()
api = Api(app)


# Creating a model for database
class Event(db.Model):
    __tablename__ = 'events'
    id = db.Column(db.Integer, primary_key=True)
    event = db.Column(db.String, nullable=False)
    date = db.Column(db.Date, nullable=False)


# Making resource fields for marshalling
resource_fields = {
    'id': fields.Integer,
    'event': fields.String,
    'date': fields.DateTime(dt_format='iso8601')
}

# Parser for arguments
parser = reqparse.RequestParser()
# Including types of arguments expected
parser.add_argument(
    'event',
    type=str,
    help="The event name is required!",
    required=True
)
parser.add_argument(
    'date',
    type=inputs.date,
    help="The event date with the correct format is required! The correct format is YYYY-MM-DD!",
    required=True
)
parser.add_argument(
    'start_time',
    type=inputs.date,
    required=False
)
parser.add_argument(
    'end_time',
    type=inputs.date,
    required=False
)


class EventResource(Resource):
    @marshal_with(resource_fields)
    def get(self):
        start = request.args.get("start_time")
        end = request.args.get("end_time")
        if start and end:
            events = Event.query.filter(Event.date.between(start, end)).all()
            if len(events) < 1:
                abort(404, {"message": "The event doesn't exist!"})
            return events
        else:
            return Event.query.all()

    def post(self):
        args = parser.parse_args()
        event = Event(id=len(Event.query.all()) + 1, event=args['event'], date=args['date'])
        db.session.add(event)
        db.session.commit()
        response = {'message': 'The event has been added!', 'event': args['event'], 'date': str(args['date'].date())}
        return response


class EventToday(Resource):
    @marshal_with(resource_fields)
    def get(self, get_date=date.today()):
        return Event.query.filter(Event.date == get_date).all()


class EventByID(Resource):
    @marshal_with(resource_fields)
    def get(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        return event

    def delete(self, event_id):
        event = Event.query.filter(Event.id == event_id).first()
        if event is None:
            abort(404, "The event doesn't exist!")
        db.session.delete(event)
        db.session.commit()
        return {'message': 'The event has been deleted!'}


api.add_resource(EventResource, '/event')
api.add_resource(EventToday, '/event/today')
api.add_resource(EventByID, '/event/<int:id>')

if __name__ == '__main__':
    if len(sys.argv) > 1:
        arg_host, arg_port = sys.argv[1].split(':')
        app.run(host=arg_host, port=arg_port)
    else:
        app.run()

