#! https://zhuanlan.zhihu.com/p/550116013
- [数学知识Part3](#数学知识part3)
  - [高斯消元](#高斯消元)
    - [883. 高斯消元解线性方程组](#883-高斯消元解线性方程组)
    - [AcWing 884. 高斯消元解异或线性方程组](#acwing-884-高斯消元解异或线性方程组)
  - [组合数](#组合数)
    - [885. 求组合数 I](#885-求组合数-i)
    - [AcWing 886. 求组合数 II](#acwing-886-求组合数-ii)
    - [AcWing 887. 求组合数 III](#acwing-887-求组合数-iii)
    - [AcWing 888. 求组合数 IV](#acwing-888-求组合数-iv)
    - [AcWing 889. 满足条件的01序列 ](#acwing-889-满足条件的01序列-)

# 数学知识Part3
本节主要说了：
- 高斯消元
- 组合数
- 卡特兰数

## 高斯消元
可以在$O(N^3)$内求解包括n个方程和n个未知数的多元线性方程组
 
对于下面这个方程组
$$
\left\{\begin{array}{c}
\mathrm{a}_{11} \mathrm{x}_{1}+\mathrm{a}_{12} \mathrm{x}_{2}+\cdots+\mathrm{a}_{1 \mathrm{n}} \mathrm{x}_{\mathrm{n}}=\mathrm{b}_{1} \\
\mathrm{a}_{21} \mathrm{x}_{1}+\mathrm{a}_{22} \mathrm{x}_{2}+\cdots+\mathrm{a}_{2 \mathrm{n}} \mathrm{x}_{\mathrm{n}}=\mathrm{b}_{2} \\
\cdots \\
\mathrm{a}_{\mathrm{n} 1} \mathrm{x}_{1}+\mathrm{a}_{\mathrm{n} 2} \mathrm{x}_{2}+\cdots+\mathrm{a}_{\mathrm{nn}} \mathrm{x}_{\mathrm{n}}=\mathrm{b}_{\mathrm{n}}
\end{array}\right.
$$
增广矩阵是：
$$
\left(\begin{array}{ccccc}
a_{11} & a_{12} & \cdots & a_{1 n} & b_{1} \\
a_{21} & a_{22} & \cdots & a_{2 n} & b_{2} \\
& & \cdots & & \\
a_{n 1} & a_{n 2} & \cdots & a_{n n} & b_{n}
\end{array}\right)
$$

解方程步骤：
1. 枚举每一列
2. 找到每一列的绝对值最大值（找主元）
3. 把具有最大值的一行换到最上面（并不是真正意义上的最上面，而是已确定的行的下面一行），这一行除以该行第一个非0系数
4. 把这一列下面所有行的值变成0
5. 化成阶梯型矩阵

判断方法：
1. 如果经过处理后，剩下的方程组数小于 n ，那么有无穷解或者无解（系数矩阵的秩等于增广矩阵的秩）
2. 如果剩下的方程组数等于 n ，那么有唯一解

![](https://pic4.zhimg.com/80/v2-5fd5a4696671d23c1edc54aa239ab0bb.png)

得到阶梯型矩阵后，要从下往上求，把每一行第一个非0数变成1，依次消去上面行同一列的系数，化成行最简阶梯型。
![](https://pic4.zhimg.com/80/v2-a5c7f74fbedf273c9489a956bdff0957.png)


### [883. 高斯消元解线性方程组](https://www.acwing.com/problem/content/885/)
```cpp
#include <iostream>
#include <algorithm>
#include <cmath>

using namespace std;

const int N = 110;
const double eps = 1e-6;

int n;
double a[N][N];


int gauss()
{
    int c, r;// c 代表 列 col ， r 代表 行 row
    for (c = 0, r = 0; c < n; c ++ )
    {
        int t = r;// 先找到当前这一列，绝对值最大的一个数字所在的行号
        for (int i = r; i < n; i ++ )
            if (fabs(a[i][c]) > fabs(a[t][c]))
                t = i;

        if (fabs(a[t][c]) < eps) continue;// 如果当前这一列的最大数都是 0 ，那么所有数都是 0，就没必要去算了，因为它的约束方程，可能在上面几行

        for (int i = c; i < n + 1; i ++ ) swap(a[t][i], a[r][i]);//// 把当前这一行，换到最上面（不是第一行，是第 r 行）去
        for (int i = n; i >= c; i -- ) a[r][i] /= a[r][c];// 把当前这一行的第一个数，变成 1， 方程两边同时除以 第一个数，必须要倒着算，不然第一个数直接变1，系数就被篡改，后面的数字没法算
        for (int i = r + 1; i < n; i ++ )// 把当前列下面的所有数，全部消成 0
            if (fabs(a[i][c]) > eps)// 如果非0 再操作，已经是 0就没必要操作了
                for (int j = n; j >= c; j -- )// 从后往前，当前行的每个数字，都减去对应列 * 行首非0的数字，这样就能保证第一个数字是 a[i][0] -= 1*a[i][0];
                    a[i][j] -= a[r][j] * a[i][c];

        r ++ ;// 这一行的工作做完，换下一行
    }

    if (r < n)// 说明剩下方程的个数是小于 n 的，说明不是唯一解，判断是无解还是无穷多解
    {// 因为已经是阶梯型，所以 r ~ n-1 的值应该都为 0
        for (int i = r; i < n; i ++ )// 
            if (fabs(a[i][n]) > eps)// a[i][n] 代表 b_i ,即 左边=0，右边=b_i,0 != b_i, 所以无解。
                return 2;
        return 1;// 否则， 0 = 0，就是r ~ n-1的方程都是多余方程
    }
    // 唯一解 ↓，从下往上回代，得到方程的解
    for (int i = n - 1; i >= 0; i -- )
        for (int j = i + 1; j < n; j ++ )
            a[i][n] -= a[j][n] * a[i][j];//因为只要得到解，所以只用对 b_i 进行操作，中间的值，可以不用操作，因为不用输出

    return 0;
}

int main()
{
    cin >> n;
    for (int i = 0; i < n; i ++ )
        for (int j = 0; j < n + 1; j ++ )
            cin >> a[i][j];

    int t = gauss();

if(!t)
        for(int i=0;i<n;i++)
            if(fabs(a[i][n])<eps)
                puts("0.00");// 去掉输出 -0.00 的情况
            else
                printf("%.2lf\n",a[i][n]);
    else if (t == 1) puts("Infinite group solutions");
    else puts("No solution");

    return 0;
}
```

### [AcWing 884. 高斯消元解异或线性方程组](https://www.acwing.com/problem/content/description/886/)

这道题目其实就是线性方程组的变形，只是把加法变成了异或运算而已,异或其实就是不进位的加法
最后一列就是未知数的解
```cpp
#include <iostream>
#include <algorithm>

using namespace std;

const int N = 110;

int n;
int a[N][N];
int gauss()
{
    int c,r;
    for(c=0,r=0;c<n;c++)
    {
        // 找主元
        int t=-1;
        for(int i=r;i<n;i++)
            if(a[i][c])
            {
                t=i;
                break;
            }
        if(t==-1) continue;
        // 交换主元行
        for(int j=c;j<=n;j++) swap(a[r][j],a[t][j]);
        // 左下角消
        for(int i=r+1;i<n;i++)
            if(a[i][c])//漏了
                for(int j=n;j>=c;j--)//漏了
                    a[i][j] ^= a[r][j];
        r++;
    }
    // 判断
    if(r<n)
    {
        for(int i=r;i<n;i++)//i=r
            if(a[i][n])
                return 2;
        return 1;
    }
    // 消右上角
    for(int i=n-1;i>=0;i--)
        for(int j=i+1;j<n;j++)
        //如果是0 就不用下面的a[j][j] 来^a[i][j]了
        //如果不是0 才需要用第j行第j列a[j][j]来^第i行第j列a[i][j] 
        //进而进行整行row[i]^row[j] 间接导致 a[i][n]^a[j][n]
            if(a[i][j])
                a[i][n]^=a[j][n];
    return 0;
}

int main()
{
    cin >> n;
    for(int i=0;i<n;i++)
        for(int j=0;j<=n;j++)
            cin >> a[i][j];
    int t = gauss();
    if(t==0)
    {
        for(int i=0;i<n;i++) cout << a[i][n] << endl;
    }
    else if(t==1) puts("Multiple sets of solutions");
    else puts("No solution");
    return 0;
}

```

## 组合数
求组合数有四种方法，根据不同的数据范围选择不同的方法。

### [885. 求组合数 I](https://www.acwing.com/problem/content/887/)
**数据范围：**
10万组询问，$0 < a,b < 2000$

暴力法 $O(n^2)$，用公式预处理所有组合数的值（打表）

递推式: $\mathrm{C}_{\mathrm{a}}^{\mathrm{b}}=\mathrm{C}_{\mathrm{a}-1}^{\mathrm{b}-1}+\mathrm{C}_{\mathrm{a}-1}^{\mathrm{b}}$
类似DP问题的考虑方式：
在a个苹果中,选出b个苹果出来,现有一个苹果p;
1. 选这个苹果的方案相当于在剩余的a-1个苹果中选b-1个苹果
2. 不选这个苹果的方案相当于在剩余的a-1个苹果中选b个苹果

将1,2两种方案相加就是在a个苹果中选择b个苹果

![组合数递推式](https://pic4.zhimg.com/80/v2-6ac6a068d37c8c102cd90ea9548d339b.png)

```cpp
#include<iostream>
#include<algorithm>

using namespace std;

const int N=2010,mod=1e9+7;

int c[N][N];//将所有的组合方式都预处理出来

void init()
{
    for(int i=0;i<=2000;i++)
     for(int j=0;j<=i;j++)
      if(!j) c[i][j]=1;
      else c[i][j]=(c[i-1][j]+c[i-1][j-1])%mod;
}

int main()
{
    int n;
    scanf("%d",&n);

    init();

    while(n--)
    {
        int a,b;
        scanf("%d%d",&a,&b);
        printf("%d\n",c[a][b]);
    }

    return 0;
}
```

### [AcWing 886. 求组合数 II](https://www.acwing.com/problem/content/888/)
**数据范围：**
1万组询问，$0 < a,b < 10^5$
不能直接预处理组合数的值了，需要预处理**阶乘**。时间复杂度$O(nlogn)$
∵mod=1e9+7是质数,所以2~1e9+6与1e9+7互质,所以可以使用费马小定理来求解逆元,逆元通过快速幂求解
![](https://pic4.zhimg.com/80/v2-f508fe44eb77f0dc0b451cd69da42c3a.png)

```cpp
#include<iostream>
#include<algorithm>

using namespace std;

typedef long long LL;
const int N=100010,mod=1e9+7;

int fact[N],infact[N];//fact表示阶乘,infact表示阶乘的逆元

int qmi(int a,int k,int p)
{
    int res=1;
    while(k)
    {
        if(k&1) res=(LL)res*a%p;
        a=(LL)a*a%p;
        k>>=1;
    }
    return res;
}

int main()
{
    fact[0]=infact[0]=1;
    for(int i=1;i<N;i++)
    {
        fact[i]=(LL)fact[i-1]*i%mod;//阶乘运算过程
        infact[i]=(LL)infact[i-1]*qmi(i,mod-2,mod)%mod;
        /*
        x=b^(p-2)%p,这里相当于是x=i^(mod-2)%mod
        所以乘x就相当于除i,因为infact表示阶乘逆元和,
        因为infact表示除以i的阶乘的逆元,所以乘infact[i-1]
        相当于乘上1/(i-1)!.又因为乘x相当于除以i,所以infact[i-1]
        乘上x等于1/i!,也就等于infact[i];
        */
    }

    int n;
    cin>>n;
    while(n--)
    {
        int a,b;
        scanf("%d%d",&a,&b);
        printf("%d\n",(LL)fact[a]*infact[a-b]%mod*infact[b]%mod);
        //mod两次是为了防止结果过大,导致溢出
    }

    return 0;
}
```
### [AcWing 887. 求组合数 III](https://www.acwing.com/problem/content/description/889/)
**数据范围：**
20组询问，$0 < a,b < 10^{18}$, $1 < p <10^5$
[卢卡斯定理 Lucas Theory](https://blog.csdn.net/qq_40679299/article/details/80489761)
[知乎介绍](https://zhuanlan.zhihu.com/p/452976974)
 $O(log_p N \times  plogp)$
$$
\mathrm{C}_{\mathrm{a}}^{\mathrm{b}}=\mathrm{C}_{\mathrm{a} \bmod \mathrm{p}}^{\mathrm{b} \bmod \mathrm{p}}\times \mathrm{C}_{\mathrm{a} / \mathrm{p}}^{\mathrm{b} / \mathrm{p}}(\bmod \mathrm{p}), \mathrm{a} / \mathrm{p} \text { 和 } \mathrm{b} / \mathrm{p} \text { 表示整除, }
$$
可以用生成函数证明，这里感觉y总讲的不清楚，自己看博客吧
```cpp
#include<iostream>
#include<algorithm>

using namespace std;

typedef long long LL;

int qmi(int a,int k,int p)
{
    int res = 1;
    while(k)
    {
        if(k&1)res = (LL)res*a%p;
        a = (LL)a*a%p;
        k>>=1;
    }
    return res;
}

int C(int a,int b,int p)//自变量类型int
{
    if(b>a)return 0;//漏了边界条件
    int res = 1;
    // a!/(b!(a-b)!) = (a-b+1)*...*a / b! 分子有b项
    for(int i=1,j=a;i<=b;i++,j--)//i<=b而不是<
    {
        res = (LL)res*j%p;
        res = (LL)res*qmi(i,p-2,p)%p;
    }
    return res;
}
//对公式敲
int lucas(LL a,LL b,int p)
{
    if(a<p && b<p)return C(a,b,p);//lucas递归终点是C_{bk}^{ak}
    return (LL)C(a%p,b%p,p)*lucas(a/p,b/p,p)%p;//a%p后肯定是<p的,所以可以用C(),但a/p后不一定<p 所以用lucas继续递归
}

int main()
{
    int n;
    cin >> n;
    while(n--)
    {
        LL a,b;
        int p;
        cin >> a >> b >> p;
        cout << lucas(a,b,p) << endl;
    }
    return 0;
}
```

### [AcWing 888. 求组合数 IV](https://www.acwing.com/problem/content/890/)
**数据范围：**
没有模数，$0 < b < a < 5000$, 最后的结果很大，我们需要用高精度把这个数算出来

先分解质因数，然后使用高精度乘法
先分解质因数：
$$
\mathrm{C}_{\mathrm{a}}^{\mathrm{b}}=\frac{\mathrm{a} !}{(\mathrm{a}-\mathrm{b}) ! \mathrm{b} !}=\mathrm{p}_{1}^{\mathrm{a} 1} * \mathrm{p}_{2}^{\mathrm{a} 2} * \cdots * \mathrm{p}_{\mathrm{k}}^{\mathrm{a} \mathrm{k}}
$$

把分子中 a! 里面的含有 p 的个数求出来，再求出分母的，再相减
$sum[i]$表示a的阶乘里面有多少个第i个质数，质数从2开始算（下取整）
$$
\operatorname{sum}[\mathrm{i}]=\frac{\mathrm{a}}{\mathrm{p}}+\frac{\mathrm{a}}{\mathrm{p}^{2}}+\frac{\mathrm{a}}{\mathrm{p}^{3}}+\cdots
$$
比如$8 !=1 * 2 * 3 * 4 * 5 * 6 * 7 * 8$
$\operatorname{sum}[1]=8 / 2+8 / 4+8 / 8=4+2+1=7$，表示第一个质数2在8的阶乘里面有7个，第二个质数是3⋅⋅⋅等等

为什么只+1而不是+k,因为a中$p^k$低阶项的次数已经被算过了比如$p^3$既是p的倍数也是$p^2$的倍数则1～8之间含2的一次有2,4,6,8四个，含2次方的有4、8，但4、8中2的一次方已经记过一次了。


步骤如下：
1. 先线性筛预处理出来小于a的所有质数

```cpp
void get_primes(int n)
{
    for(int i = 2; i <= n; ++i)
    {
        if(!st[i])
            primes[cnt++] = i;
        for(int j = 0; primes[j] <= n / i; ++j)
        {
            st[primes[j] * i] = true;
            if(i % primes[j] == 0)
                break;
        }
    }
}
```

2. 遍历得到组合数的结果里面所有质数的个数,get函数也要注意有技巧，注意sum[i] 表示第 i 个质数的个数

```cpp
int get(int a, int p)
{
    int res = 0;
    while(a)
    {
        res += a / p;
        a /= p;
    }

    return res;
}
int main()
{
	for(int j = 0; j < cnt; ++j)
	{
	    int p = primes[j];//这里相当于离散化了
	    sum[j] = get(a, p) - get(a - b, p) - get(b, p);
	}
}
```

3. 对于结果vector<int>res，首先先push_back一个 1 ，然后在分别处理每个质数的与它的个数，这里是大数相乘，最后倒序输出

**完整代码**
```cpp
用高精度乘把所有质因子乘上
#include<iostream>
#include<algorithm>
#include<vector>

using namespace std;

const int N=5010;

int primes[N],cnt;
int sum[N];
bool st[N];

void get_primes(int n)
{
    for(int i=2;i<=n;i++)
    {
        if(!st[i])primes[cnt++]=i;
        for(int j=0;primes[j]*i<=n;j++)
        {
            st[primes[j]*i]=true;
            if(i%primes[j]==0)break;//==0每次漏
        }
    }
}
// 对p的各个<=a的次数算整除下取整倍数
int get(int n,int p)
{
    int res =0;
    while(n)
    {
        res+=n/p;
        n/=p;
    }
    return res;
}
//高精度乘
vector<int> mul(vector<int> a, int b)
{
    vector<int> c;
    int t = 0;
    for (int i = 0; i < a.size(); i ++ )
    {
        t += a[i] * b;
        c.push_back(t % 10);
        t /= 10;
    }
    while (t)
    {
        c.push_back(t % 10);
        t /= 10;
    }
    // while(C.size()>1 && C.back()==0) C.pop_back();//考虑b==0时才有pop多余的0 b!=0不需要这行
    return c;
}

int main()
{
    int a,b;
    cin >> a >> b;
    get_primes(a);

    for(int i=0;i<cnt;i++)
    {
        int p = primes[i];
        sum[i] = get(a,p)-get(a-b,p)-get(b,p);//是a-b不是b-a
    }

    vector<int> res;
    res.push_back(1);

    for (int i = 0; i < cnt; i ++ )
        for (int j = 0; j < sum[i]; j ++ )//primes[i]的次数
            res = mul(res, primes[i]);

    for (int i = res.size() - 1; i >= 0; i -- ) printf("%d", res[i]);
    puts("");

    return 0;
}

```

### [AcWing 889. 满足条件的01序列 ](https://www.acwing.com/problem/content/description/891/)
将 01 序列置于坐标系中，起点定于原点。若 0 表示向右走，1 表示向上走，那么任何前缀中 0 的个数不少于 1 的个数就转化为，路径上的任意一点，横坐标大于等于纵坐标。题目所求即为这样的合法路径数量。

下图中，表示从 (0,0) 走到 (n,n) 的路径，在绿线及以下表示合法，若触碰红线即不合法。
![卡特兰数](https://pic4.zhimg.com/80/v2-c041862d8be369481e6a95b2f3fa3c76.png)

由图可知，任何一条不合法的路径（如黑色路径），都对应一条从 (0,0) 走到 (n−1,n+1) 的一条路径（如灰色路径）。而任何一条 (0,0) 走到 (n−1,n+1) 的路径，也对应了一条从 (0,0)走到 (n,n)的不合法路径。

```cpp
#include <iostream>

using namespace std;

typedef long long LL;

const int mod = 1e9 + 7;

int qmi(int a, int k, int p) {

    int res = 1 % p;
    while (k) {
        if (k & 1) res = (LL)res * a % p;
        a = (LL)a * a % p;
        k >>= 1;
    }
    return res;
}

int main() {

    int n;
    cin >> n;

    int a = 2 * n, b = n;
    int res = 1;

    for (int i = a; i > a - b; i--) res = (LL)res * i % mod;
    for (int i = 1; i <= b; i++) res = (LL)res * qmi(i, mod - 2, mod) % mod;

    res = (LL)res * qmi(n + 1, mod - 2, mod) % mod;

    cout << res << endl;

    return 0;
}

```