from flask import Flask, request
from elasticsearch import Elasticsearch
import json
import logging
import os


app = Flask(__name__)

logger = logging.getLogger()
logger.setLevel(logging.DEBUG)

url = os.environ['URL']
es = Elasticsearch(url)
index_name = os.environ['INDEX_NAME']
all_cities = []
doc = {}

mapping = '''
{
  "mappings": {
    "properties": {
      "city_name": {
        "type": "keyword"
      },
      "population": {
        "type": "integer"
      }
    }
  }
}'''



index_exists = es.indices.exists(index = index_name)

if not index_exists:
  es.indices.create(index = index_name, body = mapping)

def add_city_population(city, population):
    doc['city_name'] = city
    doc['population'] = population
    try:
        es.index(index=index_name, doc_type="_doc", body=doc)
        logging.info(str(doc) + ' added in the data!')
    except Exception as e:
        logging.error(str(e))
    return doc


@app.route("/citydetails")
def get_all_cities_population():
    query = {
      "query": {
        "match_all": {}
      }
    }
    try:
        q_results = es.search(index=index_name, body=query)

        for i in range(len(q_results['hits']['hits'])):
            doc_data = q_results['hits']['hits'][i]['_source']
            all_cities.append(doc_data)
    except Exception as e:
        logging.error(e)

    return json.dumps({'cities': all_cities})



@app.route("/citymodify", methods=['POST'])
def update_city_population():
    json_input = request.json
    query = {
      "query" : {
        "bool" : {
          "must" : {
             "term" : {
                "city_name" :  json_input['city']
             }
          }
        }
      }
    }

    q_results = es.search(index=index_name, body=query)
    logging.info('existing city search' + str(q_results))

    if q_results['hits']['total']['value'] == 0:
        city_po = add_city_population(json_input['city'], json_input['population'])
        return json.dumps({'added data': city_po})
    else:
        for i in range(len(q_results['hits']['hits'])):
            doc_body = q_results['hits']['hits'][i]['_source']
            doc_id = q_results['hits']['hits'][i]['_id']
            doc_body['population'] =  json_input['population']
            try:
                updated_doc = es.update(index=index_name, id=doc_id, body={"doc": doc_body})
                logging.info("updated doc " + str(updated_doc))
                return json.dumps({'updated data': doc_body})
            except Exception as e:
                logging.info(str(e))

@app.route('/health')
def health_check():
    return json.dumps({'success': True}), 200, {'ContentType':'application/json'}

if __name__ == "__main__":
    app.run(debug=True)
