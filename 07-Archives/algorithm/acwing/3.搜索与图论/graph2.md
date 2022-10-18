#! https://zhuanlan.zhihu.com/p/548263123
- [搜索与图论Part2](#搜索与图论part2)
  - [单源最短路](#单源最短路)
  - [多源汇最短路](#多源汇最短路)
  - [朴素Dijkstra](#朴素dijkstra)
    - [AcWing 849. Dijkstra求最短路I](#acwing-849-dijkstra求最短路i)
      - [代码实现](#代码实现)
  - [堆优化版Dijkstra](#堆优化版dijkstra)
    - [AcWing 850. Dijkstra求最短路 II ](#acwing-850-dijkstra求最短路-ii-)
      - [代码实现(STL)](#代码实现stl)
      - [代码实现(手写堆)](#代码实现手写堆)
  - [Bellman-Ford](#bellman-ford)
    - [AcWing 853. 有边数限制的最短路  ](#acwing-853-有边数限制的最短路--)
      - [代码实现](#代码实现-1)
  - [SPFA](#spfa)
    - [AcWing 851. spfa求最短路](#acwing-851-spfa求最短路)
      - [代码实现](#代码实现-2)
    - [AcWing 852. spfa判断负环](#acwing-852-spfa判断负环)
      - [代码实现](#代码实现-3)
  - [Floyd](#floyd)
    - [AcWing 851. spfa求最短路](#acwing-851-spfa求最短路-1)


# 搜索与图论Part2

这一节讲的是最短路。

常见的最短路问题，一般分为两大类：

- 单源最短路
- 多源汇最短路

在最短路问题中，源点也就是起点，汇点也就是终点,起点和终点不确定.

## 单源最短路

**单源最短路**，指的是求一个点，到其他所有点的最短距离。（起点是固定的，单一的）

根据是否存在权重为负数的边，又分为两种情况

- 所有边的权重都是正数
通常有两种算法
    - 朴素Dijkstra
    时间复杂度O($n^2$)，其中n是图中点的个数，m是边的个数
    - 堆优化版的Dijkstra
    时间复杂度O(mlogn)
两者孰优孰劣，取决于图的疏密程度（取决于点数n，与边数m的大小关系）。当是稀疏图（n和m是同一级别）时，可能堆优化版的Dijkstra会好一些。当是稠密图时（m和$n^2$是同一级别），使用朴素Dijkstra会好一些。
<br><br>

- 存在权重为负数的边
通常有两种算法
    - Bellman-Ford
    时间复杂度O(nm)
    - SPFA
    时间复杂度一般是O(m)，最差O(nm)，是前者的优化版，但有的情况无法使用SPFA，只能使用前者，比如要求最短路不超过k条边，此时只能用Bellman-Ford

## 多源汇最短路

求多个起点到其他点的最短路。（起点不是固定的，而是多个）

Floyd算法（时间复杂度O($n^3$))

![最短路算法](https://pic4.zhimg.com/80/v2-62fe9c5a4f1c84dd076b38d159d87baf.png)

最短路问题的核心在于，把**问题抽象成一个最短路问题，并建图**。图论相关的问题，不侧重于算法原理，而侧重于对问题的抽象。

Dijkstra基于贪心，Floyd基于动态规划，Bellman-Ford基于离散数学。

算法的选用：通常来说，单源最短路的，如果没有负权重的边，用Dijkstra，有负权重边的，通常用SPFA，极少数用Bellman-Ford；多源最短路的，用Floyd。

## 朴素Dijkstra
稠密图可以认为$n^2$和m一个数量级，稀疏图可以认为n和m一个数量级. 

假设图中一共有n个点，下标为1~n。下面所说的**某个点的距离**，都是指该点到起点（1号点）的距离。

算法步骤如下，用一个集合`s`来存放**最短距离已经确定的点**。

1. **初始化距离**，d[1] = 0， d[i] = +∞。即，将起点的距离初始化为0，而其余点的距离当前未确定，用正无穷表示。

2. 循环1~n
每次从**距离已知**的点中，**选取一个不在s集合中，且距离最短的点**（这一步可以用小根堆来优化），遍历该点的所有出边，更新这些出边所连接的点的距离。并把该次选取的点加入到集合s中，因为该点的最短距离此时已经确定。

3. 当所有点都都被加入到s中，表示全部点的最短距离都已经确定完毕

注意某个点的**距离已知**，并不代表此时**这个点的距离**就是最终的最短距离。在后续的循环中，可能用一条更短距离的路径，去更新。

图解：
1. 用一个 dist 数组保存源点到其余各个节点的距离，dist[i] 表示源点到节点 i 的距离。初始时，dist 数组的各个元素为无穷大。
用一个状态数组 state 记录是否找到了源点到该节点的最短距离，state[i] 如果为真，则表示找到了源点到节点 i 的最短距离，state[i] 如果为假，则表示源点到节点 i 的最短距离还没有找到。初始时，state 各个元素为假。
![step1](https://pic4.zhimg.com/80/v2-474708b34a04c100b118b75edeca5b03.png)

2. 源点到源点的距离为 0。即dist[1] = 0。
![step2](https://pic4.zhimg.com/80/v2-2b1a59af93f20c9e8780292e729c742d.png)

3. 遍历 dist 数组，找到一个节点，这个节点是：没有确定最短路径的节点中距离源点最近的点。假设该节点编号为 i。此时就找到了源点到该节点的最短距离，state[i] 置为 1。
![Image](https://pic4.zhimg.com/80/v2-e983890c52dfb462ab18659fa3b8ca9a.png)

4. 遍历 i 所有可以到达的节点 j，如果 dist[j] 大于 dist[i] 加上 i -> j 的距离，即 dist[j] > dist[i] + w[i][j]（w[i][j] 为 i -> j 的距离） ，则更新 dist[j] = dist[i] + w[i][j]。
![Image](https://pic4.zhimg.com/80/v2-ca431768be071cba701554d41fb34436.png)

5. 重复 3 4 步骤，直到所有节点的状态都被置为 1。
![Image](https://pic4.zhimg.com/80/v2-976fae501800036e6628235ca97beb45.png)

6. 此时 dist 数组中，就保存了源点到其余各个节点的最短距离。
![Image](https://pic4.zhimg.com/80/v2-882b67a60cc14da46d1f1c633c128880.png)


### [AcWing 849. Dijkstra求最短路I](https://www.acwing.com/problem/content/851/) 

#### 代码实现
这题是一个稠密图，用邻接矩阵写.
```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;
const int N = 510;
const int INF = 0x3f3f3f3f; // 正无穷
int g[N][N]; // 稠密图采用邻接矩阵存储
int d[N]; // 距离
int n, m;
bool visited[N];

int dijkstra() {
	d[1] = 0;
	// 每次
	for(int i = 1; i <= n; i++) {
		//找到一个距起点距离最小的点
		int t = 0; // d[0]未被使用, 其值一直是 INF
		for(int j = 1; j <= n; j++) {
			if(!visited[j] && d[j] < d[t]) {
				t = j;
			}
		}
		if(t == 0) break; // 未找到一个点, 提前break
		// 找到该点
		visited[t] = true; // 放入集合s
		// 更新其他所有点的距离
		for(int j = 1; j <= n; j++) {
			d[j] = min(d[j], d[t] + g[t][j]);
		}
	}
	if(d[n] == INF) return -1;
	else return d[n];
}

int main() {
	// 初始化
	memset(d, 0x3f, sizeof d);
	memset(g, 0x3f, sizeof g);
	scanf("%d%d", &n, &m);
	while(m--) {
		int x, y, z;
		scanf("%d%d%d", &x, &y, &z);
		g[x][y] = min(g[x][y], z); // 重复边只需要保留一个权重最小的即可
	}
	printf("%d", dijkstra());
	return 0;
}

```

## 堆优化版Dijkstra

堆优化版的dijkstra是对朴素版dijkstra进行了优化，在朴素版dijkstra中时间复杂度最高的寻找距离
最短的点$O(n^2)$可以使用最小堆优化。
1. 一号点的距离初始化为零，其他点初始化成无穷大。
2. 将一号点放入堆中。
3. 不断循环，直到堆空。每一次循环中执行的操作为：
    弹出堆顶（与朴素版diijkstra找到S外距离最短的点相同，并标记该点的最短路径已经确定）。
    用该点更新临界点的距离，若更新成功就加入到堆中。

每次循环寻找路径最短的点：$O(n)$ 
加入集合S：$O(n)$
更新邻接的所有边:$O(m)$  ->  更新距离：$O(mlogn)$


堆可以自己手写（用数组模拟），也可以使用现成的（C++的STL提供了priority_queue，`priority_queue<PII, vector<PII>, greater<PII>> heap`,Java的JDK中提供了PriorityQueue）
STL可能有冗余，自己实现没有冗余

特别注意，插入堆的操作，由于更新距离时，可能对一些距离已知的点进行更新（更新为更小的距离），此时不能因为这个点已经在堆中就不进行插入了，因为其距离已经变了，堆中原有的节点已经无效了，按理说，应该修改堆中对应节点的距离值，然后做调整，实际上，可以直接插入一个新的节点（此时对于同一个节点，堆中有两份），但没有关系，堆中的重复节点不会影响最终的结果。

### [AcWing 850. Dijkstra求最短路 II ](https://www.acwing.com/problem/content/852/) 

#### 代码实现(STL)
```cpp
#include<iostream>
#include<cstring>
#include<queue>

using namespace std;

typedef pair<int, int> PII;

const int N = 150010; // 把N改为150010就能ac

// 稀疏图用邻接表来存
int h[N], e[N], ne[N], idx;
int w[N]; // 用来存权重
int dist[N];
bool st[N]; // 如果为true说明这个点的最短路径已经确定

int n, m;

void add(int x, int y, int c)
{
    // 有重边也不要紧，假设1->2有权重为2和3的边，再遍历到点1的时候2号点的距离会更新两次放入堆中
    // 这样堆中会有很多冗余的点，但是在弹出的时候还是会弹出最小值2+x（x为之前确定的最短路径），
    // 并标记st为true，所以下一次弹出3+x会continue不会向下执行。
    w[idx] = c;
    e[idx] = y;
    ne[idx] = h[x]; 
    h[x] = idx++;
}

int dijkstra()
{
    memset(dist, 0x3f, sizeof(dist));
    dist[1] = 0;
    priority_queue<PII, vector<PII>, greater<PII>> heap; // 定义一个小根堆
    // 这里heap中为什么要存pair呢，首先小根堆是根据距离来排的，所以有一个变量要是距离，
    // 其次在从堆中拿出来的时候要知道知道这个点是哪个点，不然怎么更新邻接点呢？所以第二个变量要存点。
    heap.push({ 0, 1 }); // 这个顺序不能倒，pair排序时是先根据first，再根据second，这里显然要根据距离排序
    while(heap.size())
    {
        PII k = heap.top(); // 取不在集合S中距离最短的点
        heap.pop();
        int ver = k.second, distance = k.first;

        if(st[ver]) continue;//之前处理过了，现在是冗余备份
        st[ver] = true;

        for(int i = h[ver]; i != -1; i = ne[i])
        {
            int j = e[i]; // i只是个下标，e中在存的是i这个下标对应的点。
            if(dist[j] > distance + w[i])
            {
                dist[j] = distance + w[i];
                heap.push({ dist[j], j });
            }
        }
    }
    if(dist[n] == 0x3f3f3f3f) return -1;
    else return dist[n];
}

int main()
{
    memset(h, -1, sizeof(h));
    scanf("%d%d", &n, &m);

    while (m--)
    {
        int x, y, c;
        scanf("%d%d%d", &x, &y, &c);
        add(x, y, c);
    }

    cout << dijkstra() << endl;

    return 0;
}
```



#### 代码实现(手写堆)

```cpp
#include <iostream>
#include <cstring>
using namespace std;

const int N = 1e6+10, INF = 0x3f3f3f3f;

int h[N], e[N], w[N], ne[N], idx;

int d[N];

int hPos[N], hDis[N], hSize;

bool st[N];

int n, m, x, y, z;

void add(int x, int y, int z) {
	e[idx] = y;
	w[idx] = z;//权重
	ne[idx] = h[x];
	h[x] = idx++;
}

void heap_swap(int i, int j) {
	swap(hPos[i], hPos[j]);
	swap(hDis[i], hDis[j]);
}

void up(int pos) {
	while(pos > 1 && hDis[pos / 2] > hDis[pos]) {
		heap_swap(pos / 2, pos);
		pos /= 2;
	}
}

void down(int pos) {
	int mx = pos;
	if(2 * pos <= hSize && hDis[2 * pos] < hDis[mx]) mx = 2 * pos;
	if(2 * pos + 1 <= hSize && hDis[2 * pos + 1] < hDis[mx]) mx = 2 * pos + 1;
	if(mx != pos) {
		heap_swap(mx, pos);
		down(mx);
	}
}

void insert_to_heap(int x, int dis) {
	hSize++;
	hPos[hSize] = x;
	hDis[hSize] = dis;
	up(hSize);
}

void dijkstra() {
	d[1] = 0;
	insert_to_heap(1, 0);

	// 当堆非空时，执行
	while(hSize > 0) {
		int x = hPos[1];
		heap_swap(1, hSize--);
		down(1);
		if(st[x]) continue; // 由于堆中可能存在重复的节点, 需要判断, 否则会超时
		st[x] = true; // 拿出来后, 该点的距离就已经确定
		for(int j = h[x]; j != -1; j = ne[j]) {
			int u = e[j];
			if(d[u] > d[x] + w[j]) {
				d[u] = d[x] + w[j];
				insert_to_heap(u, d[u]);
			}
		}
	}
}

int main() {
	memset(h, -1, sizeof h);//邻接表表头初始化
	memset(d, 0x3f, sizeof d);
	scanf("%d%d", &n, &m);
	while(m--) {
		scanf("%d%d%d", &x, &y, &z);
		add(x, y, z);//邻接表不需要对重边进行特殊处理
	}
	dijkstra();
	if(d[n] == INF) printf("-1");
	else printf("%d", d[n]);
}
```
## Bellman-Ford


循环k次(k < n-1，因为在一个含有n个顶点的图中，任意两点之间的最短路径最多包含n-1边。)
每次循环，遍历图中所有的边。对每条边`(a, b, w)`，（指的是从a点到b点，权重是w的一条边）更新`d[b] = min(d[b], d[a] + w)`

（bellman-ford不一定需要用邻接表存储，可以定义一个类，或者C++里面的结构体，存储a，b，w。表示存在一条边a点指向b点，权重为w）。则遍历所有边时，只要遍历全部的结构体数组即可

循环的次数的含义：假设循环了k次，则表示，从起点，经过不超过k条边，走到每个点的最短距离。

该算法能够保证，在循环n次后，对所有的边`(a, b, w)`，都满足`d[b] <= d[a] + w`。这个不等式被称为**三角不等式**。上面的更新操作称为**松弛操作**。

该算法适用于有负权边的情况。

**注意：如果有负权回路的话，最短路就不一定存在了。**（注意是不一定存在）。当这个负权回路处于1号点到n号点的路径上，则每沿负权回路走一圈，距离都会减少，则可以无限走下去，1到n的距离就变得无限小（负无穷），此时1号点到n号点的最短距离就不存在。而如果负权回路不在1号点到n号点的路径上，则1到n的最短距离仍然存在。

该算法可以求出来，图中是否存在负权回路。如果迭代到第n次，还会进行更新，则说明存在一条最短路，路径上有n条边，n条边则需要n + 1个点，而由于图中一共只有n个点，所以这n + 1个点中一定有2个点是同一个点，则说明这条路径上有环；有环，并且此次进行了更新，说明这个环的权重是负的（只有更新后总的距离变得更小，才会执行更新）。

但求解负权回路，通常用SPFA算法，而不用Bellman-Ford算法，因为前者的时间复杂度更低。

由于循环了k次，每次遍历所有边（m条边）。故Bellman-Ford算法的时间复杂度是$O(k×m)$。

### [AcWing 853. 有边数限制的最短路  ](https://www.acwing.com/problem/content/855/) 

#### 代码实现
```cpp
#include<iostream>
#include<cstring>
using namespace std;

const int N = 510, M = 10010;
const int INF = 0x3f3f3f3f;
struct Edge
{
	int a, b, w;
} edge[M]; // 直接用结构体来存储全部边

int n, m, k, d[N], tmp[N];

void bellman_ford() {
	memset(d, 0x3f, sizeof d);
	d[1] = 0; // 初始化
	for(int i = 0; i < k; i++) {
		memcpy(tmp, d, sizeof d); // 需要备份,tmp存储上一次迭代的结果
		for(int j = 0; j < m; j++) {
			Edge e = edge[j];
			int a = e.a, b = e.b, w = e.w;
			if(tmp[a] == INF) continue;//这样后面不用d[n] > INF / 2判断，直接==INF即可
			d[b] =min(d[b],tmp[a] + w) ;
                // 用备份的tmp来进行计算, 以防出现串联更新的情况
                // 串联更新虽然不影响最终的最短距离, 但会影响[经过不超过k条边的最短距离]这个语义
                // 比如在外层循环进行了2次时, 此时应当找到了从起点到其他点,经过不超过2条边的最短距离
                // 而如果串联更新的话, 可能在这第2次循环时, 已经更新了多次, 得到的最短距离是经过了3条边的最短距离
                
                // 另外, 上面的if中应该用 d[b] > tmp[a] + w
                // 而不应当用 tmp[b] > tmp[a] + w
                // 当a和b之间存在重边时, 若使用后者作为条件, 则无法取到a,b之间权重最小的那条边
				// 更新

		}
	}
	if(d[n] == INF) //如果上面不判断rmp[a]==INF,这里写成d[n] > INF/2
    printf("impossible"); 
	else printf("%d", d[n]);
}

int main() {
	scanf("%d%d%d", &n, &m, &k);
	for(int i = 0; i < m; i++) {
		int x, y, z;
		scanf("%d%d%d", &x, &y, &z);
		edge[i] = {x, y, z};
	}
	bellman_ford();
	return 0;
}
```

## SPFA

若要使用SPFA算法，一定要求**图中不能有负权回路**。只要图中没有负权回路，都可以用SPFA，这个算法的限制是比较小的。

SPFA其实是对Bellman-Ford的一种优化。

它优化的是这一步：`d[b] = min(d[b], d[a] + w)`

我们观察可以发现，只有当`d[a]`变小了，才会在下一轮循环中更新`d[b]`

考虑用BFS来做优化。用一个队列queue，来存放距离变小的节点。（当图中存在负权回路时，队列永远都不会为空，因为总是会存在某个点，在一次松弛操作后，距离变小）

（和Dijkstra很像）

SPFA的好处：能解决无负权边的问题，也能解决有负权边的问题，并且效率还比较高。但是当需要求在走不超过k条边的最短路问题上，就只能用Bellman-Ford算法了。

**明确一下松弛的概念。**

- 考虑节点u以及它的邻居v，从起点跑到v有好多跑法，有的跑法经过u，有的不经过。

- 经过u的跑法的距离就是distu+u到v的距离。

- 所谓松弛操作，就是看一看distv和distu+u到v的距离哪个大一点。

- 如果前者大一点，就说明当前的不是最短路，就要赋值为后者，这就叫做松弛。

**spfa算法文字说明：**

- 建立一个队列，初始时队列里只有起始点。

- 再建立一个数组记录起始点到所有点的最短路径（该表格的初始值要赋为极大值，该点到他本身的路径赋为0）。

- 再建立一个数组，标记点是否在队列中。

- 队头不断出队，计算始点起点经过队头到其他点的距离是否变短，如果变短且被点不在队列中，则把该点加入到队尾。

- 重复执行直到队列为空。

- 在保存最短路径的数组中，就得到了最短路径。

**spfa图解**
- 给定一个有向图，如下，求A~E的最短路。
![Image](https://pic4.zhimg.com/80/v2-55900264cf4835c7f83c4f721c402d94.png)

- 源点A首先入队，然后A出队，计算出到BC的距离会变短，更新距离数组，BC没在队列中，BC入队
![Image](https://pic4.zhimg.com/80/v2-e6ae20b723ff87140536531e0477af15.png)

- B出队，计算出到D的距离变短，更新距离数组，D没在队列中，D入队。然后C出队，无点可更新。
![Image](https://pic4.zhimg.com/80/v2-6d02e1218521806364524f36282f4fea.png)

- D出队，计算出到E的距离变短，更新距离数组，E没在队列中，E入队。
![Image](https://pic4.zhimg.com/80/v2-974b3ea609cc5b36d0e56d114c75aa3f.png)

- E出队，此时队列为空，源点到所有点的最短路已被找到，A->E的最短路即为8
![Image](https://pic4.zhimg.com/80/v2-b9525b8576ea432d6894c181c80244e4.png)

### [AcWing 851. spfa求最短路](https://www.acwing.com/problem/content/853/) 

#### 代码实现
手写队列
```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;

const int N = 1e5 + 10;

const int INF = 0x3f3f3f3f;

int h[N], e[N], w[N], ne[N], idx;

int n, m;

int d[N];

int q[N], hh, tt = -1;

bool st[N];

void add(int a, int b, int c) {
    e[idx] = b;
    w[idx] = c;
    ne[idx] = h[a];
    h[a] = idx++;
}


void spfa() {
    memset(d, 0x3f, sizeof d);
    d[1] = 0;
    q[++tt] = 1;
    st[1] = true;
    while(tt >= hh) {
        int u = q[hh++];
        st[u] = false;
        for(int i = h[u]; i != -1; i = ne[i]) {
            int j = e[i];
            if(d[j] > d[u] + w[i]) {
                d[j] = d[u] + w[i];
                if(!st[j]) {
                    // 为了防止已在队列中的点, 被重复添加进队列
                    // 虽然不影响最终结果, 但会拖慢一点性能
                    st[j] = true;
                    q[++tt] = j;
                }
            }
        }
    }
}

int main() {
    memset(h, -1, sizeof h);
    scanf("%d%d", &n, &m);
    while(m--) {
        int x, y, z;
        scanf("%d%d%d", &x, &y, &z);
        add(x, y, z);
    }
    spfa();
    if(d[n] != INF) printf("%d", d[n]);
    else printf("impossible");
    return 0;
}

```
STL队列
```cpp
#include <cstring>
#include <iostream>
#include <algorithm>
#include <queue>

using namespace std;

const int N = 100010;

int n, m;
int h[N], w[N], e[N], ne[N], idx;
int dist[N];
bool st[N];

void add(int a, int b, int c)
{
    e[idx] = b, w[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
}

int spfa()
{
    memset(dist, 0x3f, sizeof dist);
    dist[1] = 0;

    queue<int> q;
    q.push(1);
    st[1] = true;

    while (q.size())
    {
        int t = q.front();
        q.pop();

        st[t] = false;

        for (int i = h[t]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (dist[j] > dist[t] + w[i])
            {
                dist[j] = dist[t] + w[i];
                if (!st[j])
                {
                    q.push(j);
                    st[j] = true;
                }
            }
        }
    }

    return dist[n];
}

int main()
{
    scanf("%d%d", &n, &m);

    memset(h, -1, sizeof h);

    while (m -- )
    {
        int a, b, c;
        scanf("%d%d%d", &a, &b, &c);
        add(a, b, c);
    }

    int t = spfa();

    if (t == 0x3f3f3f3f) puts("impossible");
    else printf("%d\n", t);

    return 0;
}
```



判断负权回路：
`dist[x]:` 起点到x的最短距离
`cnt[x]:`起点到x经过的边数
每次更新`dist[x] = dist[t] + w[i]`时同时更新`cnt[t] = cnt[t} + 1`
当`cnt[x] >= n`时意味着从1到x经过n条边和n+1个点，又抽屉原理知至少存在两个点相同，所以路径上存在一个环，且这个环一定是因为变小导致的，所以是一个负权回路.

### [AcWing 852. spfa判断负环](https://www.acwing.com/problem/content/854/) 

基本思路是，添加一个变量int ctn[N]，来记录走到第i个点所经过的边的长度即可，如果走到某个点的边的个数大于n，则说明存在负权回路。题解思路可以参考https://www.acwing.com/solution/content/6336/。由于是求是否存在负环，而不是求从1号点能够走到的负权回路，所以我们要把全部点加入到队列。可以这样理解，在原图的基础上新建一个虚拟源点，从该点向其他所有点连一条权值为0的有向边。那么原图有负环等价于新图有负环。此时在新图上做spfa，将虚拟源点加入队列中。然后进行spfa的第一次迭代，这时会将所有点的距离更新并将所有点插入队列中。执行到这一步，就等价于下面代码的做法了。
(可以想象原来的图是一个二维的图，现在出现了一个三维的点和其他所有点相连，且距离为0)
#### 代码实现

```cpp
#include <cstring>
#include <iostream>
#include <algorithm>
#include <queue>

using namespace std;

const int N = 2010, M = 10010;

int n, m;
int h[N], w[M], e[M], ne[M], idx;
int dist[N], cnt[N];
bool st[N];

void add(int a, int b, int c)
{
    e[idx] = b, w[idx] = c, ne[idx] = h[a], h[a] = idx ++ ;
}

bool spfa()
{
    queue<int> q;

    for (int i = 1; i <= n; i ++ )
    {
        st[i] = true;
        q.push(i);
    }

    while (q.size())
    {
        int t = q.front();
        q.pop();

        st[t] = false;

        for (int i = h[t]; i != -1; i = ne[i])
        {
            int j = e[i];
            if (dist[j] > dist[t] + w[i])
            {
                dist[j] = dist[t] + w[i];
                cnt[j] = cnt[t] + 1;

                if (cnt[j] >= n) return true;
                if (!st[j])
                {
                    q.push(j);
                    st[j] = true;
                }
            }
        }
    }

    return false;
}

int main()
{
    scanf("%d%d", &n, &m);

    memset(h, -1, sizeof h);

    while (m -- )
    {
        int a, b, c;
        scanf("%d%d%d", &a, &b, &c);
        add(a, b, c);
    }

    if (spfa()) puts("Yes");
    else puts("No");

    return 0;
}
```
这道题用Bellman-Ford来做可以过，思路更简单
```cpp
#include<iostream>
#include<cstring>
using namespace std;

const int N = 1e5;

int n, m;

struct Edge {
    int a, b, w;
} edges[N];

int d[N], tmp[N];


bool bellman_ford() {
    for(int i = 1; i <= n; i++) {
        memcpy(tmp, d, sizeof d);
        for(int j = 0; j < m; j++) {
            Edge e = edges[j];
            int a = e.a, b = e.b, w = e.w;
            if(d[b] > tmp[a] + w) {
                d[b] = tmp[a] + w;
                if(i == n) return true;
            }
        }
    }
    return false;
}

// bellman-ford判断负环
int main() {
    scanf("%d%d", &n, &m);
    for(int i = 0; i < m; i++) {
        int x, y, z;
        scanf("%d%d%d", &x, &y, &z);
        edges[i] = {x, y, z};
    }
    if(bellman_ford()) printf("Yes");
    else printf("No");
    return 0;
}
```

## Floyd

求解多源汇最短路问题，也能处理边权为负数的情况，但是无法处理存在负权回路的情况。

使用邻接矩阵来存储图。初始使用`d[i][j]`来存储这个图，存储所有的边

算法思路：三层循环

```cpp
for(k = 1; k <= n; k++)

​ for(i = 1; i <= n; i++)

​ for(j = 1; j <= n; j++)

​ d[i,j] = min(d[i,j] , d[i,k] + d[k,j])
```

循环结束后，`d[i][j]`存的就是点i到j的最短距离。

原理是基于动态规划。

其状态表示是：d(k, i, j)，从点i，只经过1 ~ k这些中间点，到达点j的最短距离

状态转移:`d(k,i,j) = min(d[k-1][i][j],d(k-1,i,k) + d(k-1,k,j))`，这里只用到上一层的K,类比背包问题的动态数组优化，这里K也可以用动态数组优化掉

### [AcWing 851. spfa求最短路](https://www.acwing.com/problem/content/853/) 

```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;

const int N = 210, INF = 0x3f3f3f3f;
int g[N][N]; // 邻接矩阵存储
int n, m, k;

void floyd() {
	for(int p = 1; p <= n; p++) {
		for(int i = 1; i <= n; i++) {
			for(int j = 1; j <= n; j++) {
				if(g[i][p] != INF && g[p][j] != INF) g[i][j] = min(g[i][j], g[i][p] + g[p][j]);
			}
		}
	}
}

int main() {
	scanf("%d%d%d", &n, &m, &k);
	for(int i = 1; i <= n; i++) {
		for(int j = 1; j <= n; j++) {
			if(i == j) g[i][j] = 0;
			else g[i][j] = INF;
		}
	}
	while(m--) {
		int x, y, z;
		scanf("%d%d%d", &x, &y, &z);
		g[x][y] = min(g[x][y], z); // 处理重边
	}
	floyd();
	while(k--) {
		int x, y;
		scanf("%d%d", &x, &y);
		if(g[x][y] == INF) printf("impossible\n");
		else printf("%d\n", g[x][y]);
	}
	return 0;
}

```
