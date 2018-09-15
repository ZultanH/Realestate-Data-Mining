import csv
import os
import statistics

class RowNotFound(Exception):
    pass

class Purchase:
    def __init__(self, *args, **kwargs):
        self.longitude  = float(kwargs['longitude'])
        self.latitude   = float(kwargs['latitude'])
        self.price      = float(kwargs['price'])
        self.sale_date  = kwargs['sale_date']
        self.type       = kwargs['type']
        self.sq__ft     = int(kwargs['sq__ft'])
        self.baths      = int(kwargs['baths'])
        self.beds       = int(kwargs['beds'])
        self.state      = kwargs['state']
        self.zip        = kwargs['zip']
        self.city       = kwargs['city']
        self.street     = kwargs['street']

    @staticmethod
    def create_from_dict(lookup):
        return Purchase(
            **lookup
        )

class Data:
    def __init__(self, row):
        self.row = row
    
    @classmethod
    def findRow(cls, house):
        with open("./houses.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                if house.lower() == "{},{}".format(row['street'], row['city']).lower():
                    return row
        raise RowNotFound()

    def getStreet(self):
        return self.row['street']
    
    def getCity(self):
        return self.row['city']
    
    def getZip(self):
        return self.row['zip']
    
    def getState(self):
        return self.row['state']
    
    def getBeds(self):
        return self.row['beds']
    
    def getBaths(self):
        return self.row['baths']
    
    def getSqrFT(self):
        return self.row['sq__ft']
    
    def getType(self):
        return self.row['type']
    
    def getSaleDate(self):
        return self.row['sale_date']
    
    def getPrice(self):
        return int(self.row['price'])
    
    def getLatitude(self):
        return self.row['latitude']
    
    def getLongitude(self):
        return self.row['longitude']
    
    @staticmethod
    def getData():
        purchases = []
        with open("./houses.csv") as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                p = Purchase.create_from_dict(row)
                purchases.append(p)
        return purchases
    
    @classmethod
    def getMostExpensive(cls):
        data = cls.getData()
        data.sort(key=lambda p: p.price)
        return data[-1]
    
    @classmethod
    def getLeastExpensive(cls):
        data = cls.getData()
        data.sort(key=lambda p: p.price)
        return data[0]
    
    @classmethod
    def getAveragePrice(cls):
        data = cls.getData()
        prices = [p.price for p in data]
        return statistics.mean(prices)
    
    @classmethod
    def Query(cls, *args, **kwargs):
        search_type = kwargs['search_type']
        value       = kwargs['value']
        data        = cls.getData()
        return [p for p in data if p.__dict__[search_type] == value]
    
if __name__ == "__main__":
    query = Data.Query(search_type='beds', value=2)
    for p in query:
        print(p.price, p.beds)
