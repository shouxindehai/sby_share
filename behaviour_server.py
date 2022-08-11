import pymongo
import json
import difflib
import random

myclient = pymongo.MongoClient("mongodb://localhost:27017/")
mydb = myclient["cuckoo"]
 

def find_record(task_id):
    record = mydb["analysis"].find_one({"info.id": int(task_id)})
    process = record["behavior"]["processes"]
    return process[1]["calls"]


def generate_api_list(id_list):
    id_api_list = []
    calls_table = mydb["calls"]
    #print(id_list)
    for id in id_list:
        calls_list = calls_table.find_one({"_id": id})
        for call in calls_list['calls']:
            id_api_list.append(call['api'])

    return id_api_list

def min_distance(s1, s2):
    d = [[x for x in range(len(s1)+1)] for _ in range(len(s2)+1)]
    
    for y in range(1,len(s2)+1):
        d[y][0] = d[y-1][0] + 1


    for x in range(1, len(s1)+1):
        for y in range(1, len(s2)+1):
            if s1[x-1] == s2[y-1]:
                d[y][x] = d[y-1][x-1]
            else:
                substute = d[y-1][x-1] + 1
                add = d[y][x-1] + 1
                delete = d[y-1][x] + 1
                d[y][x] = min(add, substute, delete)
    return d[-1][-1]

if __name__ == "__main__":
    
    task_table = {}
    task_id = []
    for i in range(1, 5):
        task_id.append(i)

    for t_id in task_id:
        using_id = find_record(t_id)
        api_list = generate_api_list(using_id)
        task_table[t_id] = api_list

    # random change apilist
    for i in range(30):
        r1 = random.randint(0, len(task_table[2]) - 1)
        r2 = random.randint(0, len(task_table[2]) - 1)
        task_table[2].insert(r1, task_table[2][r2])

 
    # sm = difflib.SequenceMatcher(None, task_table[1], task_table[2])
    # print(sm.ratio())

    distance = float(min_distance(task_table[2], task_table[1]))
    print(distance)
    length = float(len(task_table[1]) + len(task_table[2]))
    likely = 1 - (2 * distance) / length
    print(likely)