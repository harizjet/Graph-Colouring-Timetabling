import random
import numpy as np
import logging
import sys
import matplotlib.pyplot as plt

logging.basicConfig(stream=sys.stdout, level=logging.DEBUG)

def cost(stud_mat, nolog=False):
    tot = 0
    subj_n = len(stud_mat[0])
    for id, student in enumerate(stud_mat):
        i = 0
        d = 0
        tsum = 0
        while i < subj_n - 1:
            if student[i] + student[i+1] == 2:
                tsum += 2
                d += 1
            elif student[i] + student[i+1] == 1:
                d += 1
            i += 2

        tsum += (d-1) if d > 0 else 0
        tot += tsum
        print(f"Student {id} cost: {tsum}") if not nolog else ''
    print(f"Total Cost: {tot}") if not nolog else ''
    return tot

def swap(stud_mat, index_schedule):
    front, back = random.sample(range(stud_mat.shape[1]), 2)
    print(f"Swap position {front} and {back}")
    selected = {i: subj for subj, i in index_schedule.items() if i in [front, back]}

    if len(selected) > 1:
        index_schedule[selected[front]], index_schedule[selected[back]] = index_schedule[selected[back]], index_schedule[selected[front]]
    elif len(selected) == 1:
        if [int(x) for x in selected.keys()][0] == front:
            index_schedule[selected[front]] = back
        else:
            index_schedule[selected[back]] = front
    else:
        return stud_mat, index_schedule
    ans_mat = stud_mat.transpose().copy()
    ans_mat[back], ans_mat[front] = stud_mat.transpose()[front], stud_mat.transpose()[back]

    print(f"The Order ------> {index_schedule}")
    return ans_mat.transpose(), index_schedule

def plot_cost(raw_cost):
    fig = plt.figure(figsize=(7, 7))
    axes = fig.add_subplot(111)
    axes.plot(range(1, len(raw_cost)+1), raw_cost, label='cost')
    axes.set_xlabel('Iterations')
    axes.set_ylabel('Cost')
    axes.set_title('Hill Climbing')
    axes.legend()
    plt.show();

def solution():
    ans = dict()

    # data
    students = [[t.strip() for t in input().split(',')] for _ in range(int(input()))]
    n_students = len(students)
    # schedule = {'Math': 'peach', 'English': 'orange', 'Biology': 'green', 'Chemistry': 'black', 'Computer Science': 'rainbow', 'Geography': 'black', 'History': 'purple', 'French': 'orange', 'Psychology': 'peach', 'Spanish': 'orange'}
    schedule = {'Math': 'rainbow', 'English': 'red', 'Biology': 'black', 'Chemistry': 'yellow', 'Computer Science': 'green', 'Geography': 'yellow', 'History': 'pink', 'French': 'red', 'Psychology': 'rainbow', 'Spanish': 'red'}

    group_student  = []
    for student in students:
        group_student.append([schedule[subj] for subj in student])

    student_sched = np.zeros((n_students, 8))

    print(group_student)
    # initialized
    placement = random.sample(range(8), 6)
    index_schedule = {v: i for v, i in zip(set(schedule.values()), placement)}
    for i, student in enumerate(group_student):
        student_sched[i, [index_schedule[s] for s in student]] = 1

    bef = student_sched.copy()
    iter = 100 # number of iter
    best_sol, best_cost, best_sched = student_sched, cost(student_sched, nolog=True), index_schedule
    col_cost = [best_cost]
    raw_cost = [best_cost]
    print(f"Current Order ------> {best_sched}")
    for _ in range(iter):
        print(f"-----Iteration {_}-----")
        student_sched, index_schedule = swap(best_sol.copy(), best_sched.copy())
        thecost = cost(student_sched)
        if thecost < best_cost:
            print("######## Found better option ########")
            print(f"Current Order ------> {index_schedule}")
            col_cost += [thecost]
            best_sol, best_cost, best_sched = student_sched.copy(), thecost, index_schedule.copy()
        raw_cost += [best_cost]
        print(f"-----END {_}-----")
    print(col_cost)
    print(f"Before: \n{bef}")
    # plot_cost(raw_cost)
    return best_cost, best_sol