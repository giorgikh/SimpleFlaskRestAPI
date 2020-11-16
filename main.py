from flask import Flask, request, abort
from flask_restful import Api, Resource, reqparse, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
api = Api(app)
# config sqlite database location
app.config["SQLALCHEMY_DATABASE_URI"] = 'sqlite:///database.db'
db = SQLAlchemy(app)


class VideoModel(db.Model):
    """ create database structure, ID, Name, Like, Views. Name is required and not nullable """
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(150), nullable=False)
    likes = db.Column(db.Integer, nullable=False)
    views = db.Column(db.Integer, nullable=False)

    def __repr__(self):
        return f"Video Name - {name}, Video Likes - {likes}, Video views - {views}"


# for select query
resource_field = {
    "id": fields.Integer,
    "name": fields.String,
    "likes": fields.Integer,
    "views": fields.Integer
}
# rebuild database
# db.create_all()

# for insert request
videos_put_args = reqparse.RequestParser()
videos_put_args.add_argument(
    "name", type=str, help="you should put name before request", required=True)
videos_put_args.add_argument(
    "likes", type=str, help="you should put likes before request", required=True)
videos_put_args.add_argument(
    "views", type=str, help="you should put views before request", required=True)

# for update/path request
videos_update_args = reqparse.RequestParser()
videos_update_args.add_argument(
    "name", type=str, help="you should put name before request")
videos_update_args.add_argument(
    "likes", type=str, help="you should put likes before request")
videos_update_args.add_argument(
    "views", type=str, help="you should put views before request")

# old version
# def video_dont_exist(video_id):
#     if video_id not in videos_dict:
#         abort(404, "Video id is not valid")

# old version
# def video_exist(video_id):
#     if video_id in videos_dict:
#         abort(409, "Video already exist")

# main class for request handler


class videos(Resource):
    """ Get, Post, Delete, Path Request handler  """
    @marshal_with(resource_field)
    def get(self, video_id):
        # video_dont_exist(video_id)
        # select query  by video ID
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(404, "Couldn't find Video with thi ID")
        return result

    @marshal_with(resource_field)
    def put(self, video_id):
        # print(request.form)
        args = videos_put_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if result:
            abort(409, "this Video Already exist in Database")
        video = VideoModel(
            id=video_id, name=args["name"], likes=args["likes"], views=args["views"])
        # print(type(args))
        # videos_dict[video_id] = args
        db.session.add(video)
        db.session.commit()
        return video, 201

    @marshal_with(resource_field)
    def patch(self, video_id):
        args = videos_update_args.parse_args()
        result = VideoModel.query.filter_by(id=video_id).first()
        if not result:
            abort(409, "Couldn't find Video with thi ID in Database")
        if args["name"]:
            result.name = args["name"]
        if args["views"]:
            result.views = args["views"]
        if args["likes"]:
            result.likes = args["likes"]
        db.session.commit()
        return result

    def delete(self, video_id):
        # video_exist(video_id)
        # del videos_dict[video_id]
        result = VideoModel.query.filter_by(id=video_id).delete()
        db.session.commit()
        return f"Deleted Video with ID: {video_id}", 204


api.add_resource(videos, "/video/<int:video_id>")

if __name__ == "__main__":
    app.run(debug=True)
