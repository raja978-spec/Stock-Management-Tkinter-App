from model_connection import *
import matplotlib.pyplot as plt
from project_config import *

def generate_year_sales_report():
    # SALES BY YEAR
    plt.cla() # Clear current axis
    year_sales = run_query('SELECT YEAR(sales_date),Count(memo_id) FROM sales GROUP BY YEAR(sales_date)')
    x=[]
    y=[]
    for i in year_sales:
                x.append(str(i[0]))
                y.append(i[1])
    plt.title('Sales By Year')
    plt.xlabel('Year')
    plt.ylabel('Sales')
    plt.bar(x=x, height=y, color=background_color)
    for i in range(len(x)):
        plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')
    plt.savefig('year_sales.jpg')
    plt.close()  # Important: closes the figure and frees memory