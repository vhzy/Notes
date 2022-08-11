#! https://zhuanlan.zhihu.com/p/552584244
- [数据结构Part3](#数据结构part3)
  - [哈希表](#哈希表)
    - [哈希表的存储](#哈希表的存储)
      - [Acwing 840.模拟散列表](#acwing-840模拟散列表)
    - [字符串哈希](#字符串哈希)
      - [AcWing 841. 字符串哈希](#acwing-841-字符串哈希)
  - [STL](#stl)
    - [vector](#vector)
    - [pair](#pair)
    - [string](#string)
    - [queue](#queue)
    - [priority\_queue](#priority_queue)
    - [stack](#stack)
    - [deque](#deque)
    - [set](#set)
    - [map](#map)
    - [bitset](#bitset)


# 数据结构Part3

本节主要说了：
- 哈希表
- STL容器


## 哈希表

哈希表的作用：把一个比较大的空间，映射到一个比较小的空间。

一般做哈希运算时，取一个质数作为模，会使得冲突的概率降低

离散化可以看作一种特殊的哈希，离散化需要保序
哈希和离散化可以看这篇[文章](https://blog.csdn.net/weixin_52278699/article/details/118855796)
### 哈希表的存储

冲突解决方法

*   开放寻址法
*   拉链法

#### [Acwing 840.模拟散列表](https://www.acwing.com/problem/content/842/)

拉链法
一般不需要删除哈希表元素，如果一定要删去，一般是开一个数组，在对应位置大标记，表示删除
取模要去质数，且离2的整次幂尽可能的远。
![](https://pic4.zhimg.com/80/v2-83b5f182cbd2692d3674c84f8299bcfd.png)

```cpp
#include<iostream>
#include<cstring>
using namespace std;

const int N = 1e5 + 3;//大于1e5的第一个质数

int h[N]; // 存储的都是节点的下标，拉链槽
int e[N], ne[N], idx; // 存储节点值和next指针

int mod(int x) {
	return (x % N + N) % N;//C++里面负数取模是负数，正数取模是正数，这里保证都是正数
}

void insert(int x) {
	int k = mod(x);//k是hash值
	e[idx] = x; // 新分配一个节点
	ne[idx] = h[k]; // 这个节点的next指向链表头
	h[k] = idx; // 新的链表头
	idx++;
}

bool query(int x) {
	int k = mod(x);
	for(int i = h[k]; i != -1; i = ne[i]) {
		if(e[i] == x) return true;
	}
	return false;
}


int main() {
    int n;
	scanf("%d", &n);
	memset(h, -1, sizeof h); // -1表示空节点
	char op;
	int x;
	while(n--) {
		cin >> op >> x;
		if(op == 'I') {
			insert(x);
		} else if(op == 'Q') {
			if(query(x)) printf("Yes\n");
			else printf("No\n");
		}
	}
	return 0;
}
```

开放寻址法
只开一维数组，不需要开链表，但是一维数组长度经验上是题目数据范围的2~3倍
![](https://pic4.zhimg.com/80/v2-89e9f350aa6601bd2b9f1ef3365743c3.png)


```cpp
#include <cstring>
#include <iostream>

using namespace std;

const int N = 200003, null = 0x3f3f3f3f;//表示这个位置是空的

int h[N];

int find(int x)
{
    int t = (x % N + N) % N;
    while (h[t] != null && h[t] != x)
    {
        t ++ ;
        if (t == N) t = 0;//看完最后一个位置，循环看第一个位置
    }
    return t;//不成功的话也要返回应该存储的位置
}

int main()
{
    memset(h, 0x3f, sizeof h);

    int n;
    scanf("%d", &n);

    while (n -- )
    {
        char op[2];
        int x;
        scanf("%s%d", op, &x);
        if (*op == 'I') h[find(x)] = x;
        else
        {
            if (h[find(x)] == null) puts("No");
            else puts("Yes");
        }
    }

    return 0;
}
```

注意，memset函数，是按字节来设置值的，上面定义了`null`为`0x3f3f3f3f`，这调用memset时，只需要设置为`0x3f`即可。

特殊的，如果要初始化为0或者-1，则直接设置为0或-1就可以了，因为0的二进制表示是全零（`00000000`），-1是全1（`11111111`）。设置1个字节和4个字节是一样的。


### 字符串哈希

字符串前缀哈希法：对于字符串每个位置作为前缀，求一下其哈希值

如，有字符串 s = `ABCDE`

则求解的哈希数组

`h[1]` = `A` 的哈希值

`h[2]` = `AB` 的哈希值

`h[3]` = `ABC` 的哈希值

…

如何求解一个字符串的哈希值？

将字符串看成一个P进制的数，比如字符串`ABCD`，我们把A映射为1，B映射为2，C映射为3，D映射为4。则`ABCD`可以看成一个P进制的数字`1234`。则`ABCD`这个字符串的哈希值为

(1 × P3 + 2 × P2 + 3 × P1 + 4 × P0 ） mod Q

**通常不要把一个字母映射为0**，这样会导致重复。比如把A映射为0，则A是0，AA也是0，AAA还是0。

在做字符串哈希时，我们不考虑冲突的情况。

我们可以取 P = 131或13331，Q = 2^64 ，这样在99.99%的情况下是不会出现冲突的（据yxc所说）

可以将`h`数组的类型取成`unsigned long long`（64位），这样就无需对2^64 取模，溢出就直接相当于取模

**求解字符串前缀哈希值有什么用？**

可以求解任意的子串的哈希值！ 这是使用KMP算法都不好做到的。

**可以用于快速判断两个字符串是否相等。**（用模式匹配需要至少O(n)，而字符串哈希只需要O(1)）

比如我们要求解字符串S中`[L,R]`这段子串的哈希值

我们可以先得到`h[L-1]`的值，以及`h[R]`的值

先将`h[L-1]`左移`R-L+1`位（P进制），让其与`h[R]`对齐，然后二者相减，便得到了`[L,R]`区间的子串表示的P进制的数

即 $h[R] - h[L-1] × P^{R-L+1}$

并且，在计算字符串S的前缀哈希值时，容易得到如下的递推式

`h[i] = h[i - 1] × P + S[i]`

与KMP对比：KMP可以来做循环节问题，其他都可以用字符串哈希
#### [AcWing 841. 字符串哈希](https://www.acwing.com/problem/content/843/)

```cpp
#include<iostream>
using namespace std;

const int P = 131, N = 1e5 + 10;

typedef unsigned long long ULL;

// h[N] 用来存字符串前缀哈希, p[N] 用来存p的幂
ULL h[N], p[N];
int n, m;
char str[N];

ULL get(int l, int r) {
	return h[r] - h[l - 1] * p[r - l + 1];
}

int main() {
	scanf("%d%d%s", &n, &m, str + 1);

	p[0] = 1; // p[] 存 p 的幂
	for(int i = 1; i <= n; i++) {
		// 初始化h数组
		p[i] = p[i - 1] * P;
		h[i] = h[i - 1] * P + str[i];//str[i]不是0就可以，是多少都无所谓
	}
	while(m--) {
		int l1, r1, l2, r2;
		scanf("%d%d%d%d", &l1, &r1, &l2, &r2);
		if(get(l1, r1) == get(l2, r2)) printf("Yes\n");
		else printf("No\n");
	}
	return 0;
}
```

## STL

C++的STL库中提供了很多的数据结构，包括一些很复杂的数据结构。

本小节讲解了C++的STL库中常用的一些数据结构，主要包括了

*   vector

    变长数组，基本思想是**倍增**（类似于java中的ArrayList）

*   pair

    存储一个二元组，二元组的变量类型可以任意

*   string

    字符串，常用的函数`substr()`，`c_str()`

*   queue

    队列，`push()`，`front()`，`back()`，`pop()`

*   priority\_queue

    优先队列，本质是个堆。`push()`，`top()`，`pop()`

*   stack

    栈。`push()`，`top()`，`pop()`

*   deque

    双端队列。可以在队头队尾进行插入删除，并且支持随机访问

*   set，map，multiset，multimap

    基于平衡二叉树（红黑树），动态维护有序序列。这些set/map支持跟排序相关的操作，如lower\_bound/upper\_bound方法，也支持迭代器的`++`和`--`，但是其增删改查的时间复杂度是O(logn)。

*   unordered\_set，unordered\_map，unordered\_multiset，unordered\_multimap

    基于哈希表。这些set和map和上面的set/map类似。但是这些unordered的set/map的增删改查的时间复杂度是O(1)，效率比上面的更快，但不支持lower\_bound()和upper\_bound()，也不支持迭代器的`++`和`--`

    如使用unordered\_map，则需要头文件`#include<unordered_map>`

*   bitset

    压位

### vector

```c
#include<iostream>
#include<vector>
using namespace std;

int main() {
    vector<int> a; // 最简单的初始化方式
    vector<int> a(10); // 定义一个长度为10的vector
    vector<int> a(10, 3); //定义一个长度为10的vector,并将每个元素初始化为3
    vector<int> a[10]; // 定义一个vector数组，数组大小为10

    // vector支持的函数
    a.size(); // vector中的元素个数
    a.empty(); // vector是否为空
    // 上面2个方法的时间复杂度是O(1), 并且其他的容器都有这2个方法
    a.clear(); // 清空
    a.front(); // 返回第一个
    a.back();
    a.push_back();
    a.pop_back();
    a.begin(); // 是第一个元素的位置
    a.end(); // 是最后一个元素的下一个位置
    // vector支持用[]进行随机寻址, 这一点与数组相同
    a[0]; // 取vector中第一个元素
    // vector支持比较运算
    vector<int> a(4, 3), b(3, 4);
    // a = [3,3,3,3]   b = [4,4,4]
    if(a < b) printf("a < b\n"); // 比较大小时是按照字典序

    // vector的遍历
    vector<int> a;
    for(int i = 0; i < 10; i++) a.push_back(i);
    for(int i = 0; i <a.size(); i++) cout << a[i] << " ";
    cout << endl;

    for(vector<int>::iterator it = a.begin(); i != a.end(); i++) cout << *i << " ";
    cout << endl;

    // C++ 11 的新特性, for each 遍历
    for(auto x : a) cout << x << " ";
    cout << endl;
    return 0;
}

```

注意：操作系统为某一个程序分配内存空间所需要的时间，与要分配的空间大小无关。只与分配次数有关。比如请求分配一个大小为1的空间，和请求分配一个大小为100的空间，所需时间是一样的。

比如，一次申请大小为1000的数组，与申请1000次大小为1的数组，它们各自所需的时间，就是1000倍的关系。

所以，变长数组，要尽量减少申请空间的次数。

所以vector的倍增，大概就是，每次数组长度不够时，就把大小扩大一倍（新申请一个大小为原先2倍的数组），并把旧数组的元素copy过来

若一个vector最终元素个数为n，则其分配空间的次数为logn。拷贝元素的次数约为n。平均到每个元素上的时间复杂度就是O(1)

### pair

pair定义在`utility`库中，通常直接引入`iostream`就能够使用

```c
#include<iostream>
using namespace std;

int main() {
    pair<int,string> p;
    p.first; //第一个元素
    p.second; //第二个元素
    //pair也支持比较运算，以first为第一关键字，second为第二关键字
    // 构造一个pair
    p = make_pair(10, "hby");
    p = {10, "hby"}; // C++ 11 可以直接这样初始化
    // 当某一个事物有2个属性时，并且需要按照某一个属性进行排序时，
    // 可以将需要排序的属性放到fisrt, 另一个属性放到second

    // 当然也可以用pair来存3个属性, 如下
    pair<int, pair<int, int>> p;
}

```

### string

```c
#include<cstring>
#include<iostream>
using namespace std;

int main() {
    string a = "hby";
    a += "haha"; // 字符串拼接
    a += 'c';

    a.size();
    a.length(); // 两种取长度都可以

    a.empty();
    a.append("3");
    a.append(10, '3'); // 追加10个3

    a.find('b'); // 返回该字符的下标, 从左往右找到的第一个该字符

    a.front(); // 字符串第一个字符
    a.back(); // 字符串最后一个字符
    a.substr(1, 3); // 第一个参数是下标起始位置, 第二个参数是长度
    // 上面就是从下标为1的位置开始, 取后面长度为3的子串, 结果就是byh
    // 当第二个参数的长度, 超过了字符串的长度时, 会输出到字符串结尾为止
    a.substr(1); // 也可以省略第二个参数, 则返回下标1之后的子串

    a.c_str(); //返回字符串a存储字符串的起始地址
    printf("%s\n", a.c_str());
}

```

### queue

```c
#include<iostream>
#include<queue>
using namespace std;

int main() {
    queue<int> q;
    q.push(1); // 向队尾插入
    q.pop(); // 弹出队头元素, 注意返回的是void
    q.front(); // 返回队头
    q.back(); // 返回队尾
    q.size();
    q.empty();
    // queue 没有clear函数
    // 想清空一个queue怎么办?
    q = queue<int>(); // 直接重新构造一个queue
}

```

### priority\_queue

优先队列，底层是个堆

```c
#include<iostream>
#include<queue>
#include<vector>
using namespace std;

int main() {
    // 默认是大根堆
    priority_queue<int> q;
    // 想定义一个小根堆 怎么办？
    // 1. 想插入x时, 直接插入-x
    // 2. 定义时, 直接定义成小根堆, 如下（需要借助vector）
    priority_queue<int, vector<int>, greater<int>> heap;

    q.push();
    q.top(); // 返回堆顶元素
    q.pop(); // 弹出堆顶元素
}

```

### stack

```c
#include<iostream>
#include<stack>
using namespace std;

int main() {
    stack<int> s;
    s.push(); // 压栈
    s.top(); // 返回栈顶
    s.pop(); // 弹出栈顶
}

```

### deque

双端队列，或者叫加强版的vector。支持很多种方法，但是速度会比较慢，所以一般不怎么用

```c
#include<iostream>
#include<deque>
using namespace std;

int main() {
    deque<int> q;
    q.clear(); // 有clear

    q.front();
    q.back();

    q.push_back();
    q.pop_back();

    q.push_front();
    q.pop_front();
    // 并且支持随机寻址
    q[0];
    // 支持begin()和end()迭代器
}

```

### set

```c
#include<iostream>
#include<set>
using namespace std;

int main() {
    set<int> s; // 不能有重复元素, 插入一个重复元素, 则这个操作会被忽略
    multiset<int> ms; // 可以有重复元素
    // set 和 multiset 支持的操作

    insert(1); // 时间复杂度 O(logn)
    find(1); // 查找一个数, 若不存在, 则返回end迭代器
    count(1); // 返回某个数的个数, set只会返回0或1, multiset则可能返回大于1
    erase(1); // 删除所有1的元素  时间复杂度 O(k + logn), 其中k为元素个数
    erase(??); // 输入一个迭代器, 则只会删迭代器
    // set 比较核心的操作
    lower_bound(x); //返回大于等于x的最小的数的迭代器（注意, 返回的是迭代器）
    upper_bound(x); // 返回大于x的最小的数的迭代器 （注意, 返回的是迭代器）
    // begin() , end() 迭代器
}

```

### map

```c
#include<iostream>
#include<map>
using namespace std;

int main() {
    insert(); // 插入的是一个pair
    erase(); // 输入的参数是一个pair或者迭代器
    find();
    lower_bound();
    upper_bound();
    // 可以像使用数组一样使用map
    // map的几乎所有操作的时间复杂度是 O(logn), 除了size(), empty()

    map<string,int> m;
    m["hby"] = 1; // 插入可以直接这样操作

    cout << m["hby"] << endl; // 查找
}

```

### bitset

比如想要开一个1024长度的`bool`数组，由于C++的`bool`类型是1个字节。

则需要1024个字节，即1KB。但实际我们可以用位来表示`bool`，则只需要1024个位，即128字节

bitset支持所有的位运算，以及移位

```c
#include<iostream>
using namespace std;

int main() {
    bitset<1000> s;
    // 支持 ~, &, |, ^
    // 支持 >>, <<
    // 支持 ==, !=
    // 支持 []
    // count() 返回有多少个1
    // any() 是否至少有一个1
    // none() 是否全为0
    // set() 把所有位置置为1
    // set(k, v)  将第k位变成v
    // reset() 把所有位置变成0
    // flip() 把所有位置取反, 等价于 ~
    // flip(k) 把第k位取反
}

```

忘了某个STL容器的用法，可以到下面的官方地址查找

资料地址：www.cplusplus.com/reference/