import math
import numpy as np

SITTING = 0
ENTER = 1
LEAVE = 2
TEMP_LEAVE = 3
LOOP_LEAVE = 4
WANDERING = 5


class Process:
    def __init__(self):
        self.x_grid = 10
        self.y_grid = 5
        self.coord_matrix = None  #(person, timestamp, [y_coord, x_coord])
        self.existence_heatmap = np.zeros(
            (self.y_grid, self.x_grid)).astype(int)
        self.sitting_heatmap = np.zeros((self.y_grid, self.x_grid)).astype(int)
        self.person_state = None
        self.timestamp_buffer = 5
        self.timestamps = set()
        self.data = None
        pass

    def process_score(self, data):
        self.data = data
        self.define_timestamps()
        self.create_persons_heatmap()
        self.define_person_state()
        self.define_existence_heatmap()
        self.define_sitting_heatmap()
        result = self.get_person_state_count()
        return {
            "existence_heatmap": self.existence_heatmap.tolist(),
            "sitting_heatmap": self.sitting_heatmap.tolist(),
            "person_state": self.person_state
        }

    def set_data(self, data):
        self.data = data
        return

    def define_timestamps(self):
        data = self.data
        for person in data:
            for timestamp in data[person]:
                self.timestamps.add(timestamp)
        self.timestamps = list(self.timestamps)
        self.timestamps.sort()
        return

    def create_persons_heatmap(self):
        timestamps = self.timestamps
        data = self.data
        coord_matrix = np.ones(
            (len(data), len(self.timestamps), 2)).astype(int) * -1
        for person in self.data:
            person_data = self.data[person]
            for timestamp in person_data:
                bb = [
                    data[person][timestamp]['Top'],
                    data[person][timestamp]['Left'],
                    data[person][timestamp]['Top'] +
                    data[person][timestamp]['Height'],
                    data[person][timestamp]['Left'] +
                    data[person][timestamp]['Width']
                ]
                y = (bb[0] + bb[2]) / 2
                x = (bb[1] + bb[3]) / 2
                y = int(y * self.y_grid)
                x = int(x * self.x_grid)
                # print("{};{}: {}, {}".format(person, timestamp, y, x))
                coord_matrix[person, timestamps.index(timestamp
                                                      ), :] = np.array([y, x])
        self.coord_matrix = coord_matrix
        return

    def define_person_state(self):
        coord_matrix = self.coord_matrix
        person_state = []
        timestamps = self.timestamps
        for person in range(coord_matrix.shape[0]):
            person_coords = coord_matrix[person, :]
            unique_coords = set()
            #check sitting
            for timestamp in range(person_coords.shape[0]):
                coord = person_coords[timestamp]
                if np.equal(coord, np.array([-1, -1]))[0]:
                    continue
                else:
                    unique_coords.add(tuple(coord.tolist()))
            if len(unique_coords) == 1:
                person_state.append(SITTING)
                continue
            #check disappear first and later
            target_first = list(range(0, self.timestamp_buffer))
            target_later = list(
                range(
                    len(timestamps) - self.timestamp_buffer, len(timestamps)))
            disappear_first = False
            disappear_later = False
            for target_timestamp in target_first:
                if person_coords[target_timestamp][0] != -1:
                    break
            else:
                disappear_first = True

            for target_timestamp in target_later:
                if person_coords[target_timestamp][0] != -1:
                    break
            else:
                disappear_later = True
            if disappear_first and disappear_later:
                person_state.append(LOOP_LEAVE)
                continue
            if disappear_first and not disappear_later:
                person_state.append(ENTER)
                continue
            if not disappear_first and disappear_later:
                person_state.append(LEAVE)
                continue
            else:
                person_state.append(WANDERING)
        self.person_state = person_state
        print("person state")
        print(person_state)
        return

    def define_existence_heatmap(self):
        coord_matrix = self.coord_matrix
        existence_heatmap = self.existence_heatmap
        for person in range(coord_matrix.shape[0]):
            coords = coord_matrix[person]
            for timestamp in range(coords.shape[0]):
                if coords[timestamp][0] != -1:
                    coord = coords[timestamp]
                    existence_heatmap[coord[0], coord[1]] += 1
        self.existence_heatmap = existence_heatmap
        print("existence heatmap")
        print(existence_heatmap)
        return

    def define_sitting_heatmap(self):
        coord_matrix = self.coord_matrix
        sitting_heatmap = self.sitting_heatmap
        person_state = self.person_state
        for person in range(coord_matrix.shape[0]):
            if (person_state[person] == SITTING):
                coords = coord_matrix[person]
                for timestamp in range(coords.shape[0]):
                    if coords[timestamp][0] != -1:
                        coord = coords[timestamp]
                        sitting_heatmap[coord[0], coord[1]] += 1
                        break
        self.sitting_heatmap = sitting_heatmap
        print("sitting heatmap")
        print(sitting_heatmap)
        return

    def get_person_state_count(self):
        person_state = self.person_state
        result = {
            "SITTING": 0,
            "ENTER": 0,
            "LEAVE": 0,
            "TEMP_LEAVE": 0,
            "LOOP_LEAVE": 0,
            "WANDERING": 0
        }
        for state in person_state:
            if state == SITTING: result["SITTING"] += 1
            if state == ENTER: result["ENTER"] += 1
            if state == LEAVE: result["LEAVE"] += 1
            if state == TEMP_LEAVE: result["TEMP_LEAVE"] += 1
            if state == LOOP_LEAVE: result["LOOP_LEAVE"] += 1
            if state == WANDERING: result["WANDERING"] += 1
        return result


# import pickle
# data = pickle.load(open("bbs4.p", "rb"))

# process = GoodProcess()
# print(process.process_score(data))
# # process.set_data(data)
# # process.define_timestamps()
# # process.create_persons_heatmap()
# # process.define_person_state()
# # process.define_existence_heatmap()
# # process.define_sitting_heatmap()
# # print(process.get_person_state_count())