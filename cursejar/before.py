__author__ = 'shaked'

import sqlite3
from cursejar.settings import local
conn = sqlite3.connect(local.DATABASES.get('default').get('NAME'))

c = conn.cursor()

# Update
c.execute('''UPDATE django_site SET DOMAIN = '127.0.0.1:8000', name = 'Cursejar' WHERE id=1;''')

# Insert a row of data
c.execute('INSERT INTO socialaccount_socialapp (provider, name, secret, client_id, `key`)\
          VALUES ("facebook", "Facebook", "2d92754c7f41c59b24cb5dcae308677e", "533600183421965", "");')

c.execute("INSERT INTO socialaccount_socialapp_sites (socialapp_id, site_id) VALUES (1,1);")

# Save (commit) the changes
conn.commit()

# We can also close the connection if we are done with it.
# Just be sure any changes have been committed or they will be lost.
conn.close()
