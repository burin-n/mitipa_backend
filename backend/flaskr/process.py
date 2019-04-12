import math
import numpy as np

INITIAL = 0
MOVING = 1
STATIC = 2
UNK = -1

NOT_EXIST = 0
EXIST = 1

APPEAR = 3
DISAPPEAR = 4

SITTING = 0
ENTER = 1
LEAVE = 2
TEMP_LEAVE = 3
LOOP_LEAVE = 4
WANDERING = 5


class Process:
    def __init__(self):
        self.x_grid = 20
        self.y_grid = 10
        self.movement_heatmap = np.zeros((self.y_grid, self.x_grid))
        self.entrance_heatmap = np.zeros((self.y_grid, self.x_grid))
        self.threshold = 0.01
        self.movements_matrix = None
        self.existence_matrix = None
        self.person_type = []
        self.timestamps = set()
        self.timestamps_margin = 0.1
        self.data = None
        pass

    def define_moving_entity(self, data):
        self.data = data
        movements = {}
        person_count = 0
        for person in data:
            person_count += 1
            recent_bb = None
            movement = {}
            for timestamp in data[person]:
                self.timestamps.add(timestamp)
                bb = [
                    data[person][timestamp]['Top'],
                    data[person][timestamp]['Left'],
                    data[person][timestamp]['Top'] +
                    data[person][timestamp]['Height'],
                    data[person][timestamp]['Left'] +
                    data[person][timestamp]['Width']
                ]
                self.data[person][timestamp] = bb
                if recent_bb is None:
                    recent_bb = bb
                    movement[timestamp] = INITIAL
                    continue
                distance = self.calc_bb_distance(bb, recent_bb)
                recent_bb = bb
                if distance >= self.threshold:
                    movement[timestamp] = MOVING
                else:
                    movement[timestamp] = STATIC
            movements[person] = movement
        self.timestamps = list(self.timestamps)
        self.timestamps.sort()
        self.movements_matrix = np.ones((person_count, len(self.timestamps))).astype(int) * -1
        self.existence_matrix = np.zeros((person_count, len(self.timestamps))).astype(int)
        for person in movements:
            for timestamp in movements[person]:
                self.movements_matrix[
                    int(person), self.timestamps.
                    index(timestamp)] = movements[person][timestamp]
                self.existence_matrix[
                    int(person), self.timestamps.index(timestamp)]= 1
        print('movement matrix')
        print(self.movements_matrix)
        print('entrance matrix')
        print(self.existence_matrix)

    def define_person_state(self):
        existence_matrix = self.existence_matrix
        for person in range(existence_matrix.shape[0]):
            existence = existence_matrix[person,:]
            if np.sum(existence) == existence.shape[0]:
                #appear in the whole sequence
                if np.sum(self.movements_matrix[person,:]) == INITIAL + STATIC * (self.movements_matrix[person,:].shape[0]-1):
                    #been sitting the whole time
                    self.person_type.append(SITTING)
                    continue
                else:
                    self.person_type.append(WANDERING)
                    continue
            if np.sum(existence[0:1]) == 0:
                # appear later
                if np.sum(existence[-1:]) == 0:
                    #disappear in the end
                    self.person_type.append(LOOP_LEAVE)
                    continue
                else:
                    self.person_type.append(ENTER)
                    continue
            elif np.sum(existence[-1:]) == 0:
                #exist first then disappear
                self.person_type.append(LEAVE)
                continue
            else:
                #temporarily disappear
                self.person_type.append(TEMP_LEAVE)
                continue
        print('person type')
        print(self.person_type)
    
    def define_movement_heatmap(self):
        data = self.data
        movements_matrix = self.movements_matrix
        for person in range(len(self.person_type)):
            for timestamp in range(movements_matrix.shape[1]):
                if movements_matrix[person,timestamp] == INITIAL or movements_matrix[person,timestamp] == MOVING:
                    y = (data[person][timestamp][0] + data[person][timestamp][2]) / 2
                    x = (data[person][timestamp][1] + data[person][timestamp][3]) / 2
                    y = int(y * self.y_grid)
                    x = int(x * self.x_grid)
                    self.movement_heatmap[y,x] += 1
        print('movement heatmap')
        print(self.movement_heatmap)

    def define_entrance_heatmap(self):
        data = self.data
        movements_matrix = self.movements_matrix
        for person in range(len(self.person_type)):
            if self.person_type[person] == LOOP_LEAVE:
                initial_timestamp = np.where(movements_matrix[person] == INITIAL)[0][0]
                y = (data[person][initial_timestamp][0] + data[person][initial_timestamp][2]) / 2
                x = (data[person][initial_timestamp][1] + data[person][initial_timestamp][3]) / 2
                y = int(y * self.y_grid)
                x = int(x * self.x_grid)
                self.entrance_heatmap[y,x] += 1
        print('entrance heatmap')
        print(self.entrance_heatmap)

    def calc_bb_distance(self, a, b):
        return math.sqrt(
            math.pow(((a[0] + a[2]) / 2) - ((b[0] + b[2]) / 2), 2) +
            math.pow(((a[1] + a[3]) / 2) - ((b[1] + b[3]) / 2), 2))

    # def find_entrance(self, data):
    #     for person in data:


process = Process()
process.define_moving_entity(
    data= {
        0:{
            0:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            },
            1:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            },
            2:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            }
        },
        1:{
            0:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            },
            1:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            },
            2:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            }
        },
        2:{
            0:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            },
            1:{
                "Height": 0.8787037134170532,
                "Left": 0.00572916679084301,
                "Top": 0.12129629403352737,
                "Width": 0.21666666865348816
            }
        },
        
    }
)
process.define_person_state()
process.define_entrance_heatmap()
process.define_movement_heatmap()
