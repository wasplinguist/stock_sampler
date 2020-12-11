import sys
import threading
from flask import Flask
from flask_restful import Resource, Api, reqparse
from kiwoom_api import Kiwoom, DataFeeder
from apis.collectors import *

from PyQt5 import QtWidgets


app = Flask(__name__)
api = Api(app)
parser = reqparse.RequestParser()
qt_app = None
feeder = None


def main():
    global qt_app, feeder
    qt_app = QtWidgets.QApplication(sys.argv)
    kiwoom = Kiwoom()
    kiwoom.commConnect()
    feeder = DataFeeder(kiwoom)

    api.add_resource(OPT20005, "/opt20005", resource_class_kwargs={"feeder": feeder, "kiwoom": kiwoom})
    api.add_resource(OPT20006, "/opt20006", resource_class_kwargs={"feeder": feeder, "kiwoom": kiwoom})
    api.add_resource(OPT20007, "/opt20007", resource_class_kwargs={"feeder": feeder, "kiwoom": kiwoom})
    api.add_resource(OPT20008, "/opt20008", resource_class_kwargs={"feeder": feeder, "kiwoom": kiwoom})

    threading.Thread(
        target=app.run,
        kwargs=dict(debug=False, use_reloader=False),
        daemon=True,
    ).start()

    return qt_app.exec_()


if __name__ == "__main__":
    sys.exit(main())