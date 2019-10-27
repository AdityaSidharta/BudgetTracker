import os
import fire

from src.utils.directory import CONFIG_YAML_PATH, EXPENSE_YAML_PATH, INCOME_YAML_PATH, FINAL_PATH
from src.utils.transactions import load_transaction, get_accounts, remove_accounts, remove_keywords, \
    map_category, map_description, map_type, get_emoji, get_filename
from src.utils.io import load_yaml

# TODO: Add logger for process
def main(year: int = None, month: int = None):
    expense_dict = load_yaml(EXPENSE_YAML_PATH)
    config_dict = load_yaml(CONFIG_YAML_PATH)
    income_dict = load_yaml(INCOME_YAML_PATH)

    full_df = load_transaction(year, month)
    accounts = get_accounts(year, month) + config_dict['FILTER_ACCOUNTS']

    full_df = full_df[['id', 'account_id', 'made_on', 'amount', 'description', 'category', 'type']]
    full_df = remove_accounts(full_df, accounts)
    full_df = remove_keywords(full_df, config_dict['KEYWORD_ACCOUNTS'])

    expense_df = full_df[full_df["amount"] < 0.0].copy().reset_index(drop=True)
    expense_df['true_category'] = 'OTHER_EXPENSES'
    expense_df = map_type(expense_df)
    expense_df = map_category(expense_df, expense_dict)
    expense_df = map_description(expense_df, expense_dict)
    expense_df = get_emoji(expense_df, expense_dict)

    income_df = full_df[full_df["amount"] > 0].copy().reset_index(drop=True)
    income_df['true_category'] = 'OTHER_INCOME'
    income_df = map_type(income_df)
    income_df = map_category(income_df, income_dict)
    income_df = map_description(income_df, income_dict)
    income_df = get_emoji(income_df, income_dict)

    expense_path = os.path.join(FINAL_PATH, get_filename('expense', year, month))
    expense_df.to_csv(expense_path, index=False)

    income_path = os.path.join(FINAL_PATH, get_filename('income', year, month))
    income_df.to_csv(income_path, index=False)


if __name__ == "__main__":
    fire.Fire(main)
