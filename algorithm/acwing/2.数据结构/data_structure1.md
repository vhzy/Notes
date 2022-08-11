#! https://zhuanlan.zhihu.com/p/551806746
- [数据结构Part1](#数据结构part1)
  - [链表](#链表)
    - [AcWing 826. 单链表](#acwing-826-单链表)
    - [AcWing 827. 双链表](#acwing-827-双链表)
  - [栈和队列](#栈和队列)
    - [AcWing 828. 模拟栈](#acwing-828-模拟栈)
    - [AcWing 3302. 表达式求值](#acwing-3302-表达式求值)
    - [AcWing 829. 模拟队列 ](#acwing-829-模拟队列-)
    - [AcWing 830. 单调栈](#acwing-830-单调栈)
    - [AcWing 154. 滑动窗口](#acwing-154-滑动窗口)
  - [KMP算法](#kmp算法)

# 数据结构Part1

本节主要说了：
- 链表与邻接表
- 栈和队列
- KMP算法

## 链表

使用数组模拟**单链表**，**双链表**

使用数组模拟的链表，为**静态链表**，对单链表，开2个数组，其中1个用来存每个链表节点的**值**，另1个数组用来存每个节点的**next指针**。

对双链表，开3个数组，其中1个用来存每个链表节点的值，另外2个数组用来存每个节点的**prev**和**next**指针

单链表，用到比较多的是**邻接表**，邻接表经常用来存储**图**和**树**。（会在后续第三章讲图论时带出）

插入节点一般使用头插法

### [AcWing 826. 单链表](https://www.acwing.com/problem/content/828/)
```cpp
#include <iostream>

using namespace std;

const int N = 100010;


// head 表示头结点的下标
// e[i] 表示节点i的值
// ne[i] 表示节点i的next指针是多少
// idx 存储当前已经用到了哪个点
int head, e[N], ne[N], idx;

// 初始化
void init()
{
    head = -1;
    idx = 0;
}

// 将x插到头结点
void add_to_head(int x)
{
    e[idx] = x, ne[idx] = head, head = idx ++ ;
}

// 将x插到下标是k的点后面
void add(int k, int x)
{
    e[idx] = x, ne[idx] = ne[k], ne[k] = idx ++ ;
}

// 将下标是k的点后面的点删掉
void remove(int k)
{
    ne[k] = ne[ne[k]];
}

int main()
{
    int m;
    cin >> m;

    init();

    while (m -- )
    {
        int k, x;
        char op;

        cin >> op;
        if (op == 'H')
        {
            cin >> x;
            add_to_head(x);
        }
        else if (op == 'D')
        {
            cin >> k;
            if (!k) head = ne[head];
            else remove(k - 1);//注意删除第k个输入后面的数，那函数里放的是下标，k要减去1
        }
        else
        {
            cin >> k >> x;
            add(k - 1, x);
        }
    }

    for (int i = head; i != -1; i = ne[i]) cout << e[i] << ' ';
    cout << endl;

    return 0;
}
```

### [AcWing 827. 双链表](https://www.acwing.com/problem/content/829/)

```cpp
#include <iostream>

using namespace std;

const int N = 100010;

int m;
int e[N], l[N], r[N], idx;

// 在节点a的右边插入一个数x
void insert(int a, int x)
{
    e[idx] = x;
    l[idx] = a, r[idx] = r[a];
    l[r[a]] = idx, r[a] = idx ++ ;
}

// 删除节点a
void remove(int a)
{
    l[r[a]] = l[a];
    r[l[a]] = r[a];
}

int main()
{
    cin >> m;

    // 0是左端点，1是右端点
    r[0] = 1, l[1] = 0;
    idx = 2;

    while (m -- )
    {
        string op;
        cin >> op;
        int k, x;
        if (op == "L")
        {
            cin >> x;
            insert(0, x);
        }
        else if (op == "R")
        {
            cin >> x;
            insert(l[1], x);
        }
        else if (op == "D")
        {
            cin >> k;
            remove(k + 1);
        }
        else if (op == "IL")
        {
            cin >> k >> x;
            insert(l[k + 1], x);
        }
        else
        {
            cin >> k >> x;
            insert(k + 1, x);
        }
    }

    for (int i = r[0]; i != 1; i = r[i]) cout << e[i] << ' ';
    cout << endl;

    return 0;
}
```

## 栈和队列
栈，特性是**后进先出**，逻辑上可以理解为只有一个开口的桶，

队列，特性是**先进先出**，逻辑上可以理解为在两端有开口的桶，只能从其中一端插入，另一端取出，就像排队一样，先排队的会先被服务，后排队的后被服务。

### [AcWing 828. 模拟栈](https://www.acwing.com/problem/content/830/)

```cpp
#include <iostream>

using namespace std;

const int N = 100010;

int m;
int stk[N], top;

int main()
{
    cin >> m;
    while (m -- )
    {
        string op;
        int x;

        cin >> op;
        if (op == "push")
        {
            cin >> x;
            stk[ ++ top] = x;
        }
        else if (op == "pop") top -- ;
        else if (op == "empty") cout << (top ? "NO" : "YES") << endl;
        else cout << stk[top] << endl;
    }

    return 0;
}
```

### [AcWing 3302. 表达式求值](https://www.acwing.com/problem/content/3305/)

这道题是用栈来模拟树的中序遍历，从而求解中缀表达式的值，题解参考[https://www.acwing.com/solution/content/69284/](https://www.acwing.com/solution/content/69284/)，核心思想是双栈（操作数栈，运算符栈），加上运算符优先级。相对应的，后缀表达式的求值就非常简单，只需要一个操作数栈即可。

遇到各节点后的处理

1.  数字

    数字并不会产生计算过程, 所以只需提取数字, 将数字压栈

2.  括号

    括号分为两个运算符 `(` 和 `)`

    遇到 `(` 说明会往下走, 所以只需将 `(` 压栈

    遇到 `)` 说明会往上走, 所以要计算括号表示的子树的结果, 所以要逆向计算运算符直至遇到 `(`

3.  普通二元运算符

    如果当前运算符优先级比上一运算符高, 说明是往下走, 则只需将运算符压栈

    如果当前运算符优先级比上一运算符低, 说明是往上走, 则需要一直计算上一运算符直至当前运算符优先级比上一运算符高

```c++
#include <iostream>
#include <cstring>
#include <unordered_map>
#include <stack>
using namespace std;

// 运算符优先级
unordered_map<char, int> p = {{'+', 1}, {'-', 1}, {'*', 2}, {'/', 2}};

stack<int> num;
stack<char> op;

bool is_digit(char c) {
	return c >= '0' && c <= '9';
}

// 执行计算, 弹出2个操作数和1个运算符, 直接计算, 并将结果重新压栈
void eval() {
	int b = num.top(); num.pop();
	int a = num.top(); num.pop();
	char c = op.top(); op.pop();
	int res = 0;
	if(c == '+') res = a + b;
	else if(c == '-') res = a - b;
	else if(c == '*') res = a * b;
	else res = a / b;
	num.push(res);
}

int main() {
	string s;
	cin >> s;
	int res = 0;
	for(int i = 0; i < s.size(); i++) {
		if(is_digit(s[i])) {
		    // 提取连续的数字
			int x = 0, j = i;
			while(j < s.size() && is_digit(s[j])) {
				x = x * 10 + s[j] - '0';
				j++;
			}
			num.push(x);
			i = j - 1;
		} else if(s[i] == '(') op.push(s[i]);
		else if(s[i] == ')') {
			while(op.top() != '(') eval();
			op.pop();
		} else {
			while(!op.empty() && p[op.top()] >= p[s[i]]) eval();//输入运算符比栈顶运算符优先级低
			op.push(s[i]);
		}
	}
	while(!op.empty()) eval();//剩余的进行计算
	printf("%d\n", num.top());
	return 0;
}
```

### [AcWing 829. 模拟队列 ](https://www.acwing.com/problem/content/831/)

```cpp
#include<iostream>
#include<string>
using namespace std;

const int N = 1e5 + 10;
int queue[N];
int head = 0, tail = -1;

void push(int x) { queue[++tail] = x; }

void pop() { head++; }

bool empty() { return head > tail; }

int query() { return queue[head]; }

int main() {
	int n, x;
	cin >> n;
	while(n--) {
		string op;
		cin >> op;
		if(op == "push") {
			cin >> x;
			push(x);
		} else if(op == "pop") {
			pop();
		} else if(op == "empty") {
			if(empty()) printf("YES\n");
			else printf("NO\n");
		} else if(op == "query") {
			printf("%d\n", query());
		}
	}
	return 0;
}

```

### [AcWing 830. 单调栈](https://www.acwing.com/problem/content/832/)

应用场景：给定一个序列，对于序列中的每个数，求解它左边离他最近且比它小的数（或者右边，或者比它大）

比如对于序列`[3, 4, 2, 7, 5]`，求解每个数左边最近的且比它小的数（不存在则返回-1），答案是

`[-1, 3, -1, 2, 2]`

考虑的方法和双指针类似，先想一下暴力做法，再进行优化

暴力做法就是，先枚举i = 0~n，然后枚举j，j从i-1开始到0

```c
int a[n] = {3, 4, 2, 7, 5};
for(int i = 0; i < n; i++) {
    for(int j = i - 1; j >= 0; j--) {
        if(a[i] > a[j]) {
            printf("%d ", a[j]); // 输出
            break; // 跳出循环, 继续对下一个i进行处理
        }
    }
}

```

如果采用栈来做的话，就是对于i = 0~n，用一个栈来存i前面所有的数，而我们观察发现，有的数是不会作为答案的。对于 i 前面的数，比如 m 和 n 都小于i ，假设 m < n，则a[m]在a[n]的左边，如果a[m] ≥ a[n]，则a[m]是不会作为答案输出的。因为i往左寻找，最多找到n这个位置，而a[n]要比a[m]更小，所以不会再往左找到m。于是，我们只需要保证栈中的元素有单调性即可。

即，若m < n，且a[m] >= a[n]，则往栈中压入a[n]时，会删除先前压入的a[m]。最后保证栈中的元素是升序排列的。

而当需要找第i个数的左边最近的且比它小的数时，先将a[i]和栈顶元素比较，若栈顶元素≥a[i]，则弹出栈顶元素。因为对i后面的数，答案最多取到a[i]，所以此时的栈顶对i后面的数是无用的，直接删除。一直删除栈顶元素，直到栈顶元素＜a[i]，此时的栈顶就是答案，再把a[i]压入栈，继续下一个位置的判断。

每个元素都只有一次压栈和出栈的机会，所以时间复杂度是O(n)

![单调栈](https://pic4.zhimg.com/80/v2-56889addf5a59612965697d7cc4f4ab6.gif)

```cpp
// 每个元素都只有一次压栈和出栈的机会，所以时间复杂度是O(n)
#include<iostream>
using namespace std;
const int N = 1e5 + 10;
int stk[N];
int top;

int main() {
    int n, t;
    scanf("%d", &n);
    for(int i = 0; i < n; i++) {
        scanf("%d", &t);
        while(top > 0 && stk[top] >= t) top--; // 保持栈为单调递增
        if(!top) printf("-1 "); // 栈空
        else printf("%d ", stk[top]);
        stk[++top] = t; // 入栈
    }
    return 0;
    
}
```

### [AcWing 154. 滑动窗口](https://www.acwing.com/problem/content/156/)
最经典的应用：求解滑动窗口中的最大值和最小值

也是先想一个暴力的做法，然后考虑一下能删掉那些元素，是否能得到单调性。

最大值滑动窗口队列单调递减，队头就是最大值
最小值滑动窗口队列单调递增，队头就是最小值

解题思路（以最大值为例）：

由于我们需要求出的是滑动窗口的最大值。

*   如果当前的滑动窗口中有两个下标 `i` 和 `j` ，其中`i`在`j`的左侧（`i`<`j`），并且`i`对应的元素不大于j对应的元素（`nums[i]≤nums[j]`），则：

    当滑动窗口向右移动时，只要 `i` 还在窗口中，那么 `j` 一定也还在窗口中。这是由于 `i` 在 `j` 的左侧所保证的。

    **因此，由于 `nums[j]` 的存在，`nums[i]` 一定不会是滑动窗口中的最大值了，我们可以将`nums[i]`永久地移除。**

*   因此我们可以使用一个队列存储所有还没有被移除的下标。在队列中，这些下标按照从小到大的顺序被存储，并且它们在数组`nums`中对应的值是严格单调递减的。

*   当滑动窗口向右移动时，我们需要把一个新的元素放入队列中。

    为了保持队列的性质，我们会不断地将新的元素与队尾的元素相比较，如果新元素大于等于队尾元素，那么队尾的元素就可以被永久地移除，我们将其弹出队列。我们需要不断地进行此项操作，直到队列为空或者新的元素小于队尾的元素。

*   由于队列中下标对应的元素是严格单调递减的，因此此时队首下标对应的元素就是滑动窗口中的最大值。

*   窗口向右移动的时候。因此我们还需要不断从队首弹出元素保证队列中的所有元素都是窗口中的，因此当队头元素在窗口的左边的时候，弹出队头。
```cpp
#include<iostream>
using namespace std;

const int N = 1e6 + 10;

int n, k;
int a[N], q[N]; // 其中a数组存放原始的数据, q数组用来做单调队列

int main() {
	scanf("%d%d", &n, &k);
	for(int i = 0; i < n; i++) scanf("%d", &a[i]);

	// 找出滑动窗口的最小值
	int hh = 0, tt = -1; // hh是队头, tt是队尾
	for(int i = 0; i < n; i++) {
		// 队列非空, 且对头下标在滑动窗口左边界的左侧时, 移除队头
		while(hh <= tt && q[hh] < i - k + 1) hh++;
		while(hh <= tt && a[q[tt]] >= a[i]) tt--; // 当队尾元素 >= 当前元素时, 移除队尾
		q[++tt] = i; // 队列里从队头到队尾, 是单调递增的, 队头元素就是当前滑动窗口的最小值
		if(i >= k - 1) printf("%d ", a[q[hh]]); // 从第k个位置开始, 进行输出
	}
	printf("\n");

	// 找出滑动窗口的最大值
	hh = 0, tt = -1;
	for(int i = 0; i < n; i++) {
		while(hh <= tt && q[hh] < i - k + 1) hh++;
		while(hh <= tt && a[q[tt]] <= a[i]) tt--;// 当队尾元素 <= 当前元素时, 移除队尾
		q[++tt] = i; // 队列里从队头到队尾, 是单调递减的,  队头元素就是当前滑动窗口的最大值
		if(i >= k - 1) printf("%d ", a[q[hh]]);
	}
	return 0;
}

```

## KMP算法
时间复杂度O(n)的模式匹配算法。详解参考这篇文章[一文看懂KMP算法](https://blog.csdn.net/vcj1009784814/article/details/116662859)或者`算法竞赛进阶指南`的字符串一章


[AcWing 831. KMP字符串](https://www.acwing.com/problem/content/description/833/)
```cpp
#include<iostream>
using namespace std;
const int N = 1e5 + 10, M = 1e6 + 10;
char p[N], s[M];
int ne[N]; // 针对模式串P的next数组
int n, m;

int main() {
    // 字符串的起始下标从1开始, 方便处理边界
    cin >> n >> p + 1 >> m >> s + 1;
    /* 如果用scanf读入的话
    scanf("%d", &n);
    scanf("%s", p + 1);
    scanf("%d", &m);
    scanf("%s", s + 1);
    */
    // 先求解 next 数组
    // 下标从1开始取, next[i] 的值, 表示以 i 为右端点的字串, 最大的前缀和后缀的长度, 这个长度不能超过 i
    // 故 next[1] 的 值不能超过1, 故 next[1] = 0, 从下标 2 开始计算 next数组
    for(int i = 2, j = 0; i <= n; i++) {
        // 错开一位进行匹配, 每次匹配 i 和 j + 1 位, 第一次则匹配 2 和 1 
        while(j > 0 && p[i] != p[j + 1]) j = ne[j]; // 当前面有匹配上的位时, 看看当前位是否匹配, 若不匹配, 需要回溯 j 
        if(p[i] == p[j + 1]) j++; // 该位匹配上了, 则 j 往后移动一位, 并且当前位置的 next[i] = j;
        ne[i] = j;
    }
    // 求解完毕 next 数组, 开始进行模式匹配
    for(int i = 1, j = 0; i <= m; i++) {
        while(j > 0 && s[i] != p[j + 1]) j = ne[j]; // 回溯 j
        if(s[i] == p[j + 1]) j++; // 当前位匹配, 后移j
        if(j == n) {
            // 匹配完成, 开始下一次可能的匹配
            printf("%d ", i - n);//题目的输出是从0开始，原本应该是i-n+1，现在就不用+1了
            j = ne[j];
        }
    }
    return 0;
}
```

暴力做法：
```cpp
#include<iostream>
using namespace std;

const int N = 1e6 + 10, M = 1e5 + 10;
char s[N], p[M];

int main() {
	int n, m; // 主串S和模式串P的长度
	cin >> n >> m;
	// 读入主串S和模式串P, 下标都从1开始
	cin >> s + 1 >> p + 1;

	// 枚举 i = [1, n], 尝试匹配
	int i, j;
	for(i = 1; i <= n; i++) {
		for(j = 1; j <= m; j++) {
			if(s[i + j - 1] != p[j]) break;
		}
		if(j == m + 1) printf("%d ", i); // 匹配成功, 打印起始坐标
	}
	return 0;
}
```