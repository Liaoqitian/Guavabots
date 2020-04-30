# Put your solution here.
import networkx as nx
import random

def solve(client):
    client.end()
    client.start()
    all_students = list(range(1, client.students + 1))
    # random_students = random.sample(all_students, 10)
    non_home = list(range(1, client.home)) + list(range(client.home + 1, client.v + 1))
    outcome = {}
    sortex = []
    bot_Locations = []
    bot_each_location = {}
    foundSoFar = 0
    for vertex in non_home:
        report = list(client.scout(vertex, all_students).values())
        num_true = sum(report)
        outcome[vertex] = num_true
        bot_each_location[vertex] = 0
    bot_each_location[client.home] = 0
    outcome = sorted(outcome.items(), key = lambda kv : kv[1], reverse = True)
    for element in outcome: 
        sortex.append(element[0])
    for vertex in sortex:
        dijk = nx.dijkstra_path(client.G, vertex, client.home) 
        pred = dijk[1]
        numBots = client.remote(vertex, pred) 
        if vertex in bot_Locations: 
            bot_Locations.remove(vertex) 
        foundSoFar = foundSoFar + numBots - bot_each_location[vertex]
        bot_each_location[vertex] = 0
        if pred not in bot_Locations and numBots != 0 and pred != client.home:
            bot_Locations.append(pred)
        bot_each_location[pred] += numBots
        if foundSoFar == client.l:
            break
    traverse = []
    for vertex in bot_Locations:
        if (vertex not in traverse):
            dijk = nx.dijkstra_path(client.G, vertex, client.home)
            i = 0
            while (i < len(dijk) - 1):
                if dijk[i] in bot_Locations:
                    traverse.append(dijk[i])
                if (dijk[i+1] in bot_Locations and dijk[i+1] != client.home):
                    traverse.append(dijk[i+1])
                client.remote(dijk[i], dijk[i + 1])
                i += 1 
    client.end()
