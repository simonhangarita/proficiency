from typing import List, Dict,Any,Tuple
import pandas as pd
import numpy as np
from datetime import datetime as dt
def clean_messy_dataset(dataset:List[Dict[Any,Any]])->List[Dict[Any,Any]]:
    """
    remove duplicate transaction_ids, fill missing amounts with 0, and return the list sorted by date descending.
    Args:
        dataset (List[Dict[Any,Any]]): Dataset with messy data
    Returns:
        List[Dict[Any,Any]]): Dataset without repeated values or null values in the amount field
    """
    values_without_repetition=set()
    clean_dataset=[]
    for row_data in dataset:
        if row_data["transaction_id"] not in values_without_repetition:
            values_without_repetition.add(row_data["transaction_id"])
            new_row=row_data.copy()
            if new_row['amount'] is None:
                new_row['amount']=0
            clean_dataset.append(new_row)
    clean_dataset=sorted(clean_dataset,key=lambda x:x["created_at"],reverse=True)
    return clean_dataset
def group_and_aggregate(dataset:Dict[str,List[Any]])->pd.DataFrame:
    """
    Using the sales data, compute: (1) total revenue per category, (2) number of orders per category, 
    (3) average order value per category. Print results sorted by total revenue descending.
    Args:
        dataset (Dict[str,List[Any]]): dataset containing sales data
    Returns:
        pd.DataFrame: dataset in DataFrame format containing the category, total revenue, number of orders abd average order value
    """
    df=pd.DataFrame(dataset)
    total_revenue = df.groupby('category')['revenue'].sum().reset_index().rename(columns={'revenue':'total_revenue'})
    #We create a column that we will only use to group and find the number of total orders
    df['number_of_orders']=1
    number_orders=df.groupby('category')['number_of_orders'].sum().reset_index()
    average_value=df.groupby('category')['revenue'].mean().reset_index().rename(columns={'revenue':'average_order_value'})
    df_group=total_revenue.merge(number_orders,on='category')
    df_group=df_group.merge(average_value,on='category')
    df_group=df_group.sort_values(by='total_revenue',ascending=False)
    return df_group
def top_n_users_by_spend(dataset:Dict[str,List[Any]])->pd.DataFrame:
    """
    From the transactions DataFrame: (1) find the top 3 users by total spend, 
    (2) compute the mean and standard deviation of total spend across all users, 
    (3) add a column "segment"  label users whose total spend is more than 1 std dev above the mean as "high value", the rest as "standard"
    Args:
         dataset (Dict[str,List[Any]]): dataset containing transactions data
    Returns:
        pd.DataFrame: dataframe containing the new column that flags outliers
    """
    df=pd.DataFrame(dataset)
    total_spend_user=df.groupby("user_id")["amount"].sum().reset_index().sort_values(by='amount',ascending=False)
    #We show the top 3 users by total spend and add a new column to flag the top 3
    top_3_spend_user=total_spend_user.head(3)
    print(top_3_spend_user)
    total_spend_user['top 3 spend user']=total_spend_user.apply(lambda x:1 if x["user_id"] in top_3_spend_user["user_id"] else 0,axis=1)
    #Compute the mean and std across all users
    mean=total_spend_user["amount"].mean()
    std=total_spend_user["amount"].std()
    total_spend_user["segment"]=total_spend_user.apply(lambda x:"high value" if x['amount']>mean+std else "standard",axis=1)
    return total_spend_user
def month_retention_cohort(dataset:Dict[str,List[Any]])->pd.pivot:
    """
    From the purchase dataframe we will build a cohort to determine client retention after the first buy month, 
    Args:
         dataset (Dict[str,List[Any]]): dataset containing purchases data
    Returns:
        pd.pivot: pivot table with the client retention by cohort
    """
    #First we need to find the cohorts which are going to be determined by the first month they purchase
    df=pd.DataFrame(dataset)
    #We will create another column based on the column purchased_date converting it to  a datetime column which allows us to manipulate date format
    df["purchase_datetime"] = pd.to_datetime(df["purchase_date"])
    #And we also create a column for the month which we would use for the cohort
    df["month"] = df["purchase_datetime"].dt.to_period("M").dt.to_timestamp()
    cohort_group=df.groupby('user_id')['month'].min().reset_index().rename(columns={'month':'first_month'})
    df = df.merge(cohort_group, on="user_id")
    #Now we will compute the month since the first purchase for each purchase
    df["months_since_first"] = ((df["month"].dt.year - df["first_month"].dt.year) * 12 +
                                (df["month"].dt.month - df["first_month"].dt.month)
                                )
    #Build the cohort retention rates using pivot table
    pivot_cohort=df.groupby(['months_since_first','first_month'])['user_id'].nunique().reset_index().pivot(index='first_month',
                                                                                                           columns='months_since_first',
                                                                                                          values='user_id')
    pivot_size=pivot_cohort[0]
    retention_cohort=pivot_cohort.divide(pivot_size,axis=0).round(2)*100
    
    return retention_cohort

data = {
    "user_id":       [1,2,3,1,2,4,5,3,1,5,2,4],
    "amount":        [75,120,200,50,90,300,60,180,110,95,40,85],
    "purchase_date": ["2024-01-08","2024-01-15","2024-01-22",
                      "2024-02-05","2024-02-18","2024-01-30",
                      "2024-02-10","2024-02-25","2024-03-22",
                      "2024-03-15","2024-03-08","2024-03-20"]
}
print(month_retention_cohort(data))