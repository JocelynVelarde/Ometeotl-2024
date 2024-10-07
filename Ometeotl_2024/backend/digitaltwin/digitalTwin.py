"""
digitalTwin class is a class that represents a digital twin of a farm.

Dimension 0: Ripeness of the plants.
Dimension 1: Number of weeds.
Dimension 2: Health of the plants.
Dimension 3: Water status of the plants.
Dimension 4: Diversity of the leaves.

"""



import numpy as np
import random

class Twin:
    def __init__(self, name, size_x, size_y):
        self.name = name
        self.size_x = size_x
        self.size_y = size_y
        self.resolution_x = 5
        self.resolution_y = 5
        self.grid_x = size_x // self.resolution_x
        self.grid_y = size_y // self.resolution_y
        self.matrix = np.zeros((self.grid_y, self.grid_x, 5), dtype=np.float32)
        self.total_blocks = self.grid_x * self.grid_y
        self.test_size = self.total_blocks*.05
        self.ilness_log ={
            "Uncertain": 0,
            "Overwatered": 0,
            "Dry": 0,
            "Variegated": 0,
            "Healthy": 0
        }
        self.pest_log = { "Rust": 0,
            "Fungus": 0,
            "Pest": 0,
            "Burning": 0}
        self.normalization = {0: (0, 1.5),
                              1: (0, 1),
                              2: (0, 1),
                              3: (0, 1.5),
                              4: (0, 1)}

    def get_ripeness(self, plot_data):

        ripeness_scores = {
            "freshripe": 1.00,
            "freshunripe": 0.75,
            "ripe": 1.00,
            "overripe": 1.25,
            "rotten": 1.50,
            "unripe": 0.50
        }

        total_plants = 0
        weighted_ripeness_sum = 0


        for tag, count in plot_data.items():
            ripeness_score = ripeness_scores.get(tag, 0)
            weighted_ripeness_sum += ripeness_score * count
            total_plants += count


        if total_plants == 0:
            return None
        overall_health = weighted_ripeness_sum / total_plants

        return overall_health

    def get_weeds(self, weed_count):
        return weed_count

    def get_healthy_plants(self, healty_leaf_count, unhealthy_leaf_count):
        if unhealthy_leaf_count == 0:
            return 1
        return healty_leaf_count / (healty_leaf_count + unhealthy_leaf_count)

    def get_water(self, illness_result, pest_results):
        self.ilness_log['Healthy'] += illness_result['Healthy']
        self.ilness_log['Overwatered'] += illness_result['Overwatered']
        self.ilness_log['Dry'] += illness_result['Dry']

        self.pest_log['Rust'] += pest_results['Rust']
        self.pest_log['Fungus'] += pest_results['Fungus']
        self.pest_log['Pest'] += pest_results['Pest']
        self.pest_log['Burning'] += pest_results['Burning']

        healthy, overwatered, dry = illness_result['Healthy'], illness_result['Overwatered'], illness_result['Dry']

        total = healthy + overwatered + dry

        if total == 0:
            return 1

        healthy_ratio = healthy / total
        overwatered_ratio = overwatered / total
        dry_ratio = dry / total

        if healthy_ratio >= overwatered_ratio and healthy_ratio >= dry_ratio:
            return 1
        elif dry_ratio > healthy_ratio and dry_ratio > overwatered_ratio:
            return 0.5
        else:
            return 1.5

    def get_leaf_types(self, leaf_types):
        return leaf_types['leaf_type_count']

    def get_random_coordinates(self):
        rows, cols, dims = self.get_shape()
        coordinates_set = set()

        while len(coordinates_set) < self.test_size:
            coord = (random.randint(0, rows - 1), random.randint(0, cols - 1))
            coordinates_set.add(coord)

        return  sorted(list(coordinates_set), key=lambda x: x[0])

    def run_analysis(self, json_data):

        data = json_data['results']

        coordinate = tuple(data['coordinate'])

        ripeness = self.get_ripeness(data['plot_data'])

        weed_count = self.get_weeds(data['weed_count'])

        healthy_plants = self.get_healthy_plants(data['healthy_plants'], data['unhealthy_plants'])

        water_status = self.get_water(data['illnesses'], data['pests'])

        leaf_diversity = self.get_leaf_types(data['leaf_types'])


        self.set_value(coordinate, 0, ripeness)
        self.set_value(coordinate, 1, weed_count)
        self.set_value(coordinate, 2, healthy_plants)
        self.set_value(coordinate, 3, water_status)
        self.set_value(coordinate, 4, leaf_diversity)

    def normalize_matrix(self, value_range, dimension):
        min_value, max_value = value_range
        matrix_min = np.min(self.matrix[:,:,dimension])
        matrix_max = np.max(self.matrix[:,:,dimension])

        # Scale to [0, 1]
        normalized_matrix = (self.matrix[:,:,dimension] - matrix_min) / (matrix_max - matrix_min)

        # Scale to [min_value, max_value]
        normalized_matrix = normalized_matrix * (max_value - min_value) + min_value

        return normalized_matrix

    def get_matrix(self):
            return self.matrix

    def get_shape(self):
        return self.matrix.shape

    def set_value(self, coordinate, dimension, value):
        cord = (*coordinate, dimension)
        self.matrix[cord] += value

    def average_values(self):
        rows, cols, dims = self.get_shape()

        for i in range(dims):
            twod_matrix = self.matrix[:,:,i].copy()
            zeros = np.zeros((rows, cols), dtype=np.float32)
            zeros[0:-1, : ] =  zeros[0:-1, : ] + twod_matrix[0:-1, : ]
            zeros[1:-1,:] = zeros[1:-1,:] + twod_matrix[1:-1,:]
            zeros[:, 0:-1] = zeros[:, 0:-1] + twod_matrix[:, 0:-1]
            zeros[:, 1:-1] = zeros[:, 1:-1]  + twod_matrix[:, 1:-1]
            zeros = zeros / 4
            self.matrix[:,:,i] = zeros
            self.matrix[:, :, i] = self.normalize_matrix(self.normalization[i], i)
    def get_dimension(self, dim):
        return self.matrix[:,:,dim]
