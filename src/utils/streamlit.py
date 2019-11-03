import matplotlib.pyplot as plt
import pandas as pd
import seaborn as sns
import streamlit as st
from src.utils.directory import FINAL_PATH
import os

from src.utils.color import color


def plot_category(input_df, input_dict):
    sns.set()
    plt.figure(figsize=(10, 4))
    plot_df = input_df.copy()
    sns.barplot(x="amount", y="true_category", data=plot_df)
    plt.tight_layout()
    st.pyplot()


def display_category(input_df, input_dict):
    df = input_df.copy()
    df["amount"] = df["amount"].apply(lambda x: "S$ {:.2f}".format(x))
    df.columns = ["CATEGORY", "AMOUNT"]
    st.table(df)


def plot_timeline(input_df, option, input_dict):
    sns.set()
    plt.figure(figsize=(10, 4))
    full_df = input_df.copy()
    categories = list(input_dict.keys())
    if len(option) == 0:
        plot_df = full_df.set_index(pd.to_datetime(full_df.made_on))
        resample_df = plot_df.resample("D")["amount"].sum().reset_index()
        sns.lineplot(x=resample_df.made_on.astype(str), y=resample_df.amount)
        plt.xticks(rotation=90)
        st.pyplot()
    else:
        for category in option:
            category_df = full_df[full_df["true_category"] == category].copy().reset_index(drop=True)
            plot_df = category_df.set_index(pd.to_datetime(category_df.made_on))
            resample_df = plot_df.resample("D")["amount"].sum().reset_index()
            sns.lineplot(
                x=resample_df.made_on.astype(str),
                y=resample_df.amount,
                color=color(categories.index(category)),
                label=category,
            )
        plt.xticks(rotation=90)
        st.pyplot()


def plot_historical_timeline(year, month, input_dict, historical_option):
    sns.set()
    plt.figure(figsize=(10, 4))
    current_df = pd.read_csv(os.path.join(FINAL_PATH, "expense_{}_{}.csv".format(year, month)))
    categories = list(input_dict.keys())
    previous_dfs = {}
    for filename in os.listdir(FINAL_PATH):
        if filename.startswith('expense_') and