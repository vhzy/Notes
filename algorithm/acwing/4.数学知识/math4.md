- [数学知识Part4](#数学知识part4)
  - [容斥原理](#容斥原理)
    - [AcWing 890. 能被整除的数](#acwing-890-能被整除的数)
  - [博弈论](#博弈论)
    - [概念1](#概念1)
    - [AcWing 891. Nim游戏](#acwing-891-nim游戏)
    - [AcWing 892. 台阶-Nim游戏 ](#acwing-892-台阶-nim游戏-)
    - [概念2](#概念2)
    - [AcWing 893. 集合-Nim游戏](#acwing-893-集合-nim游戏)
    - [AcWing 894. 拆分-Nim游戏](#acwing-894-拆分-nim游戏)

# 数学知识Part4
本节主要说了：
- 容斥原理
- 博弈论
  
## 容斥原理

在计数时，必须注意没有重复，没有遗漏。为了使重叠部分不被重复计算，人们研究出一种新的计数方法，这种方法的基本思想是：先不考虑重叠的情况，把包含于某内容中的所有对象的数目先计算出来，然后再把计数时重复计算的数目排斥出去，使得计算的结果既无遗漏又无重复，这种计数的方法称为容斥原理。

$$
\left|\mathrm{S}_{1} \bigcup \mathrm{S}_{2} \bigcup \mathrm{S}_{3}\right|=\left|\mathrm{S}_{1}\right|+\left|\mathrm{S}_{2}\right|+\left|\mathrm{S}_{3}\right|-\left|\mathrm{S}_{1} \bigcap \mathrm{S}_{2}\right|-\left|\mathrm{S}_{1} \bigcap \mathrm{S}_{3}\right|-\left|\mathrm{S}_{2} \bigcap \mathrm{S}_{3}\right|+\left|\mathrm{S}_{1} \bigcap \mathrm{S}_{2} \bigcap \mathrm{S}_{3}\right|
$$

n 个元素以此类推，只要记住奇数个元素求交集是加，偶数个元素是减

证明：要证明每个元素只被计算了一次，假设 x 属于 k 个集合，那么有
$$
\mathrm{C}_{\mathrm{k}}^{1}-\mathrm{C}_{\mathrm{k}}^{2}+\mathrm{C}_{\mathrm{k}}^{3}-\mathrm{C}_{\mathrm{k}}^{4}+\cdots+(-1)^{\mathrm{k}-1} \mathrm{C}_{\mathrm{k}}^{\mathrm{k}}=1
$$
$(1+x)^n$,带入x=-1即可证明

### [AcWing 890. 能被整除的数](https://www.acwing.com/problem/content/892/)
暴力枚举时间复杂度是$O(N \times M)$,肯定会超时，要用容斥原理来算时间复杂度$O(2^m)$,m=16,每个集合内部是$O(m)$的，总共就是$(2^mm)=10^6$可以在1s里面算出来。

1. n 中 p 的倍数的个数就是 n / p
2. 由于被整除的数都是质数，比如，算 2 和3 的倍数有多少个，就是算 n 里面 6 的倍数有多少个。多个质数也是相乘起来就完事了，但注意如果乘积大于了 n ，那么直接 break 掉就可以了。状压二进制表示选与不选这个质数，通过位运算实现(也可以用暴力搜索DFS来写)
以后这种集合的形式都可以尝试二进制枚举

```c++
#include<iostream>
#include<algorithm>

using namespace std;

typedef long long LL;

const int N=20;
int p[N];

int main()
{
    int n,m;
    cin>>n>>m;
    for(int i=0;i<m;i++) cin>>p[i];

    int res=0;

    for(int i=1;i<1<<m;i++)//1<<m表示小于2^m
    {
        int t=1,cnt=0;    //t表示当前所有质数的乘积，cnt表示包含几个1
        for(int j=0;j<m;j++)
        if(i>>j&1)        //位运算lowbit判断某一位是否是1
        {
            if((LL)t*p[j]>n)
            {
                t=-1;
                break;
            }
            t*=p[j];
            ++cnt;
        }

        if(t!=-1)
        {
            if(cnt%2) res=res+n/t;
            else res=res-n/t;
        }
    }

    printf("%d",res);

    return 0;
}

```

## 博弈论

### 概念1

**公平组合游戏ICG**
若一个游戏满足：
由两名玩家交替行动；
在游戏进程的任意时刻，可以执行的合法行动与轮到哪名玩家无关；
不能行动的玩家判负；
则称该游戏为一个公平组合游戏。
NIM博弈属于公平组合游戏，但城建的棋类游戏，比如围棋，就不是公平组合游戏。因为围棋交战双方分别只能落黑子和白子，胜负判定也比较复杂，不满足条件2和条件3。

**有向图游戏**
给定一个有向无环图，图中有一个唯一的起点，在起点上放有一枚棋子。两名玩家交替地把这枚棋子沿有向边进行移动，每次可以移动一步，无法移动者判负。该游戏被称为有向图游戏。
任何一个公平组合游戏都可以转化为有向图游戏。具体方法是，把每个局面看成图中的一个节点，并且从每个局面向沿着合法行动能够到达的下一个局面连有向边。


### [AcWing 891. Nim游戏](https://www.acwing.com/problem/content/description/893/)

先手必胜状态：先手进行某一个操作，留给后手是一个必败状态时，对于先手来说是一个必胜状态。即先手可以走到某一个必败状态。
先手必败状态：先手无论如何操作，留给后手都是一个必胜状态时，对于先手来说是一个必败状态。即先手走不到任何一个必败状态。
先给出结论：
$\mathrm{a}_{1}^{\wedge} \mathrm{a}_{2}{ }^{\wedge} \mathrm{a}_{3}^{\wedge} \ldots \mathrm{a}_{\mathrm{n}} \neq 0$,先手必胜

$\mathrm{a}_{1}^{\wedge} \mathrm{a}_{2}{ }^{\wedge} \mathrm{a}_{3}^{\wedge} \ldots \mathrm{a}_{\mathrm{n}} = 0$，先手必败

**证明**
- 操作到最后时，每堆石子数都是0，$0⊕0⊕…0=0$
<br>
- 在操作过程中，如果 $a_1⊕a_2⊕…⊕a_n=x≠0$。
那么玩家必然可以通过拿走某一堆若干个石子将异或结果变为0。
证明：不妨设x的二进制表示中最高一位1在第k位，那么在a1,a2,…,an中，必然有一个数$a_i$，它的第k位是1，且$a_i⊕x<a_i$，那么从第 i 堆石子中拿走$(a_i−a_i⊕x)$个石子，第i堆石子还剩$a_i−(a_i−a_i⊕x)=a_i⊕x$，此时$a_1⊕a_2⊕…⊕a_i⊕x⊕…⊕a_n=x⊕x=0$。
<br>
- 在操作过程中，如果 $a_1⊕a_2⊕…⊕a_n=0$，那么无论玩家怎么拿，必然会导致最终异或结果不为0。
反证法：假设玩家从第i堆石子拿走若干个，结果仍是0。不妨设还剩下a′个，因为不能不拿，所以
$0≤a′<a_i$，且$a_1⊕a_2⊕…⊕a′⊕…⊕a_n=0$。那么$(a_1⊕a_2⊕…⊕a_i⊕…a_n)
⊕(a_1⊕a_2⊕…⊕a′⊕…⊕an)=ai⊕a′=0$，则 $ai=a′$，与假设$0≤a′<a_i$矛盾。

基于上述三个证明：
1. 如果先手面对的局面是$a1⊕a2⊕…⊕an≠0$，那么先手总可以通过拿走某一堆若干个石子，将局面变成$a1⊕a2⊕…⊕an=0$。如此重复，最后一定是后手面临最终没有石子可拿的状态。先手必胜。
2. 如果先手面对的局面是$a1⊕a2⊕…⊕an=0$，那么无论先手怎么拿，都会将局面变成$a1⊕a2⊕…⊕an≠0$，
那么后手总可以通过拿走某一堆若干个石子，将局面变成$a1⊕a2⊕…⊕an=0$。
如此重复，最后一定是先手面临最终没有石子可拿的状态。先手必败。

```c++
#include <iostream>
#include <cstdio>
using namespace std;

/*
先手必胜状态：先手操作完，可以走到某一个必败状态
先手必败状态：先手操作完，走不到任何一个必败状态
先手必败状态：a1 ^ a2 ^ a3 ^ ... ^an = 0
先手必胜状态：a1 ^ a2 ^ a3 ^ ... ^an ≠ 0
*/

int main(){
    int n;
    scanf("%d", &n);
    int res = 0;
    for(int i = 0; i < n; i++) {
        int x;
        scanf("%d", &x);
        res ^= x;
    }
    if(res == 0) puts("No");
    else puts("Yes");
    return 0;
}
```

### [AcWing 892. 台阶-Nim游戏 ](https://www.acwing.com/problem/content/894/)

此时我们需要将奇数台阶看做一个经典的Nim游戏，**如果先手时奇数台阶上的值的异或值为0，则先手必败，反之必胜**

证明：
先手时，如果奇数台阶异或非0，根据经典Nim游戏，**先手总有一种方式使奇数台阶异或为0，于是先手留了奇数台阶异或为0的状态给后手**
于是轮到后手：
1. 当后手移动偶数台阶上的石子时，先手只需将对手移动的石子继续移到下一个台阶，这样奇数台阶的石子相当于没变，**于是留给后手的又是奇数台阶异或为0的状态**
2. 当后手移动奇数台阶上的石子时，留给先手的奇数台阶异或非0，根据经典Nim游戏，**先手总能找出一种方案使奇数台阶异或为0**
因此无论后手如何移动，**先手总能通过操作把奇数异或为0的情况留给后手**，当奇数台阶全为0时，只留下偶数台阶上有石子。
（核心就是：先手总是把奇数台阶异或为0的状态留给对面，即总是将必败态交给对面）

因为**偶数台阶上的石子要想移动到地面，必然需要经过偶数次移动**，又因为奇数台阶全0的情况是留给后手的，因此先手总是可以将石子移动到地面，当将最后一个（堆）石子移动到地面时，后手无法操作，即后手失败。

**因此如果先手时奇数台阶上的值的异或值为非0，则先手必胜，反之必败！**

```cpp
#include <iostream>

using namespace std;

int main()
{
    int res = 0;
    int n;
    cin >> n;

    for(int i = 1 ; i <= n ; i++)
    {
        int x;
        cin >> x;
        if(i % 2) res ^= x;
    }

    if(res) puts("Yes");
    else puts("No");
    return 0;
}
```

### 概念2

**Mex运算**
设S表示一个非负整数集合。定义mex(S)为求出不属于集合S的最小非负整数的运算，即：
mex(S) = min{x}, x属于自然数，且x不属于S


**SG函数**
在有向图游戏中，对于每个节点x，设从x出发共有k条有向边，分别到达节点y1, y2, …, yk，定义SG(x)为x的后继节点y1, y2, …, yk 的SG函数值构成的集合再执行mex(S)运算的结果，即：
$SG(x) = mex({SG(y1), SG(y2), …, SG(yk)})$
特别地，整个有向图游戏G的SG函数值被定义为有向图游戏起点s的SG函数值，即$SG(G) = SG(s)$。

**有向图游戏的和 —— 模板题 AcWing 893. 集合-Nim游戏**
设G1, G2, …, Gm 是m个有向图游戏。定义有向图游戏G，它的行动规则是任选某个有向图游戏Gi，并在Gi上行动一步。G被称为有向图游戏G1, G2, …, Gm的和。
有向图游戏的和的SG函数值等于它包含的各个子游戏SG函数值的异或和，即：
$S G(G)=S G(G 1)^{\wedge} S G(G 2)^{\wedge} \ldots{ }^{\wedge} S G(G m)$

**定理**
有向图游戏的某个局面必胜，当且仅当该局面对应节点的SG函数值大于0。
有向图游戏的某个局面必败，当且仅当该局面对应节点的SG函数值等于0。

### [AcWing 893. 集合-Nim游戏](https://www.acwing.com/problem/content/895/)

 比如，对于一个有 10  个石子的石头堆，每次只能拿 2  个或 5  个，那么这个 SG 图如下，其中红色的为 SG 的值
 ![求初始状态SG](https://pic4.zhimg.com/80/v2-a4fbd2670889bfbf68209afccebf4d9d.png)

![](https://pic4.zhimg.com/80/v2-d58afd439ed72cf24bb8c6860a0b818d.png)

通过**记忆化搜索**实现
```c++
#include<iostream>
#include<cstring>
#include<algorithm>
#include<unordered_set>

using namespace std;

const int N=110,M=10010;
int n,m;
int f[M],s[N];//s存储的是可供选择的集合,f存储的是所有可能出现过的情况的sg值

int sg(int x)//记忆化搜索保证每个状态只算一次
{
    if(f[x]!=-1) return f[x];
    //因为取石子数目的集合是已经确定了的,所以每个数的sg值也都是确定的,如果存储过了,直接返回即可
    unordered_set<int> S;
    //set代表的是有序集合(注:因为在函数内部定义,所以下一次递归中的S不与本次相同)
    for(int i=0;i<m;i++)
    {
        int sum=s[i];
        if(x>=sum) S.insert(sg(x-sum));
        //先延伸到终点的sg值后,再从后往前排查出所有数的sg值
    }

    for(int i=0;;i++)
    //循环完之后可以进行选出最小的没有出现的自然数的操作
     if(!S.count(i))
      return f[x]=i;
}

int main()
{
    cin>>m;
    for(int i=0;i<m;i++)
    cin>>s[i];

    cin>>n;
    memset(f,-1,sizeof(f));//初始化f均为-1,方便在sg函数中查看x是否被记录过

    int res=0;
    for(int i=0;i<n;i++)
    {
        int x;
        cin>>x;
        res^=sg(x);
        //观察异或值的变化,基本原理与Nim游戏相同
    }

    if(res) printf("Yes");
    else printf("No");

    return 0;
}
```

### [AcWing 894. 拆分-Nim游戏](https://www.acwing.com/problem/content/896/)

相比于集合-Nim，这里的**每一堆可以变成小于原来那堆的任意大小的两堆**
即a[i]a[i]可以拆分成(b[i],b[j]),为了避免重复规定b[i]>=b[j],即：a[i]>b[i]>=b[j]
相当于一个局面拆分成了两个局面，由SG函数理论，多个独立局面的SG值，等于这些局面SG值的异或和。
因此需要存储的状态就是sg(b[i])^sg(b[j])（与集合-Nim的唯一区别）

PS：因为这题中原堆拆分成的两个较小堆小于原堆即可，因此任意一个较小堆的拆分情况会被完全包含在较大堆中，因此S可以开全局。

![SG函数性质](https://pic4.zhimg.com/80/v2-c53b3b0c008dadb7f4c6ebe6a3caab12.png)

```cpp
#include <iostream>
#include <cstring>
#include <unordered_set>

using namespace std;

const int N = 110;

int n;
int f[N];
unordered_set<int> S;

int sg(int x)
{
    if(f[x] != -1) return f[x];


    for(int i = 0 ; i < x ; i++)
        for(int j = 0 ; j <= i ; j++)//规定j不大于i，避免重复
            S.insert(sg(i) ^ sg(j));//相当于一个局面拆分成了两个局面，由SG函数理论，多个独立局面的SG值，
                                   //等于这些局面SG值的异或和

    for(int i = 0 ; ; i++)
        if(!S.count(i))
            return f[x] = i;
}

int main()
{
    memset(f , -1 , sizeof f);

    cin >> n;
    int res = 0;
    while(n--)
    {
        int x;
        cin >> x;
        res ^= sg(x);
    }

    if(res) puts("Yes");
    else puts("No");
    return 0;
}

```