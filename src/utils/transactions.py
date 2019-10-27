import os
import pandas as pd
from src.utils.directory import RAW_PATH


def get_accounts(year, month):
    accounts = []
    for filename in os.listdir(RAW_PATH):
        if filename.endswith("_{}_{}.csv".format(year, month)):
            index = filename.index("_{}_{}.csv".format(year, month))
            account = filename[:index].split(' ')[0]
            accounts.append(account)
    return accounts


def load_transaction(year, month):
    list_df = []
    for filename in os.listdir(RAW_PATH):
        if filename.endswith("_{}_{}.csv".format(year, month)):
            list_df.append(pd.read_csv(os.path.join(RAW_PATH, filename)))
    return pd.concat(list_df, axis=0, ignore_index=True)


def remove_accounts(input_df, accounts):
    df = input_df.copy()
    for account in accounts:
        df = df[~df.description.apply(lambda x: account in x)]
    return df.reset_index(drop=True)


def remove_keywords(input_df, keywords):
    df = input_df.copy()
    for keyword in keywords:
        df = df[~df.description.apply(lambda x: keyword in x)]
    return df.reset_index(drop=True)


def get_filename(account_name, year, month):
    return "{}_{}_{}.csv".format(account_name, year, month)


def map_type(input_df):
    df = input_df.copy()
    df.loc[df['type'] == 'INT', 'true_category'] = 'INTEREST'
    df.loc[df['type'] == 'ATINT', 'true_category'] = 'INTEREST'
    df.loc[df['type'] == 'AWL', 'true_category'] = 'CASH'
    return df


def map_category(input_df, transaction_dict):
    df = input_df.copy()
    for key, items in transaction_dict.items():
        true_category = key
        categories = items['mapping']
        for category in categories:
            df.loc[df['category'] == category, 'true_category'] = true_category
    return df


def map_description(input_df, transaction_dict):
    df = input_df.copy()
    for key, items in transaction_dict.items():
        true_category = key
        keywords = items['description']
        for keyword in keywords:
            df.loc[df['description'].apply(lambda x: keyword in x), 'true_category'] = true_category
    return df

def get_emoji(input_df, transaction_dict):
    df = input_df.copy()
    df['emoji'] = ""
    for key, items in transaction_dict.items():
        true_category = key
        emoji = items['emoji']
        df.loc[df['true_category'] == true_category, 'emoji'] = emoji
    return df