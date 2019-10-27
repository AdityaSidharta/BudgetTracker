import streamlit as st
import seaborn as sns
import matplotlib.pyplot as plt
from emoji import emojize


def plot_category(input_df, input_dict):
    sns.set()
    plt.figure(figsize=(10, 4))
    plot_df = input_df.copy()
    sns.barplot(x='amount', y='true_category', data=plot_df)
    plt.tight_layout()
    st.pyplot()


def display_category(input_df, input_dict):
    df = input_df.copy()
    df['amount'] = df['amount'].apply(lambda x: "S$ {:.2f}".format(x))
    df.columns = ['CATEGORY', 'AMOUNT']
    st.table(df)

def plot_timeline(input_df, option):
    sns.set()
    plt.figure(figsize=(10, 4))
    plot_df = input_df.copy()
    if len(option) == 0:
        
