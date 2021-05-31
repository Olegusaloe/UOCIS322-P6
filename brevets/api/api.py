# Streaming Service

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

SERIES = {
    0: {
        'name': 'Breaking Bad',
        'from': 2008,
        'to': 2013,
        'ongoing': False,
        'creators': ['Vince Gilligan'],
        'cast': {
            'Bryan Cranston': ['Walter White'],
            'Aaron Paul': ['Jesse Pinkman'],
            'Anna Gunn': ['Skyler White'],
            'Bob Odenkirk': ['Saul Goodman'],
            'Jonathan Banks': ['Mike Ehrmantraut'],
            'Giancarlo Esposito': ['Gus Fring']
        },
        'imdb_rating': 9.5,
        'genre': ['crime', 'drama']
    },
    1: {
        'name': 'Better Call Saul',
        'from': 2015,
        'to': 2021,
        'ongoing': False,
        'creators': ['Vince Gilligan', 'Peter Gould'],
        'cast': {
            'Bob Odenkirk': [
                'Saul Goodman',
                'James McGill'
            ],
            'Jonathan Banks': ['Mike Ehrmantraut'],
            'Giancarlo Esposito': ['Gus Fring']
        },
        'imdb_rating': 8.7,
        'genre': ['crime', 'drama']
    },
    2: {
        'name': 'Curb Your Enthusiasm',
        'from': 2000,
        'to': None,
        'ongoing': True,
        'creators': ['Larry David'],
        'cast': {'Larry David': ['Larry David'],
                 'Jeff Garlin': ['Jeff Greene'],
                 'Cheryl Hines': ['Cheryl David'],
                 'Susie Essman': ['Susie Greene']
                 },
        'imdb_rating': 8.7,
        'genre': ['comedy']
    }
}


class TVShow(Resource):
    def get(self, uid):
        return SERIES[uid]


class TVShows(Resource):
    def get(self):
        return SERIES


# Create routes
# Another way, without decorators
api.add_resource(TVShow, '/TVShow/<int:uid>')
api.add_resource(TVShows, '/TVShows')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True)
