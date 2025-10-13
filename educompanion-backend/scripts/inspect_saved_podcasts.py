from config.database import db_instance
from bson import ObjectId
import os, json

if not db_instance.connect():
    print('Failed to connect to MongoDB')
    exit(1)

db = db_instance.get_db()
col = db.saved_podcasts

print('Listing saved_podcasts (limit 200):')
for doc in col.find().limit(200):
    out = {
        '_id': str(doc.get('_id')),
        'title': doc.get('title'),
        'user_id': str(doc.get('user_id')) if doc.get('user_id') is not None else None,
        'path': doc.get('path'),
        'share_token': doc.get('share_token') if 'share_token' in doc else None,
        'share_expires': str(doc.get('share_expires')) if 'share_expires' in doc else None,
    }
    exists = False
    if out['path']:
        exists = os.path.exists(out['path'])
    out['file_exists'] = exists
    print(json.dumps(out, ensure_ascii=False))

db_instance.close()
