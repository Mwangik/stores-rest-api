# import sqlite3
from flask_restful import Resource,reqparse
from flask_jwt import jwt_required
from models.item_model import ItemModel



class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',type = float,required= True,help = "item must have a price")
    parser.add_argument('store_id',type = int,required= True,help = "every item must have a store")
    # parser = reqparse.RequestParser()
    # data = parser.parse_args()

    
    @jwt_required()
    def get(self, name):
        # for item in items:  #lamda function--> item = next(filter(lambda x:x['name] == name, items))
        #     if item['name'] == name:
        #         return item
        # return {'message':f'item with name {name} not found'}, 404
        item = ItemModel.find_by_name(name)
        if item:
            return item.json()
        else:
            return {'message':f'item with name {name} not found'}, 404
        

    def post(self, name): #here we need the json payload
       
        # for item in items:
        #     if item['name'] == name:
        #         return {'message':'item already exists'}, 400
        if ItemModel.find_by_name(name):
            return {'message':f'item with name {name} already exists'}, 400

        data = Item.parser.parse_args()
            
        item = ItemModel(name,data['price'],data['store_id'])
        # items.append(item)
        try:
            item.save_to_db()
        except:
            return {'message':'error occured inserting item to db'},500
        return item.json(), 201

    def delete(self,name):
        
        # global items
        # items = list(filter(lambda x: x['name'] != name, items))
        # return {'message':'item deleted'}
        # for item in items:
        #     if item['name'] == name:
        #         items.remove(item)
        # return {'message':'item deleted'}
        # query = "DELETE FROM items WHERE name = ?"
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()
        # cursor.execute(query,(name,))

        # connection.commit()#make sure to commit even when you delete
        # connection.close()
        # return {'message':f'{name} deleted'}

        item = ItemModel.find_by_name(name)
        if item:
            item.delete_from_db()
        return {'message':'item deleted'}

    def put(self,name):
        data = Item.parser.parse_args()
    #     item = next(filter(lambda x: x['name'] == name, items), None)
    #     if item is None:
    #         item = {'name':name,'price':data['price']}
    #         items.append(item)
    #     else:
    #         item.update(data)
    #     return item, 201
        item = ItemModel.find_by_name(name)
        # updated_item = ItemModel(name, data['price'])
        if item:
            item.price = data['price']
        else: #create item
            item = ItemModel(name,data['price'],data['store_id'])
        item.save_to_db()
        return item.json()



        


class ItemList(Resource):
    def get(self):
        # return {'items':items}
        # query = "SELECT * FROM items"
        # items = []
        # connection = sqlite3.connect('data.db')
        # cursor = connection.cursor()

        # result = cursor.execute(query)
        # for row in result:
        #     items.append({'name':row[0],'price':row[1]})
        
        # connection.commit()
        # connection.close()
        # return {'items':items}
        return {'items': [item.json() for item in ItemModel.query.all()]}
        #return {'items':list(map(lambda x: x.json(), ItemModel.query.all()))}