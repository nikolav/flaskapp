
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

def with_doc_timestamps(doc, *, CREATED_AT = 'created_at', UPDATED_AT = 'updated_at'):
  tt = utcnow()
  doc.setdefault(CREATED_AT, tt)
  doc[UPDATED_AT] = tt
  return doc

def to_utc(dt: datetime):
  return dt.replace(tzinfo = timezone.utc) if dt.tzinfo is None else dt.astimezone(timezone.utc)

