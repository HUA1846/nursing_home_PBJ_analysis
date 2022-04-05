import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib as mpl
import ipywidgets as widgets
from ipywidgets import interact, interact_manual
from collections import deque

# connect to database
import sqlalchemy as db
engine = db.create_engine('postgresql+psycopg2://postgres:1111@localhost/postgres')
connection = engine.connect()
metadata = db.MetaData()
occupancy = db.Table('occ', metadata, autoload=True, autoload_with=engine)

from utils.utils import states
ensign_color = '#0019FE'

states = deque(states)
states.appendleft(None)

def get_pre_post_covid_df(onlyEnsign, state=None):
    if not onlyEnsign:
        pre_query = db.select([occupancy]).where(db.or_(db.and_(occupancy.columns.year==2020,
                                                 occupancy.columns.month < 4,
                                                 occupancy.columns.occupancy<=1), 
                                                 db.and_(occupancy.columns.year==2019,
                                                 occupancy.columns.occupancy<=1)))
        post_query = db.select([occupancy]).where(db.or_(db.and_(occupancy.columns.year==2020,
                                                 occupancy.columns.month >= 4,
                                                 occupancy.columns.occupancy<=1), 
                                                 db.and_(occupancy.columns.year==2021,
                                                 occupancy.columns.occupancy<=1)))
        
    else:
        pre_query = db.select([occupancy]).where(db.or_(db.and_(occupancy.columns.year==2020,
                                                                occupancy.columns.ensign == True,
                                                                occupancy.columns.month < 4,
                                                                occupancy.columns.occupancy<=1), 
                                                         db.and_(occupancy.columns.ensign == True,
                                                                 occupancy.columns.year==2019,
                                                                occupancy.columns.occupancy<=1)))
        post_query = db.select([occupancy]).where(db.or_(db.and_(occupancy.columns.year==2020,
                                                                 occupancy.columns.ensign == True,
                                                                 occupancy.columns.month >= 4,
                                                                 occupancy.columns.occupancy<=1), 
                                                         db.and_(occupancy.columns.ensign == True,
                                                                 occupancy.columns.year==2021,
                                                                 occupancy.columns.occupancy<=1)))
    df_pre = pd.read_sql_query(pre_query, con=engine)
    df_post = pd.read_sql_query(post_query, con=engine)
    
    if state is not None:
        df_pre = df_pre[df_pre['state']==state]
        df_post = df_post[df_post['state']==state]
        
    return df_pre, df_post


@interact
def plot_2020_2021_occupancy_interactive(onlyEnsign=[True, False], state=states):
    color = 'orange'
    if not onlyEnsign:
        df_2020, df_2021 = get_pre_post_covid_df(False)

        
    else:
        df_2020, df_2021 = get_pre_post_covid_df(True)
        color = ensign_color
    
    if state is not None:
        df_2020 = df_2020[df_2020['state']==state]
        df_2021 = df_2021[df_2021['state']==state]
        
    fig, axes = plt.subplots(1, 2, figsize=(12,4))

    axes[0].set_facecolor((1, 1, 1))
    axes[1].set_facecolor((1, 1, 1))

    y, x, _ = axes[0].hist(x=df_2020['occupancy'], bins=np.arange(0, df_2020['occupancy'].max() + 0.1, 0.05), color=color)
    axes[0].set_title('pre-covid occupancy')
    axes[0].set_xlabel('certified bed occupancy')
    axes[0].set_ylabel('days')
    axes[0].set_xlim(0,1)
    mean_2020 = df_2020['occupancy'].mean()
    median_2020 = df_2020['occupancy'].median()
    axes[0].vlines(mean_2020, ymin=0, ymax=y.max(), linestyles='dashed', color='r',
                  label=f'mean: {round(mean_2020,2)}')
    axes[0].vlines(median_2020, ymin=0, ymax=y.max(), linestyles='dashed', color='g',
                  label=f'median: {round(median_2020,2)}')
    axes[0].legend();

    y1, x1, _ = axes[1].hist(x=df_2021['occupancy'], bins=np.arange(0, df_2021['occupancy'].max() + 0.1, 0.05), color=color)
    axes[1].set_title('post-covid occupancy')
    axes[1].set_xlabel('certified bed occupancy')
    axes[1].set_xlim(0,1)
    mean_2021 = df_2021['occupancy'].mean()
    median_2021 = df_2021['occupancy'].median()
    axes[1].vlines(df_2021['occupancy'].mean(), ymin=0, ymax=y1.max(), linestyles='dashed', color='r',
                  label=f'mean: {round(mean_2021,2)}')
    axes[1].vlines(median_2021, ymin=0, ymax=y1.max(), linestyles='dashed', color='g',
                  label=f'median: {round(median_2021,2)}')
    axes[1].legend();
    
    plt.show()


def plot_2020_2021_occupancy(onlyEnsign, state):
    color = 'orange'
    if not onlyEnsign:
        df_2020, df_2021 = get_pre_post_covid_df(False)

        
    else:
        df_2020, df_2021 = get_pre_post_covid_df(True)
        color = ensign_color
    
    if state is not None:
        df_2020 = df_2020[df_2020['state']==state]
        df_2021 = df_2021[df_2021['state']==state]
        
    fig, axes = plt.subplots(1, 2, figsize=(12,4))

    axes[0].set_facecolor((1, 1, 1))
    axes[1].set_facecolor((1, 1, 1))

    y, x, _ = axes[0].hist(x=df_2020['occupancy'], bins=np.arange(0, df_2020['occupancy'].max() + 0.1, 0.05), color=color)
    axes[0].set_title('pre-covid occupancy')
    axes[0].set_xlabel('certified bed occupancy')
    axes[0].set_ylabel('days')
    axes[0].set_xlim(0,1)
    mean_2020 = df_2020['occupancy'].mean()
    median_2020 = df_2020['occupancy'].median()
    axes[0].vlines(mean_2020, ymin=0, ymax=y.max(), linestyles='dashed', color='r',
                  label=f'mean: {round(mean_2020,2)}')
    axes[0].vlines(median_2020, ymin=0, ymax=y.max(), linestyles='dashed', color='g',
                  label=f'median: {round(median_2020,2)}')
    axes[0].legend();

    y1, x1, _ = axes[1].hist(x=df_2021['occupancy'], bins=np.arange(0, df_2021['occupancy'].max() + 0.1, 0.05), color=color)
    axes[1].set_title('post-covid occupancy')
    axes[1].set_xlabel('certified bed occupancy')
    axes[1].set_xlim(0,1)
    mean_2021 = df_2021['occupancy'].mean()
    median_2021 = df_2021['occupancy'].median()
    axes[1].vlines(df_2021['occupancy'].mean(), ymin=0, ymax=y1.max(), linestyles='dashed', color='r',
                  label=f'mean: {round(mean_2021,2)}')
    axes[1].vlines(median_2021, ymin=0, ymax=y1.max(), linestyles='dashed', color='g',
                  label=f'median: {round(median_2021,2)}')
    axes[1].legend();
    
    plt.show()