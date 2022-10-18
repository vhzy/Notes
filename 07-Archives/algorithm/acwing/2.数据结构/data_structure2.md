#! https://zhuanlan.zhihu.com/p/552299999
- [数据结构Part2](#数据结构part2)
	- [Trie树](#trie树)
		- [AcWing 835. Trie字符串统计](#acwing-835-trie字符串统计)
		- [AcWing 143. 最大异或对](#acwing-143-最大异或对)
	- [并查集](#并查集)
		- [AcWing 836. 合并集合](#acwing-836-合并集合)
		- [AcWing 837. 连通块中点的数量](#acwing-837-连通块中点的数量)
		- [Acwing 240. 食物链](#acwing-240-食物链)
	- [堆](#堆)
		- [AcWing 838. 堆排序](#acwing-838-堆排序)
		- [AcWing 839. 模拟堆](#acwing-839-模拟堆)


# 数据结构Part2

本节主要说了：
- Trie树（字典树）
- 并查集
- 堆

## Trie树
Trie树，又称字典树，是用来**高效存储和查找字符串集合**的一种数据结构

(一般来说，存储类型一样，都是小写或者大写或者数字)

查找时，可以高效的查找某个字符串是否在Trie树中出现过，并且可以查找出现了多少次

其逻辑结构如下

假设我们需要维护一个字符串集合，它需要支持两种操作

*   向集合插入一个字符串`x`
*   查询一个字符串在集合中出现了多少次

假设我们有一个字符串集合，包含如下的字符串

`abcd`，`abc`，`aced`，`bbac`，`abde`，`bcac`

将这些字符串依次进行插入，构建出来的Trie树逻辑结构如下（图中最后一行e也应该是红色的）
![字典树](https://pic4.zhimg.com/80/v2-c50a03556b68b3f94965311e06d8eccb.png)

### [AcWing 835. Trie字符串统计](https://www.acwing.com/problem/content/837/)

```cpp
#include<iostream>
#include<string>
using namespace std;

const int N = 1e5 + 10;

int q[N][26];
int cnt[N]; // 用来计数，表示以节点i为结尾的字符串, 出现了多少次
int idx; // 用来分配新的节点

// 注意这里, 使用数组来模拟指针的

// 下标idx为0的节点, 既是根节点，也用来表示空节点

// 如一个节点下标为1，则q[1][0]表示这个节点的a儿子，若q[1][0] = 0, 表示1这个节点没有a儿子(空节点)，若q[1][0] = x , x不为0, 则表明1这个节点有a儿子，且a儿子的节点下标为x

// 更通俗地讲, q[i][j]，表示了一个节点i连接其儿子节点的边，而j属于0~25, 表示了26个小写字母，当q[i][j] = x，且x不为0时，表明i这个节点有一儿子节点为某个字母, 且这个儿子节点下标为x


void insert(string s) {
    int p = 0; //从根节点开始，根节点是0，从前往后遍历
    for(int i = 0; i < s.size(); i++) {
        int u = s[i] - 'a';   //当前节点的编号
        if(q[p][u] == 0) q[p][u] = ++idx;
        p = q[p][u]; // 更新当前节点
    }
    cnt[p]++;
}

int query(string s) {
    int p = 0;
    for(int i = 0; i < s.size(); i++) {
        int u = s[i] - 'a';
        if(q[p][u] == 0) return 0; // 不存在该节点
        p = q[p][u];
    }
    return cnt[p];
}

int main() {
    int n;
    char op;
    string s;
    scanf("%d", &n);
    while(n--) {
        cin >> op >> s;
        if(op == 'I') {
            insert(s);
        } else if(op == 'Q') {
            int c = query(s);
            printf("%d\n", c);
        }
    }
    return 0;
}
```

### [AcWing 143. 最大异或对](https://www.acwing.com/problem/content/145/)
字典树不单单可以高效存储和查找字符串集合,还可以存储二进制数字

本题每个数以二进制方式存入字典树,找的时候从最高位去找有无该位的异.

先想一个暴力做法，两层循环，穷举所有组合

```c
int res = 0;
for(int i = 0; i < n; i++) {
    for(int j = 0; j < i; j++)
        res = max(res, a[i] ^ a[j]);
}

```

上面的代码中，有两层循环，其中，内层循环的含义是：对于当前已经固定的`a[i]`，在`[0,i)`之间找到一个`j`，使得`a[j] ^ a[i]`最大。

然而，对于内层循环，可以用Trie树优化，我们知道Trie树存的是字符串的集合，在这道题的场景下，我们考虑让Trie树来存储每个数字的二进制表示（二进制串）。每插入一个数到Trie树，从Trie树的根节点开始往下，先存这个数的二进制最高位，一直到叶子节点，存这个数的最低位。然后对于每一个`a[i]`，从其二进制的高位开始，在Trie树中查找，每次尝试找与`a[i]`当前位不同的分支节点，一直找下去，找到叶子节点，这个二进制串代表的数，就是与`a[i]`做异或最大的数。代码题解如下：


```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10, M  = 31 * N;  // N 是数的个数上限, M是Trie树中节点个数的上限
// 由于每个二进制位,要么是0, 要么是1, 所以这个trie树是个二叉树
int son[M][2];  // 这个数组, 用来存Trie树
// 注意Trie树的节点个数不是N, 而是大于N的, 每个数最多有31个二进制位, 那么Trie树中总的节点数我们开大一些, 开为  31 * N 
int n, idx; // n 是数的个数, idx用来分配Trie树的节点下标
int q[N]; // 用来存输入的数

// 插入一个数到Trie树中
void insert(int x) {
	int p = 0; // 从根节点开始
	// 从数字二进制表示的最高位开始插入
	for(int i = 30; i >= 0; i--) {
		// 由于x的大小不超过2^31, 所以x的二进制表示最多31位
		// 也就是0-30, 从最高位第31位开始, 即下标30
		int u = (x >> i) & 1; //取这一位的二进制位
		if(son[p][u] == 0) son[p][u] = ++idx;
		p = son[p][u];
	}
}

// 查找和x做异或, 结果最大的值
int query(int x) {
	int p = 0, res = 0;
	for(int i = 30; i >= 0; i--) {
		int u = (x >> i) & 1;
		if(son[p][!u]) u = !u; // 若存在与x当前位相反的分支, 则走过去, 否则保持原样
		p = son[p][u];
		res = (res << 1) + u; // 计算这个最后的结果值
	}
	return res;
}

int main() {
	scanf("%d", &n);
	for(int i = 0; i < n; i++) scanf("%d", &q[i]);
	int res = 0;
	for(int i = 0; i < n; i++) {
		insert(q[i]); // 先插入当前的数q[i]到Trie树中
		int x = query(q[i]); // 此时Trie树中存的是全部 j = [0,i)的全部q[j]的二进制串
        // 这里相当于从[0,i)找与a[i]异或结果最大的那个数
		res = max(res, q[i] ^ x); // 更新结果
	}
	printf("%d", res);
	return 0;
}
```

## 并查集
并查集结构能够支持快速（接近O(1)）进行如下的操作

1.  **将两个集合合并**
2.  **询问两个元素是否在一个集合当中**

并查集可以在近乎O(1)的时间复杂度下，完成上述2个操作

并查集的基本原理：**用树的形式来维护一个集合**。**用树的根节点来代表这个集合。对于树中的每个节点，都存储其父节点的编号。比如一个节点编号为x，我们用p[x]来表示其父节点的编号**

当我们想求，某一个节点所属的集合时，找到其父节点，并一直往上找，直到找到根节点，则根节点的编号，就是该节点所属的集合的编号。

问题1：如何判断根节点？

对于根节点x，我们设置p[x] = x。那么，可以用p[x] == x 来判断是否是根节点

问题2：如何求某个节点x所属的集合编号？

`while(p[x] != x) x = p[x];` 一直向上走，直到找到根节点

问题3：如何合并2个集合？

直接将一个集合作为另一个集合根节点的一个儿子节点即可。

假设一个A集合的根节点编号为x，另一个B集合根节点编号为y，则合并操作就是p[x] = y。即，将A集合的根节点作为B集合根节点的一个儿子。即，将A集合直接插到B集合里面。

对于查找某个节点x的所属集合，时间复杂度一开始可能没有O(1)，可能需要O(logn)，如果是二叉树的话。但可以采用**路径压缩**进行优化，当搜索完某个节点的所属集合时，直接将搜索路径上的所有节点的父节点，直接指向根节点，这样下次查询时就是O(1)。

并查集还有一种优化方式是**按秩合并**，大概是说的，将两个集合合并时，将高度较矮的那棵树，接到高度较高的树下面，具体的yxc没讲，这种优化用的比较少，而且好像也没有很有用

并查集在面试中经常考察。
### [AcWing 836. 合并集合](https://www.acwing.com/problem/content/838/)
裸并查集，不带任何额外信息
```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10;
int n, m;
int p[N]; //存每个节点的父亲节点编号

int find(int x) {
	if(p[x] != x) p[x] = find(p[x]); // 路径压缩, 递归方式, 可能会由于递归过深而栈溢出
	return p[x];
}

int find2(int x) {
    int r = x;
    while(p[r] != r) r = p[r]; // 先找到根
    // 再通过迭代循环的方式进行路径压缩
    int t;
    while(p[x] != x) {
        t = x;
        x = p[x];
        p[t] = r;
    }
    return r;
}

int main() {
	scanf("%d%d", &n, &m);
	for(int i = 0; i < n; i++) p[i] = i; // 初始化
	while(m--) {
//strlen()函数以’\0’字符判断字符串结束，输入的时候会把这个’\0’字符存储在op[1]
//char数组一般用scanf(“%s”)读入，string一般用cin读入，前者是c的字符串写法，后者是c++的字符串写法，同时写会出问题
//总结，用scanf读入一个字符，最好读入一个字符串，因为scanf读入字符串会自动把空格、回车、制表符忽略掉，可以降低我们出错的概率
		char op[2];
		int a, b;
		scanf("%s%d%d", op, &a, &b);
		if(op[0] == 'M') {
			p[find(a)] = find(b);
		} else if(op[0] == 'Q') {
			if(find(a) == find(b)) printf("Yes\n");
			else printf("No\n");
		}
	}
	return 0;
}
```

### [AcWing 837. 连通块中点的数量](https://www.acwing.com/problem/content/839/)
本题还要额外维护集合中元素的个数

```cpp
#include<iostream>
#include<string>
using namespace std;

const int N = 1e5 + 10;
int n, m;
int p[N], cnt[N];

int find(int x) {
	if(p[x] != x) p[x] = find(p[x]);
	return p[x];
}

int main() {
	scanf("%d%d", &n, &m);
	for(int i = 0; i < n; i++) {
		p[i] = i; // 初始化
		cnt[i] = 1;
	}
	while(m--) {
		string op;
		int a, b;
		cin >> op;
		if(op == "C") {
			cin >> a >> b;
			if(find(a) == find(b)) continue; // 特判一下，若同属一个集合, 后续操作不用再进行
			cnt[find(b)] += cnt[find(a)]; // 将b集合的元素个数加上a的元素个数, 要先加, 再把a接到b
			p[find(a)] = find(b); // 将a接到b
		} else if(op == "Q1") {
			cin >> a >> b;
			if(find(a) == find(b)) printf("Yes\n");
			else printf("No\n");
		} else if(op == "Q2") {
			cin >> a;
			printf("%d\n", cnt[find(a)]);
		}
	}
	return 0;
}
```

### [Acwing 240. 食物链](https://www.acwing.com/problem/content/242/)

用并查集维护额外信息

（并查集的变形，本题是带权并查集，可以额外维护每个节点到根节点的距离）

维护每个点到根节点的距离，用不同的距离来表示不同种类的动物。每个点到根节点的距离模3余0，表示是1类，模3余1，表示是2类，模3余2，表示是3类。其中，2类吃1类，3类吃2类，1类吃3类。

![](https://pic4.zhimg.com/80/v2-1c78c8603891ec19058fbf23b611a0f7.png)

```cpp
#include<iostream>
using namespace std;

const int N = 5e4 + 10;
int n, m;
int p[N], d[N]; // d是到根节点的距离

int find(int x) {
	if(p[x] != x) {
		int t = find(p[x]);
		d[x] += d[p[x]];
		p[x] = t;
	}
	return p[x];
}

int main() {
	scanf("%d%d", &n, &m);
	for(int i = 1; i <= n; i++) p[i] = i;

	int res = 0;
	while(m--) {
		int t, x, y;
		scanf("%d%d%d", &t, &x, &y);
		if(x > n || y > n) res++;   //假话
		else {
			int px = find(x), py = find(y);
			if(t == 1) {    //到根节点距离Mod3不同说明是假话
				if(px == py && (d[x] - d[y]) % 3) res++;
				else if(px != py) {//px py不在一个集合里面，要放到一个集合里面
					p[px] = py;
					d[px] = d[y] - d[x];//mod3同余，这里复习好好看一下
				}
			} else {
				if(px == py && (d[x] - d[y] - 1) % 3) res++;
				else if(px != py) {
					p[px] = py;
					d[px] = d[y] + 1 - d[x];
				}
			}
		}
	}
	printf("%d", res);
	return 0;
}
```

**小结**

并查集最核心的部分，就是记录每个节点的父节点的数组`p[]`，以及查找某个节点所属的树的根节点的函数`find()`，以及路径压缩

初始化使得全部`p[i] = i`，表示每个点都是一个独立的集合。

合并时直接将一个集合的根节点，直接接入到另一个集合的根节点下面即可，即`p[find(a)] = find(b)`

核心就是找到某个节点所属的树的根节点

```c
int find(int x) {
    if(p[x] != x) p[x] = find(p[x]); // 路径压缩
    return p[x];
}
```

## 堆
堆的基本操作（以小根堆为例）
(STL支持1,2,3)，在STL中就是优先队列,priority_queue
1.  **插入一个数**
2.  **求集合当中的最小值**
3.  **删除最小值**
4.  删除任意一个元素
5.  修改任意一个元素

堆的基本结构是一颗完全二叉树。以小根堆为例，每个节点都要小于其左右两个子树种的所有节点。

通常用数组来模拟存储一颗二叉树，采用二叉树层序遍历的方式作为数组的下标。若数组下标从0开始，若某个节点下标为x，则其左儿子下标为2x + 1，其右儿子下标为2x + 2。若数组下标从1开始，若某个节点下标为x，则其左儿子下标为2x，右儿子下标为2x + 1。

堆通过**向下调整**（down）和**向上调整**（up）来维持堆的特性。

down操作用来将一个较大的数，下沉到合适的位置

up操作用来将一个较小的数，上浮到合适的位置

这两个操作的复杂度都是$O（log N）$

可以通过down和up操作，完成上述的5个堆的基本操作（数组下标从1开始）

1.  **插入一个数**

    插入到数组末尾，并对于新插入的这个数，向上调整

    `heap[++size] = x; up(size);`

2.  **求集合当中的最小值**

    直接返回堆顶，即数组的首元素

    `heap[1]`

3.  **删除最小值**

    先交换堆顶和堆尾，然后堆的大小减一，再针对新的堆顶，向下调整

    `swap(heap[1], heap[size]); size--; down(1)`

4.  删除任意一个元素

    交换当前元素和堆尾，然后堆的大小减一，再根据新的当前元素的大小，决定是做down操作还是做up操作
    也可以不管这么多把down和up都做一遍

    `swap(heap[i], heap[size]); size--; down(i) 或者 up(i)`

5.  修改任意一个元素

    直接修改，并且根据修改后的新值，来决定做down还是up

    `heap[i] = x; down(i) 或者 up(i)`

建堆，一个一个往里面插入时$O（N \times log N）$

可以从2/n往上down到n即可，也就是从堆尾往上，找到第一个非叶子节点，从第一个非叶子节点往前，对所有的非叶子节点，依次执行down操作。这样，**建堆的时间复杂度是O(n)**。可以用错位相减法计算复杂度。

若数组下标从1开始，且堆总共有n个元素，则从后往前，第一个非叶子节点的下标为n/2。

### [AcWing 838. 堆排序](https://www.acwing.com/problem/content/840/)
本题只需要用到求最小值和删除堆顶操作，只用down操作就可以了
```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10;

int h[N], hs;//hs是堆大小
int n, m;

// 堆的下标从1开始
void down(int x) {
	int min = x;
	if(2 * x <= hs && h[2 * x] < h[min]) min = 2 * x;//有左儿子，且左儿子更小
	if(2 * x + 1 <= hs && h[2 * x + 1] < h[min]) min = 2 * x + 1;
	if(min != x) {
		swap(h[min], h[x]); // 需要调整
		down(min); // 递归调整
	}
}

int main() {
	scanf("%d%d", &n, &m);
	for(int i = 1; i <= n; i++) scanf("%d", &h[i]);
	hs = n;
	for(int i = n / 2; i >= 1; i--) down(i); // 这个建堆过程实际的时间复杂度是O(n)
	while(m--) {
		printf("%d ", h[1]);//输出堆顶元素
		swap(h[1], h[hs]);//
		hs--;
		down(1);
	}
	return 0;
}
```

堆的两个基本操作：down和up
```cpp
// u是往下调整的节点下标
void down(int u) {
    int t = u;
    if(u * 2 <= size && h[u * 2] < h[t]) t = u * 2;
    if(u * 2 + 1 <= size && h[u * 2 + 1] < h[t]) t = u * 2 + 1;
    if(u != t) {
        swap(h[u], h[t]);
        down(t); // 因为最多是logn的复杂度, 可以直接用递归, 不用担心溢出
    }
}

void up(int u) {
    while(u / 2 > 0 && h[u / 2] > h[u]) {
        swap(h[u / 2], h[u]);
        u /= 2;
    }
}
```

### [AcWing 839. 模拟堆](https://www.acwing.com/problem/content/841/)

```cpp
#include<iostream>
#include<string>
using namespace std;
const int N = 1e5 + 10;
int h[N], ph[N], hp[N];
// ph[i] = k 表示第i个插入的数, 在堆中的节点的下标是k,pointer2heap
// hp[k] = i 表示堆中下标为k的节点，是第i个插入的
int hSize, n;

void heap_swap(int i, int j) {
	swap(ph[hp[i]], ph[hp[j]]);
	swap(hp[i], hp[j]);
	swap(h[i], h[j]);
}

void down(int i) {
	int min = i;
	int leftSon = 2 * i;
	if(leftSon <= hSize && h[leftSon] < h[min]) min = leftSon;
	if(leftSon + 1 <= hSize && h[leftSon + 1] < h[min]) min = leftSon + 1;
	if(min != i) {
		heap_swap(i, min);
		down(min);
	}
}

void up(int i) {
	while(i > 1 && h[i] < h[i / 2]) {
		heap_swap(i, i / 2);
		i /= 2;
	}
}

int main() {
	scanf("%d", &n);
	string op;
	int x, k;
	int insertCnt = 0;
	for(int i = 1; i <= n; i++) {
		cin >> op;
		if(op == "I") {
			scanf("%d", &x);
			h[++hSize] = x;
			ph[++insertCnt] = hSize;
			hp[hSize] = insertCnt;
			up(hSize);
		} else if(op == "PM") {
			printf("%d\n", h[1]);
		} else if(op == "DM") {
			heap_swap(1, hSize--);
			down(1);
		} else if(op == "D") {
			scanf("%d", &k);
			int hPos = ph[k];
			heap_swap(hPos, hSize--);
			down(hPos);
			up(hPos);
		} else if(op == "C") {
			scanf("%d%d", &k, &x);
			int hPos = ph[k];
			h[hPos] = x;
			down(hPos);
			up(hPos);
		}
	}
	return 0;
}
```