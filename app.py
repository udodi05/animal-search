# This is a comment to test out fork
from flask import Flask, request, jsonify, render_template
import couchdb
import requests
from bs4 import BeautifulSoup
import random
import time

time.sleep(10)

app = Flask(__name__)

# CouchDB setup with admin credentials
couch = couchdb.Server('http://admin:admin@couchdb:5984/')
db_name = 'animal_info'
if db_name in couch:
    db = couch[db_name]
else:
    db = couch.create(db_name)

@app.route('/add_animal', methods=['POST'])
def add_animal():
    data = request.json
    animal_name = data.get('name')

    if not animal_name:
        return jsonify({'error': 'Animal name is required'}), 400

    # Check for existing entry and update if found
    existing_id = None
    for doc_id in db:
        doc = db[doc_id]
        if doc.get('name').lower() == animal_name.lower():
            existing_id = doc_id
            break

    # Search for animal information
    search_url = f'https://en.wikipedia.org/wiki/{animal_name}'
    response = requests.get(search_url)

    if response.status_code != 200:
        return jsonify({'error': 'Animal information not found'}), 404

    soup = BeautifulSoup(response.text, 'html.parser')

    # Validate if the search result corresponds to an animal
    if not soup.find('table', {'class': 'infobox'}):
        return jsonify({'error': 'The name provided does not correspond to a valid animal'}), 400

    paragraphs = soup.find_all('p')
    animal_info = ' '.join([para.text for para in paragraphs[:3]])

    # Search for animal image
    image_url = None
    infobox = soup.find('table', {'class': 'infobox'})
    if infobox:
        img_tag = infobox.find('img')
        if img_tag and img_tag['src']:
            image_url = f"https:{img_tag['src']}"

    # Improved search for animal breeds/variants
    breeds = []
    seen_breeds = set()
    breed_tables = soup.find_all('table', {'class': 'wikitable'})
    for breed_table in breed_tables:
        rows = breed_table.find_all('tr')[1:]  # Skip header row
        for row in rows:
            cols = row.find_all('td')
            if len(cols) > 0:
                breed_name = cols[0].text.strip()
                if breed_name and breed_name.lower() not in seen_breeds:
                    # Search all columns for an image
                    breed_image = None
                    for col in cols:
                        img_tag = col.find('img')
                        if img_tag and img_tag.get('src'):
                            breed_image = f"https:{img_tag['src']}"
                            break
                    breeds.append({'name': breed_name, 'image': breed_image})
                    seen_breeds.add(breed_name.lower())
                if len(breeds) == 5:
                    break
        if len(breeds) == 5:
            break

    # Store in CouchDB (update if exists, else create new)
    doc = {
        'name': animal_name,
        'info': animal_info,
        'image': image_url,
        'breeds': breeds
    }
    if existing_id:
        doc['_id'] = existing_id
        doc['_rev'] = db[existing_id]['_rev']
        db.save(doc)
        return jsonify({'message': 'Animal information updated successfully', 'data': doc}), 200
    else:
        db.save(doc)
        return jsonify({'message': 'Animal information added successfully', 'data': doc}), 201

@app.route('/get_animal/<name>', methods=['GET'])
def get_animal(name):
    for doc_id in db:
        doc = db[doc_id]
        if doc.get('name').lower() == name.lower():
            return jsonify({'data': doc}), 200

    return jsonify({'error': 'Animal not found'}), 404

@app.route('/all_animals', methods=['GET'])
def all_animals():
    animals = []
    for doc_id in db:
        doc = db[doc_id]
        animals.append({k: v for k, v in doc.items() if not k.startswith('_')})
    return jsonify({'animals': animals}), 200

@app.route('/random_animal', methods=['GET'])
def random_animal():
    # List of common animals to pick from
    animal_list = [
        'dog', 'cat', 'horse', 'elephant', 'lion', 'tiger', 'bear', 'rabbit', 'giraffe', 'zebra',
        'kangaroo', 'panda', 'wolf', 'fox', 'leopard', 'cheetah', 'goat', 'sheep', 'cow', 'pig',
        'chicken', 'duck', 'goose', 'turkey', 'ostrich', 'camel', 'donkey', 'buffalo', 'deer', 'moose',
        'hippopotamus', 'rhinoceros', 'bat', 'otter', 'beaver', 'squirrel', 'hedgehog', 'porcupine', 'badger', 'skunk'
    ]
    animal_name = random.choice(animal_list)
    # Reuse the add_animal logic
    with app.test_request_context(json={'name': animal_name}):
        resp = add_animal()
        # If add_animal returns a tuple, extract the response and status
        if isinstance(resp, tuple):
            data, status = resp
        else:
            data = resp
            status = 200
        return data, status

# Route for the web interface
@app.route('/')
def home():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
