
from bson import ObjectId

from flask_app        import mongo
from src.utils.dates  import with_doc_timestamps
from src.utils.discts import Dicts

from src.schemas.serialization import SchemaMongoDocData


class Collections:
  _err, client = mongo


  @staticmethod
  def ls(collection_name, q = {}):
    return Collections.client.db[collection_name].find(q)
    
    
  @staticmethod
  def dump(dd, *args, **kwargs):
    # serialize( <doc | doc[]>dd )
    return SchemaMongoDocData(*args, **kwargs).dump(dd)
  
  
  @staticmethod
  def toID(id):
    return ObjectId(id) if (isinstance(id, str) and ObjectId.is_valid(id)) else id
  

  @staticmethod
  def commit(collection_name, *, patches):
    # patches: { merge?: boolean; data: {'id'?: ID, 'data': dict} }[]
    changes = 0
    
    if patches:
      col = Collections.client.db[collection_name]

      for patch in patches:
        dd     = dict(patch.get('data') or {})
        raw_id = dd.pop('id', None)
        
        # create when no id provided
        if not raw_id:
          col.insert_one(with_doc_timestamps(dd))
          changes += 1
          continue

        oid   = Collections.toID(raw_id)
        q     = { '_id': oid }
        merge = patch.get('merge', True)
        
        res = col.update_one(q, 
            { 
              # deep merge | shallow merge
              '$set': Dicts.dotted(dd) if merge else dd, 
              '$currentDate': { 'updated_at': True } 
            }, 
            upsert = False,
          )
        
        # if query:q didn't match, insert
        if 0 == res.matched_count:
          col.insert_one(with_doc_timestamps(dd))
        
        changes += 1

    return changes
  
  
  @staticmethod
  def rm(collection_name, *ids):
    countd = 0
    if ids:
      col    = Collections.client.db[collection_name]
      res    = col.delete_many({ '_id': { '$in': [Collections.toID(id) for id in ids] } })
      countd = res.deleted_count
    
    return countd
  
  
  @staticmethod
  def count_all(collection_name):
    return Collections.count(collection_name, {})


  @staticmethod
  def count(collection_name, q, **kwargs):
    return Collections.client.db[collection_name].count_documents(q, **kwargs)

