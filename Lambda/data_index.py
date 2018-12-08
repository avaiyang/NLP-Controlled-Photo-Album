from elasticsearch import Elasticsearch, RequestsHttpConnection
from requests_aws4auth import AWS4Auth
import boto3


host = 'xxxxxxxxx' # For example, my-test-domain.us-east-1.es.amazonaws.com
region = 'us-east-1' # e.g. us-west-1
ACCESS_KEY = 'xxxxxxxxx'
SECRET_KEY = 'xxxxxxxxx'

def authenticate_user(service):
    credentials = boto3.Session().get_credentials()
    awsauth = AWS4Auth(ACCESS_KEY, SECRET_KEY, region, service)
    return awsauth

def connect_to_elastic_search():
    service = 'es'
    awsauth = authenticate_user(service)
    es = Elasticsearch(
            hosts = [{'host': host, 'port': 443}],
            http_auth = awsauth,
            use_ssl = True,
            verify_certs = True,
            connection_class = RequestsHttpConnection
        )
    
    return es