#! https://zhuanlan.zhihu.com/p/551395221
- [基础知识Part3](#基础知识part3)
  - [双指针](#双指针)
    - [AcWing 799. 最长连续不重复子序列](#acwing-799-最长连续不重复子序列)
    - [AcWing 800. 数组元素的目标和](#acwing-800-数组元素的目标和)
    - [AcWing 2816. 判断子序列](#acwing-2816-判断子序列)
  - [位运算](#位运算)
  - [离散化](#离散化)
    - [AcWing 802.区间和](#acwing-802区间和)
      - [分析](#分析)
      - [问题](#问题)
  - [区间合并](#区间合并)

# 基础知识Part3
本节主要说了：
- 双指针
- 位运算
- 离散化
- 区间合并

## 双指针

双指针算法，通常是适用于有两层循环的情况（循环变量分别为`i`，`j`）。首先是写一个暴力的解法，然后观察一下`i`和`j`之间是否存在单调性的关系（即`i`和`j`是否都往着同一个方向移动，不回头）。若`i`和`j`之间存在着这种单调性关系，则我们可以用双指针，来将时间复杂度从O(n2)降低到O(n)。

*   2个指针指向不同的序列

    比如**归并排序**

*   2个指针指向同一个序列

    比如**快速排序**
对于形如

```c
for(int i = 0; i < n; i++) {
    for(int j = 0; j < n; j++) {

    }
}

```

这一类的双层循环，可能可以使用双指针来进行优化，从而能够把时间复杂度从O(n2)降低到O(n)，比如求**一个数组中最长的连续不重复的子序列的长度**

### [AcWing 799. 最长连续不重复子序列](https://www.acwing.com/problem/content/801/)
最容易想到的暴力解法是：枚举 i = 0~n，对于每个i，将其看作右端点，尝试找到其左边最远的左端点。

```c++
int maxLen = 0;
for(int i = 0; i < n; i++) {
    for(int j = 0; j <= i; j++) {
        // 若[j, i]区间内不包含重复元素
        if(noRepeat(j, i)) maxLen = max(maxLen, i - j + 1);
    }
}

```

经过简单的推算，可以得知，当某个`[j, i]`区间内有重复元素，那么对于所有`i + 1`之后的数作为右端点，其左边的最远端点，最多取到`j + 1`。也就是说，随着`i`从左往右移动，每个`i`对应的最远的左端点`j`，也只能单向地从左往右移动。所以可以采用双指针算法，两个指针`i`，`j`最多只需要各自从0走到n（共2n次操作），即可找到答案，时间复杂度为O(n)。

```c++
int maxLen = 1;
for(int i = 0, j = 0; i < n; i++) {
    while(j <= i && hasRepeat(j, i)) j++;  // 若[j, i]区间内包含重复元素, 右移j
    maxLen = max(maxLen, i - j + 1); // 找到当前i作为右端点, 最长的子序列
}
// 其中 hasRepeat 函数检查是否有重复元素, 可以用哈希表，或者开一个数组用计数排序的思路
```

```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10;
int n;
int q[N], c[N];  // 这里对于判断重复, 采用了计数排序的思想, 若数的范围较大, 或者数不是整数, 可以考虑用哈希表

int main() {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d", &q[i]);
    
    int res = 0;
    for(int i = 0, j = 0; i < n; i++) {
        c[q[i]]++; // i往后移动一位, 计数加一, 将q[i]这个数纳入判重的集合
        while(c[q[i]] > 1) {  // 若在[j, i]区间内有重复元素的话, 只可能重复新加入的这个q[i], 只需判断q[i]的个数大于1,不需要维护j<i>
            // 有重复, j 往右移动一位
            c[q[j]]--; // 将j这个位置的数的计数减1, 即把q[j]从判重的集合中移除
            j++;
        }
        res = max(res, i - j + 1); // 针对该i, 找到最远的左端点j
    }
    printf("%d", res);
    return 0;
}
```

### [AcWing 800. 数组元素的目标和](https://www.acwing.com/problem/content/802/)
双指针算法需要保证单调性，如果两个指针都是从前往后遍历，无法保证单调性；
因此，i从 0开始 从前往后遍历
j从 m - 1开始 从后向前遍历，时间复杂度$O(n)$
和纯暴力的 $O(n^2)$ 算法的区别就在于，j指针不会回退
![](https://pic4.zhimg.com/80/v2-bb40b80d3535b1891fb90695c0e6d34e.png)
```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10;

int a[N], b[N];

int main() {
	int n, m, x;
	scanf("%d%d%d", &n, &m, &x);
	for(int i = 0; i < n; i++) scanf("%d", &a[i]);
	for(int i = 0; i < m; i++) scanf("%d", &b[i]);
	int i = 0, j = m - 1;
	while(i < n && j >= 0) {
		int sum = a[i] + b[j];
		if(sum < x) i++;
		else if(sum > x) j--;
		else break;
	}
	printf("%d %d\n", i, j);
	return 0;
}
```

### [AcWing 2816. 判断子序列](https://www.acwing.com/problem/content/2818/)
1.`j`指针用来扫描整个`b`数组，`i`指针用来扫描`a`数组。若发现`a[i]==b[j]`，则让`i`指针后移一位。
2.整个过程中，`j`指针不断后移，而`i`指针只有当匹配成功时才后移一位，若最后若`i==n`，则说明匹配成功。
![判断子序列](https://pic4.zhimg.com/80/v2-ecb26b48cb274f7acf24740e63ba193d.png)
```cpp
#include<iostream>
#include<cstdio>
using namespace std;
const int N=1e5+10;
int a[N],b[N];
int main()
{
    int n,m;
    scanf("%d%d",&n,&m);
    for(int i = 0;i < n; i++) scanf("%d",&a[i]);
    for(int j = 0;j < m; j++) scanf("%d",&b[j]);

    int i = 0;
    for(int j = 0;j < m; j++)
    {
        if(i < n&&a[i] == b[j])  i++;
    }
    if(i == n) puts("Yes");
    else puts("No");
    return 0;
}
```

## 位运算
1.  获取一个数的二进制的第k位：`x >> k & 1`

    即，先将x右移k位，然后和`1`做`与运算`

2.  获取一个数的二进制的最后一位1：`lowbit(x) = x & -x`

    如，10的二进制表示是`1010`，则对10做`lowbit`运算，得到`10`（二进制），转为十进制即为2

    `lowbit`运算的原理是，`x & -x`，由于`-x`采用补码表示，它等于对x的原码取反再加1，即`-x = ~x + 1`

    比如 x 的二进制表示是：

    `100101000`，对x取反得

    `011010111`，加1得

    `011011000`

    所以`x & (~X + 1)`，则x的最后一位1，被保留了下来，这个位置后面，两个数全是0，这个位置前面，两个数是取反，做与运算后也全为0。

    `lowbit`的最简单的应用：**统计x的二进制表示中，1的个数**。具体的实现方式是：每次对x做`lowbit`运算，并将运算结果从x中减去。循环做下去，直到x被减为0，一共减了多少次，x中就有多少个1。

[AcWing 801. 二进制中1的个数](https://www.acwing.com/problem/content/803/)
```cpp
#include<iostream>
using namespace std;

const int N = 1e5 + 10;
int n;

int lowbit(int x) {
    return x & -x;
}

int main() {
    scanf("%d", &n);
    while(n--) {
        int x;
        scanf("%d", &x);
        int c = 0;
        while(x > 0) {
            x -= lowbit(x);
            c++;
        }
        printf("%d ", c);
    }
    return 0;
}
```

## 离散化
有的数组，其元素的**值域很大**，比如数组中的元素取值都是`[0, 10^9]`，但**元素的个数很少**，比如只有1000个元素。

有时（例如计数排序的思想），我们需要将元素的值，作为数组的下标来操作。此时不可能开一个`10^9`大小的数组。

此时我们把这些元素，映射为从0（或者从1）开始的自然数。（也可以理解为对稀疏数组进行压缩）

例子如下

有一个数组a，`[1, 3, 100, 2000, 500000]`（已经排好序），我们把这个数组中的元素，映射为

`[0, 1, 2, 3, 4]`，这个映射的过程，称之为**离散化**

离散化有2个要点：

*   原数组a中若有重复元素，可能需要去重
*   如何根据`a[i]`，算出其离散化后的值：由于原数组已经排好序，故这里用二分查找即可,输入一个离散数组的位置（映射前的位置）x返回连续数组的位置+1（映射后的位置+1）。+1的目的是为了求区间和时少一步下标为0的判断。

离散化的代码模板
```cpp
// C++
vector<int> v; // 待离散化的数组
sort(v.begin(), v.end()); // 将数组先排序
v.erase(unique(v.begin(), v.end()), v.end()); // 对数组进行去重
// 进行离散化, 将数组的值依次映射到 0,1,2,3,4,5, ... 等自然数

// 根据数的值, 求出其离散化的值
int find(int x) {
    int l = 0, r = v.size() - 1;
    while(l < r) {  // 找到第一个大于等于x的离散化的值
        int mid = l + r >> 1;
        if(v[mid] >= x) r = mid;
        else l = mid + 1;
    }
    return r + 1; // 是否加1, 跟题目相关, 若是前缀和差分等需要下标从1开始, 则需要加1
}
```

### [AcWing 802.区间和](https://www.acwing.com/problem/content/804/)
#### 分析

主要分为5大步：
1.读输入。将每次读入的`x c` `push_back()`到`add`中，将每次读入的位置`x` `push_back()`到`index`中，将每次读入的`l r` `push_back()`到`query`中。
2.排序、去重。
3.通过遍历`add`，完成在离散化的数组映射到的`a`数组中进行加上`c`的操作（用到`find`函数）。
4.初始化`s`数组。
5.通过遍历`query`，完成求区间`[l,r]`的和。

#### 问题

1.为什么要在`index`中需要`index.push_back(l);index.push_back(r);`？

**首先要明确`index`中存放的是位置而不是值，也就是存放的是`x`而不是`c`。**

因为再求区间和的时候，我们提前分析到可以使用前缀和来做，求前缀和就需要下标`l r`，如果不加入`l r`到`index`中的话，第5步中遍历时`query`就没有办法通过输入的`l r`去访问`a`或者`s`。因为`find`函数就是输入映射前的下标，返回在`index`中的下标`+1`。

举个例子，拿平时的数组来说，下标都是整形，但是如果要求`a[1.5]`肯定是有错误的，在这里也一样。

2.为什么要排序和去重？

**首先要明确`find`函数的功能，输入一个离散数组的位置（映射前的位置）`x`返回连续数组的位置`+1`（映射后的位置`+1`）。`+1`的目的是为了求区间和时少一步下标为`0`的判断。**

排序很好理解，因为在`find`函数中是使用了二分来查找`x`在`index`中的下标`+1`，想要使用二分`index`就必须具有某种性质这里就可以找一个最简单的办法使他单调（但是y总说过二分!=单调性）。

图中的例子为本题的样例。（前半部分为在`x`处加`c`后`alls(即index)`与`a`中的内容，后半部分为假设不去重求[3,7]的区间和）
![离散化](https://pic4.zhimg.com/80/v2-1936c08709c36b067db356ac16d20c28.png)

```cpp
// C++, 按照yxc的思路的解法
// 将所有用到的下标先存起来, 对全部下标进行离散化(所有的x, l, r)
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;

typedef pair<int, int> PII;

const int N = 3e5 + 10; // 用到的下标总数为  n + 2m , 300000 量级

vector<PII> add; // 插入操作
vector<PII> query; // 询问操作
vector<int> index; //所有待离散化的下标

int s[N]; // 记录前缀和
int a[N]; // 记录值

// 进行离散化
int find(int x) {
    int l = 0, r = index.size() - 1;
    while(l < r) {
        int mid = l + r >> 1;
        if(index[mid] >= x) r = mid;
        else l = mid + 1;
    }
    return l + 1; // 离散化后的下标从1开始, 因为需要计算前缀和
}

int main() {
    int n, m;
    scanf("%d%d", &n, &m);
    // 读入全部数据
    while(n--) {
        int x, c;
        scanf("%d%d", &x, &c);
        add.push_back({x, c});
        index.push_back(x); // 添加待离散化的下标
    }
    while(m--) {
        int l, r;
        scanf("%d%d", &l, &r);
        query.push_back({l, r});
        index.push_back(l);// 添加待离散化的下标
        index.push_back(r);
    }
    // 对所有的下标点进行离散化
    sort(index.begin(), index.end()); // 先对 index 排序
    index.erase(unique(index.begin(), index.end()), index.end());; // 对 index 数组进行去重
    
    // 处理插入
    for(int i = 0; i < add.size(); i++) {
        int p = find(add[i].first); // 找到待插入的位置(离散化后的位置)
        a[p] += add[i].second; // 插入
    }
    
    // 计算前缀和
    for(int i = 1; i <= index.size(); i++) {
        s[i] = s[i - 1] + a[i]; // 对所有用到的下标, 计算前缀和
    }
    
    // 处理查询
    for(int i = 0; i < query.size(); i++) {
        int l = find(query[i].first);
        int r = find(query[i].second);
        printf("%d\n", s[r] - s[l - 1]);
    }
    return 0;
}
```
练习题[759. 格子染色](https://www.acwing.com/problem/content/761/)

## 区间合并

[AcWing 803. 区间合并](https://www.acwing.com/problem/content/805/)
给定很多个区间，若2个区间有交集，将二者合并成一个区间

做法思路：

1.  先按照区间的左端点进行排序
2.  然后遍历每个区间，进行合并即可（类似双指针的思想）

```cpp
#include <iostream>
#include <vector>
#include <algorithm>
using namespace std ;
typedef pair<int,int> pii ;
vector<pii> nums,res ;
int main()
{
    int st=-2e9,ed=-2e9 ;                           //ed代表区间结尾，st代表区间开头
    int n ;
    scanf("%d",&n) ; 
    while(n--)
    {
        int l,r ; 
        scanf("%d%d",&l,&r) ;
        nums.push_back({l,r}) ;
    }
    sort(nums.begin(),nums.end()) ;                 //按左端点排序
    for(auto num:nums)                   
    {
        if(ed<num.first)                            //情况1：两个区间无法合并
        {
            if(ed!=-2e9) res.push_back({st,ed}) ;   //区间1放进res数组
            st=num.first,ed=num.second ;            //维护区间2
        }
        //情况2：两个区间可以合并，且区间1不包含区间2，区间2不包含区间1
        else if(ed<num.second)  
            ed=num.second ;                         //区间合并
    }  
    //(实际上也有情况3：区间1包含区间2，此时不需要任何操作，可以省略)

    //注：排过序之后，不可能有区间2包含区间1

    res.push_back({st,ed});

    //考虑循环结束时的st,ed变量，此时的st,ed变量不需要继续维护，只需要放进res数组即可。
    //因为这是最后的一个序列，所以不可能继续进行合并。

    /*
    for(auto r:res)
        printf("%d %d\n",r.first,r.second) ;
    puts("") ;
    */

    //(把上面的注释去掉，可以在调试时用)

    printf("%d",res.size()) ;           //输出答案
    return 0 ;
}
```