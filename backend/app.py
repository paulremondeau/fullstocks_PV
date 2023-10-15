#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""app.py:  app

This is the main app application file.
"""


__author__ = "Paul RÉMONDEAU"
__copyright__ = "Paul RÉMONDEAU"
__version__ = "1.0.0"
__maintainer__ = "Paul RÉMONDEAU"
__email__ = "paul.remondeau@ik.me"
__status__ = "Production"
__logger__ = "app.py"

LOG_CONFIG_FILE = "config/log_config.ini"


# =================================================================================================
#     Libs
# =================================================================================================

import json
import re
import os
import datetime
from typing import Dict, List
import logging
import logging.config

import pandas as pd
import pytz

import plotly.express as px
import plotly

EUROPE_TIMEZONE = pytz.timezone("Europe/Paris")

from flask import Flask, request

# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from config import API_KEY, API_PLAN, FRONTEND_URL

basedir = os.path.abspath(os.path.dirname(__file__))

# =================================================================================================
#     LOGS
# =================================================================================================


logging.config.fileConfig(os.path.join(basedir, LOG_CONFIG_FILE))
logger = logging.getLogger(__logger__)
logger.info("Logger initialized.")


# =================================================================================================
#     Flask App
# =================================================================================================

app = Flask(__name__)
app.config.from_object(__name__)
# app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///" + os.path.join(
#     basedir, "db.sqlite"
# )
#
# app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
# app.app_context().push()

# enable CORS
cors = CORS(
    app,
    resources={
        r"/send_graph/*": {"origins": FRONTEND_URL},
        r"/system_metadata/*": {"origins": FRONTEND_URL},
    },
)
logger.info("Backend server initialized.")

# =================================================================================================
#     Database
# =================================================================================================

# db = SQLAlchemy(app)
# ma = Marshmallow(app)

# SYMBOL_LENGTH = 20
# EXCHANGE_LENGTH = 30
# COUNTRY_LENGTH = 30


# class StockTimeSeries(db.Model):
#     symbol = db.Column(db.String(SYMBOL_LENGTH), primary_key=True)
#     timeDelta = db.Column(db.String(6), primary_key=True)
#     exchange = db.Column(db.String(EXCHANGE_LENGTH))
#     timezone = db.Column(db.String(100))
#     timeseries = db.Column(db.PickleType(comparator=pd.Series.equals))
#     marketChecked = db.Column(db.Boolean)

#     def __init__(
#         self, symbol, timeDelta, exchange, timezone, timeseries, marketChecked
#     ):
#         self.symbol = symbol
#         self.timeDelta = timeDelta
#         self.exchange = exchange
#         self.timezone = timezone
#         self.timeseries = timeseries
#         self.marketChecked = marketChecked


# class StockTimeSeriesSchema(ma.Schema):
#     class Meta:
#         fields = (
#             "symbol",
#             "timeDelta",
#             "exchange",
#             "timezone",
#             "timeseries",
#             "marketChecked",
#         )


# stock_timeseries_schema = StockTimeSeriesSchema()
# stocks_timeseries_schema = StockTimeSeriesSchema(many=True)


# class MarketState(db.Model):
#     exchange = db.Column(db.String(EXCHANGE_LENGTH), primary_key=True)
#     country = db.Column(db.String(COUNTRY_LENGTH))
#     isMarketOpen = db.Column(db.Boolean)
#     timeToOpen = db.Column(db.PickleType())
#     timeToClose = db.Column(db.PickleType())
#     dateCheck = db.Column(db.Float)

#     def __init__(
#         self, exchange, country, isMarketOpen, timeToOpen, timeToClose, dateCheck
#     ):
#         self.exchange = exchange
#         self.country = country
#         self.isMarketOpen = isMarketOpen
#         self.timeToOpen = timeToOpen
#         self.timeToClose = timeToClose
#         self.dateCheck = dateCheck


# class MarketStateSchema(ma.Schema):
#     class Meta:
#         fields = (
#             "exchange",
#             "country",
#             "isMarketOpen",
#             "timeToOpen",
#             "timeToClose",
#             "dateCheck",
#         )


# market_schema = MarketStateSchema()
# markets_schema = MarketStateSchema(many=True)


# class AvailableSymbols(db.Model):
#     exchange = db.Column(db.String(EXCHANGE_LENGTH), primary_key=True)
#     symbolsList = db.Column(db.PickleType())
#     dateCheck = db.Column(db.Float)

#     def __init__(self, exchange, symbolsList, dateCheck):
#         self.exchange = exchange
#         self.symbolsList = symbolsList
#         self.dateCheck = dateCheck


# class AvailableSymbolsSchema(ma.Schema):
#     class Meta:
#         fields = (
#             "exchange",
#             "symbolsList",
#             "dateCheck",
#         )


# available_symbols_schema = AvailableSymbolsSchema()
# available_symbols_many_schema = AvailableSymbolsSchema(many=True)

# db.create_all()

# logger.info("Database initialized.")

# =================================================================================================
#     Routes
# =================================================================================================


@app.route("/send_graph", methods=["GET"])
def send_graph():
    df_monthly = pd.read_csv(
        "../database/PVDAQ/monthly_aggregation/system_10_aggregation.csv"
    )
    fig_monthly = px.bar(
        df_monthly, x="month", y="energy", title="Monthly production (kWh)"
    )
    graphJSON_monthly = plotly.io.to_json(fig_monthly)

    df_daily = pd.read_csv(
        "../database/PVDAQ/daily_evolution_power/system_10_daily.csv"
    )
    fig_daily = px.line(
        df_daily,
        x="hours_minutes",
        y="DC_power_mean",
        color="Month",
        title="Daily evolution of the DC power production (W) for each month",
    )
    for scat in fig_daily.data:
        if scat.legendgroup in [
            "February",
            "April",
            "June",
            "August",
            "October",
            "December",
        ]:
            scat.visible = "legendonly"
    graphJSON_daily = plotly.io.to_json(fig_daily)

    res = {
        "info": [],
        "monthly_chart": graphJSON_monthly,
        "daily_chart": graphJSON_daily,
    }
    return res


@app.route("/system_metadata", methods=["GET"])
def send_metadata():
    df = pd.read_csv("../database/PVDAQ/metadata_deluxe.csv")
    res = {}
    for system in df.iloc:
        res[int(system["system_id"])] = system[1:].to_json()
    return json.dumps(res)


@app.route("/spec")
def spec():
    swag = swagger(app)
    swag["info"]["version"] = "1.0"
    swag["info"]["title"] = "PV Analytics backend"

    return json.dumps(swag)


# Start the app
if __name__ == "__main__":
    # Production server

    SWAGGER_URL = "/api/docs"
    API_URL = "/spec"
    swaggerui_blueprint = get_swaggerui_blueprint(SWAGGER_URL, API_URL)

    from waitress import serve

    app.register_blueprint(swaggerui_blueprint, url_prefix=SWAGGER_URL)

    serve(app, host="0.0.0.0", port=5000)
