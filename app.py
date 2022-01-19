from multiprocessing.sharedctypes import Value
from urllib import response
from flask import Flask, request, Response, render_template
from flask_restx import Resource, Api, fields
from flask import abort, jsonify
import requests
app = Flask(__name__)
api = Api(app)


ns_movie = api.namespace('ns_movie', description='Movie APIs')

movie_data = api.model(
    'Movie Data',
    {
      "title": fields.String(description="movie Title", required=True),
      "director": fields.String(description="movie Director", required=True),
      "genre": fields.String(description="movie genre", required=True),
      "rating": fields.Integer(description="movie Rating", required=True),
      "runtime": fields.Integer(description="movie Runtime", required=True)
    }
)

movie_info={}
number_of_movies=0

@ns_movie.route('/movie')
class movies(Resource):
    def get(self):
        return {
            'number_of_movies':number_of_movies,
            'movie_info':movie_info
        }

@ns_movie.route('/movie/<int:movie_id>')
class movies_genre_movie(Resource):
    def get(self, movie_id):
        if not movie_id in movie_info.keys():
            abort(404, description=f"Title {movie_id} doesn't exists")

        return{
            'movie_id':movie_id,
            'data':movie_info[movie_id]
        }

    @api.expect(movie_data)
    def post(self,movie_id):
        if movie_id in movie_info.keys():
            abort(409,description=f"movie_id {movie_id} already exists")

        params = request.get_json()
        movie_info[movie_id]=params
        global number_of_movies
        number_of_movies+=1

        return Response(status=200)
    def delete(self, movie_id):
        if not movie_id in movie_info.keys():
            abort(404, description=f"movie_id ID {movie_id} doesn't exists")

        del movie_info[movie_id]
        global number_of_movies
        number_of_movies -= 1

        return Response(status=200)

    @api.expect(movie_data)
    def put(self, movie_id):
        if not movie_id in movie_info.keys():
            abort(404, description=f"movie_id ID {movie_id} doesn't exists")

        params=request.get_json()
        movie_info[movie_id] = params

        return Response(status=200)

@app.route("/home")
def homepage():
    return render_template("index.html")

@app.route("/detail")
def detailpage():
    id=request.args.get('movie_id')
    res=requests.get('http://localhost:5000/ns_movie/movie/'+str(id))
    data=res.json()
    print(type(data))
    print(res.json())
    title=data['data']['title']
    director=data['data']['director']
    genre=data['data']['genre']
    rating=data['data']['rating']
    runtime=data['data']['runtime']
    movie_id=data['movie_id']
    image_file="assets/"+str(movie_id)+".jpg"
    return render_template("detail.html", title=title,director=director,genre=genre,rating=rating,runtime=runtime,movie_id=movie_id,image_file=image_file)

if __name__ == "__main__":
    app.run(debug=True, host='0.0.0.0', port=5000)