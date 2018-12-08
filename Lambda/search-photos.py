import json
import boto3
import data_index

def lambda_handler(event, context):
    print(event)
    query = event['currentIntent']['slots']['searchque']
    print('query',query)
    
    keys = query.split(',')
    Res = []
    es = data_index.connect_to_elastic_search()
    out = []
    outS = ""
    outRes = []
    for i in range(len(keys)):
        print (keys[i])
        res = es.search(q=keys[i])
        Res.append(res)
        print("Got %d Hits:" % res['hits']['total'])
        print (res)
        for i in res['hits']['hits']:
            bucket = i['_source']['bucket']
            image = i['_source']['objectKey']
            a = "https://s3.amazonaws.com/" + bucket + "/" + image
            if a not in out:
                out.append(a)
                outS += a + ", "
                outRes.append({'title': image.split(".")[0],'attachmentLinkUrl': a,'imageUrl': a})
        print('File path: ', out)
    
    result = {
        "dialogAction":{
            "type":"Close",
            "fulfillmentState":"Fulfilled",
            "message":{
                "contentType":"PlainText",
                "content":outS
            },
            "responseCard": {
                'version': '0',
                'contentType': 'application/vnd.amazonaws.card.generic',
                'genericAttachments': outRes
            }
        }
    }
    return result