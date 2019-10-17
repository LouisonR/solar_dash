import os
import sqlalchemy as db
import pandas as pd
import numpy as np
from matplotlib import pyplot as plt
import seaborn as sns
from datetime import datetime as dt
from dateutils import relativedelta


dir_path = os.path.dirname(os.path.realpath(__file__))
DATABASE_URL = "sqlite:///" + dir_path + "/data/sqlite_demo_wpo.db"

engine = db.create_engine(DATABASE_URL, connect_args={'check_same_thread': False})
connection = engine.connect()
metadata = db.MetaData()


def load_table(table_name):
    return db.Table(table_name, metadata, autoload=True, autoload_with=engine)

def get_stmt(stmt):
    result_proxy = connection.execute(stmt)
    return result_proxy.fetchall()

def get_sites_id_name():
    site = load_table("site")
    stmt = db.select([site.c.id_site, site.c.name])
    sites_lst = [(sit[0], sit[1]) for sit in get_stmt(stmt)]
    return sites_lst

def get_clients_id():
    client = load_table("client")
    stmt = db.select([client.c.id_client])
    clients_id_lst = [int(client_id[0]) for client_id in get_stmt(stmt)]
    return clients_id_lst

def get_variables_id_name():
    variable = load_table("variable")
    stmt = db.select([variable.c.id_variable, variable.c.french_name])
    variables_lst = [(var[0], var[1]) for var in get_stmt(stmt)]
    return variables_lst

def get_access_sites(clientid):
    site = load_table("site")
    if clientid == 0:
        s_site = db.select([site.c.id_site, site.c.name])
    else:
        s_site = db.select([site.c.id_site, site.c.name]).where(site.c.client_id == clientid)
    sites_access_lst = get_stmt(s_site)
    return sites_access_lst

def get_equipment_sel(site_id):
    #print("site selected: ", site_id)
    equipment = load_table("equipment")
    s_equi = db.select([equipment.c.id_equipment]).where(equipment.c.site_id == site_id)
    return [id[0] for id in get_stmt(s_equi)]

def get_measure_sel(equi_sel, variable_id):
    #print("variable selected:", variable_id)
    #print("equipments selected:", equi_sel)
    measure = load_table("measure")
    s_meas = db.select([measure.c.value, measure.c.ts, measure.c.equipment_id])
    s_meas = s_meas.where(measure.c.equipment_id.in_ (equi_sel))
    s_meas = s_meas.where(measure.c.variable_id == variable_id)
    return get_stmt(s_meas)

def get_df(site_id, variable_id, starting_date, ending_date):

    equi_sel = get_equipment_sel(site_id)
    measures_select = get_measure_sel(equi_sel, variable_id)

    df = pd.DataFrame(measures_select, columns=["value", "date", "equipment"])
    df['datetime'] = pd.to_datetime(df['date'])
    df.drop(['date'], axis=1, inplace=True)
    df_sel = df[(df.datetime > starting_date) & (df.datetime < ending_date)]
    return df_sel
