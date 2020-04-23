#!/usr/bin/env python3

# Delete (3) MongoDB databases, (3) Kafka topics,
# create sample data by hitting Zuul API Gateway endpoints,
# and return MongoDB documents as verification.

# usage: python3 ./refresh.py

from pprint import pprint
from pymongo import MongoClient
import requests
import time

client = MongoClient('mongodb://localhost:27017/')


def main():
    delete_databases()
    delete_topics()

    create_sample_data()

    get_mongo_doc('accounts', 'customer.accounts')
    get_mongo_doc('orders', 'customer.orders')
    get_mongo_doc('fulfillment', 'fulfillment.requests')


def delete_databases():
    dbs = ['accounts', 'orders', 'fulfillment']
    for db in dbs:
        client.drop_database(db)
        print('MongoDB dropped: ' + db)

    dbs = client.database_names()
    print('Reamining databases:')
    print(dbs)
    print('\n')


def delete_topics():
    # call Kafka Manager API
    topics = ['accounts.customer.change',
              'orders.order.fulfill',
              'fulfillment.order.change']
    for topic in topics:
        kafka_manager_url = 'http://localhost:9000/clusters/dev/topics/delete?t=' + topic
        r = requests.post(kafka_manager_url, data={'topic': topic})
        time.sleep(3)
        print('Kafka topic deleted: ' + topic)
    print('\n')


def create_sample_data():
    sample_urls = [
        'http://localhost:8080/accounts/customers/sample',
        'http://localhost:8080/orders/customers/sample/orders',
        'http://localhost:8080/orders/customers/sample/fulfill',
        'http://localhost:8080/fulfillment/fulfillments/sample/process',
        'http://localhost:8080/fulfillment/fulfillments/sample/ship',
        'http://localhost:8080/fulfillment/fulfillments/sample/in-transit',
        'http://localhost:8080/fulfillment/fulfillments/sample/receive']

    for sample_url in sample_urls:
        r = requests.get(sample_url)
        print(r.text)
        time.sleep(5)
    print('\n')


def get_mongo_doc(db_name, collection_name):
    db = client[db_name]
    collection = db[collection_name]
    pprint(collection.find_one())
    print('\n')


if __name__ == "__main__":
    main()
