#! https://zhuanlan.zhihu.com/p/548044954
- [搜索与图论Part1](#搜索与图论part1)
  - [DFS和BFS](#dfs和bfs)
    - [DFS](#dfs)
      - [AcWing 842. 排列数字](#acwing-842-排列数字)
        - [问题定义](#问题定义)
        - [逻辑推导](#逻辑推导)
        - [代码实现](#代码实现)
      - [AcWing 843. n-皇后问题](#acwing-843-n-皇后问题)
        - [问题定义](#问题定义-1)
        - [逻辑推导(方法一)](#逻辑推导方法一)
        - [代码实现（方法一）](#代码实现方法一)
        - [逻辑推导(方法二)](#逻辑推导方法二)
        - [代码实现(方法二)](#代码实现方法二)
    - [BFS](#bfs)
      - [AcWing 844. 走迷宫](#acwing-844-走迷宫)
        - [逻辑推导](#逻辑推导-1)
        - [代码实现](#代码实现-1)
      - [AcWing 845. 八数码](#acwing-845-八数码)
        - [逻辑推导](#逻辑推导-2)
        - [代码实现](#代码实现-2)
    - [树与图的存储](#树与图的存储)
    - [树与图的深度优先遍历](#树与图的深度优先遍历)
      - [AcWing 846. 树的重心](#acwing-846-树的重心)
        - [问题定义](#问题定义-2)
        - [逻辑推导](#逻辑推导-3)
        - [代码实现](#代码实现-3)
    - [树与图的深度优先遍历](#树与图的深度优先遍历-1)
      - [AcWing 847. 图中点的层次 ](#acwing-847-图中点的层次-)
        - [问题定义](#问题定义-3)
        - [逻辑推导](#逻辑推导-4)
        - [代码实现](#代码实现-4)
    - [拓扑排序](#拓扑排序)
      - [AcWing 848. 有向图的拓扑序列](#acwing-848-有向图的拓扑序列)
        - [问题定义](#问题定义-4)
        - [逻辑推导](#逻辑推导-5)
        - [代码实现](#代码实现-5)

# 搜索与图论Part1

## DFS和BFS
DFS：深度优先搜索（Depth-First-Search）

BFS：宽度优先搜索（Breadth-First-Search）

**DFS和BFS的对比：**

- DFS使用栈（stack）来实现，BFS使用队列（queue）来实现

- DFS所需要的空间是树的高度h，而BFS需要的空间是2h （DFS的空间复杂度较低）

- DFS不具有最短路的特性，BFS具有最短路的特性

通常来说，求“最短”的操作，都可以用BFS来做，而其他一些奇怪的操作，或者对空间复杂度要求比较高，则用DFS来做

### DFS

DFS中的2个重要概念：

- 回溯：回溯的时候，一定要记得恢复现场
- 剪枝：提前判断某个分支一定不合法，直接剪掉该分支

#### [AcWing 842. 排列数字](https://www.acwing.com/problem/content/844/)
##### 问题定义
给定一个整数 n，将数字 1∼n 排成一排，将会有很多种排列方法。

现在，请你按照字典序将所有的排列方法输出。

##### 逻辑推导
经典DFS问题，对于数n，其排列一共有n个位置，我们深搜从第一个位置开始枚举，直到第n个位置，每个位置放一个数字，而每个数字只能使用一次，所以对于1~n这n个数字，我们需要维护一个状态，来表示某个数字是否已经被使用过。
当我们深搜到某个位置x时，若在这个位置之前，某个数k已经被使用过，则位置x上不能再放数k。即，每次在某一个位置上枚举数字，选择一个当前还未被使用过的数字，放置在该位置上，然后深搜下一个位置。**记得回溯时，需要还原这个数字的状态。**将这个数字从**已被使用**，还原为**未被使用**。另外需要一个`path`变量，来存储当前深搜所经过的路径，当深搜到叶子节点时，这个`path`即是一种排列，输出即可。

![排列数字](https://pic4.zhimg.com/80/v2-7db76789251b28129dc68cee308467b0.png)
##### 代码实现
```cpp
#include<iostream>
using namespace std;
const int N = 10;
bool visited[N];
int n, path[N];

// x 代表当前是第几个位置的数， x 可能取值为1，2，3....，n
void dfs(int x) {
	if(x == n ) {
		// 到达根节点, 深搜结束, 输出
		for(int i = 0; i < n; i++) printf("%d ", path[i]);
		printf("\n");
        return ;
	}
    // 否则, 枚举1~n, 找到一个可用数字, 放到当前位置
	for(int i = 1; i <= n; i++) {
		if(!visited[i]) {
            // 当数字i还未被使用过时, 将i放到当前位置x上, 并标记其为 已被使用, 随后深搜下一个位置x + 1
			path[x] = i;
			visited[i] = true;
			dfs(x + 1);
			visited[i] = false; // 这里只需要还原状态变量即可, path[x]会在下一个循环被覆盖掉
		}
	}
}

int main() {
	scanf("%d", &n);
	dfs(0); // 先从第一个位置的数开始深搜
	return 0;
}
```

#### [AcWing 843. n-皇后问题](https://www.acwing.com/problem/content/845/)
##### 问题定义
n−皇后问题是指将 n 个皇后放在 n×n 的国际象棋棋盘上，使得皇后不能相互攻击到，即任意两个皇后都不能处于同一行、同一列或同一斜线上。
现在给定整数 n，请你输出所有的满足条件的棋子摆法。

##### 逻辑推导(方法一)
首先经过思考和提炼，容易发现，每一行只能放一个皇后，则问题被精简成了，从第一行开始，到第n行，依次确定每一行的皇后的摆放位置。我们需要针对行，列，对角线，反对角线，维护状态变量。

比如`col[i]`表示第i列上的状态，若`col[i] = true`，表示该列已经被一个皇后占用，该列上无法再放多一个皇后，同理，`dg[i]`表示第i条对角线的状态，`rdg[i]`表示第i条反对角线的状态。

而由于我们是依次在每一行上摆放一个皇后，这就变相地保证了，每一行只有一个皇后，则行是不可能冲突的，所以就无需维护针对行的状态。另外需要注意，若棋盘是n × n，则一共有n列，n行，但对角线有2n - 1条，反对角线也是2n - 1条，可自行画图验证。我们需要确定对于一个点[x, y]，其所在的是第几条对角线，以及第几条反对角线，以及对角线，反对角线的编号从哪里开始。

可以通过截距表示某一条对角线`b = y - x`和`b = y + x`
注意`b = y - x`可能是负数，但是我们数组下标不能是负数，因此需要加便宜了n，最后得到：
`b = y - x + n`和`b = y + x`

![对角线表示](https://pic4.zhimg.com/80/v2-d40e26ad41df334f76f60dfd73463f5e.png)

##### 代码实现（方法一）

```cpp
#include<iostream>
using namespace std;
const int N = 20;
char ans[N][N]; // 结果矩阵
bool col[N], dg[N], rdg[N]; // 状态变量
int n;

// 从第一行开始摆放皇后, x代表当前需要摆放的是第几行
void dfs(int x) {
	if(x == n ) {
		// 深搜到达叶子节点, 输出
		for(int i = 0; i < n; i++) {
			for(int j = 0; j < n; j++) printf("%c", ans[i][j]);
			printf("\n");	
		}
		printf("\n");
		return ;
	}

	for(int y = 0; y < n; y++) {
		// 枚举的是列, 看这一行的1~n列中, 哪一列可以放皇后
		if(!col[y] && !dg[x + y ] && !rdg[y - x + n]) {
			// 若当前位置[x,y] 所在的列, 对角线, 反对角线, 皆没有被占用, 则当前位置可以放皇后
			col[y] = dg[x + y] = rdg[y - x + n] = true; // 更新状态变量
			ans[x][y] = 'Q'; // 放皇后
			dfs(x + 1); // 深搜下一行
			ans[x][y] = '.'; // 还原
			col[y] = dg[x + y] = rdg[y - x + n] = false; // 还原状态变量
		}
	}
}

int main() {
	scanf("%d", &n);
    // 初始化结果矩阵
	for(int i = 0; i < n; i++) {
		for(int j = 0; j < n; j++) ans[i][j] = '.';
	}
	dfs(0);
	return 0;
}

```

##### 逻辑推导(方法二)
若不经过思考提炼，则更一般的做法（更暴力的做法）是：从棋盘的第一个位置[1, 1]依次枚举到最后一个位置[n,n]。每个位置都有两种选择：放或者不放皇后（这就对应了两个分支）。对比解法一，此时我们就需要多维护一个针对行的状态变量了。其余逻辑和解法一类似，只是需要对每个位置的点进行枚举

##### 代码实现(方法二)
```cpp
#include<iostream>
using namespace std;
const int N = 20;
char ans[N][N]; // 结果矩阵
bool row[N], col[N], dg[2 * N], rdg[2 * N]; // 状态变量
int n;

// x 是第几行, y 是第几列, s 是当前已经放了几个皇后了
void dfs(int x, int y, int s) {
	
	// 若某一行枚举结束, 移动到下一行第一个元素
	if(y == n + 1) {
		x++;
		y = 1;
	}
	// 所有点已经枚举完毕, 此时只有当摆放了n个皇后时, 才是一个可行的解
    // 因为dfs的全部叶子节点，是对n^2个位置，每个位置选择放或者不放的一种排列, 
    // 则每个叶子节点到根节点的路径, 可能一共摆放了不到n个皇后, 极端一点, 每个位置都选择不放, 也形成了一个叶子节点
	if(x == n + 1) {
		if(s == n) {
			for(int i = 1; i <= n; i++) {
				for(int j = 1; j <= n; j++) printf("%c", ans[i][j]);
				printf("\n");
			}
			printf("\n");
		}
		return ; // 已经枚举完所有位置, 直接返回
	}
	// 两种情况
	// 1. 当前位置不放皇后, 则直接走到下一个位置
	dfs(x, y + 1, s);
	// 2. 尝试在当前位置放皇后
	if(!row[x] && !col[y] && !dg[x + y - 1] && !rdg[y - x + n]) {
		// 当前位置可以放皇后
		ans[x][y] = 'Q'; // 放皇后
		row[x] = col[y] = dg[x + y - 1] = rdg[y - x + n] = true; // 更新状态变量
		dfs(x, y + 1, s + 1); // 放下去的皇后数量加一, 走到下一个位置
		// dfs完毕, 恢复现场
		ans[x][y] = '.';
		row[x] = col[y] = dg[x + y - 1] = rdg[y - x + n] = false;
	}
}

int main() {
	scanf("%d", &n);
	for(int i = 1; i <= n; i++) {
		for(int j = 1; j <= n; j++) ans[i][j] = '.';
	}
	dfs(1, 1, 0); // 从[1,1]开始深搜, 初始放的皇后数量为0
	return 0;
}
```
显然，解法二由于枚举了棋盘上的所有位置，其性能相比解法一要差一些

### BFS

从左到右，一层一层的搜，所以叫宽度优先搜索。宽搜的基本框架：
```cpp
1. 插入一个初始状态到queue中
2. while(queue非空)
 2.1 把队头拿出来
 2.2 扩展队列
3. end
```

#### [AcWing 844. 走迷宫](https://www.acwing.com/problem/content/846/)

##### 逻辑推导
- 用 a[n][m] 存储地图，d[n][m] 存储起点到 n,m 的距离。

- 从起点开始广度优先遍历地图。

- 当地图遍历完，就求出了起点到各个点的距离，输出f[n][m]即可。
![走迷宫](https://pic4.zhimg.com/80/v2-38eb4e203eb737c0b043a26520a7c20e.png)

##### 代码实现
```cpp
#include<cstring>
#include<iostream>
#include<queue>
using namespace std;

typedef pair<int,int> PII;

const int N = 110;
int n, m;
int a[N][N], d[N][N]; // a用来存矩阵数组, d用来存从起点走到该点的距离

int main() {
	scanf("%d%d", &n, &m);

	for(int i = 0; i < n; i++) {
		for(int j = 0; j < m; j++) {
			scanf("%d", &a[i][j]);
		}
	}

	// -1表示该点还未走到
	memset(d, -1, sizeof d);

	queue<PII> q;
	// 初始化
	q.push({0,0});
	d[0][0] = 0;
    // 每次往下走需要调整的x和y
	int dx[4] = {0, 1, 0, -1};	
	int dy[4] = {1, 0, -1, 0};
	while(!q.empty()) {
		PII p = q.front();
		q.pop();
		for(int i = 0; i < 4; i++) {
			int x = p.first + dx[i];
			int y = p.second + dy[i];
            // 当这个点在边界内, 且这个点为0, 且该点还未被走到过, 则走过去
			if(x >= 0 && x < n && y >= 0 && y < m && a[x][y] == 0 && d[x][y] == -1) {
				q.push({x,y});
				d[x][y] = d[p.first][p.second] + 1;
			}
		}
	}
	printf("%d\n", d[n - 1][m - 1]);
	return 0;
}

```

#### [AcWing 845. 八数码](https://www.acwing.com/problem/content/847/)

##### 逻辑推导
求的其实是个最小的操作步数，考虑用BFS来做。把每一种棋盘的状态，当作树中的一个节点，其实就是寻找初始状态，到最终状态，是否存在一个路径，并找出最短路。难点在于棋盘的状态表示，以及如何将状态进行存储，并记录每种状态之间的距离。


1、题目的目标
![目标](https://pic4.zhimg.com/80/v2-f53b50e1b2c213d845eb04d6f5b8ddd1.png)
**求最小步数 -> 用BFS**

2、移动情况
![移动情况](https://pic4.zhimg.com/80/v2-11c26c345c0a7ade294cf0f8fe5cda0e.png)

移动方式：
![移动方式](https://pic4.zhimg.com/80/v2-a554dc391477df6dca174438aaec4681.png)

转以后：a = x + dx[i], b = y + dy[i].

思想：将每一种情况作为1个节点，目标情况即为终点

从初始状况移动到目标情况 —> 求最短路

3、问题

第一点：怎么表示一种情况使其能作为节点？

第二点：如何记录每一个状态的“距离”（即需要移动的次数）？

第三点：队列怎么定义，dist数组怎么定义？

4、解决方案

将 “3*3矩阵” 转化为 “字符串”，如：
![字符串视角](https://pic4.zhimg.com/80/v2-115a3ddcb146d6451e57992b54705f50.png)

所以：
```cpp
队列可以用 queue<string>
//直接存转化后的字符串
dist数组用哈希表 unordered_map<string, int>
//将字符串和数字联系在一起，字符串表示状态，数字表示距离
```

5、矩阵与字符串的转换方式
![](https://pic4.zhimg.com/80/v2-eaf6136e36250360c77a31a166d53617.png)

##### 代码实现
```cpp
#include <iostream>
#include <algorithm>
#include <queue>
#include <unordered_map>

using namespace std;

int bfs(string start)
{
    //定义目标状态
    string end = "12345678x";
    //定义队列和dist数组
    queue<string> q;
    unordered_map<string, int> d;
    //初始化队列和dist数组
    q.push(start);
    d[start] = 0;
    //转移方式
    int dx[4] = {1, -1, 0, 0}, dy[4] = {0, 0, 1, -1};

    while(q.size())
    {
        auto t = q.front();
        q.pop();
        //记录当前状态的距离，如果是最终状态则返回距离
        int distance = d[t];
        if(t == end) return distance;
        //查询x在字符串中的下标，然后转换为在矩阵中的坐标
        int k = t.find('x');
        int x = k / 3, y = k % 3;

        for(int i = 0; i < 4; i++)
        {
            //求转移后x的坐标
            int a = x + dx[i], b = y + dy[i];
            //当前坐标没有越界
            if(a >= 0 && a < 3 && b >= 0 && b < 3)
            {
                //转移x
                swap(t[k], t[a * 3 + b]);
                //如果当前状态是第一次遍历，记录距离，入队
                if(!d.count(t))
                {
                    d[t] = distance + 1;
                    q.push(t);
                }
                //还原状态，为下一种转换情况做准备
                swap(t[k], t[a * 3 + b]);
            }
        }
    }
    //无法转换到目标状态，返回-1
    return -1;
}

int main()
{
    string c, start;
    //输入起始状态
    for(int i = 0; i < 9; i++)
    {
        cin >> c;
        start += c;
    }

    cout << bfs(start) << endl;

    return 0;
}
```

### 树与图的存储

首先，树是一种特殊的图（无环连通图）。所以，这里只说图的存储即可。

首先，图分为2种，**有向图**和**无向图**。

有向图中2个点之间的边是有方向的，比如a -> b，则只能从a点走到b点，无法从b点走到a点。

无向图中2个点之间的边是没有方向的，比如a - b，则可以从a走到b，也可以从b走到a。

通常，我们可以将无向图看成有向图。比如上面，对a到b之间的边，我们可以建立两条边，分别是a到b的，和b到a的。

所以，我们只需要考虑，有向图如何存储，即可。通常有2种存储方式

- 邻接矩阵
用一个二维数组来存，比如g[a,b]存储的就是a到b的边。邻接矩阵无法存储重复边，比如a到b之间有2条边，则存不了。（用的较少，因为这种方式比较浪费空间，对于有n个点的图，需要$n^2$的空间，这种存储方式适合存储稠密图）

- 邻接表
使用单链表来存。对于有n个点的图，我们开n个单链表，每个节点一个单链表。单链表上存的是该节点的邻接点（用的较多）,一般用头插法

![有向图存储](https://pic4.zhimg.com/80/v2-e0008bc6907d051dfe2b2e35cf515cec.png)
```cpp
//邻接表存储方式
const int N = 100010, M = N * 2;
int h[N], e[M], ne[M], idx;// 其中 h存放头结点，e存放链表节点的值, ne存放链表节点的next指针

void add(int a, int b) //a所对应的单链表中插入b 
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx++;
}

int main()
{
    memset(h, -1, sizeof h) //头结点全部初始化为-1
}
```

树和图遍历有2种方式，深度优先遍历和宽度优先遍历。

我们只需要考虑有向图的遍历即可。

### 树与图的深度优先遍历
由于遍历时，每个点最多只会被遍历一次，所以深度优先遍历的时间复杂度是O(n+m)，

n是节点数，m是边数

```c++
//图的深度优先遍历
#include<cstring>
#include<iostream>
#include<algorithm>
using namespace std;

int n, m;
const int N = 100010, M = N * 2;
int h[N], e[M], ne[M], idx;
bool st[N];//记录图上的某个节点是否访问过

void add(int a, int b) 
{
    e[idx] = b, ne[idx] = h[a], h[a] = idx++;
}

void dfs(int u)
{
    st[u] = true;//标记一下，已经被搜过了
    for(int i = h[u]; i != -1; i = ne[i])
    {
        int j = e[i]; //i相当于idx,j是图里面节点的编号
        if(!st[j]) dfs(j);
    }
}


int main()
{
    memset(h, -1, sizeof h) //头结点全部初始化为-1
}
```


#### [AcWing 846. 树的重心](https://www.acwing.com/problem/content/848/)

##### 问题定义
给定一颗树，树中包含 n 个结点（编号 1∼n）和 n−1 条无向边。

请你找到树的重心，并输出将重心删除后，剩余各个连通块中点数的最大值。

重心定义：重心是指树中的一个结点，如果将这个点删除后，剩余各个连通块中点数的最大值最小，那么这个节点被称为树的重心。

##### 逻辑推导
本题的本质是树的dfs， 每次dfs可以确定以u为重心的最大连通块的节点数，并且更新一下ans。

也就是说，dfs并不直接返回答案，而是在每次更新中迭代一次答案。

这样的套路会经常用到，在 树的dfs 题目中

深度优先遍历，可以算出每个子树所包含的节点个数，递归的处理子节点的过程中，返回就可以得到每个子树包含的节点数量.而其余部分就是总结点数减去当前节点机器子节点总数

![树的重心1](https://i.imgur.com/9PXteEf.png)
![树的重心2](https://i.imgur.com/HCgULuT.png)

##### 代码实现
```cpp
#include <iostream>
#include <algorithm>
#include <cstring>

using namespace std;

const int N = 1e5 + 10; //数据范围是10的5次方
const int M = 2 * N; //以有向图的格式存储无向图，所以每个节点至多对应2n-2条边

int h[N]; //邻接表存储树，有n个节点，所以需要n个队列头节点
int e[M]; //存储元素
int ne[M]; //存储列表的next值
int idx; //单链表指针
int n; //题目所给的输入，n个节点
int ans = N; //表示重心的所有的子树中，最大的子树的结点数目

bool st[N]; //记录节点是否被访问过，访问过则标记为true

//a所对应的单链表中插入b  a作为根 
void add(int a, int b) {
    e[idx] = b, ne[idx] = h[a], h[a] = idx++;
}

//返回以u为根的子树中节点的个数，包括u节点
int dfs(int u) {
    int res = 0; //存储 删掉某个节点之后，最大的连通子图节点数
    st[u] = true; //标记访问过u节点
    int sum = 1; //存储 以u为根的树 的节点数, 包括u，如图中的4号节点

    //访问u的每个子节点
    for (int i = h[u]; i != -1; i = ne[i]) {
        int j = e[i];
        //因为每个节点的编号都是不一样的，所以 用编号为下标 来标记是否被访问过
        if (!st[j]) {
            int s = dfs(j);  // u节点的单棵子树节点数 如图中的size值
            res = max(res, s); // 记录最大联通子图的节点数
            sum += s; //以j为根的树 的节点数
        }
    }

    //n-sum 如图中的n-size值，不包括根节点4；
    res = max(res, n - sum); // 选择u节点为重心，最大的 连通子图节点数
    ans = min(res, ans); //遍历过的假设重心中，最小的最大联通子图的 节点数
    return sum;
}

int main() {
    memset(h, -1, sizeof h); //初始化h数组 -1表示尾节点
    cin >> n; //表示树的结点数

    // 题目接下来会输入，n-1行数据，
    // 树中是不存在环的，对于有n个节点的树，必定是n-1条边
    for (int i = 0; i < n - 1; i++) {
        int a, b;
        cin >> a >> b;
        add(a, b), add(b, a); //无向图
    }

    dfs(1); //可以任意选定一个节点开始 u<=n

    cout << ans << endl;

    return 0;
}

```

### 树与图的深度优先遍历

#### [AcWing 847. 图中点的层次 ](https://www.acwing.com/problem/content/849/)

##### 问题定义
给定一个 n 个点 m 条边的有向图，图中可能存在重边和自环。

所有边的长度都是 1，点的编号为 1∼n。

请你求出 1 号点到 n 号点的最短距离，如果从 1 号点无法走到 n 号点，输出 −1。

##### 逻辑推导
比较裸的一道题，由于所有边的长度都是 1，所以可以用BFS解决问题。

##### 代码实现
```cpp
#include <cstring>
#include <iostream>

using namespace std;

const int N=1e5+10;

int h[N], e[N], idx, ne[N];
int d[N]; //存储每个节点离起点的距离  d[1]=0
int n, m; //n个节点m条边
int q[N]; //存储层次遍历序列 0号节点是编号为1的节点

void add(int a, int b)
{
    e[idx]=b,ne[idx]=h[a],h[a]=idx++;
}

int bfs()
{
    int hh=0,tt=0;

    q[0]=1; //0号节点是编号为1的节点

    memset(d,-1,sizeof d);

    d[1]=0; //存储每个节点离起点的距离

    //当我们的队列不为空时
    while(hh<=tt)
    {
        //取出队列头部节点
        int t=q[hh++];

        //遍历t节点的每一个邻边
        for(int i=h[t];i!=-1;i=ne[i])
        {
            int j=e[i];
            //如果j没有被扩展过
            if(d[j]==-1)
            {
                d[j]=d[t]+1; //d[j]存储j节点离起点的距离，并标记为访问过
                q[++tt] = j; //把j结点 压入队列
            }
        }
    }

    return d[n];
}

int main()
{
    cin>>n>>m;
    memset(h,-1,sizeof h);
    for(int i=0;i<m;i++)
    {
        int a,b;
        cin>>a>>b;
        add(a,b);
    }

    cout<<bfs()<<endl;
}

```

### 拓扑排序

图的宽度优先搜索的应用，求拓扑序（拓扑序是针对有向图的）

什么是拓扑序：将一个图的很多节点，排成一个序列，使得图中的所有边，都是从前面的节点，指向后面的节点。则这样一个节点的排序，称为一个拓扑序。

若图中有环，则一定不存在拓扑序。

可以证明，一个**有向无环图**，一定存在一个拓扑序列。有向无环图，又被称为**拓扑图**。

对于每个节点，存在2个属性，**入度**和**出度**。

入度，即，有多少条边指向自己这个节点。

出度，即，有多少条边从自己这个节点指出去。

所有入度为0的点，可以排在当前最前面的位置。

算法流程：
```cpp
将所有入度为0的点入队。
while(queue非空) {
	t = queue.pop(); // 获取队头
	枚举t的全部出边 t->j
	  删掉边t->j, j节点的入度减一
	  if(j的入度为0) 将j入队
}

```
一个有向无环图，一定存在至少一个**入度为0**的点，

#### [AcWing 848. 有向图的拓扑序列](https://www.acwing.com/problem/content/850/)

##### 问题定义
给定一个 n 个点 m 条边的有向图，点的编号是 1 到 n，图中可能存在重边和自环。

请输出任意一个该有向图的拓扑序列，如果拓扑序列不存在，则输出 −1。

若一个由图中所有点构成的序列 A 满足：对于图中的每条边 (x,y)，x 在 A 中都出现在 y 之前，则称 A 是该图的一个拓扑序列。

##### 逻辑推导
比较裸的一道题，由于所有边的长度都是 1，所以可以用BFS解决问题。

##### 代码实现
```cpp
#include<cstring>
#include<iostream>
using namespace std;

const int N = 1e5 + 10;

int h[N], e[N], ne[N], idx; // 邻接表来存图
int in[N]; // 每个点的入度
int q[N], hh, tt = -1; // 数组模拟队列

int n, m;

void add(int x, int y) {
	// y的入度加一
	in[y]++;
	// 邻接表
	e[idx] = y;
	ne[idx] = h[x];
	h[x] = idx++;
}


int main() {
	memset(h, -1, sizeof h);
	scanf("%d%d", &n, &m);
	int x, y;
	while(m--) {
		scanf("%d%d", &x, &y);
		add(x, y);
	}
	// 将所有入度为0的点加入到队列中
	for(int i = 1; i <= n; i++) {
		if(in[i] == 0) q[++tt] = i;
	}

	while(tt >= hh) {
		int t = q[hh++]; // 弹出队头
		for(int i = h[t]; i != -1; i = ne[i]) {
			int u = e[i];
			if(--in[u] == 0) {
				// 移除了节点t, 节点u入度减一, 若等于0, 加入到队列
				q[++tt] = u;
			}
		}
	}
	if(tt == n - 1) {
		for(int i = 0; i < n; i++) printf("%d ", q[i]);
	} else printf("-1");
	
	return 0;
}

```