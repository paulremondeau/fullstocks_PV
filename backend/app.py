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
DATABASE_PATH = "./database"


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

import plotly.express as px
import plotly


from flask import Flask

# from flask_sqlalchemy import SQLAlchemy
# from flask_marshmallow import Marshmallow
from flask_cors import CORS
from flask_swagger import swagger
from flask_swagger_ui import get_swaggerui_blueprint

from config import FRONTEND_URL

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
#     Routes
# =================================================================================================


@app.route("/send_graph", methods=["GET"])
def send_graph():
    df_monthly = pd.read_csv(
        f"{DATABASE_PATH}/PVDAQ/monthly_aggregation/system_10_aggregation.csv"
    )
    fig_monthly = px.bar(
        df_monthly, x="month", y="energy", title="Monthly production (kWh)"
    )
    graphJSON_monthly = plotly.io.to_json(fig_monthly)

    df_daily = pd.read_csv(
        f"{DATABASE_PATH}/PVDAQ/daily_evolution_power/system_10_daily.csv"
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

    df_efficiency = pd.read_csv(
        f"{DATABASE_PATH}/PVDAQ/efficiency_data/efficiency_system_10.csv"
    )
    fig_efficiency = px.scatter(
        df_efficiency,
        x="Irradiance (W/m²)",
        y="Module temperature (°C)",
        color="Efficiency",
        title="Module efficiency evolution in function of irradiance and temperature",
    )
    graphJSON_efficiency = plotly.io.to_json(fig_efficiency)

    res = {
        "info": [],
        "monthly_chart": graphJSON_monthly,
        "daily_chart": graphJSON_daily,
        "efficiency_chart": graphJSON_efficiency,
    }
    return res


@app.route("/system_metadata", methods=["GET"])
def send_metadata():
    df = pd.read_csv(f"{DATABASE_PATH}/PVDAQ/metadata_deluxe.csv")
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
