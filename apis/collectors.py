from flask import jsonify, request
from flask_restful import Resource, Api, reqparse

# 업종분봉조회요청
class OPT20005(Resource):
    def __init__(self, feeder):
        self.feeder = feeder

    def get(self):
        return self.run_qt()

    def post(self):
        return self.run_qt()

    def run_qt(self):
        json_data = request.get_json(force=True)
        params = {"업종코드": json_data['code'],
                  "틱범위": json_data['tic']}
        data = self.feeder.request(trCode="opt20005", **params)

        return jsonify(data)

# 업종일봉조회요청
class OPT20006(Resource):
    def __init__(self, feeder):
        self.feeder = feeder

    def get(self):
        return self.run_qt()

    def post(self):
        return self.run_qt()

    def run_qt(self):
        json_data = request.get_json(force=True)
        params = {"업종코드": json_data['code'],
                  "기준일자": json_data['end_date']}
        data = self.feeder.request(trCode="opt20006", **params)
        print(data)

        return jsonify(data)

# 업종주봉조회요청
class OPT20007(Resource):
    def __init__(self, feeder):
        self.feeder = feeder

    def get(self):
        return self.run_qt()

    def post(self):
        return self.run_qt()

    def run_qt(self):
        json_data = request.get_json(force=True)
        params = {"업종코드": json_data['code'],
                  "기준일자": json_data['end_date']}
        data = self.feeder.request(trCode="opt20007", **params)
        print(data)

        return jsonify(data)

# 업종월봉조회요청
class OPT20008(Resource):
    def __init__(self, feeder):
        self.feeder = feeder

    def get(self):
        return self.run_qt()

    def post(self):
        return self.run_qt()

    def run_qt(self):
        json_data = request.get_json(force=True)
        params = {"업종코드": json_data['code'],
                  "기준일자": json_data['end_date']}
        data = self.feeder.request(trCode="opt20008", **params)
        print(data)

        return jsonify(data)