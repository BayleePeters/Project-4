#import required modules
import pandas as pd
import numpy as np

#create a new data frame from CSV file for 2016 purchase prices
purchasePrices = pd.read_csv("2016PurchasePrices.csv")
purchasePrices = purchasePrices.drop_duplicates().reset_index(drop=True)

#create a new data frame from CSV file for beginning inventory
begInv = pd.read_csv("D:\ACC470\BegInvFINAL.csv")

#aggregate records in beginning inventory data frame by grouping by brand
begInv = begInv.groupby("Brand").sum()
begInv = begInv.reset_index()

#merge begInv and purchasePrices data frames on Brand
merged1 = pd.merge(purchasePrices,begInv, on = "Brand", how = "outer")

#create a new column in the merged data frame for BegExtCost
merged1["Beg Ext Cost"] = merged1["onHand"] * merged1["PurchasePrice"]

#create a new data frame that only contains beginning inventory onhand, extended cost, and brand
begInv = merged1[["onHand","Beg Ext Cost", "Brand"]]

#rename column header from onHand to BegQty
begInv = begInv.rename(columns={"onHand":"BegQty"})

#Display data frame to ensure it looks as expected
print("This is beginning iventory")
print(begInv)

#create a new data frame from CSV file for ending inventory
endInv = pd.read_csv("D:\ACC470\EndInvFINAL.csv")

#aggregate records in ending inventory data frame by grouping by brand
endInv = endInv.groupby("Brand").sum()
endInv = endInv.reset_index()

#merge endInv and purchasePrices data frames on Brand
merged2 = pd.merge(purchasePrices,endInv, on = "Brand", how = "outer")

#create a new column in the merged data frame for EndExtCost
merged2["End Ext Cost"] = merged2["onHand"] * merged2["PurchasePrice"]

#create a new data frame that only contains ending inventory onhand, extended cost, and brand
endInv = merged2[["onHand","End Ext Cost", "Brand"]]

#rename column header from onHand to EndQty
endInv = endInv.rename(columns={"onHand":"EndQty"})

#Display data frame to ensure it looks as expected
print("This is ending inventory")
print(endInv)

#create a new data frame from CSV file for sales
sales = pd.read_csv("D:\ACC470\SalesFINAL.csv")

#aggregate records in sales data frame by grouping by brand
sales = sales.groupby("Brand").sum()
sales = sales.reset_index()

#create a new data frame that only contains sales dollars and brand
sales = sales[["SalesDollars","Brand"]]

#Display data frame to ensure it looks as expected
print("This is sales")
print(sales)

#merge the beginning and ending inventory data frames and name this new data frame turnover
turnover = pd.merge(begInv, endInv, on = "Brand", how = "outer")

#merge the turnover data frame and the sales data frame ; keep the same name turnover
turnover = pd.merge(turnover, sales, on = "Brand", how = "outer")

#create a new column in the turnover data frame for turnoverRatio
turnover["turnoverRatio"] = (turnover["SalesDollars"] * int(2)) / (turnover["End Ext Cost"] + turnover["Beg Ext Cost"])

#create a new data frame that only contains brand, description, and classification
descriptions = purchasePrices[["Brand", "Description", "Classification"]]

#merge the turnover data frame and descriptions data frame ; keep the same name turnover
turnover = pd.merge(turnover, descriptions, on = "Brand", how = "outer")

#create a new data frame that only contains brand, description, ending inventory, ending extention cost, classification, and turnoverratio
turnover = turnover[["Brand","Description", "Classification", "EndQty", "End Ext Cost", "turnoverRatio"]]

#display the turnover data frame to ensure it looks as expected
print("This is turnover")
print(turnover)

#create a new data frame from CSV file for purchases
purchases = pd.read_csv("D:\ACC470\PurchasesFINAL.csv")
purchases = purchases.groupby("Brand").sum()
purchases = purchases.reset_index()

#create a new data frame that only contains brand and quantity
purchases = purchases[["Brand","Quantity"]]

#merge the turnover data frame and descriptions data frame ; keep the same name turnover
turnover = pd.merge(turnover, purchases, on = "Brand", how = "outer")

#rename column header from Quantity to Purch Qty
turnover = turnover.rename(columns={"Quantity":"Purch Qty"})

#change na values to zero
turnover = turnover.fillna(0)

#Display data frame to ensure it looks as expected
print("This is turnover including purchased quantity")
print(turnover)

#extract data from turnover data frame that has turnover ratio of zero ; call this data frame obsolete
obsolete = turnover[turnover["turnoverRatio"] == 0]

#extract data from obsolete data frame that had no purchase quantity
obsolete = obsolete[obsolete["Purch Qty"] == 0]

#extract data from obsolete data frame that is classified as wine
obsolete = obsolete[obsolete["Classification"] == 2]

#extract data from obsolete data frame that has an ending inventory greater than 0
obsolete = obsolete[obsolete["EndQty"] > 0]

#create a new data frame that only contains brand, description, ending inventory, ending extention cost, classification, and turnoverratio
obsolete = obsolete[["Brand","Description", "Classification", "EndQty", "End Ext Cost", "turnoverRatio"]]

#create a new data frame that only contains brand, description, ending inventory, ending extention cost, and classification
obsolete = obsolete[["Brand","Description", "Classification", "EndQty", "End Ext Cost" ]]

#aggregate records in obsolete data frame by grouping by brand
obsolete = obsolete.groupby("Brand").sum()
obsolete = obsolete.reset_index()

#print obsolete data frame
print("This is obsolete")
print(obsolete)

#display the cost of ending inventory records in the obsolete data frame
total = obsolete["End Ext Cost"].sum()
print ("The total ending inventory is " + str(total))


