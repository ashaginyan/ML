# -*- coding: utf-8 -*-
from flask import Flask, jsonify
from flask_restful import Api, Resource, reqparse
import psycopg2
from lxml import etree
import requests
import pandas as pd
from src.models import Strict_model, Middle_model, Risk_model, get_score
import numpy as np


app = Flask(__name__)
api = Api(app)

class Retrain(Resource):
    def get(self):
        strict_model = Strict_model()
        middle_model = Middle_model()
        risk_model = Risk_model()
        r = requests.get("http://easytrading.pw/API/HistoryEnters/getEntersFORML.ashx")
        root = etree.XML(r.text)
        tree = etree.ElementTree(root)
        l = {}
        for i, child in enumerate(root):
            if i == 0:
                for j, child2 in enumerate(child):
                    l[child2.tag] = [child2.text]
        for i, child in enumerate(root):
            if i > 0:
                for j, child2 in enumerate(child):
                    l[child2.tag].append(child2.text)
        data = pd.DataFrame(data=l)

        data = data.rename(columns={"Result": "result"})

        for column in data.columns:
            try:
                data[column] = data[column].str.replace(',', '.').astype(float)
            except:
                pass

        strict_model.train(data)
        middle_model.train(data)
        risk_model.train(data)
        score_strict = get_score(strict_model.y_test, strict_model.y_pred_test)
        score_middle = get_score(middle_model.y_test, middle_model.y_pred_test)
        score_risk = get_score(risk_model.y_test, risk_model.y_pred_test)

        with open('scores.txt', 'w') as f:
            f.write(
                f'{round(score_strict[0] * 100)} {round(score_strict[1] * 100)} {round(score_strict[2] * 100)} {round(score_strict[3] * 100)}\n')
            f.write(
                f'{round(score_middle[0] * 100)} {round(score_middle[1] * 100)} {round(score_middle[2] * 100)} {round(score_middle[3] * 100)}\n')
            f.write(
                f'{round(score_risk[0] * 100)} {round(score_risk[1] * 100)} {round(score_risk[2] * 100)} {round(score_risk[3] * 100)}\n')

        return {'score_strict': [score_strict[0], score_strict[1], score_strict[2], score_strict[3]],\
                'score_middle': [score_middle[0], score_middle[1], score_middle[2], score_middle[3]],
                'score_risk': [score_risk[0], score_risk[1], score_risk[2], score_risk[3]]}


class Result(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument("enter")
        parser.add_argument("TimeFrame")
        parser.add_argument("riskprofit")
        parser.add_argument("R0_P")
        parser.add_argument("PATTERN_PR_T")
        parser.add_argument("R0_T")
        parser.add_argument("R0_Way")
        parser.add_argument("R0_Pattern")
        parser.add_argument("R_Forecast_Pattern")
        parser.add_argument("R_Forecast_Percent")
        # parser.add_argument("result")
        parser.add_argument("R1_P")
        parser.add_argument("R1_T")
        parser.add_argument("R1_Way")
        parser.add_argument("R1_Pattern")
        parser.add_argument("R2_Pattern")
        parser.add_argument("B0_P")
        parser.add_argument("B0_T")
        parser.add_argument("B0_Way")
        parser.add_argument("B0_Pattern")
        parser.add_argument("B_Forecast_Pattern")
        parser.add_argument("B_Forecast_Percent")
        parser.add_argument("B1_Way")
        parser.add_argument("B1_Pattern")
        parser.add_argument("P0_P")
        parser.add_argument("P0_T")
        parser.add_argument("P0_Way")
        parser.add_argument("P0_Pattern")
        parser.add_argument("P_Forecast_Pattern")
        parser.add_argument("P_Forecast_Percent")
        parser.add_argument("P1_Way")
        parser.add_argument("P1_Pattern")
        parser.add_argument("PATTERN_PR_P")
        params = parser.parse_args()
        js = {"TimeFrame": params["TimeFrame"], "riskprofit": params["riskprofit"], "PATTERN_PR_P": params["PATTERN_PR_P"],
              "PATTERN_PR_T": params["PATTERN_PR_T"],
              "R0_P": params["R0_P"], "R0_T": params["R0_T"], "R0_Way": params["R0_Way"],
              "R0_Pattern": params["R0_Pattern"], "R_Forecast_Pattern": params["R_Forecast_Pattern"],
              "R_Forecast_Percent": params["R_Forecast_Percent"], "R1_P": params["R1_P"],
              "R1_T": params["R1_T"],
              "R1_Way": params["R1_Way"], "R1_Pattern": params["R1_Pattern"], "R2_Pattern": params["R2_Pattern"],
              "B0_P": params["B0_P"], "B0_T": params["B0_T"], "B0_Way": params["B0_Way"],
              "B0_Pattern": params["B0_Pattern"], "B_Forecast_Pattern": params["B_Forecast_Pattern"],
              "B_Forecast_Percent": params["B_Forecast_Percent"],
              "B1_Way": params["B1_Way"], "B1_Pattern": params["B1_Pattern"], "P0_P": params["P0_P"],
              "P0_T": params["P0_T"], "P0_Way": params["P0_Way"], "P0_Pattern": params["P0_Pattern"],
              "P_Forecast_Pattern": params["P_Forecast_Pattern"],
              "P_Forecast_Percent": params["P_Forecast_Percent"], "P1_Way": params["P1_Way"],
              "P1_Pattern": params["P1_Pattern"]}
        data = pd.DataFrame(data=js, index=[0,])
        data.rename(columns={'Result': 'result'})

        for column in data.columns:
            try:
                data[column] = data[column].str.replace(',', '.').astype(float)
            except:
                pass

        strict_model = Strict_model()
        middle_model = Middle_model()
        risk_model = Risk_model()

        for i, col in enumerate(data.columns):
            data.iloc[0, i] = np.nan_to_num(data.iloc[0, i])

        y_strict, y_proba_strict = strict_model.test(data)

        y_middle = middle_model.test(data)

        y_risk, y_proba_risk = risk_model.test(data)

        if y_strict[0] == 0:
            y_strict[0] = 1
        else:
            y_strict[0] = -1
        if y_middle[0] == 0:
            y_middle[0] = 1
        else:
            y_middle[0] = -1
        if y_risk[0] == 0:
            y_risk[0] = -1

        if y_strict[0] == - 1:
            strict_proba = y_proba_strict[:, 1]
        else:
            strict_proba = y_proba_strict[:, 0]

        if y_risk[0] == - 1:
            risk_proba = y_proba_risk[:, 0]
        else:
            risk_proba = y_proba_risk[:, 1]

        scores = {}
        with open('scores.txt', 'r') as f:
            for i, line in enumerate(f):
                if i == 0:
                    scores['strict'] = [float(num) for num in line.strip().split()]
                if i == 1:
                    scores['middle'] = [float(num) for num in line.strip().split()]
                if i == 2:
                    scores['risk'] = [float(num) for num in line.strip().split()]


        return {'strict_model': {"answer": y_strict.tolist()[0], "confidence": strict_proba.tolist()[0]*100,
                                 "percentage_of_found_failure": scores['strict'][1],
                                 "percentage_of_cut_off_success": 100 - scores['strict'][0]},
                'middle_model': {"answer": float(y_middle), "percentage_of_found_failure": scores['middle'][1],
                                 "percentage_of_cut_off_success": 100 - scores['middle'][0]},
                'risk_model': {"answer": y_risk.tolist()[0], "confidence": risk_proba.tolist()[0]*100,
                "percentage_of_found_success": scores['risk'][1],
                               "percentage_of_cut_off_failure": 100 - scores['risk'][0]}}


@app.route('/', methods=['GET'])
def home():
    return "Hello"

api.add_resource(Result, "/result/post")
api.add_resource(Retrain, "/retrain/get")

if __name__ == '__main__':
    app.run(debug=True)
