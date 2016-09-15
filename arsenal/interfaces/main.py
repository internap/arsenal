from arsenal.adapters.memory_datastore import MemoryDatastore
from arsenal.core.manager import Manager
from arsenal.interfaces.api import Api
from flask import Flask


def wire_stuff(app):
    datastore = MemoryDatastore()
    # TODO(lindycoder): put a real thing in there if you got the TEST for it!
    manager = Manager(datastore, None)
    Api(app, manager)

app = Flask(__name__)
app.config['PROPAGATE_EXCEPTIONS'] = True

wire_stuff(app)
