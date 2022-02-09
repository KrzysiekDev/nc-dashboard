import plotly_express as px
import streamlit as st

from transform.data_processing import BUY_SELL_METHODS, FARMING_METHODS, LP_METHODS, get_days, get_ratios, \
    process_transaction_data


def one_address_page(nc, lp, address, nc_price, uni_v2_price):
    st.header('Address details')

    transactions = process_transaction_data(nc, address, scale=0.95)

    lp_transactions = process_transaction_data(lp, address)

    farm_transactions = process_transaction_data(lp, address, FARMING_METHODS)

    has_lp_transactions = len(lp_transactions) > 0

    has_farm_transactions = len(farm_transactions) > 0

    balance = abs(transactions.tail(1)['Balance'].values[0])

    sells, buys = get_ratios(transactions, address, BUY_SELL_METHODS)

    st.subheader('NC stats')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Time", f'{get_days(transactions)} days')
    col2.metric("Balance", f'{balance:,.2f} NC')
    col3.metric("Buys", f'{buys:,.2f} NC')
    col4.metric("Sells", f'{sells:,.2f} NC')

    transfered, received = get_ratios(transactions, address, ['Transfer'])

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Transfered", f'{transfered:,.2f} NC')
    col2.metric("Received", f'{received:,.2f} NC')
    col3.metric("NC price", f"{nc_price:,.9f} USD")
    col4.metric("Value", f"{balance * nc_price:,.2f} USD")

    if (has_lp_transactions):
        st.subheader('LP stats')
        lp_balance = abs(lp_transactions.tail(1)['Balance'].values[0])
        removed, added = get_ratios(lp_transactions, address, LP_METHODS)
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Time", f'{get_days(lp_transactions)} days')
        col2.metric("Balance", f'{lp_balance:,.2f} UNI-V2')
        col3.metric("Added liquidity", f'{added:,.2f} UNI-V2')
        col4.metric("Removed liquidity", f'{removed:,.2f} UNI-V2')

        col1, col2, _, _ = st.columns(4)
        col1.metric("LP price", f'{uni_v2_price:,.9f} USD')
        col2.metric("Value", f'{(lp_balance * uni_v2_price):,.2f} USD')

    if (has_farm_transactions):
        st.subheader('Farm stats')
        farm_balance = abs(-farm_transactions.tail(1)['Balance'].values[0])
        added, removed = get_ratios(lp_transactions, address, FARMING_METHODS)
        _, claimed = get_ratios(transactions, address, ['Claim'])
        col1, col2, col3, col4 = st.columns(4)
        col1.metric("Time", f'{get_days(farm_transactions)} days')
        col2.metric("Balance", f'{farm_balance:,.2f} UNI-V2')
        col3.metric("Staked", f'{added:,.2f} UNI-V2')
        col4.metric("Unstaked", f'{removed:,.2f} UNI-V2')

        claimed_value = nc_price * claimed
        stacked_value = farm_balance * uni_v2_price

        col1, col2, col3, _ = st.columns(4)
        col1.metric("Claimed", f'{claimed:,.2f} NC')
        col2.metric("Claimed Value", f'{claimed_value:,.2f} USD')
        col3.metric("Stacked Value", f'{stacked_value:,.2f} USD')

    st.header('NC balance history')

    st.plotly_chart(px.line(transactions[['DateTime', 'Balance']], x='DateTime', y='Balance'), use_container_width=True)

    if (has_lp_transactions):
        st.header('LP balance history')
        st.plotly_chart(px.line(lp_transactions[['DateTime', 'Balance']], x='DateTime', y='Balance'),
                        use_container_width=True)
