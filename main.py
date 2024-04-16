from flask import Flask, jsonify, request,make_response
import random
import uuid
import json



app = Flask(__name__)

#creates a endpoint that is used by clients to send maps
@app.route('/sendmap',methods=['POST'])
def map():
    '''The data send to this endpoint is organized as follows:
    {
        "uuid": "uuid",
        "roomcode": "roomcode",
        "Money": "money",
        "MapData": "mapdata"
        "MapCost": "mapcost"
    }
    '''
    #get the data from the request
    print(request.get_data())
    print(request)
    data = request.get_json()
    uuid = data["User"].get('UID')
    roomcode = data["User"].get('RoomCode')
    money = data["User"].get('Money')
    mapdata = data.get('MapData')
    mapcost = data.get('MapCost')
    maplist = []
    print(uuid)
    print(roomcode)
    print(money)
    print(mapdata)
    print(mapcost)
    print(type(roomcode))

    print("data inbound \n")
    print(data)
    print(type(data))


    #check if the data is missing
    if uuid is None or roomcode is None or money is None or mapdata is None or mapcost is None:
        return jsonify({'error': 'UUID, roomcode, money, mapdata or mapcost is missing in the request.'}), 400
    #check if the person has enough money
    if money < mapcost:
        return jsonify({'error': 'Not enough money'}), 400
    # Add the map to the map.json file
    with open('maps.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        data[roomcode]["EditedScene"].append(mapdata)
        
        #going to make a really shitty queue system
        #loop = True
        #i=0
        #print(data[roomcode]['maps'][f'{i}'])
        '''while loop:
            if f'{i}' in data[roomcode]['maps']:
                i = i+1
            else:
                data[roomcode]['maps'][i] = mapdata
                loop = False'''
        with open('maps.json', 'w') as ff:
            ff.write(json.dumps(data))
        with open('data.json', 'r') as fff:
            data = fff.read()
            data = json.loads(data)
            data[uuid]['money'] = data[uuid]['money'] - mapcost
            with open('data.json', 'w') as ffff:
                ffff.write(json.dumps(data))
        return jsonify({'status': 'Map added to room'})
    
@app.route('/getmap/<roomcode>',methods=['GET'])
def getmap(roomcode):
    print("Start Map Get\n\n\n")  
    with open('maps.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        
        print(data[roomcode])
        print("\n\n\n")
        if roomcode in data and data[roomcode]['EditedScene']:
            with open('maps.json', 'w') as ff:
                mapstoreturn = str(data[roomcode]['EditedScene'][0])
                temp = make_response(mapstoreturn)
                print(mapstoreturn)
                print("\n\n\n")
                #clear the queue for the room code
                data[roomcode]['EditedScene'].pop(0)
                ff.write(json.dumps(data)) 
                print("penisliccker6040\n\n\n")   
                print(mapstoreturn)     
                return temp     
        else:
            return jsonify({'error': 'Room code not found'}), 404


#creates an endpoint that sends a uuid
@app.route('/getuser',methods=['GET'])
def getuuid():
    uid = str(uuid.uuid4())
    money = 100
    roomcode = "null"
    pendingfunds = 0
    # add the user to the data.json file
    with open('data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        data[uid] = {'money':money,'roomcode':roomcode,'pendingfunds':pendingfunds}
        with open('data.json', 'w') as ff:
            ff.write(json.dumps(data))
    
    #return all the data
    return jsonify({'UID':uid,'Money':money,'RoomCode':roomcode})

@app.route('/pendingmoney/<user>',methods=['GET'])
def getpendingmoney(user):
    with open('data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        if user in data:
            with open('data.json', 'w') as ff:
                pendingfunds = data[user]['money']
                ff. write(json.dumps(data))
                return jsonify({'Balance':pendingfunds})
        else:
            return jsonify({'error': 'UUID not found in data.json'}), 404
        
@app.route('/addmoney/<user>/<amount>',methods=['GET'])
def addmoney(user, amount):
    with open('data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        if user in data:
            with open('data.json', 'w') as ff:
                pendingfunds = data[user]['money']
                data[user]["money"] = pendingfunds + int(amount)
                ff.write(json.dumps(data)) 
                return jsonify({'Balance':pendingfunds})


@app.route('/createroom/<code>',methods=['GET'])
def createroom(code):
    with open('rooms.json', 'r') as f:
        #check if the room code is already in use
        data = f.read()
        data = json.loads(data)
        if code in data:
            return jsonify({'error': 'Room code already in use'}), 400
        else:
            with open('rooms.json', 'w') as ff:
                data[code] = {'users':[], 'EditedScene':{}}
                ff.write(json.dumps(data))
            with open('maps.json', 'r') as fff:
                data = fff.read()
                data = json.loads(data)
                data[code] = {'EditedScene':[]}
                with open('maps.json', 'w') as ffff:
                    ffff.write(json.dumps(data))
                return jsonify({'status': 'Room created'})

@app.route('/joinroom/<code>/<user>',methods=['GET'])
def joinroom(code, user):
    with open('rooms.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        if code in data:
            data[code]['users'].append(user)
            with open('rooms.json', 'w') as ff:
                ff.write(json.dumps(data))
            with open('data.json', 'r') as fff:
                data = fff.read()
                data = json.loads(data)
                data[user]['roomcode'] = code
                with open('data.json', 'w') as ffff:
                    ffff.write(json.dumps(data))
            return jsonify({'status': 'User added to room'})
        else:
            return jsonify({'error': 'Room code not found'}), 404



if __name__ == '__main__':
    app.run(debug=True)
