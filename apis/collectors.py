from flask import jsonify, request
from flask_restful import Resource, Api, reqparse

# 업종분봉조회요청
class OPT20005(Resource):
    def __init__(self, feeder, kiwoom):
        self.feeder = feeder
        self.kiwoom = kiwoom

    def get(self):
        return self.run_qt()

    def post(self):
        return self.run_qt()

    def run_qt(self):
        json_data = request.get_json(force=True)
        params = {"업종코드": json_data['code'],
                  "틱범위": json_data['tic']}
        data = []
        data.append(self.feeder.request(trCode="opt20005", **params))

        # while 다돌면 160일치 다 나오니, 입맛대로 변경해서 쓰셈.
        idx = 0
        while self.kiwoom.isNext == 2:
            print(f'idx - {idx}')
            params = {"업종코드": json_data['code'],
                      "틱범위": json_data['tic'],
                      "get_next": self.kiwoom.isNext}
            data.append(self.feeder.request(trCode="opt20005", **params))
            idx += 1
            #시험삼아 한 코드니 지우도록.
            if idx > 3:
                break

        return jsonify(data)

# 업종일봉조회요청
class OPT20006(Resource):
    def __init__(self, feeder, kiwoom):
        self.feeder = feeder
        self.kiwoom = kiwoom

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
    def __init__(self, feeder, kiwoom):
        self.feeder = feeder
        self.kiwoom = kiwoom

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
    def __init__(self, feeder, kiwoom):
        self.feeder = feeder
        self.kiwoom = kiwoom

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