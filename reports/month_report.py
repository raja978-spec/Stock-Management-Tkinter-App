from model_connection import *
import matplotlib.pyplot as plt
from project_config import *
import os

def generate_monthly_sales_report():
        plt.cla()
        # SALES BY MONTH
        x=[]
        y=[]
        
        result = run_query(f"SELECT month(sales_date), COUNT(memo_id) FROM sales WHERE year(sales_date) = '2025'  GROUP BY month(sales_date) LIMIT 100") 
        for i in result:
            x.append(i[0])
            y.append(i[1])
        
        for i in range(len(x)):
            plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')

        plt.title('2025 Monthly sales report')
        plt.xlabel('Months')
        plt.ylabel('Sales')
        
        plt.bar(x=x, height=y, color=background_color)
        plt.savefig('month_sales.jpg')
        plt.close()