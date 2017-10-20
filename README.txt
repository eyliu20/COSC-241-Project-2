Team:
eylie20@amherst.edu
crabasa20@amherst.edu

Evaulation function for Q5:
if lose: -500
if win: +500
+= -2/total ghost distance (manhattan)
if there is at least 1 food
+= -1(distance to nearest food + detour distance (2 if there is a wall in the way, 0 otherwise)) * random between 0.5 and 1.5
+= -5(amount of food remaining)
+= -100(number of capsules left)
+= score

We had an issue wherein pacman would get stuck because he was in the "closest" spot but there was a wall preventing him from going nearer to the food
Similarly, we had an issue in which pacman would stand next to a food pellet but not pick it up because that would increase the distance to the nearest food
To fix this problem we implemented the noise function seen above. The randomness ensures that pacman will sometimes take an action that he would normally think suboptimal in these "tie-breaking" scenarios.



Resources used:
Stack overflow for misc. Python-related questions

Time spent on assignment: 11 hours

How hard was the assignment?
0

How much did you learn from the assignment?
1



