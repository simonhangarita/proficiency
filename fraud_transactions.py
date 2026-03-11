import pandas as pd

"""
Tienes este dataset de transacciones. Escribe el codigo Python que usarias para responder las preguntas:
1. Cual es la tasa de fraude general del dataset?
2. Cual es el monto promedio de transacciones fraudulentas vs. legitimas?
3. Que paises de IP tienen mayor proporcion de fraude?
4. Crea una nueva columna high_risk que sea True si el monto es mayor a $500 y la cuenta tiene menos de 30 dias. Cuantas transacciones son high_risk
"""
data = {
    'transaction_id': range(1, 11),
    'user_id': [101, 102, 101, 103, 104, 102, 105, 103, 101, 106],
    'amount': [850, 120, 430, 95, 1200, 75, 300, 88, 920, 60],
    'country_ip': ['NG','US','US','US','RO','US','US','US','NG','US'],
    'account_age_days': [2, 730, 2, 7, 1, 730, 180, 7, 2, 365],
    'is_fraud': [1, 0, 1, 0, 1, 0, 0, 0, 1, 0]
}

df = pd.DataFrame(data)

#We will create a function to calculate the rate of a column in a dataframe so that we can reuse it for several questions
def calculate_rate(df:pd.DataFrame, column:str)->int:
    #We will asume for this calculation thet the column is binary and that it exist in the dataframe
    try:
        rate= len(df[df[column]==True])/len(df)
    except Exception as e:
        print(f"An error occurred: {e}")
        return -1
    return rate
if __name__ == "__main__":
    # 1. Tasa de fraude general: To calculate this, we would neet to know that
    #  the Fraud rate is equeal to the number of fraudulent transactions divided by the total number of transactions.
    fraud_rate=calculate_rate(df, 'is_fraud')
    print(f"Fraud rate: {fraud_rate:.2%}")
    #2.¿Cual es el monto promedio de transacciones fraudulentas vs. legítimas?
    avg_fraud_amount=df[df['is_fraud']==1]['amount'].mean()
    avg_legit_amount=df[df['is_fraud']==0]['amount'].mean()
    print(f'Average amount of fraudulent transactions: ${avg_fraud_amount:.2f}')
    print(f'Average amount of legitimate transactions: ${avg_legit_amount:.2f}')
    #3.¿Que paises de IP tienen mayor proporción de fraude?
    def agregate_fraud_proportion(group:pd.Series):
        return group.sum() / len(group)*100
    country_fraud_proportion=df.groupby('country_ip').agg(fraud_proportion=("is_fraud", agregate_fraud_proportion)).reset_index().sort_values(by='fraud_proportion', ascending=False)
    #country_fraud_proprtion=country_fraud_proportion.rename(columns={'is_fraud':'fraud_proportion'})
    print("Fraud proportion by country:")
    print(country_fraud_proportion)
    #4.Crea una nueva columna high_risk
    df['high_risk'] = (df["account_age_days"] < 30) & (df["amount"] > 500)
    print(f"Number of high risk transactions: {df['high_risk'].sum()}")
    print(df)