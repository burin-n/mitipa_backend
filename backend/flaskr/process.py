import math
import numpy as np

INITIAL = 0
MOVING = 1
STATIC = 2
APPEAR = 3
DISAPPEAR = 4


class Process:
    def __init__(self):
        # self.x_grid = 20
        # self.y_grid = 10
        self.threshold = 0.01
        self.movements_matrix = []
        self.timestamps = set()
        pass

    def define_moving_entity(self, data):
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
        self.movements_matrix = np.ndarray((person_count, len(self.timestamps))).astype(int)
        for person in movements:
            for timestamp in movements[person]:
                self.movements_matrix[
                    int(person), self.timestamps.
                    index(timestamp)] = movements[person][timestamp]
        print(self.movements_matrix)
    # def define_entrance(self):
    #     for

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