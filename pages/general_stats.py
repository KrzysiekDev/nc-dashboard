import plotly_express as px
import streamlit as st

from transform.data_processing import process_transaction_data


def general_stats_page(nc, lp, nc_price, uni_v2_price, circulating_supply, hodlers, total_liquidity, locked_lp_tokens,
                       reward):
    st.header('General stats')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("MarketCap", f'{1_000_000_000 * nc_price:,.2f} USD')
    col2.metric("Circulating supply", f'{circulating_supply:,} NC')
    col3.metric("Circulating MarketCap", f'{circulating_supply * nc_price:,.2f} USD')
    col4.metric("Hodlers", f'{hodlers} addresses')

    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Transactions", f'{len(nc)}')
    col2.metric("Total liquidity", f'{total_liquidity:,.2f} UNI-V2')
    col3.metric("LP value", f'{total_liquidity * uni_v2_price:,.2f} USD')
    col4.metric("Locked LP tokens", f'{locked_lp_tokens:,.2f} UNI-V2')

    col1, col2, col3, col4 = st.columns(4)

    col1.metric("Locked tokens ratio", f'{(locked_lp_tokens / total_liquidity) * 100:,.2f}%')
    col2.metric("Locked LP value", f'{locked_lp_tokens * uni_v2_price:,.2f} USD')
    col3.metric("Reward value", f'{(reward * nc_price):,.2f} USD')
    col4.metric("Reward", f'{reward:,} NC')

    transactions = process_transaction_data(nc, '0xba93f37118f9d0ac9f620cd7bfb9fd79635db7d3', subtract=1_000_000_000)

    lp_transactions = process_transaction_data(lp, '0x0000000000000000000000000000000000000000', invert=True)

    st.header('Circulating supply history')
    st.plotly_chart(px.line(transactions[['DateTime', 'Balance']], x='DateTime', y='Balance'), use_container_width=True)

    st.header('LP balance history')
    st.plotly_chart(px.line(lp_transactions[['DateTime', 'Balance']], x='DateTime', y='Balance'),
                    use_container_width=True)
