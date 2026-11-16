
# CMPS 6610 Problem Set 05
## Answers

**Name:** Khoa Le


Place all written answers from `problemset-05.md` here for easier grading.




- **1a. (7 pts)** Shortest shortest path

Done in `main.py`. I use the recursive Dijkstra from class with `helper(visited, frontier)`. Each call pop the smallest thing from the heap. If the vertex is already visited, skip it and recurse. Else I save its (weight, edges), push all its neighbors, and recurse. It stop when the frontier is empty.

The only thing I change from normal Dijkstra is the heap key. Instead of just the weight, it is the pair (weight, number of edges):

```python
heappush(frontier, (weight + w, edges + 1, u))
```

Since Python compare tuples by the first item first, and only look at the second item when the first one is tie. So the first time I pop a vertex, it has the smallest weight, and if there is a tie it has the fewest edges.

Take an example from the test graph, `d` can be reach with weight 7 in three ways: `s-c-d` (2 edges), `s-a-b-d` (3 edges), `s-a-b-c-d` (4 edges). The tie goes to the edge count.

-> $(7, 2)$

- **1b. (4 pts)** Work and span

Work: it is the same as Dijkstra. Every edge push at most one entry into the heap, and each push or pop is $O(\log |E|)$. Comparing a pair is still $O(1)$, so the edge count doesn't change anything.

Span: the heap is one shared thing, so the pushes and pops happen one by one. Nothing run in parallel, so span equals the work.

$$W \in O(|E| \log |E|), \qquad S \in O(|E| \log |E|)$$

- **2a. (3 pts)** Expression tree algorithm with work and span

I go through the expression from left to right with a stack:

1. Literal: make a leaf and push it.
2. Operator: push it.
3. `(`: skip it.
4. `)`: pop the right child, the operator, and the left child. Make a node with the operator as root and the two children under it. Push the node.

At the end there is only one thing left in the stack, which is the root of $T_E$. A constant like `-3` count as one literal.

Work: every symbol is push and pop at most once, $O(1)$ each.

Span: each step need the stack from the step before, so it is a chain and span equals the work.

$$W(n) \in O(n), \qquad S(n) \in O(n)$$

- **2b. (2 pts)** Corresponding arithmetic expression work and span?

I evaluate from the bottom up. A leaf return its value (or the value of the variable). An internal node evaluate its two children in parallel, then apply its operator.

Work: every node is evaluate once with $O(1)$ work.

Span: the two children don't depend on each other, so the critical path only follow one path from the root to a leaf. That is the height $h$ of the tree.

$$W(n) \in O(n), \qquad S(n) \in O(h)$$

If the tree is balanced, $h = O(\log n)$. Worst case like `(((a+b)+c)+d)...` the tree is a chain, so $h = O(n)$.

- **2c. (2 pts)** work/span to update a previously computed value

I keep the value I computed at every node. When one variable change, I update its leaf and then only recompute the nodes on the path from that leaf up to the root. Other nodes keep their saved value, so each node on the path only need one new value from its child.

Work: there are $h$ nodes on the path, $O(1)$ each.

Span: each node need the new value from the node below it, so the path is a chain.

$$W(n) \in O(h), \qquad S(n) \in O(h)$$

So it is $O(\log n)$ for balanced tree and $O(n)$ for the worst case.

- **3a. (2 pts)** Maximum depth of a $d$-ary heap

Since every node has $d$ children, each level has $d$ times more nodes than the level above it. So level $i$ has up to $d^i$ nodes.

The heap fill a level before going to the next one, so with $n$ nodes we need about $d^h = n$, which means $h = \log_d n$.

-> $h \in O(\log_d n)$

- **3b. (3 pts)** Work done by `delete-min` and `insert` operations in a $d$-ary heap.

`insert`: the new element swap up. At each level I only compare it with its parent, so 1 comparison.
$$W_{insert} \in O(\log_d n)$$

`delete-min`: the element swap down. At each level I have to find the smallest of the $d$ children, so $d$ comparisons.
$$W_{delete} \in O(d \log_d n)$$

- **3c. (3 pts)** New bound on the work for Dijkstra's using $d$-ary heap

Dijkstra do one `delete-min` per vertex, so $|V|$ of them. And at most one `insert` per edge, so $|E|$ of them. The heap hold at most $|V|$ entries.

$$W = O(|V| \cdot d \log_d |V| \;+\; |E| \log_d |V|)$$

First part is from the `delete-min`s, second part is from the `insert`s.

- **3d. (3 pts)** What value of $d$ yields an overall running time of $O(|E|)$?

Lets pick $d = |V|^{\epsilon}$, which is the same as $d = |E| / |V|$. Then
$$\log_d |V| = \frac{\log |V|}{\epsilon \log |V|} = \frac{1}{\epsilon}$$
which is a constant. Put it back into 3c:

- `delete-min` part: $|V| \cdot |V|^{\epsilon} \cdot \frac{1}{\epsilon} = \frac{|E|}{\epsilon}$
- `insert` part: $|E| \cdot \frac{1}{\epsilon}$

$$W = O\left(\frac{|E|}{\epsilon}\right)$$

And since $\epsilon$ is a constant,

-> $d = |E|/|V|$ gives $W = O(|E|)$

- **4a. (2 pts)** Consider the following graph with 3 vertices.


Compute $\mathit{APSP}(i, j, k)$ for all $i, j, k$.

From what I understand from the caption, the weights go clockwise, so the edges are directed: $0 \to 2$ (2), $2 \to 1$ (1), $1 \to 0$ (-2). The cycle add up to $1 > 0$, so there is no negative cycle. Also $\mathit{APSP}(i,i,k) = 0$ for every $k$.

(i,j) | k=0 | k=1 | k=2
---|---|---|---
(0,1) | $\infty$ | $\infty$ | 3
(0,2) | 2 | 2 | 2
(1,0) | -2 | -2 | -2
(1,2) | 0 | 0 | 0
(2,0) | $\infty$ | -1 | -1
(2,1) | 1 | 1 | 1

(1,2) at k=0 is 1->0->2, (2,0) at k=1 is 2->1->0, and (0,1) at k=2 is 0->2->1.

- **4b. (3 pts)** Relationship between $\mathit{APSP}(i, j, 1)$ and $\mathit{APSP}(i, j, 2)$.

$\mathit{APSP}(i,j,2)$ is the same as $\mathit{APSP}(i,j,1)$, unless going through vertex 2 make it shorter. If the path go through 2, then it is a path $i \to 2$ plus a path $2 \to j$, and both of them only use vertex 0 and 1.

$$\mathit{APSP}(i,j,2) = \min\big(\mathit{APSP}(i,j,1),\ \mathit{APSP}(i,2,1) + \mathit{APSP}(2,j,1)\big)$$

Same thing for one level down:

$$\mathit{APSP}(i,j,1) = \min\big(\mathit{APSP}(i,j,0),\ \mathit{APSP}(i,1,0) + \mathit{APSP}(1,j,0)\big)$$

Check with the table: $\mathit{APSP}(0,1,2) = \min(\infty,\ 2 + 1) = 3$.

- **4c. (3 pts)** Optimal substructure property for $\mathit{APSP}(i, j, k).$

$$\mathit{APSP}(i,j,k) = \min\big(\mathit{APSP}(i,j,k-1),\ \mathit{APSP}(i,k,k-1) + \mathit{APSP}(k,j,k-1)\big)$$

Base case: $\mathit{APSP}(i,j,-1) = 0$ if $i = j$, $w(i,j)$ if there is an edge, and $\infty$ otherwise.

Proof: look at the shortest path from $i$ to $j$ that only use vertices $0..k$. There are two cases.

Case 1: it doesn't use $k$. Then it only use $0..k-1$, so it is $\mathit{APSP}(i,j,k-1)$.

Case 2: it use $k$. Since there is no negative cycle, it use $k$ only once. So it split into a path $i \to k$ and a path $k \to j$, and both only use $0..k-1$. Each part must be shortest, otherwise I can swap in a shorter one and get a shorter path. So it is $\mathit{APSP}(i,k,k-1) + \mathit{APSP}(k,j,k-1)$.

We don't know which case it is, so take the min.

- **4d. (3 pts)** Number of subproblems and work

There are $n$ choices each for $i$, $j$, and $k$, so we have $n^3$ distinct subproblems. Each one is just a min of two values I already have, so it is $O(1)$.

$$W(n) \in O(n^3)$$

- **4e. (3 pts)** Compare against running Dijkstra $n$ times

Lets calculate running Dijkstra once from every vertex:
$$W = O(|V| \cdot |E| \log |E|)$$

Sparse graph, $|E| = O(n)$: Dijkstra is $O(n^2 \log n)$, which is better than $O(n^3)$.

Dense graph, $|E| = \Theta(n^2)$: Dijkstra is $O(n^3 \log n)$, so the DP is better by a $\log n$ factor.

Also the DP still work with negative edge weights like the graph in 4a, Dijkstra doesn't.

So the DP is better for dense graph or negative weights, but not for sparse graph.

- **5a. (3 pts)** Is a solution to MST guaranteed to be a solution to MMET? Why or why not?

Yes.

Proof: let $T$ be an MST and $e$ the heaviest edge in $T$. Suppose there is another spanning tree $T'$ that has every edge lighter than $e$.

If I remove $e$ from $T$, it split into two parts. $T'$ connect everything, so it has some edge $e'$ that cross between the two parts. Since every edge of $T'$ is lighter than $e$, $w(e') < w(e)$.

Then $T - e + e'$ is a spanning tree with less total weight than $T$. That contradict $T$ being an MST.

Therefore, no spanning tree has a smaller max edge than $T$, so $T$ is an MMET.

-> Yes. But the other way is not true, an MMET doesn't have to be an MST.

- **5b. (2 pts)** Algorithm for the next best tree

The second best tree is not the MST, so it must be missing at least one edge of the MST. So I try removing each MST edge one at a time and find the best tree without it:

```
T = MST(G)                      # Kruskal or Prim
best = None
for each edge e in T:
    T2 = MST(G without e)       # skip if G without e is disconnected
    if best is None or weight(T2) < weight(best):
        best = T2
return best
```

- **5c. (2 pts)** What is the work of your algorithm?

The MST has $|V| - 1$ edges, so the loop run $|V| - 1$ times. Each time Kruskal is $O(|E| \log |E|)$.

$$W = O(|V| \cdot |E| \log |E|)$$
