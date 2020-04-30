# Guavabot!
## Overview 
Your group runs an autonomous food delivery company called Guavabot. Everything is going great - you just raised $10 million in VC funding, and you've deployed to three locations worldwide - Singapore, Tel Aviv, and Toronto. Unfortunately your intern ran rm -rf / on your production servers, losing the locations of all your bots! The bots took quite a while to develop and the prototypes are valuable, so you want to locate them and move them home. Thankfully, you have a worldwide network of students who report the locations of the bots to you via app, but these customers are not always right and may incorrectly inform you about bots' locations.

## Problem
Your group runs an autonomous food delivery company called Guavabot. Everything is going great - you just raised $10 million in VC funding, and you've deployed to three locations worldwide - Singapore, Tel Aviv, and Toronto. Unfortunately your intern ran rm -rf / on your production servers, losing the locations of all your bots! The bots took quite a while to develop and the prototypes are valuable, so you want to locate them and move them home. Thankfully, you have a worldwide network of students who report the locations of the bots to you via app, but these customers are not always right and may incorrectly inform you about bots' locations.

## Statement
You have some number of bots lost in the city. Your goal is to find these bots and move them home in the shortest time. You have two operations, both that take some time: remote and scout. A remote moves all bots from a vertex to a neighbour of that vertex. A scout sends a student to a vertex and has the student report if a bot is there.

Formally, your delivery system is for a specific city, i.e. a connected weighted undirected graph such that all edge weights 
w_e > 0, with a designated home vertex h∈V. The Guavabots live at a set of locations L⊆V with exactly one Guavabot in each starting location; but you do not know this set of starting locations. In addition, you have a set of k students that you can send to vertices on the graph to inform you if Guavabots are present there; however, the students are unreliable and are incorrect on a fixed, unknown subset of vertices. You are given and know the graph G, edge weights w_e, home vertex h, number of Guavabots |L|, and the number of students k. All graphs are complete, have |L|=5 bots, n=100 vertices, and k∈{10, 20, 40} students. You do not know the starting locations of the Guavabots L or the opinions of the students (until you ask for them by scouting).

## Actions
You get the bots home by performing a series of actions of your choice. Your available actions are:
scout on (i, v), where i is a student and v∈V. In this case, student i visits the vertex and reports to you whether they see Guavabots at the vertex (they give this as a yes/no answer). However, their report may be incorrect. You have to wait for the student to move to the vertex and report you the answer, which takes 1 time.
For more information on how student reports work, see students.
remote on the directed edge (u, v), provided that {u,v}∈E. This tells you how many Guavabots there were at u that received the command, then all the Guavabots at u move to v. Regardless of the presence of Guavabots at u, it takes w_uv time to wait and see if your command has moved any Guavabots.

As the graph is undirected, you can remote along either direction on any edge.
You can only perform one action at a time, and you cannot "undo" an action.
We call an instance of this problem and the sequence of actions you take a "rescue".

## Constraints
After you remote along an edge {u, v} in the direction u → v, any future scouts on u or v will fail (as you already know about the existence of Guavabots at either vertex). The only exception is if no bots were remoted along the edge, in which case you can scout on v in the future. You cannot perform a scout at the home vertex h, ever.

## Students
Each student i can give you a report on any vertex so long you haven't used it in a remote already. If a student is incorrect on a vertex, they will always report the opposite of the truth; students are incorrect a fixed, but unknown number of times. This means that for each student i, there is a fixed, unknown subset S_i⊆V of vertices that they will be wrong at. These sets S_1,…,S_k are fixed for the input, meaning they are completely determined before your rescue even starts; in other words, the student opinions will not change depending on how your algorithm runs.
There are no guarantees on how correct the students will be beyond the fact that |S_i|≤|V|/2 for all students i. It is up to you to come up with an algorithm that uses the student reports as effectively as possible.

## Time
Time is measured as follows:
When you start, the current time is zero.
There is a fixed time every scout action takes; after every scout your time is incremented by 1.
After a remote on the edge {u,v}, your time is incremented by w_uv, regardless of the direction you remote on {u,v}
The scout cost 1 is much smaller than most edge weights w_e.

## Goal
You are given a score once you end the rescue. If the time taken so far is t and the number of Guavabots that are home is 
g, this score is:

100/(|L|+1) * (g+α/(α+t)) where α∼1000 is a constant among all inputs which is yet to be determined, but is within an order a magnitude of 1000 and is about the raw time of an average solver that gets all the bots home.
You want to get as high a score as possible. The minimum score for any instance is 0, and the maximum score for any instance is 100 (neither side is necessarily attainable, your score will fall in between).

This scoring function was designed such that returning more bots is always better than spending less time. For example, say that we have 5 bots scattered on a graph:  

If we return 5 bots and take 10000 time, our score is ≈84.8  
If we return 2 bots and take 100 time, our score is ≈48.5  
If we return 1 bot and take 10 time, our score is ≈33.17  
Another way to see it: treat your score as a tuple (g,t). Scores will be ordered by g descending first, then by 
t ascending.

## Example

Remember that you don't know the locations of the bots or if the student opinions are correct (you also don't know the student opinions until you scout). If you ignore the opinions of the students, then you have no choice but to remote from every vertex to home. This would take about 400 time total depending on the order you do remotes. Your score would be about 90.47.

Try to see how if you follow the students' opinions, you can learn more and get a higher score.

## Algorithm Design
1. 	Because we know every vertex has a Guavabot, we can always keep track of their locations and thus we do not have to call scout at all. We use Kruskal’s algorithm to find an MST T of G. Then consider T as unweighted and run DFS on T starting from H and keep track of the “prev” pointers. Call remote on edge (u, v) where u is in the reversed linearization order and v is the vertex referred by u’s prev pointer.  
 
2. 	In this more general case, we know the locations of each Guavabot. Similarly, we do not need to call scout. It is best to avoid exploiting new edges and use only the “inevitable” edges. An “inevitable” edge is defined as an edge on which we have to call remote no matter where the other bots are located at. Intuitively, we want to herd every bot in the neighborhood to a specific vertex, then send the entire butch of bots to the next vertex and repeat the process until they reach home. We run Prim’s Algorithm with a modified priority queue to find an MST T of G. We prioritize the edges with vertices that have bots in it. More specifically, suppose there is a cut S such that G is partitioned into S and V-S. (u, v) and (u’, v’) are both minimum weight edges that cross the cuts. Then we prioritize (u, v) if more vertices in {u, v} has bots than vertices in {u’, v’}. Then consider T as unweighted and run DFS on T starting from H and keep track of the “prev” pointers. Call remote on edge (u, v) in the reversed linearization order of u and v is the vertex referred by u’s prev pointer.  
 
3. 	 First, let all the k students scout all the vertices. Then, call remote on the vertices in the order of majority vote, i.e. call remote on the vertex that has been confirmed to be “True” by the most students first, specifically, move the bots from this vertex to its closest neighbor (along the lowest-weight adjacent edge). Meanwhile, we also keep track of the number of bots “n” that have been moved and located so far. Continue the process until n = |L|, by which time we have found all the bots their respective locations. 

4. 
(a) Naive algorithm: proceed with the algorithm in part(1) to move all the bots home. 
Advantage: Easier implementation  
Disadvantage: Significantly longer runtime since we did not take advantage of the possibility of avoiding redundant edges.  

(b) Use the algorithm in part(3) to find the locations of all the bots. Then proceed with the algorithm in part(2) to move them home.  
Advantage: Better runtime since we try to only use the “inevitable” edges and avoid using the redundant ones. Since we also rank the vertices according to the majority vote, we start with the vertex that is most likely to contain a bot. Thereby, we also reduce the total cost of the remote operations as opposed to starting with a random vertex.  
Disadvantage: Harder implementation since we have to call scout multiple times and rank the vertices according to their majority vote. We probably need to construct a priority queue to substantiate the ranking.  
Possible improvements: Use Multiplicative Weights Algorithm or Machine Learning (the one we used in HW12) instead of Majority Vote.  

5. The first algorithm works best if the bots are uniformly and universally distributed. This means that each vertex has one bot from the beginning. Then we can directly apply part(1) without having to worry about where the bots are located at. 
On the other hand, it does not work so well when the bots are scattered around in the graph. In this case, there is no guarantee that the leaf node contains a bot, so it is unnecessary to start the search in the reversed linearization order, which would result in excessive runtime. Besides, the algorithm does not take full advantage of “inevitable” edges, as the priority queue only recognizes the lowest-weight edges, but we should actually avoid using new edges even if they are a little lower-weighted.  

The second algorithm works well if the bots are scattered on the graph. In this case, it is best to locate the vertices first before foolhardily trying to start calling remote right away. In other words, it is better to have an educated guess first.  
It does not work so well when a large portion of bots lie on the vertices which most students tend to lie about. In this case, these vertices would rank relatively low by the majority vote. But in truth, they should be ranked much higher. In other words, the priority queue we constructed is rendered useless and might even backfire. The algorithm also does not work well when there are bots on most of the vertices, in which case it is better to skip step (4) and assume there are bots on every vertex. It is no longer necessary to find out the exact locations since we would not be severely punished if we assume there are bots on every vertex. 


