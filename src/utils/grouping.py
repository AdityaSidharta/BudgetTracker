import pandas as pd

MAX_CATEGORY = 5
MAX_TRANSACTION = 5


def get_category(input_df):
    df = input_df.copy()
    category_df = df.groupby('true_category')['amount'].sum().reset_index().sort_values('amount').reset_index(
        drop=True)
    n_df = len(category_df)
    if n_df <= MAX_CATEGORY:
        result_df = category_df
    else:
        top_df, others_df = category_df.loc[:MAX_CATEGORY-1, :], category_df.loc[MAX_CATEGORY-1:, :]
        sum_others_df = pd.DataFrame({
            'true_category': ['OTHER CATEGORIES'],
            'amount': [others_df.amount.sum()]
        })
        result_df = top_df.append(sum_others_df).reset_index(drop=True)
    return result_df
