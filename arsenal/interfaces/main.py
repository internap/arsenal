from arsenal.adapters.memory_datastore import MemoryDatastore
from arsenal.core.manager import Manager
from arsenal.interfaces.api import Api
from flask import Flask


def wire_stuff(app):
    datastore = MemoryDatastore()
    manager = Manager(datastore)
    Api(app, manager)

app = Flask(__name__)
wire_stuff(app)
