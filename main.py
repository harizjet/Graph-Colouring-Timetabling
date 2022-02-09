from graph_coloring import graph_coloring_algo as gca
from hill_climbing import hill_climbing_algo as hca

data1 = '''
0
Undergraduate, Graduate, Colloquium, Library, Staffing, Promotion
12
Undergraduate, Library
Undergraduate, Staffing
Undergraduate
Undergraduate, Graduate
Graduate, Staffing
Graduate, Staffing, Promotion
Graduate
Colloquium, Library
Colloquium, Staffing
Colloquium
Library, Promotion
Promotion
'''

data2 = '''
0
Math, English, Biology, Chemistry, Computer Science,  Geography, History, French, Psychology, Spanish
7
Math, English, Biology, Chemistry
Math, English, Computer Science, Geography
Biology, Psychology, Geography, Spanish
Biology, Computer Science, History, French
English, Psychology, Computer Science, History
Psychology, Chemistry, Computer Science, French
Psychology, Geography, History, Spanish
'''

data3 = '''
1
7
Math, English, Biology, Chemistry
Math, English, Computer Science, Geography
Biology, Psychology, Geography, Spanish
Biology, Computer Science, History, French
English, Psychology, Computer Science, History
Psychology, Chemistry, Computer Science, French
Psychology, Geography, History, Spanish
'''

if __name__ == '__main__':
    opt = int(input())
    if opt == 0:
        ans, n = gca.solution()
    elif opt == 1:
        ans, n = hca.solution()

    print(ans, n, sep='\n')
