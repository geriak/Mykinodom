import os
import firebase_admin
from firebase_admin import credentials
from firebase_admin import db

# Fetch the service account key JSON file contents
cred = credentials.Certificate("../mydev-kino-andoid-firebase-adminsdk-sts0w-77e9f2eeff.json")
# Initialize the app with a service account, granting admin privileges
firebase_admin.initialize_app(cred, {
    'databaseURL': 'https://mydev-kino-andoid.firebaseio.com/'
})
try:
    firebase_admin.get_app()
except:
    firebase_admin.initialize_app(cred)


ref = db.reference('/global/providerList/')
print(ref.get())