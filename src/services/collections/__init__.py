
from bson import json_util
from bson import ObjectId

from flask_app import mongo


class Collections:
  _err, client = mongo

  @staticmethod
  def dump_doc(doc):
    # whole doc to extended JSON dict
    d = json_util.loads(json_util.dumps(doc))
    oid = d.pop('_id', None)
    d['id'] = str(oid) if isinstance(oid, ObjectId) else oid['$oid'] if (isinstance(oid, dict) and ('$oid' in oid)) else oid
    return d
  
  @staticmethod
  def exists(collection_name):
    return collection_name in Collections.client.db.list_collection_names() if collection_name else False

  @staticmethod
  def by_name(collection_name):
    return Collections.client.db[collection_name].find({}) if Collections.exists(collection_name) else []


