import random
import json
from datetime import datetime, timedelta

from digitalTwin import Twin

coordinates = [(0, 0), (0, 12), (1, 17), (2, 13), (2, 15), (3, 4), (3, 6), (3, 2), (7, 18), (8, 1)]


def generate_random_data():
    return {
        "results": {
            "coordinate": random.choice(coordinates),
            "timestamp": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime("%Y-%m-%d %H:%M:%S"),
            "plot_data": {
                "freshripe": random.randint(5, 25),
                "freshunripe": random.randint(5, 25),
                "overripe": random.randint(5, 25),
                "ripe": random.randint(5, 25),
                "rotten": random.randint(5, 25),
                "unripe": random.randint(5, 25)
            },
            "weed_count": random.randint(5, 25),
            "healthy_plants": random.randint(5, 25),
            "unhealthy_plants": random.randint(5, 25),
            "illnesses": {
                "Uncertain": random.randint(5, 25),
                "Overwatered": random.randint(5, 25),
                "Dry": random.randint(5, 25),
                "Variegated": random.randint(5, 25),
                "Healthy": random.randint(5, 25)
            },
            "pests": {
                "Rust": random.randint(5, 25),
                "Fungus": random.randint(5, 25),
                "Pest": random.randint(5, 25),
                "Burning": random.randint(5, 25)
            },
            "leaf_types": {
                "leaf_type_count": random.randint(1, 5),
                "leaf_types": ["Corn leaf blight"]
            }
        }
    }


random_entries = [generate_random_data() for _ in range(10)]

farm = Twin("Farm1", 100, 50)

for entry in random_entries:
    farm.run_analysis(entry)

#farm.average_values()
print(farm.matrix[:,:,0])
farm.average_values()
print("para")
print(farm.matrix[:,:,0])