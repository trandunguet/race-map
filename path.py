import math

class Dot:
    def __init__(self, id, x, y, adj):
        self.id = id
        self.x = x
        self.y = y
        self.adj = adj
    
    def distance(self, x, y):
        return math.sqrt((self.x - x) ** 2 + (self.y - y) ** 2)


class Path:
    def __init__(self):
        self.next_dot_id = 0
        self.dots = {}
        self.checkpoints = {}

    def delete_dot(self, x, y):
        nearest_id = self.find_two_nearest_dots(x, y)[0]
        for adj_id in self.dots[nearest_id].adj:
            adj = self.dots[adj_id]
            adj.adj.remove(nearest_id)
        self.dots.pop(nearest_id)

    def add_dot(self, id, x, y, adj):
        new_dot = Dot(id, x, y, adj)
        self.dots[id] = new_dot
        self.next_dot_id = max(self.next_dot_id, id + 1)

    def create_dot(self, x, y, n):
        """x, y: coordinate

        n: number of adjacent dots"""

        id = self.next_dot_id
        self.next_dot_id += 1

        adj = self.find_two_nearest_dots(x, y)[:n]

        self.add_dot(id, x, y, adj)
        for adj_id in adj:
            adj_dot = self.dots[adj_id]
            adj_dot.adj.append(id)

    def find_two_nearest_dots(self, x, y):
        if len(self.dots) < 2:
            return list(self.dots)

        result = [-1, -1]
        result_d = [1e9, 1e9]
        for id, dot in self.dots.items():
            d = dot.distance(x, y) 

            if d < result_d[0]:
                result[1] = result[0]
                result_d[1] = result_d[0]
                result[0] = id
                result_d[0] = d
                continue

            if d < result_d[1]:
                result[1] = id
                result_d[1] = d
        
        return result
