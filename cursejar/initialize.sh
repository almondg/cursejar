!#/bin/bash

echo "Removing old DB"
rm cursejar/settings/core.db
echo "Done."

echo "Syncing DB..."
python manage.py syncdb
echo "Done."

echo "Migrating changes..."
python manage.py migrate
echo "Done."

echo "Insert site data to DB..."
python before.py
echo "Done."

