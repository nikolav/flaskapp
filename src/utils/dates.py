
from datetime import datetime
from datetime import timezone
# from typing   import Optional
# from zoneinfo import ZoneInfo


DATE_FORMATS = {
  # REST/JSON
  'ISO-8601': '%Y-%m-%dT%H:%M:%SZ',
  # headers/cookies
  'RFC-1123': '%a, %d %b %Y %H:%M:%S GMT',
}

def utcnow():
  return datetime.now(timezone.utc)

def with_doc_timestamps(doc, *, 
    field_created_at = 'created_at', 
    field_updated_at = 'updated_at'):
  tt = utcnow()
  doc.setdefault(field_created_at, tt)
  doc[field_updated_at] = tt
  return doc

def to_utc(dt: datetime):
  return dt.replace(tzinfo = timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

