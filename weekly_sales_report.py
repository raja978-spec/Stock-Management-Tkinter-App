import matplotlib.pyplot as plt
from model_connection import *
from project_config import *

def generate_weekly_sales_report():
    results = run_query('select Week(sales_date), count(memo_id) from sales where Year(sales_date) = "2025" group by Week(sales_date)')
    x=[]
    y=[]
    for data in results:
        x.append(str(data[0]))
        y.append(data[1])
    
    plt.cla()
    plt.figure(figsize=(10,5))
    plt.title('2025 Weekly Sales Report')
    plt.xlabel('Weeks')
    plt.ylabel('Sales')
    plt.bar(x=x, height=y, color=background_color)
    for i in range(len(x)):
            plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')
    plt.savefig('weekly_sales_report.jpg')
    plt.close()

