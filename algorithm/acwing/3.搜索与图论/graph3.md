- [搜索与图论Part3](#搜索与图论part3)
  - [最小生成树](#最小生成树)
    - [朴素版Prim](#朴素版prim)
      - [AcWing 858. Prim算法求最小生成树](#acwing-858-prim算法求最小生成树)
        - [代码实现](#代码实现)
    - [Kurskal](#kurskal)
      - [AcWing 859. Kruskal算法求最小生成树](#acwing-859-kruskal算法求最小生成树)
        - [代码实现](#代码实现-1)
  - [二分图](#二分图)
    - [染色法](#染色法)
      - [AcWing 860. 染色法判定二分图](#acwing-860-染色法判定二分图)
        - [代码实现](#代码实现-2)
    - [匈牙利算法](#匈牙利算法)
      - [AcWing 861. 二分图的最大匹配](#acwing-861-二分图的最大匹配)
        - [代码实现](#代码实现-3)

# 搜索与图论Part3
这一节讲解的是最小生成树和二分图

##  最小生成树
什么是最小生成树？首先，给定一个节点数是n，边数是m的无向连通图G。

则由全部的n个节点，和n-1条边构成的无向连通图被称为G的一颗生成树，在G的所有生成树中，边的权值之和最小的生成树，被称为G的最小生成树。

有两种常用算法：

- Prim算法（普利姆）
    - 朴素版Prim（时间复杂度$O(n^2)$，适用于稠密图）
    - 堆优化版Prim（时间复杂度$O(mlogn)$，适用于稀疏图,用的少）

- Kruskal算法（克鲁斯卡尔）
  适用于稀疏图，时间复杂度$O(mlogm)$

![最小生成树](https://pic4.zhimg.com/80/v2-9d59b41a5f22dce72fdac8614625ed6a.png)
对于最小生成树问题，如果是稠密图，通常选用朴素版Prim算法，因为其思路比较简洁，代码比较短，如果是稀疏图，通常选用Kruskal算法，因为其思路比Prim简单清晰。堆优化版的Prim通常不怎么用。

### 朴素版Prim
其算法流程如下,（其中用集合s表示，当前已经在连通块中的所有的点）
```c++
1. 初始化距离, 将所有点的距离初始化为+∞
2. n次循环
  1. t <- 找到不在集合s中, 且距离最近的点
  2. 用t来更新其他点到集合s的距离
  3. 将t加入到集合s中

```
注意，一个点t到集合s的距离，指的是：若点t和集合s中的3个点有边相连。则点t到集合s的距离就是，t与3个点相连的边中，权重最小的那条边的权重。 

#### [AcWing 858. Prim算法求最小生成树](https://www.acwing.com/problem/content/860/)

##### 代码实现
```c++
#include<iostream>
#include<cstring>
using namespace std;
const int N = 510, INF = 0x3f3f3f3f;
int n, m;
int g[N][N], d[N];
bool visited[N];

void prim() {
	memset(d, 0x3f, sizeof d); // 初始化距离为正无穷
	int sum = 0;
	for(int i = 1; i <= n; i++) {
		// 循环n次
		// 选出距离集合s最小的点
		int t = 0;
		for(int j = 1; j <= n; j++) {
			if(!visited[j] && d[j] <= d[t]) t = j; // 这里用<=, 可以避免对第一次选点做特判
		}
		if(i == 1) d[t] = 0;// 第一次加入集合的点, 其到集合的距离为0
		if(d[t] == INF) {
		    // 选中的点距离是正无穷, 无效
		    printf("impossible\n");
		    return;
		}
		// 把这个点放到集合s里
		visited[t] = true; 
		sum += d[t]; // 这次放进来的
		// 更新其他点到集合s的距离, 
		for(int j = 1; j <= n; j++) {
			if(!visited[j] && g[t][j] != INF && g[t][j] < d[j]) 
			    d[j] = g[t][j];
		}
	}
	printf("%d\n", sum);
}

int main() {
	memset(g, 0x3f, sizeof g);
	scanf("%d%d", &n, &m);
	while(m--) {
		int x, y, w;
		scanf("%d%d%d", &x, &y, &w);
		g[x][y] = min(g[x][y], w);
		g[y][x] = g[x][y];
	}
	prim();
	return 0;
}
```

### Kurskal
其算法流程如下
```c++
1. 先将所有边，按照权重，从小到大排序(算法瓶颈O(mlogm))

2. 从小到大枚举每条边(a，b，w)
    若a，b不连通，则将这条边，加入集合中（将a点和b点连接起来）

3. 直到所有节点连通，算法结束

```
Kruskal算法初始时，相当于所有点都是独立的，没有任何边。

Kruskal不需要用邻接表或者邻接矩阵来存图，只需要存所有边就可以了

其实就是并查集的简单应用，kruskal的算法流程中，为了确定2个点是否处于同一连通块，需要用到并查集。
可以参考[acwing-837: 连通块中点的数量](https://www.acwing.com/problem/content/839/)

#### [AcWing 859. Kruskal算法求最小生成树](https://www.acwing.com/problem/content/861/)

##### 代码实现
```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;
const int N = 1e5 + 10, M = 2e5 + 10;

struct Edge {
	int a, b, w;
	bool operator < (const Edge& W) {
		return w < W.w;
	}
} edges[M];

int n, m;
int p[N];//并查集的数组

int find(int x) {
	if(x != p[x]) p[x] = find(p[x]);
	return p[x];
}

void kruskal() {
	// 先对所有边从小到大排序
	sort(edges, edges + m);
	int totalW = 0, edgeCtn = 0;
	// 枚举全部边
	for(int i = 0; i < m; i++) {
		int a = edges[i].a, b = edges[i].b, w = edges[i].w;
		a = find(a); //a等于a的祖宗节点
		b = find(b);
		if(a != b) {
			// 若a和b两个祖宗节点不连通不连通, 则加入这条边
			p[a] = b; // 将a和b连通
			totalW += w;
			edgeCtn++;
		}
	}
	if(edgeCtn == n - 1) printf("%d\n", totalW);
	else printf("impossible\n");
}

int main() {
	scanf("%d%d", &n, &m);
	for(int i = 0; i < m; i++) {
		int a, b, w;
		scanf("%d%d%d", &a, &b, &w);
		edges[i] = {a, b, w};
	}

	for(int i = 1; i <= n; i++) p[i] = i;

	kruskal();

	return 0;
}

```

##  二分图
二分图指的是，可以将一个图中的所有点，分成左右两部分，使得图中的所有边，都是从左边集合中的点，连到右边集合中的点。而左右两个集合内部都没有边。图示如下
![二分图](https://pic4.zhimg.com/80/v2-67d4630234d233d0481784dfb81bdf5f.png)

这一节讲了2部分内容，分别**是染色法**和**匈牙利算法**。

- 染色法
  判断是否是二分图，通过深度优先遍历实现，时间复杂度是$O(n×m)$；
- 匈牙利算法
  计算二分图的最大匹配，时间复杂度理论上是$O(n×m)$，但实际运行时间一般远小于$O(n×m)$。

![二分图](https://pic4.zhimg.com/80/v2-1f231da46e9d8e48189e27c42b5de363.png)

图论中的一个重要性质：**一个图是二分图，当且仅当图中不含奇数环**

奇数环，指的是这个环中边的个数是奇数。（环中边的个数和点的个数是相同的）

在一个环中，假设共有4个点（偶数个），由于二分图需要同一个集合中的点不能互相连接。

则1号点属于集合A，1号点相连的2号点就应当属于集合B，2号点相连的3号点应当属于集合A，3号点相连的4号点应当属于集合B。4号点相连的1号点应当属于集合A。这样是能够二分的。

而若环中点数为奇数，初始时预设1号点属于集合A，绕着环推了一圈后，会发现1号点应当属于集合B。这就矛盾了。所以存在奇数环的话，这个图一定无法二分。

可以用染色法来判断一个图是否是二分图，使用深度优先遍历，从根节点开始把图中的每个节点都染色，每个节点要么是黑色要么是白色（2种），只要染色过程中没有出现矛盾，说明该图是一个二分图，否则，说明不是二分图。（由于图中不含奇数环，所以染色过程中一定没有矛盾）

### 染色法


#### [AcWing 860. 染色法判定二分图](https://www.acwing.com/problem/content/862/)

##### 代码实现
```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;
const int N = 1e5 + 10, M = 2e5 + 10; // 由于是无向图, 需要建两条边, 所以边数设为2倍
// 使用邻接表来存储图
int h[N], e[M], ne[M], idx; // 注意这里单链表的实现, 数组大小开为M

int n, m;
int color[N];

void add(int x, int y) {
	// 链表的头插法
	e[idx] = y;
	ne[idx] = h[x];
	h[x] = idx++;
}

bool dfs(int x) {
	// 深搜这个节点的全部子节点
	for(int i = h[x]; i != -1; i = ne[i]) {
		int u = e[i]; // 子节点
		if(color[u] == -1) {
			// 子节点还未染色, 则直接染色, 并深搜
			color[u] = !color[x];
			if(!dfs(u)) return false;
		} else if(color[u] == color[x]) return false; // 若子节点和父节点颜色一致, 则说明矛盾, 自环应该也算矛盾?
	}
	// 深搜结束, 未出现矛盾, 则染色成功, 判定是二分图
	return true;
}

int main() {
	memset(h, -1, sizeof h); // 初始化空链表
	memset(color, -1, sizeof color); // 颜色初始化为-1, 表示还未染色
	scanf("%d%d", &n, &m);
	while(m--) {
		int x, y;
		scanf("%d%d", &x, &y);
		add(x, y);
		add(y, x);
	}
	bool flag = true;
	// 依次对所有点进行染色
	for(int i = 1; i <= n; i++) {
		if(color[i] == -1) {
			// 该点还未染色, 则直接染色, 随便染一个色即可(0或1), 并dfs, dfs完成后, 就对这个点所在的连通块都染上了色
			color[i] = 0;
			// 进行dfs, 若在对这个连通块染色的过程中出现矛盾, 则直接break
			if(!dfs(i)) {
				flag = false;
				break;
			}
		}
	}
	if(flag) printf("Yes\n");
	else printf("No\n");
	return 0;
}

```

由于染色的本质是遍历图，所以除了dfs，也可以用bfs来做，但是需要注意，bfs中的队列，存的是一个<点的编号，点颜色>这样的二元组（pair），bfs的题解如下：
```cpp
#include <iostream>
#include <queue>
#include <cstring>
using namespace std;

const int N = 2e5 + 10;

typedef pair<int, int> PII;

int h[N], e[N], ne[N], idx;

int c[N]; // color

int n, m, u, v;

void add(int a, int b) {
	e[idx] = b;
	ne[idx] = h[a];
	h[a] = idx++;
}

bool bfs(int x, int xc) {
	queue<PII> q;
	q.push({x, xc});
	while(!q.empty()) {
		PII p = q.front();
		q.pop();
		int o = p.first, oc = p.second;
		for(int i = h[o]; i != -1; i = ne[i]) {
			int u = e[i];
			if(c[u] == 0) {
				c[u] = 3 - oc;
				q.push({u, c[u]});
			} else if(c[u] == oc) return false;
		}
	}
	return true;
}

int main() {
	memset(h, -1, sizeof h);
	scanf("%d%d", &n, &m);
	while(m--) {
		scanf("%d%d", &u, &v);
		add(u, v);
		add(v, u);
	}

	bool flag = true;
	for(int i = 1; i <= n; i++) {
		if(c[i] == 0) {
			c[i] = 1;
			if(!bfs(i, 1)) {
				flag = false;
				break;
			}
		}
	}

	if(flag) printf("Yes");
	else printf("No");
}

```
课后题：[acwing - 257: 关押罪犯](https://www.acwing.com/problem/content/259/)
可以使用二分图来做，也可以使用并查集

### 匈牙利算法
匈牙利算法，是给定一个二分图，用来求二分图的最大匹配的。

给定一个二分图G，在G的一个子图M中，M的边集中的任意两条边，都不依附于同一顶点，则称M是一个匹配。就是每个点只会有一条边相连，没有哪一个点，同时连了多条边。（参考yxc的例子：男生女生恋爱配对，最多能凑出多少对）

所有匹配中包含边数最多的一组匹配，被称为二分图的最大匹配。其边数即为最大匹配数

假设一个二分图，左半边部分节点表示男生，右半边部分节点表示女生。一个男生节点和一个女生节点连了一条边，则表示这两个人之间有感情基础，可以发展为情侣。当我们把一对男女凑成一对时，称为这两个节点匹配。

匈牙利算法的核心思想是：我们枚举左半边所有男生（节点），每次尝试给当前男生找对象。我们先找到这个男生看上的全部女生。（即找到这个节点连接的所有右侧的节点）。遍历这些女生，当一个女生没有和其他男生配对时，直接将这个女生和这个男生配对。则该男生配对成功。当这个女生已经和其他男生配对了，则尝试给这个女生的男朋友，找一个备胎。如果这个女生的男朋友有其他可选择的备胎。则将这个女生的男朋友和其备胎配对。然后将这个女生和当前男生配对。如此找下去…对于这个男生，只有所有情况下都无法配对时才将其放弃.


#### [AcWing 861. 二分图的最大匹配](https://www.acwing.com/activity/content/problem/content/927/)

##### 代码实现
```cpp
#include<iostream>
#include<cstring>
#include<algorithm>
using namespace std;
const int N = 1010,  M = 1e5 + 10;

int h[N], e[M], ne[M], idx;
int match[N];
bool st[N]; // 状态变量

int n1, n2, m;

void add(int a, int b) {
    e[idx] = b;
    ne[idx] = h[a];
    h[a] = idx++;
}

// 给一个男生找女朋友
bool find(int x) {
    // 找出这个男生所有看上的女生
    for(int i = h[x]; i != -1; i = ne[i]) {
        int u = e[i]; // 女生节点编号
        if(st[u]) continue; // 如果这个女生已经被标记, 则跳过
        st[u] = true; // 先把这个女生标记, 使得后续递归时时跳过这个女生
        if(match[u] == 0 || find(match[u])) {
            // 如果当前这个女生没有被匹配, 或者能够给这个女生已匹配的男生另外找个备胎, 则可以
            match[u] = x;
            return true;
        }
    }
    return false; // 找了一圈还是不行
}

int main() {
    memset(h, -1, sizeof h);
    scanf("%d%d%d", &n1, &n2, &m);
    while(m--) {
        int a, b;
        scanf("%d%d", &a, &b);
        add(a, b); // 只从左半边连到右半边
    }

    // 枚举左半边所有点
    int res = 0;
    for(int i = 1; i <= n1; i++) {
        // 每次给一个男生找女朋友时, 清空状态变量
        memset(st, false, sizeof st);
        if(find(i)) res++;
    }
    printf("%d\n", res);
    return 0;
}
```

课后题：[acwing - 372: 棋牌摆放](https://www.acwing.com/problem/content/374/)