@app.route('/api/test/verify',methods=['POST'])
def verify():
    data = request.get_json()
    uuid = data.get('uuid')
    c = data.get('result')
    print(c)

    if uuid is None or c is None:
        return jsonify({'error': 'UUID or result is missing in the request.'}), 400

    # Read the JSON file and find the entry with the uuid
    with open('data.json', 'r') as f:
        json_data = json.load(f)
        if uuid in json_data:
            print(json_data[uuid]['result'])
            if json_data[uuid]['result'] == c:
                json_data[uuid]['status'] = 'correct'
                # Update the JSON file with the modified data
                with open('data.json', 'w') as f:
                    json.dump(json_data, f, indent=4)
                return jsonify({'status': 'correct'})
            else:
                return jsonify({'status': 'incorrect'})
        else:
            return jsonify({'error': 'UUID not found in data.json'}), 404
        
@app.route('/api/test',methods=['GET'])
def test():
    a = random.randint(0, 100)
    b = random.randint(0, 100)
    uid = str(uuid.uuid4())
    c = a+b
    #jsonify the data
    jsondata = {'a':a,'b':b,'result':c,'status':'pending'}
    # load data.json
    with open('data.json', 'r') as f:
        data = f.read()
        data = json.loads(data)
        #append the new entry to the file
        data[uid] = jsondata
    #write the new data to the file
    with open('data.json', 'w') as f:
        f.write(json.dumps(data))