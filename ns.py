'''
ns.py
by Sofia Lee

This program reports the best NS subscription to get based on how many
trips will be taken that month and then sorts them in a table from
cheapest to most expensive.
'''

from sys import argv
from tabulate import tabulate
import pandas as pd


class Subscription:
    '''
    Each Subscription has the following:
        A name
        A cost
        A multiplier for peak hours
        A multiplier for offpeak hours
       
        A function for getting the total cost for a given trip and frequency
    '''
    def __init__(self, name, cost, daluren, spits):
        self.name = name
        self.cost = cost
        self.spits = spits
        self.daluren = daluren

    def get_cost(self, distance_cost, offpeak, peak, weeks_per_month):
        multiplier = offpeak * self.daluren + peak * self.spits
        return self.cost + distance_cost * multiplier * weeks_per_month

def load_data():
    stations = pd.read_csv('stations.csv', na_filter=False)
    stations = {x:y for x, y in zip(stations['code'].tolist(),
                                    stations['name_long'].tolist())}

    distances = pd.read_csv('distances.csv', na_filter=False)
    distances = distances.set_index('Station')
    distances = distances.to_dict()
    
    prices = pd.read_csv('prices.csv')
    prices = prices.to_dict()

    return stations, distances, prices

def station_check(input_string, stations):
    station_found = False
    station_names = {stations[s]:s for s in stations}

    while not station_found:
        station_req = input(input_string)

        if station_req in stations:
            return station_req
        elif station_req in station_names:
            return station_names[station_req]
        else:
            print('Station not found! Please input a valid station.')
           

def main():
    stations, distances, prices = load_data()
    
    # Get user input
    origin = station_check('Origin station. ', stations)
    destination = station_check('Destination station. ', stations)
    distance = int(distances[origin][destination])

    print(f'The distance between {stations[origin]} and {stations[destination]} is {distance} rate units.')

    if distance > 200:
        distance = 200

    price = float(prices['full'][distance])

    offpeak = int(input('Off-peak trips per week. '))
    peak = int(input('Peak hour trips per week. '))
    month = int(input('Weeks a month. '))

    rides = month*(offpeak+peak)

    # define the subscriptions
    sub = [Subscription('None', 0, 1, 1),
        Subscription('Dal Voordeel', 5.1, .6, 1),
        Subscription('Altijd Voordeel', 24.2, .6, .8),
        Subscription('Dal Vrij', 107.9, 0, 1),
        Subscription('Altijd Vrij', 362.4, 0, 0)]
       
    # Only add the traject if it applies
    if distance < 81:
        traject_prices = {}
        with open('traject_2022.csv', 'r') as f:
            traject_prices = {i+1:float(v) for i, v in enumerate(f.readlines())}

        sub.append(Subscription('Traject Vrij', traject_prices[distance], 0, 0))
        
    cost_matrix = [[s.name, s.get_cost(price, offpeak, peak, month)]
                                                            for s in sub]

    cost_matrix.sort(key=lambda a: a[1])

    print(f'\nShowing info for {rides} trip(s) from {stations[origin]} to {stations[destination]} a month:\n')
    print(tabulate(cost_matrix, headers=['Subscription', 'Cost']))

if __name__ == '__main__':
    main()
