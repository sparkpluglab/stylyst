'''
Created on Aug 21, 2013

@author: ranjeetbhatia
'''

from pymongo import Connection
import sys
import time
import requests
from bson.binary import Binary
import gridfs
import random


connection = Connection()
styledb = connection.stylyst
stylefs=gridfs.GridFS(styledb)
curated_sets=styledb.curated_sets
set_url = 'https://www.polyvore.com/cgi/set.load?.in=json&.out=json&request={"id":"%s"}'
item_url = 'https://www.polyvore.com/cgi/thing?.in=json&.out=json&request={"id":"%s"}'

headers={'User-agent':'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_8) AppleWebKit/537 (KHTML, like Gecko) Chrome/28 Safari/537'}

valid_keys =["description","category_id","thing_id","title","imgurl"]
image_url = "http://polyvoreimg.com/cgi/img-thing/size/l/tid/%s.jpg"


def expand_curated_set(curated_set):
    time.sleep(random.randint(1,5))
    r = requests.get( set_url % curated_set["id"],headers=headers)
    curated_set["user_name"] = r.json()["collection"]["user_name"]
    #get all things and the category id
    curated_set["items"] = []
    for item in r.json()["collection"]["items"]:
        if "category_id" in item and "thing_id" in item and item["category_id"]:
            item = {k:v for (k, v) in item.iteritems() if k in valid_keys}
            item["site_imgurl"] = image_url % item["thing_id"]
            # wait for few seconds before making image request
            time.sleep(random.randint(1,5))
            img_binary=Binary(requests.get(item["site_imgurl"]).content)
            item["imgid"]=stylefs.put(img_binary)
            curated_set["items"].append(item)
    return curated_set


#loop to process all curated_sets
curated_set = True
while curated_set:
    try:
        time.sleep(random.randint(1,5))
        curated_set = curated_sets.find_one({"complete":{"$exists":False}})
        if curated_set:
            print "procesing set:"+curated_set["id"]
            curated_set = expand_curated_set(curated_set)
            curated_set["complete"]=1
            print curated_sets.update({"id":curated_set["id"]},curated_set,safe=True)
    except Exception, info:
        print sys.exc_info(), info
        print 'Error on line {}'.format(sys.exc_info()[-1].tb_lineno)
