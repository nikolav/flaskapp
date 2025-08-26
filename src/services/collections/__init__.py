
from functools import reduce
from bson import json_util
from bson import ObjectId

from flask_app import mongo
from src.utils import Utils


class Collections:
  _err, client = mongo

  @staticmethod
  def ls(collection_name, q):
    coll = Collections.client.db[collection_name]
    return coll.find(q)

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
  def lsa(collection_name):
    return Collections.client.db[collection_name].find({}) if Collections.exists(collection_name) else []
  
  @staticmethod
  def toID(id):
    return ObjectId(id) if (isinstance(id, str) and ObjectId.is_valid(id)) else id
  
  @staticmethod
  def id_exists(collection_name, id):
    col = Collections.client.db[collection_name]
    return None != col.find_one({ '_id': Collections.toID(id) }, { '_id': 1 })
  
  @staticmethod
  def commit(collection_name, *, patches):
    # patches: { merge?: boolean; data: dict }[]
    changes = 0
    
    if patches:
      col = Collections.client.db[collection_name]
      for patch in patches:
        if not (('id' in patch['data']) and Collections.id_exists(collection_name, patch['data']['id'])):
          # create
          if 'id' in patch['data']:
            del patch['data']['id']
          col.insert_one(patch['data'])

        else:
          # update
          oid = Collections.toID(patch['data'].pop('id', None))
          
          if False == patch.get('merge', None):
            # replace
            col.find_one_and_replace({ '_id': oid }, patch['data'])
            
          else:
            # patch
            col.find_one_and_update({ '_id': oid }, { '$set': patch['data'] })

        changes += 1

    return changes
  
  @staticmethod
  def rm(collection_name, *, ids):
    col = Collections.client.db[collection_name]
    res = col.delete_many({ '_id': { '$in': [Collections.toID(id) for id in ids] } })
    return res.deleted_count
  
  @staticmethod
  def count_all(collection_name):
    col = Collections.client.db[collection_name]
    return col.estimated_document_count()

  @staticmethod
  def count(collection_name, q, **kwargs):
    coll = Collections.client.db[collection_name]
    return coll.count_documents(q, **kwargs)



