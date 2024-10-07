import random
import json
import numpy as np
from datetime import datetime, timedelta
import numpy as np
import matplotlib.pyplot as plt

from digitalTwin import Twin


class Example:

    def __init__(self, days, day_entries):
        self.days = days
        self.day_entries = day_entries
        self.farm = Twin("Example Farm", 100, 50)

    coordinates = [(0, 0), (0, 12), (1, 17), (2, 13), (2, 15), (3, 4), (3, 6), (3, 2), (7, 18), (8, 1)]

    def generate_random_data(self, coordinates):
        return {
            "results": {
                "coordinate": random.choice(coordinates),
                "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
                "plot_data": {
                    "freshripe": random.randint(5, 25),
                    "freshunripe": random.randint(5, 25),
                    "overripe": random.randint(5, 25),
                    "ripe": random.randint(5, 85),
                    "rotten": random.randint(5, 25),
                    "unripe": random.randint(5, 75)
                },
                "weed_count": random.randint(5, 25),
                "healthy_plants": random.randint(5, 85),
                "unhealthy_plants": random.randint(5, 25),
                "illnesses": {
                    "Uncertain": random.randint(5, 25),
                    "Overwatered": random.randint(5, random.randint(6, 30)),
                    "Dry": random.randint(5, 25),
                    "Variegated": random.randint(5, random.randint(6, 30)),
                    "Healthy": random.randint(5, 75)
                },
                "pests": {
                    "Rust": random.randint(5, 10),
                    "Fungus": random.randint(5, 25),
                    "Pest": random.randint(5, 40),
                    "Burning": random.randint(5, 33)
                },
                "leaf_types": {
                    "leaf_type_count": random.randint(1, 5)
                }
            }
        }


    def time_analysis(self):
        for i in range(self.days):
            day_coordinates = self.farm.get_random_coordinates()
            random_entries = [self.generate_random_data(day_coordinates) for _ in range(self.day_entries)]
            for entry in random_entries:
                self.farm.run_analysis(entry)
            self.farm.average_values()

    def print(self, dim):
        plt.imshow(self.farm.matrix[:,:,dim], cmap='hot', interpolation='nearest')
        plt.colorbar()
        plt.title('Heatmap')
        plt.show()




