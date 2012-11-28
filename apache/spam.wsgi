ALLDIRS = ['/var/www/wsgi/apps/virtenv/lib/python2.7/site-packages']

import sys 
import site
sys.stdout = sys.stderr

# Remember original sys.path.
#prev_sys_path = list(sys.path) 

# Add each new site-packages directory.
for directory in ALLDIRS:
  site.addsitedir(directory)
  
sys.path.append('/var/www/wsgi/apps/spam')
from pkg_resources import load_entry_point

# Reorder sys.path so new directories at the front.
#new_sys_path = [] 
#for item in list(sys.path): 
#    if item not in prev_sys_path: 
#        new_sys_path.append(item) 
#        sys.path.remove(item) 
#sys.path[:0] = new_sys_path

import os
os.environ['PYTHON_EGG_CACHE'] = '/var/www/wsgi/apps/spam/python-eggs'

from paste.deploy import loadapp
application = loadapp('config:/var/www/wsgi/apps/spam/development_local.ini')

# init the app by calling '/' to be sure that all threads register toscawidgets
# and their resources
import paste.fixture
app = paste.fixture.TestApp(application)
app.get("/")

