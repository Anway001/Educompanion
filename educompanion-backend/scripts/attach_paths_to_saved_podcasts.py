from config.database import db_instance
from bson import ObjectId
import os, json

# Determine backend root and generated dirs
script_dir = os.path.dirname(__file__)
backend_root = os.path.abspath(os.path.join(script_dir, '..'))
saved_dir = os.path.join(backend_root, 'generated', 'saved_podcasts')
generated_dir = os.path.join(backend_root, 'generated')

print('Backend root:', backend_root)
print('Saved dir:', saved_dir)
print('Generated dir:', generated_dir)

if not db_instance.connect():
    print('Failed to connect to MongoDB')
    exit(1)

db = db_instance.get_db()
col = db.saved_podcasts

updated = 0
for doc in col.find({}):
    if doc.get('path'):
        continue
    title = doc.get('title') or ''
    found = None
    # look for exact filename in saved_dir
    if title:
        candidate = os.path.join(saved_dir, title)
        if os.path.exists(candidate):
            found = candidate
    # if not found, look for any file in saved_dir that contains title
    if not found and os.path.isdir(saved_dir):
        for fname in os.listdir(saved_dir):
            if title and title in fname:
                candidate = os.path.join(saved_dir, fname)
                if os.path.exists(candidate):
                    found = candidate
                    break
    # fallback: search generated_dir recursively for a matching file
    if not found and os.path.isdir(generated_dir):
        for root, dirs, files in os.walk(generated_dir):
            for fname in files:
                if title and title in fname:
                    candidate = os.path.join(root, fname)
                    if os.path.exists(candidate):
                        found = candidate
                        break
            if found:
                break

    if found:
        try:
            col.update_one({'_id': doc['_id']}, {'$set': {'path': found}})
            updated += 1
            print('Updated', str(doc['_id']), '->', found)
        except Exception as e:
            print('Failed to update', str(doc['_id']), e)
    else:
        print('No file found for', str(doc.get('_id')), 'title=', title)

print('Done. Updated', updated, 'documents')

db_instance.close()
