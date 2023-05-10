
class MinHeap:
    def __init__(self):
        self.heap = []

    def __len__(self):
        return len(self.heap)

    def left(self, j):  # returns index of left child of jth element
        return 2 * j + 1

    def right(self, j):  # returns the index of right child of jth element
        return 2 * j + 2

    def parent(self, j):  # returns the index of root of jth element
        return (j - 1) // 2

    def swap(self, i, j):
        self.heap[i], self.heap[j] = self.heap[j], self.heap[i]

    def DownHeap(self, j):
        if self.left(j) < len(self.heap):
            left = self.left(j)
            sm_child = left
            if self.right(j) < len(self.heap):
                right = self.right(j)
                if self.heap[right][0] <= self.heap[left][0]:
                    sm_child = right
            if self.heap[sm_child][0] < self.heap[j][0]:
                self.swap(j, sm_child)
                self.DownHeap(sm_child)
            elif self.heap[sm_child][0] == self.heap[j][0]:
                if self.heap[sm_child][2] < self.heap[j][2]:
                    self.swap(j, sm_child)
                    self.DownHeap(sm_child)

    def UpHeap(self, j):
        parent = self.parent(j)
        if j > 0 and self.heap[j][0] < self.heap[parent][0]:
            self.swap(j, parent)
            self.UpHeap(parent)

    def append(self, j):
        self.heap.append(j)
        self.UpHeap(len(self.heap) - 1)

    def heappush(self, key):
        self.heap.append(key)
        self.UpHeap(len(self.heap) - 1)

    def heappop(self):
        if (len(self) != 0):
            self.heap[0], self.heap[len(self) - 1] = self.heap[len(self) - 1], self.heap[0]
            pop = self.heap.pop()
            self.DownHeap(0)
            return pop
        else:
            print('error')


def Expected_coll(x, v):  # it returns the list of expected collisions
    temp = MinHeap()
    for i in range(len(v)):  # in this loop we are simply comparing velocities of balls for getting the required collisions and appending the corresponding collisions in the heap.
        if i != len(v) - 1:
            if v[i] * v[i + 1] >= 0:
                if v[i] > v[i + 1]:
                    if (x[i + 1] - x[i]) > 0:
                        t = (x[i + 1] - x[i]) / (v[i] - v[i + 1])
                    else:
                        t = -(x[i + 1] - x[i]) / (v[i] - v[i + 1])
                    Xi = x[i + 1] + v[i + 1] * t
                    temp.heappush([t, i, Xi, 0])
            elif v[i] * v[i + 1] < 0:
                if v[i] > 0:
                    t = (x[i + 1] - x[i]) / (v[i] - v[i + 1])
                    Xi = x[i] + v[i] * t
                    temp.heappush([t, i, Xi, 0])
    return temp


collision = []
total_time = 0
total_coll = 0


def listCollisions(M, x, v, m, t):  # this is our final function which return all the collisions
    global total_time
    global total_coll
    global collision
    update_lst = [0] * len(M)
    exp_coll = Expected_coll(x, v)                # initial expected collisions
    time_of_collision = [0] * len(M)
    while total_coll <= m and total_time <= t:
        if exp_coll.heap != []:
            fst_coll = exp_coll.heappop()  # fastest collision
            tm = fst_coll[0]  # time of fastest collision
            ball_i = fst_coll[1]  # index of ball which is colliding in fastest collision
            if update_lst[ball_i] == fst_coll[3]:  # this condition discards the previous expected collisions which are not happening in the present.
                vel = v[ball_i]  # copying v[i] so that it can be used in further calculations.
                v[ball_i] = (M[ball_i] * v[ball_i] + 2 * M[ball_i + 1] * v[ball_i + 1] - M[ball_i + 1] * v[ball_i]) / (M[ball_i] + M[ball_i + 1])  # changing the velocity of ith ball
                v[ball_i + 1] = (M[ball_i + 1] * v[ball_i + 1] + 2 * M[ball_i] * vel - M[ball_i] * v[ball_i + 1]) / (M[ball_i] + M[ball_i + 1])  # changing the velocity of i+1th ball
                loc = x[ball_i]  # copying x[i] so that it can be used in further calculations.
                x[ball_i] = x[ball_i + 1] = loc + vel * (tm - time_of_collision[ball_i])  # changing the positions x[i] and x[i+1].
                time_of_collision[ball_i] = time_of_collision[ball_i + 1] = tm  # saving the time of collision of ith and i+1th ball in time_of_collision list so that we can trace it afterwards.
                if ball_i - 1 >= 0:  # checking whether i-1th ball exists or not
                    loc_i = x[ball_i - 1] + v[ball_i - 1] * (tm - time_of_collision[ball_i - 1])  # storing the changed value of i-1th ball which will be used in further calculations.
                    if v[ball_i - 1] * v[ball_i] >= 0:  # checking the collision of i-1th and ith balls.
                        if v[ball_i - 1] > v[ball_i]:
                            if (x[ball_i] - loc_i) > 0:
                                t1 = (x[ball_i] - loc_i) / (v[ball_i - 1] - v[ball_i])
                            else:
                                t1 = -(x[ball_i] - loc_i) / (v[ball_i - 1] - v[ball_i])
                            Xi = x[ball_i] + v[ball_i] * t1
                            update_lst[ball_i - 1] += 1  # increasing the no of collisions of i-1th ball
                            fst_coll[3] = update_lst[ball_i - 1]  # changing the 4th index of and making it equal to the i-1th index of update_lst
                            exp_coll.heappush([t1 + tm, ball_i - 1, Xi, fst_coll[3]])  # pushing the required collision tuple in expected collision list
                    elif v[ball_i - 1] * v[ball_i] < 0:
                        if v[ball_i - 1] > 0:
                            if (x[ball_i] - loc_i) > 0:
                                t1 = (x[ball_i] - loc_i) / (v[ball_i - 1] - v[ball_i])
                            else:
                                t1 = -(x[ball_i] - loc_i) / (v[ball_i - 1] - v[ball_i])
                            Xi = loc_i + v[ball_i - 1] * t1
                            update_lst[ball_i - 1] += 1  # increasing the no of collisions of i-1th ball in the update_lst
                            fst_coll[3] = update_lst[ball_i - 1]  # changing the 4th index of and making it equal to the i-1th index of update_lst
                            exp_coll.heappush([t1 + tm, ball_i - 1, Xi, fst_coll[3]])  # pushing the required collision tuple in expected collision list
                if ball_i + 2 < len(v):  # checking whether (i+2)th ball exists or not
                    loc_j = x[ball_i + 2] + v[ball_i + 2] * (tm - time_of_collision[
                        ball_i + 2])  # storing the changed value of (i-1)th ball which will be used in further calculations
                    if v[ball_i + 2] * v[ball_i + 1] >= 0:
                        if v[ball_i + 1] > v[ball_i + 2]:
                            t1 = (loc_j - x[ball_i + 1]) / (v[ball_i + 1] - v[ball_i + 2])
                            Xi = x[ball_i + 1] + v[ball_i + 1] * t1
                            update_lst[ball_i + 1] += 1  # increasing the no of collisions of i+1th ball in the update_lst
                            fst_coll[3] = update_lst[ball_i + 1]  # changing the 4th index of and making it equal to the i-1th index of update_lst
                            exp_coll.heappush([t1 + tm, ball_i + 1, Xi, fst_coll[3]])  # pushing the required collision tuple in expected collision list
                    elif v[ball_i + 1] * v[ball_i + 2] < 0:
                        if v[ball_i + 1] > 0:
                            t1 = (loc_j - x[ball_i + 1]) / (v[ball_i + 1] - v[ball_i + 2])
                            Xi = x[ball_i + 1] + v[ball_i + 1] * t1
                            update_lst[ball_i + 1] += 1  # increasing the no of collisions of i+1th ball in the update_lst
                            fst_coll[3] = update_lst[ball_i + 1]  # changing the 4th index of and making it equal to the i-1th index of update_lst
                            exp_coll.heappush([t1 + tm, ball_i + 1, Xi, fst_coll[3]])  # pushing the required collision tuple in expected collision list
                total_coll = 1 + total_coll  # increasing the total collisions loop invariant
                total_time = tm  # modifying the total time loop invariant
                fst_coll[2] = round(fst_coll[2], 4)
                fst_coll[0] = round(fst_coll[0], 4)
                if total_coll <= m and total_time <= t:
                    collision.append((fst_coll[0], fst_coll[1],fst_coll[2]))
            elif update_lst[ball_i] != fst_coll[3]:
                continue
        else:
            break  # finally breaking the loop when expected collision list is empty
    return collision
