import streamlit as st
import datetime as dt

import pandas as pd
from src.utils.datetime import MONTHS
from src.utils.directory import FINAL_PATH, EXPENSE_YAML_PATH, INCOME_YAML_PATH
import fire
import os
from src.utils.io import load_yaml
from emoji import emojize
from src.utils.grouping import get_category
from src.utils.streamlit import plot_category, display_category#, plot_timeline, plot_historical_timeline, display_dataframe


def main(year: int = None, month: int = None):
    today = dt.datetime.now()
    today_year = today.year
    today_month = today.month

    if (year is None) and (month is None):
        year = today_year
        month = today_month - 1
    elif ((year is None) and (month is not None)) or ((year is not None) and (month is None)):
        raise ValueError("year and month must be specified together")
    if year > today_year:
        raise AssertionError("Could not get information for the current month / future")
    elif year == today_year:
        assert month <= today_month - 1, "Could not get information for the current month / future"
    else:
        assert month <= 12

    expense_df = pd.read_csv(os.path.join(FINAL_PATH, "expense_{}_{}.csv".format(year, month)))
    income_df = pd.read_csv(os.path.join(FINAL_PATH, "income_{}_{}.csv".format(year, month)))
    expense_dict = load_yaml(EXPENSE_YAML_PATH)
    income_dict = load_yaml(INCOME_YAML_PATH)

    expense_category_df = get_category(expense_df)
    expense_category_df['amount'] = expense_category_df['amount'] * -1.
    income_category_df = get_category(income_df)

    st.title(emojize("Transaction details for {}, {} :smirk:".format(MONTHS[month], year), use_aliases=True))
    st.subheader("Total Expenses : S${:.2f}".format(expense_df.amount.sum() * -1.))
    st.subheader("Total Income : S${:.2f}".format(income_df.amount.sum()))

    st.header("Top expenses by category")
    plot_category(expense_category_df, expense_dict)
    display_category(expense_category_df, expense_dict)

    st.header("Top income by category")
    plot_category(income_category_df, income_dict)
    display_category(income_category_df, income_dict)

    st.header("Expenses Timeline")
    timeline_option = st.multiselect('Category', list(expense_dict.keys()), default=[])
    plot_timeline(expense_df, timeline_option)

    st.header("Historical Timeline")
    historical_option = st.multiselect('Category', list(expense_dict.keys()), default=[])
    plot_historical_timeline(year, month, historical_option)

    st.header("Expenses Transaction DataFrame")
    expense_option = st.multiselect('Category', list(expense_dict.keys()), default=[])
    display_dataframe(expense_df, expense_option)

    st.header("Income Transaction DataFrame")
    income_option = st.multiselect("Category", list(income_dict.keys()), default=[])
    display_dataframe(income_df, income_option)

if __name__ == "__main__":
    fire.Fire(main)
