from model_connection import run_query
import matplotlib.pyplot as plt
from project_config import *
import os

def generate_item_wise_sales():
        plt.cla()
        # SALES BY MONTH
        x=[]
        y=[]
        
        result = run_query(f"SELECT item_name, COUNT(memo_id) FROM sales GROUP BY item_name ORDER BY COUNT(memo_id) DESC") 
        for i in result:
            x.append(i[0])
            y.append(i[1])
        
        for i in range(len(x)):
            plt.text(x[i], y[i], str(y[i]), ha='center', va='bottom')

        plt.title('Item wise sales')
        plt.xlabel('Item name')
        plt.ylabel('Sales')
        
        plt.bar(x=x, height=y, color=background_color)
        plt.xticks(rotation=15, ha='right') 
        #plt.savefig('item_wise_sales.jpg')
        plt.show()
        plt.close()
generate_item_wise_sales()