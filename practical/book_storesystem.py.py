import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

class Bookstore:


    def __init__(self):
        try:
            self.inventory = pd.read_csv('inventory.csv')
        except:

            self.inventory = pd.DataFrame(columns=['author','title','genre','price','quantity'])
        try:
            self.sales = pd.read_csv('sales.csv')
        except:
            self.sales = pd.DataFrame(columns=['date','title','sold quantity','total revenue'])

    def add_book(self, title, author, genre, price, qty):
        if price <= 0 or qty < 0: #
            print("price and quatity must be more then 0")
        else:
             
             new_row = pd.DataFrame([[author,title,genre,price,qty]], columns=self.inventory.columns)
             self.inventory = pd.concat([self.inventory,new_row],ignore_index=True)
             self.inventory.to_csv('inventory.csv',index=False)
             print("book added")


    def update_inventory(self, title, qty):
        if title in self.inventory['title'].values:
            self.inventory.loc[self.inventory['title']==title,'quantity'] = qty
            self.inventory.to_csv('inventory.csv',index=False)
            print("inventory updated")

        else:
            print("book not found")

    def record_sales(self, title, qty):
        if title in self.inventory['Title'].values:
            stock = self.inventory.loc[self.inventory['title']==title,'quantity'].values[0]
            price = self.inventory.loc[self.inventory['title']==title,'price'].values[0]
            if stock >= qty:


                
                self.inventory.loc[self.inventory['Title']==title,'Quantity'] -= qty
                
                today = pd.Timestamp.now().strftime('%Y-%m-%d')
                new_sale = pd.DataFrame([[today,title,qty,qty*price]], columns=self.sales.columns)
                self.sales = pd.concat([self.sales,new_sale],ignore_index=True)
                self.inventory.to_csv('inventory.csv',index=False)
                self.sales.to_csv('sales.csv',index=False)
                print("sale recorded")
            else:
                print("not enough stock")
        else:
            print("book not found")

    def generate_report(self):
        print(self.inventory.describe())
        print(self.sales.describe())

        if not self.sales.empty:
            self.sales['date'] = pd.to_datetime(self.sales['date'])
            self.sales['month'] = self.sales['date'].dt.to_period('m')

            self.sales.groupby('Title')['Sold Quantity'].sum().plot(kind='bar')
            plt.title('Total Sales per Book')
            plt.show()

            self.sales.groupby('Month')['Sold Quantity'].sum().plot(marker='o')
            plt.title('Monthly Sales Trend')
            plt.show()

            merged = pd.merge(self.sales,self.inventory[['Title','Genre']],on='Title',how='left')
            merged.groupby('Genre')['Total Revenue'].sum().plot(kind='pie',autopct='%1.1f%%')
            plt.title('Revenue Share by Genre')
            plt.ylabel('')
            plt.show()

            merge_price = pd.merge(self.sales,self.inventory[['title','price']],on='title',how='left')
            grp = merge_price.groupby('Title').agg({'price':'mean','sold quaantity':'sum'})
            sns.heatmap(grp.corr(),annot=True,cmap='coolwarm') #
            plt.title('Price vs Sales Volume Correlation')
            plt.show()

            print("Mean Price:",np.mean(grp['price']))
            print("Max Price:",np.max(grp['price']))
            print("Min Price:",np.min(grp['  price']))
            print("Mean Sales:",np.mean(grp['sold Quantity']))
            print("Max Sales:",np.max(grp['sold Quantity']))
            print("Min Sales:",np.min(grp['sold Quantity']))

if __name__ == '__main__':
    bs = Bookstore()
    while True:
        print("1.add ")
        print("2.update ")
        print("3.sell")
        print("4.report ")
        print("5.exit")

        ch = input("choice: ")
        if ch=='1' :
            t = input("title: ")
            a = input("author: ")
            g = input("genre: ")
            p = float(input("price: "))
            q = int(input("quantity: "))
            bs.add_book(t,a,g,p,q)
        elif ch=='2':
            t = input("title: ")
            q = int(input("quantity: "))
            bs.update_inventory(t,q)

        elif ch=='3':
            t = input("title: ")
            q = int(input("quantity: "))
            bs.record_sales(t,q)
        elif ch=='4':
            bs.generate_report()
        elif ch=='5':
            break
        else:
            print("invalid ")


