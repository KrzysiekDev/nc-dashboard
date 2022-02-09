import datetime as dt
import json

import pandas as pd
import streamlit as st

LP_METHODS = [
    'Add Liquidity ETH',
    'Remove Liquidity ETH With Permit Supporting Fee On Transfer Tokens',
    'Remove Liquidity With Permit',
    'Remove Liquidity'
]
FARMING_METHODS = ['Stake', 'Unstake']
BUY_SELL_METHODS = [
    'Swap Exact ETH For Tokens',
    'Swap Exact Tokens For ETH Supporting Fee On Transfer Tokens',
    'Swap Exact Tokens For Tokens',
    'Swap Exact Tokens For Tokens Supporting Fee On Transfer Tokens',
    'Swap ETH For Exact Tokens', 'Swap'
]

NC_PATH = r"./data/NC.csv"
LP_PATH = r"./data/LP.csv"
GLOBAL_PATH = r"./data/global_data.json"

pd.options.mode.chained_assignment = None


@st.cache
def read_data():
    nc = pd.read_csv(NC_PATH, thousands=',', parse_dates=['DateTime'])
    lp = pd.read_csv(LP_PATH, thousands=',', parse_dates=['DateTime'])
    return nc, lp


@st.cache
def read_global_data():
    with open(GLOBAL_PATH, 'r') as f:
        data = json.load(f)
    return data


@st.cache
def get_all_addresses(df):
    addresses = set(df.From.unique())
    addresses.update(df.To.unique())
    addresses = list(addresses)
    addresses.append('')
    addresses.sort()
    return addresses


@st.cache
def process_transaction_data(df, address=None, methods=None, scale=1, invert=False, subtract=None):
    if address:
        trn = df[(df['From'] == address) | (df['To'] == address)]
    else:
        trn = df

    if methods:
        trn = trn[trn['Method'].isin(methods)]

    trn.loc[:, 'Balance'] = trn['Quantity']
    trn.loc[:, 'Balance'][trn.From == address] *= -1
    trn.loc[trn['Balance'] < 0, 'Balance'] /= scale
    trn.loc[:, 'Balance'] = trn['Balance'].cumsum()
    if invert:
        trn.loc[:, 'Balance'] *= -1
    if subtract:
        trn.loc[:, 'Balance'] = subtract - trn.loc[:, 'Balance']
    return trn


@st.cache
def get_days(trn):
    return (dt.datetime.today() - trn.DateTime.min()).days


@st.cache
def get_ratios(trn, address, methods=None):
    if methods is None:
        methods = []
    from_quantity = trn[trn.Method.isin(methods)][trn.From == address].Quantity.sum()
    to_quantity = trn[trn.Method.isin(methods)][trn.To == address].Quantity.sum()
    return from_quantity, to_quantity
