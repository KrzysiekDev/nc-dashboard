import streamlit as st

from pages.general_stats import general_stats_page
from pages.one_address import one_address_page
from transform.data_processing import get_all_addresses, read_data, read_global_data

st.set_page_config('NC Coin Dashboard', '⛓', 'wide')

st.title('NC Coin Dashboard')

nc, lp = read_data()
global_data = read_global_data()

nc_price = global_data['nc_price']
uni_v2_price = global_data['uni_v2_price']
circulating_supply = global_data['circulating_supply']
hodlers = global_data['hodlers']
total_liquidity = global_data['total_liquidity']
locked_lp_tokens = global_data['locked_lp_tokens']
reward = global_data['reward']

addresses = get_all_addresses(nc)

address = st.selectbox('Choose address', addresses)

if address != '':
    one_address_page(nc, lp, address, nc_price, uni_v2_price)
else:
    general_stats_page(nc, lp, nc_price, uni_v2_price, circulating_supply, hodlers, total_liquidity, locked_lp_tokens,
                       reward)
