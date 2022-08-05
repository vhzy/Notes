#! https://zhuanlan.zhihu.com/p/549635340
- [数学知识Part2](#数学知识part2)
	- [欧拉函数](#欧拉函数)
		- [公式法](#公式法)
			- [什么是欧拉函数呢？](#什么是欧拉函数呢)
			- [欧拉函数如何求解呢？](#欧拉函数如何求解呢)
			- [AcWing 873. 欧拉函数](#acwing-873-欧拉函数)
		- [筛法](#筛法)
	- [快速幂](#快速幂)
		- [AcWing 875. 快速幂](#acwing-875-快速幂)
		- [AcWing 876. 快速幂求逆元 ](#acwing-876-快速幂求逆元-)
	- [扩展欧几里得算法](#扩展欧几里得算法)
		- [AcWing 877. 扩展欧几里得算法 ](#acwing-877-扩展欧几里得算法-)
		- [AcWing 878. 线性同余方程 ](#acwing-878-线性同余方程-)
	- [中国剩余定理*](#中国剩余定理)
		- [AcWing 204. 表达整数的奇怪方式](#acwing-204-表达整数的奇怪方式)

# 数学知识Part2
本节主要说了：
- 欧拉函数
- 快速幂
- 扩展欧几里得算法
- 中国剩余定理

笔记只记录结论和代码，证明过程来自[博客](https://blog.csdn.net/vcj1009784814/article/details/119035186).
## 欧拉函数

### 公式法

#### 什么是欧拉函数呢？
欧拉函数用 $\phi(n)$来表示，它的含义是， **1到 n 中与 n 互质的数的个数**

比如，$\phi(6) = 2$，解释：1到6当中，与6互质的数只有1，5，共两个数。

两个数 a , b 互质的含义是 $gcd(a,b)=1$.

#### 欧拉函数如何求解呢？

对于一个数 N ，将其写为分解质因数的形式$N = P_1^{k_1} \times P_2^{k_2} \times ... \times P_n^{k_n} $

则$\phi(N) = N \times (1-\frac{1}{P_1}) \times (1-\frac{1}{P_2}) \times ... \times (1-\frac{1}{P_n})$，这就是欧拉函数的求解公式

比如 N = 6 ， 6有2个质因子2和3，则$\phi(6)=6 \times\left(1-\frac{1}{2}\right) \times\left(1-\frac{1}{3}\right)=2$

时间复杂度的瓶颈在分解质因数上，$O(\sqrt n)$

证明就是容斥原理，见下图
![](https://pic4.zhimg.com/80/v2-d3ad57d4d18e43230a346ff89f5eaa28.png)
![](https://pic4.zhimg.com/80/v2-bf42f9ceb81b3164364f3e5e3ec0d451.png)


#### [AcWing 873. 欧拉函数](https://www.acwing.com/activity/content/problem/content/942/)
```cpp
#include <iostream>

int euler(int x) {
	int ans = x;
	for(int i = 2; i <= x / i; i++) {
		if(x % i == 0) {
			while(x % i == 0) x /= i;
			ans = ans / i * (i - 1);
		}
	}
	if(x > 1) ans = ans / x * (x - 1);
	return ans;
}

int main() {
	int n, a;
	scanf("%d" ,&n);
	while(n--) {
		scanf("%d", &a);
		printf("%d\n", euler(a));
	}
}
```
![](https://pic4.zhimg.com/80/v2-df4be6e214f952f0d2b8d96d6483d042.png)

### 筛法
上面的公式法，适用于求解某一个数的欧拉函数，就类似于用试除法判断某一个数是否是质数。

然而，有的时候，我们需要**求解某一个范围内全部数的欧拉函数**（比如求解 1 到 N 之间所有数的欧拉函数），此时若对每个数依次套用欧拉公式，则整体的时间复杂度为$O(N \times \sqrt{N})$，因为欧拉函数的计算依赖于分解质因数，而分解质因数的时间复杂度是$O(\sqrt{N})$。这个时间复杂度是不被接受的，太慢了，所以我们需要变换思路。

联想到在求解 1 到 N 之间全部质数的时候，我们采用的是筛法，而不是对每个数依次判断是否是质数。类似的，求解 1 到 N 之间全部数的欧拉函数，我们也可以用类似的思想。

借鉴前面筛选质数时所采用的线性筛法，能够在$O ( N )$的时间复杂度内求解出 1 到 N 每个数的欧拉函数。在本章（数论）后面的学习中，会发现线性筛法在执行过程中不仅仅能求出欧拉函数，还能求出很多其他的内容。

我们先把线性筛法的代码写一遍
```cpp
#include<iostream>
#include<algorithm>
using namespace std;

const int N = 1e6 + 10;

bool st[N];

int primes[N], ctn;

void get_primes_linear(int n) {
	for(int i = 2; i <= n; i++) {
		if(!st[i]) primes[ctn++] = i;
		for(int j = 0; primes[j] <= n / i; j++) {
			st[primes[j] * i] = true;
			if(i % primes[j] == 0) break;
		}
	}
}
```
![](https://pic4.zhimg.com/80/v2-0a095e6627110b4211e725701ba5c4ba.png)
![](https://pic4.zhimg.com/80/v2-6ab997fb270d1c25bfb8ae45360176ed.png)

[AcWing 874. 筛法求欧拉函数](https://www.acwing.com/problem/content/876/)
```cpp
#include<iostream>
using namespace std;

typedef long long LL;

const int N = 1e6 + 10;

int primes[N], ctn;

bool st[N];

LL phi[N];

void get_eulers(int n) {
	phi[1] = 1;
	for(int i = 2; i <= n; i++) {
		if(!st[i]) {
			primes[ctn++] = i;
			phi[i] = i - 1;
		}
		for(int j = 0; primes[j] <= n / i; j++) {
			st[primes[j] * i] = true;
			if(i % primes[j] == 0) {
				phi[primes[j] * i] = primes[j] * phi[i];
				break;
			}
			phi[primes[j] * i] = (primes[j] - 1) * phi[i];
		}
	}
}

int main() {
	int n;
	scanf("%d", &n);
	get_eulers(n);
	LL sum = 0;
	for(int i = 1; i <= n; i++) sum += phi[i];
	printf("%lld", sum);
	return 0;
}
```

![欧拉定理](https://pic4.zhimg.com/80/v2-efe38c8d4eb04e584664842c522759b6.png)

## 快速幂
快速幂，是用来快速求解出$a^k \mod p$的结果，时间复杂度为$O(logk)$，其中 a，k，p 都可以$10^9$内，如果是按照朴素做法的话，则需要 $O(k)$ 的时间复杂度，如果$k = 10^9$，则这个复杂度就比较高了，而如果是$O(\log_2k)$，即便 $k=10^9$，也大概只需要 30 次计算即可，非常的快。

 那么，快速幂是怎么做到的呢？

快速幂的核心思路是：反复平方法（思想上有点类似逆向二分。二分是每次在当前基础上减一半，快速幂是每次在当前基础上扩大一倍）。

个人觉得就是二进制优化，和前面背包问题的二进制优化本质一样。

原理如下图：
![快速幂原理](https://i.imgur.com/qXahQLM.png)

### [AcWing 875. 快速幂](https://www.acwing.com/problem/content/877/)

```cpp
#include<iostream>
using namespace std;

typedef long long LL;

// 快速幂求解 a^k mod p
int qmi(int a, int k, int p) {
	int res = 1;
	// 求 k 的二进制表示
	while(k > 0) {
		if(k & 1 == 1) res = (LL) res * a % p;
		k = k >> 1;
		a = (LL)a * a % p;
	}
	return res;
}

int main() {
	int n;
	scanf("%d", &n);
	while(n--) {
		int a, k, p;
		scanf("%d%d%d", &a, &k, &p);
		printf("%d\n", qmi(a, k, p));
	}
	return 0;
}
```

### [AcWing 876. 快速幂求逆元 ](https://www.acwing.com/activity/content/problem/content/945/)

**乘法逆元**的定义：若两个数 b 和 m 互质，则对任意整数 a ，如果 b 能整除 a ，则存在一个整数 x ，使得 $\frac{a}{b} \equiv a \times x \mod m$

则称 x 是 b 在模 m 下的乘法逆元，记作$b^{-1} \mod m$

容易得到： $b \times b^{-1} \equiv 1 \mod m$，即$b \times b^{-1} \mod m = 1$

求一个数 b 在模 m 下的逆元，即求一个数 x ，满足$b \times x \mod m = 1$即可

若 m 是一个质数，将其记为 p ，则根据上面的费马小定理，有$b^{p-1} \mod p = 1，则 b 的逆元 b^{-1} \mod p$就等于$b^{p-2} \mod p$

若 m 不是一个质数（但注意 b 和 m 是互质的），则根据欧拉定理，有 $b^{\phi(m)} \mod m = 1$，则 b的逆元 $b^{-1} \mod p$ 就等于 $b^{\phi(m)-1} \mod p$

这道题考察的就是快速幂+费马小定理

```cpp
#include<iostream>
using namespace std;

typedef long long LL;

int qmi(int a, int k, int p) {
	int res = 1;
	while(k > 0) {
		if(k & 1 == 1) res = (LL) res * a % p;
		k = k >> 1;
		a = (LL) a * a % p;
	}
	return res;
}

int main() {
	int n;
	scanf("%d", &n);
	while(n--) {
		int a, p;
		scanf("%d%d", &a, &p);
		if(a % p == 0) printf("impossible\n"); // a 和 p 不互质时无解
		else printf("%d\n", qmi(a, p - 2, p));
	}
	return 0;
}
```

## 扩展欧几里得算法
裴蜀定理：对任意的一对正整数 a ，b ，一定存在一对非零整数 x ，y ，使得$ax + by = gcd(a,b)$

令$ax + by = d$，则 d  一定是$gcd(a,b)$的倍数。这个是显而易见的，令 a  和 b 的最大公约数是 c ，即令 $gcd(a,b)=c$则 a  一定是 c 的倍数，b 也一定是 c 的倍数，故$ax+by$也一定是 c 的倍数。则最小可以凑出的倍数就是 1 。所以裴蜀定理是成立的。

那么给定一对正整数 a ，b ，如何求解出一对 x ，y ，使得$ax+by=gcd(a,b)$成立呢？

求解 x ，y 的过程，就可以采用扩展欧几里得算法。

扩展欧几里得算法，是在欧几里得算法上的扩展。而欧几里得算法，就是前面求解最大公约数时，用到的辗转相除法。

### [AcWing 877. 扩展欧几里得算法 ](https://www.acwing.com/problem/content/879/)
```cpp
#include<iostream>
using namespace std;

int gcd(int a, int b, int &x, int &y) {
	if(b == 0) {
		x = 1;
		y = 0;
		return a;
	} else {
		 int d = gcd(b, a % b, y, x); // 注意这里要交换 x 和 y 的位置
		 y -= a / b * x;
		 return d;
	}
}

int main() {
	int n;
	scanf("%d", &n);
	while(n--) {
		int a, b, x, y;
		scanf("%d%d", &a, &b);
		gcd(a, b, x ,y);
		printf("%d %d\n", x, y);
	}
	return 0;
}
```
![代码解释](https://pic4.zhimg.com/80/v2-0b01612768c768653b39ec0496e76d41.png)

### [AcWing 878. 线性同余方程 ](https://www.acwing.com/problem/content/880/)

即，给定 a ，b ，m ，求解一个 x ，使得满足 $ax \equiv b(\mod m)$

因为上面等式的含义是：ax 除以 m ，余数是 b ，所以ax 一定是 m 的某个倍数，加上 b ，即 $ax = my+b$

再变形一下，得 $ax-my=b$，令 $y ′ = − y$ ，则有$ax+my^{'}=b$
这样就转变成了上面使用扩展欧几里得算法能够求解问题，只需要保证 **b 是 a 和 m 的最大公约数的倍数**即可，否则无解。

为什么要保证 b 是 a 和 m 的最大公约数的倍数呢？解释如下

假设 a 和 m 的最大公约数是 k ，那么根据上面的裴属定理，一定有一组 (x,y) ，使得 ax+my=k成立，那么对于 k 的倍数，比如 t 倍，就是 tk，则一定有$atx+mty = tk$。所以，只要保证 b 是 a 和 m 的最大公约数的某个倍数，这个线性同余方程就有解，否则无解。

1. 因为 $a∗x≡b(mod m)$ 等价于 $a∗x−b$ 是m的倍数，因此线性同余方程等价为 $a∗x+m∗y=b$
2. 根据 Bezout 定理，上述等式有解当且仅当 $gcd(a,m)|b$
3. 因此先用扩展欧几里得算法求出一组整数 x0,y0, 使得 $a∗x0+m∗y0=gcd(a,m)$。 然后 $x=x_0∗b/gcd(a,m)%m$即是所求。


最后这里$\mod m$是因为$a x \% m=b \Longleftrightarrow a \cdot(x \% m) \% m=b$
所以对 x % m仍是个答案
因为输出要在int范围，所以%m

```cpp
#include<iostream>
using namespace std;

typedef long long LL;

int gcd(int a, int b, int &x, int &y) {
	if(b == 0) {
		x = 1;
		y = 0;
		return a;
	} else {
		 int d = gcd(b, a % b, y, x); // 注意这里要交换 x 和 y 的位置
		 y -= a / b * x;
		 return d;
	}
}

int main() {
	int n;
	scanf("%d", &n);
	while(n--) {
		int a, b, m, x, y;
		scanf("%d%d%d", &a, &b, &m);
		int d = gcd(a, m, x ,y);
		if(b % d != 0) printf("impossible\n");
        else printf("%d\n", (LL)x * b / d % m);
	}
	return 0;
}
```


## 中国剩余定理*
例子：有一个数，它除以3余2，除以5余3，除以7余2，问这个数是多少？

即 $x \equiv 2(\mod 3)，x \equiv 3(\mod 5)，x \equiv 2(\mod 7)$

该问题的求解步骤如下：
1. 找出3和5的公倍数中，除以7余1的最小数，即15；找出3和7的公倍数中，除以5余1的最小数，即21；找出5和7的公倍数中，除以3余1的最小数，即70。
2. 用15乘以2（除7余2的2），用21乘以3（除5余3的3），用70乘以2（除3余2的2），把3个乘积加起来；得 15 × 2 + 21 × 3 + 70 × 2 = 233 
3. 用 233 除以 3，5，7的最小公倍数 105 ，得到余数 23，答案即为23
   
这个求解过程，被称为中国剩余定理。更一般的描述如下：

给定一堆两两互质的数$m_1,m_2,…,m_k$
存在一个数 x ，满足
$$
\begin{aligned}
&\mathrm{x} \equiv \mathrm{a}_{1}\left(\bmod \mathrm{m}_{1}\right) \\
&\mathrm{x} \equiv \mathrm{a}_{2}\left(\bmod \mathrm{m}_{2}\right) \\
&\cdots \\
&\mathrm{x} \equiv \mathrm{a}_{\mathrm{k}}\left(\bmod \mathrm{m}_{\mathrm{k}}\right)
\end{aligned}
$$

求解这个 x ，如下：
令$M = m_1 \times m_2 \times… \times m_k$,令$M_i = \frac{M}{m_i}$,即$M_i$是除了$m_i$之外其他所有数的乘积。

而由于对于$j \in [1,k]$，$m_j$之间两两互质，所以$M_i$ 和$m_i$互质

而根据上面介绍的欧拉定理和乘法逆元，对于两个互质的数 $M_i$和$m_i$，一定存在一个乘法逆元$M_i^{-1}$，使得 $M_i \times M_i^{-1} \equiv 1 (\mod m_i)$ 

则 $x = a_1 \times M_1 \times M_1^{-1} + a_2 \times M_2 \times M_2^{-1} + ... + a_k \times M_k \times M_k^{-1}$，这个求解公式，就是中国剩余定理

特殊的，满足中国剩余定理的最小解是：
$x=(a_1​×M_1​×M_1^{−1}​+a_2​×M_2​×M_2^{−1}​+...+a_k​×M_k​×M_k^{−1​})modM$

上面式子中的乘法逆元，可以用扩展欧几里得算法求解

参考链接：[中国剩余定理学习笔记](https://blog.csdn.net/vcj1009784814/article/details/119035186)

### [AcWing 204. 表达整数的奇怪方式](https://www.acwing.com/activity/content/problem/content/948/)
[题解](https://www.acwing.com/solution/content/21747/)
下面图片中二元一次方程通解的证明可见[博客](https://zhuanlan.zhihu.com/p/396678425)
![表达整数的奇怪方式](https://pic4.zhimg.com/80/v2-895ad1139a9870dcda240a61e472ee19.png)
```cpp
#include <iostream>
#include <algorithm>
using namespace std;

typedef long long LL;

// 扩展欧几里得算法
LL exgcd(LL a, LL b, LL &x, LL &y) {
	if (b == 0) {
		x = 1;
		y = 0;
		return a;
	}
	LL d = exgcd(b, a % b, y, x);
	y -= a / b * x;
	return d;
}

int main() {
	int n;
	scanf("%d", &n);
	bool no_ans = false;
	LL a1, m1;

	cin >> a1 >> m1;
	for (int i = 0; i < n - 1; i++) {
		LL a2, m2;
		cin >> a2 >> m2;
		LL k1, k2;
		LL d = exgcd(a1, a2, k1, k2);
		if ((m2 - m1) % d != 0) {
			no_ans = true;
			break;
		}
		k1 *= (m2 - m1) / d; //因为此时k1是k1*a1+k2*a2=d的解,所以要乘上(m2-m1)/d的倍数大小
		LL t = a2 / d;
		k1 = (k1 % t + t) % t; // 将k1置为最小的正整数解
		// 更新a1和m1, 准备下一轮的合并
		m1 = a1 * k1 + m1;
		//m1在被赋值之后的值为当前"x"的值，此时赋值是为了方便下一轮的继续使用
		a1 = abs(a1 / d * a2);
		//循环结束时a1的值为当前所有的a1,a2,……an中的最小公倍数
	}
	if (no_ans) printf("-1");
	    //当循环结束时，此时的值应该与最小公倍数取模,以求得最小正整数解
	else printf("%lld", (m1 % a1 + a1) % a1);
}

```