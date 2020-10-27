import pandas as pd 
import matplotlib.pyplot as plt
#import seaborn as sns

class DataVisualization:
    def __init__(self, df):
        self.df = df
        self.exit = True
        self.choices = {
		"1": self.belgium_house,
		"2": self.wallonia_house,   
		"3": self.flanders_house,
		"4": False
		}
    def display(self):
        print("""
            Visualizations:
            1. The most expensive and the cheapest house by location in Belgium
            2. The most expensive and the cheapest house by location in Wallonia 
            3. The most expensive and the cheapest house by location in Flanders
            4. Quit
            """)
        while self.exit == True: 
            choice = input('please enter the number of your request: ')
            action = self.choices.get(choice, "Your choice is not a valid choice")
            action()

    def avarage_df(self, house_filtered):
        by_locality = house_filtered.groupby('locality')['price'].mean()
        by_local = pd.DataFrame(by_locality)
        locality_max = by_local[by_local.price==by_local.price.max()].index[0]
        locality_min = by_local[by_local.price==by_local.price.min()].index[0]
        print('The avarage price of houses in the most expensive municipalities: ', by_local.price.max(), 'in', locality_max)
        print('The avarage price of houses in the cheapest municipalities:', by_local.price.min(), 'in', locality_min)

        by_local.sort_values(by='price', ascending=False)
        max_by_local = by_local[:8]
        min_by_local = by_local[-8:]

        plt.figure(figsize=(15,4))

        # Create plot axes for the first line plot
        plt.subplot(1, 2, 1) 

        plt.bar(max_by_local.index, max_by_local.price)
        plt.xlabel('Location of Houses', fontsize=15)
        plt.ylabel('Price of Houses', fontsize=15)
        plt.title('The Most Expensive House', fontsize=20)

        # Create plot axes for the second line plot
        plt.subplot(1, 2, 2) 

        plt.bar(min_by_local.index, min_by_local.price)
        plt.xlabel('Location of Houses', fontsize=15)
        plt.ylabel('Price of Houses', fontsize=15)
        plt.title('The Cheapest House', fontsize=20)

        plt.savefig("pictures/The most expensive and the cheapest price of 3-room house by location in Belgium.png")

        # Display the plot
        plt.show()


    def median_df(self, house_filtered):
        by_locality = house_filtered.groupby('locality')['price'].median()
        by_local = pd.DataFrame(by_locality)
        locality_max = by_local[by_local.price==by_local.price.max()].index[0]
        locality_min = by_local[by_local.price==by_local.price.min()].index[0]
        print('The median price of houses in the most expensive municipalities: ', by_local.price.max(), 'in', locality_max)
        print('The median price of houses in the cheapest municipalities:', by_local.price.min(), 'in', locality_min)

    def per_square(self, house_filtered):
        by_locality1 = house_filtered.groupby('locality')['price'].mean()
        by_locality2 = house_filtered.groupby('locality')['area'].mean()
        by_local1 = pd.DataFrame(by_locality1)
        by_local2 = pd.DataFrame(by_locality2)

        # Merge the DataFrames: o2o
        o2o = pd.merge(left=by_local1, right=by_local2, left_on='locality', right_on='locality')
        o2o['price_per_m2'] = o2o.price/o2o.area
        locality_max = o2o[o2o.price_per_m2==o2o.price_per_m2.max()].index[0]
        locality_min = o2o[o2o.price_per_m2==o2o.price_per_m2.min()].index[0]
        print('The avarage price of square of houses in the most expensive municipalities : ', o2o.price_per_m2.max(), 'in', locality_max)
        print('The avarage price of square of houses in the cheapest municipalities:', o2o.price_per_m2.min(), 'in', locality_min)

    def belgium_house(self):    

        house_filtered = self.df.loc[(self.df.rooms_number==3) & (self.df.house_is==True)]
        print('The most expensive and the cheapest price of 3-room house by location in Belgium')
        self.avarage_df(house_filtered)
        self.median_df(house_filtered)
        self.per_square(house_filtered)

    def wallonia_house(self):

        house_filtered = self.df.loc[(self.df.rooms_number==3) & (self.df.house_is==True) & (self.df.region=='Wallonia')]
        print('The most expensive and the cheapest price of 3-room house by location in Wallonia')
        self.avarage_df(house_filtered)
        self.median_df(house_filtered)
        self.per_square(house_filtered)

    def flanders_house(self):
        house_filtered = self.df.loc[(self.df.rooms_number==3) & (self.df.house_is==True) & (self.df.region=='Flanders')]
        print('The most expensive and the cheapest price of 3-room house by location in Flanders')
        self.avarage_df(house_filtered)
        self.median_df(house_filtered)
        self.per_square(house_filtered)

    def quit(self):
    	print("Thank you for using our Visualizations.")
    	self.exit = False
    	return self.exit    	

