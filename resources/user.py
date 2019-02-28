from flask_restful import Resource,reqparse
import sqlite3

from models.user_model import UserModel 

class UserRegister(Resource):

    parser = reqparse.RequestParser()
    parser.add_argument('username',type = str,required = True,help = 'username required')
    parser.add_argument('password',type = str,required = True,help = 'password required')
    
    def post(self):
        data = UserRegister.parser.parse_args()

        if not UserModel.find_by_username(data['username']):
            # connection = sqlite3.connect('data.db')
            # cursor = connection.cursor()
            # query = "INSERT INTO users VALUES(NULL,?,?)"

            # cursor.execute(query,(data['username'],data['password']))

            # connection.commit()
            # connection.close()
            # return {'message':'user created successfully'}
            user = UserModel(data['username'],data['password'])
            user.save_to_db()
        return {'message':'user with that username  already exists'}, 400

