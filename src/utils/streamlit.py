import matplotlib.pyplot as plt
import pandas as pd
import numpy as np
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


def plot_historical_timeline(year, month, option, input_dict):
    sns.set()
    plt.figure(figsize=(10, 4))
    current_df = pd.read_csv(os.path.join(FINAL_PATH, "expense_{}_{}.csv".format(year, month)))
    categories = list(input_dict.keys())
    previous_dfs = {}
    for filename in os.listdir(FINAL_PATH):
        file_type, file_year, file_month = filename.split("_")
        if (file_type == "expense" and file_year == year and file_month < month) or (
            file_type == "expense" and file_year < year
        ):
            previous_dfs["{}-{}".format(year, month)] = pd.read_csv(
                os.path.join(FINAL_PATH, "expense_{}_{}.csv".format(file_year, file_month))
            )
    if len(option) == 0:
        dates = []
        values = []
        dates.append("{}-{}".format(year, month))
        values.append(current_df["amount"].sum())
        for key, previous_df in previous_dfs.items():
            dates.append(key)
            values.append(previous_df["amount"].sum())
        dates, values = np.array(dates), np.array(values)
        index = np.argsort(dates)
        sns.lineplot(x=dates[index], y=values[index], label="overall")
        plt.xticks(rotation=90)
        st.pyplot()
    else:
        for category in option:
            dates = []
            values = []
            current_category_df = current_df[current_df["true_category"] == category].copy().reset_index(drop=True)
            dates.append("{}-{}".format(year, month))
            values.append(current_category_df["amount"].sum())
            for key, previous_df in previous_dfs.items():
                previous_category_df = (
                    previous_df[previous_df["true_category"] == category].copy().reset_index(drop=True)
                )
                dates.append(key)
                values.append(previous_category_df["amount"].sum())
                dates, values = np.array(dates), np.array(values)
                index = np.argsort(dates)
                sns.lineplot(x=dates[index], y=values[index], color=color(categories.index(category)), label=category)
        plt.xticks(rotation=90)
        st.pyplot()


def display_dataframe(input_df, option, sort_option, order_option):
    if sort_option == "Date":
        sort_value = "made_on"
    elif sort_option == "Name":
        sort_value = "description"
    elif sort_option == "Amount":
        sort_value = "amount"
    else:
        raise ValueError("sort_option is not correct")
    if order_option == "Ascending":
        ascending = True
    else:
        ascending = False
    if len(option) == 0:
        st.table(input_df.sort_values(sort_value, ascending=ascending))
    else:
        st.table(input_df[input_df["true_category"] == option].sort_values(sort_value, ascending=ascending))
