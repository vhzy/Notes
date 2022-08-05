#! https://zhuanlan.zhihu.com/p/549192612
- [数学知识Part1](#数学知识part1)
  - [质数](#质数)
    - [质数的判定--试除法](#质数的判定--试除法)
    - [分解质因数](#分解质因数)
    - [筛法](#筛法)
      - [朴素筛法](#朴素筛法)
      - [埃氏筛法](#埃氏筛法)
      - [线性筛法](#线性筛法)
  - [约数](#约数)
    - [AcWing 869. 试除法求约数 ](#acwing-869-试除法求约数-)
      - [代码实现](#代码实现)
    - [870. 约数个数](#870-约数个数)
      - [代码实现](#代码实现-1)
    - [AcWing 871. 约数之和数](#acwing-871-约数之和数)
      - [代码实现](#代码实现-2)
    - [AcWing 872. 最大公约数 ](#acwing-872-最大公约数-)

# 数学知识Part1

数学知识章节，主要讲解了
- 数论
- 组合计数
- 高斯消元
- 简单博弈论

这一小节主要讲解的是数论，主要包括了质数，约数，欧拉函数，快速幂，扩展欧几里得算法，中国剩余定理。

## 质数
对所有的大于1的自然数字，定义了【质数/合数】这一概念。对于所有小于等于1的自然数，没有这个概念，它们既不是质数也不是合数。

质数的定义：对于大于1的自然数，如果这个数的约数只包含1和它本身，则这个数被称为质数，或者素数

### 质数的判定--试除法
[866. 试除法判定质数](https://www.acwing.com/problem/content/868/)
采用试除法。

对于一个数n，从2枚举到n-1，若有数能够整除n，则说明除了1和n本身，n还有其他约数，则n不是质数；否则，n是质数,时间复杂度$O(N)$

```cpp
//朴素做法
#include<iostream>
using namespace std;

bool is_prime(int n) {
	if(n < 2) return false;
	for(int i = 2; i <= n / i; i++) {
		if(n % i == 0) return false;
	}
	return true;
}

int main() {
	int m;
	scanf("%d", &m);
	while(m--) {
		int a;
		scanf("%d", &a);
		if(is_prime(a)) printf("Yes\n");
		else printf("No\n");
	}
	return 0;
}

```


优化：由于**一个数的约数都是成对出现的**。比如12的一组约数是3，4，另一组约数是2，6。则我们只需要枚举较小的那一个约数即可，时间复杂度**稳定**$O(\sqrt{N})$

我们用$d ∣ n$来表示d整除n，比如$3 ∣ 12$
只要满足$d ∣ n$，则一定有 $ \frac{n}{d} | n$,因为约数总是成对出现的
我们只枚举小的那一部分的数即可，令$d ≤ \frac{n}{d}$，则$d ≤\sqrt{n}$ 
则对于数n，只需要枚举2到$\sqrt{n}$即可
```cpp
bool is_prime(int n) {
    if(n < 2) return false;
    for(int i = 2; i <= n / i; i++) {
        if(n % i == 0) return false;
    }
    return true;
}
```
注意有一个细节，for循环的结束条件，推荐写成`i <= n / i`。

有的人可能会写成`i <= sqrt(n)`，这样每次循环都会执行一次sqrt函数，而这个函数是有一定时间复杂度的。而有的人可能会写成

`i * i < =n`，这样当i很大的时候（比如i比较接近int的最大值时），`i * i`可能会溢出，从而导致结果错误。
​

### 分解质因数
[867. 分解质因数](https://www.acwing.com/problem/content/869/)
**朴素思路**
还是采用试除法。对于一个数N，总能够写成如下的式子：

$\mathrm{N}=\mathrm{P}_{1}^{\mathrm{k}_{1}} \times \mathrm{P}_{2}^{\mathrm{k}_{2}} \times \ldots \ldots \mathrm{P}_{\mathrm{n}}^{\mathrm{k}_{\mathrm{n}}}$​，其中$P_1$到$P_n$ 皆是质数，$k_1$ 到$k_n$都是大于0的正整数.

对于一个数n求解质因数的过程如下：

从2到n，枚举所有数，依次判断是否能够整除 n 即可。
```cpp
#include<iostream>
using namespace std;

void divide(int n) {
    for(int i = 2; i <= n; i++) {
        if(n % i == 0) {
            int s = 0;
            while(n % i == 0) {
                s++;
                n /= i;
            }
            printf("%d %d\n", i, s);
        }
    }
}

int main() {
	int m;
	scanf("%d", &m);
	while(m--) {
		int a;
		scanf("%d", &a);
		divide(a);
		printf("\n");
	}
	return 0;
}
```

这里可能有个疑问，不是应当枚举所有的质数吗？怎么是枚举所有数？枚举所有数如果取到合数怎么办？那分解出来的就不是质因子了啊。

下面进行一下解释：

我们枚举数时，对于每个能整除`n`的数，先把这个数除干净了，再继续枚举后面的数，这样能保证，后续再遇到能整除的数，一定是质数而不是合数。

除干净是什么意思呢？比如 n=24，我们先枚举2，发现2能整除24，则除之，24÷2=12，得到的结果是12，发现2仍然能整除之，则除之，12÷2=6，仍能整除，除之！6÷2=3。2不能整除3了。则停止。继续枚举下一个数3，3÷3=1。

质因数分解结束。则24 = $2^3$ × $3^1$，24的质因子就有两个，分别是2和3。

那么，把一个数除干净了，怎么就能保证后续遇到能整除的数一定是质数了呢？

假设后续枚举到一个合数`k`，这个合数能整除`n`，则这个合数的某个质因子`p`，也能整除`n`。就比如合数6能整除24，则6的质因子2，肯定也能整除24。

合数k的质因子`p`一定比合数本身小，而我们是从小到大进行枚举，则`p`一定在`k`之前被枚举过了，而之前枚举`p`时，是把`p`除干净了的，此时不应当还能被`p`整除，这就矛盾了。所以在枚举时，如果遇到能整除的数，只可能是质数，而不可能是合数。（我们是从2开始枚举的，而2是一个质数）

**优化**
其实这里的优化和上面一样
从2枚举到n，时间复杂度就是O(n)。其实不必枚举到n。下面进行一下优化

有一个重要性质：**n中最多只包含一个大于$\sqrt{n}$ 的质因子**
这个结论很好证明，因为我们知道一个数n分解质因数后可以写成
$\mathrm{N}=\mathrm{P}_{1}^{\mathrm{k}_{1}} \times \mathrm{P}_{2}^{\mathrm{k}_{2}} \times \ldots \ldots \mathrm{P}_{\mathrm{n}}^{\mathrm{k}_{\mathrm{n}}}$
其中$P_1$到$P_n$ 都是n的质因子，若存在两个大于$\sqrt{n}$的质因子，就算两个质因子的指数都是最小的1，它们相乘过后也大于n了，产生了矛盾。

所以我们只用枚举到$\sqrt{n}$即可。枚举的i一定满足$i <= \sqrt{n}$，即$i <= \frac{n}{i}$
最坏时间复杂度$O(\sqrt{n})$，最好时间复杂度$O(logN)$

```cpp
void divide(int n) {
    for(int i = 2; i <= n / i; i++) {
        if(n % i == 0) {
            int s = 0;
            while(n % i == 0) {
                s++;
                n /= i;
            }
            printf("%d %d\n", i, s);
        }
    }
    // 如果除完之后, n是大于1的, 
    // 说明此时的n就是那个大于 原根号n 的最大的质因子, 单独输出一下
    if(n > 1) printf("%d %d\n", n, 1);
}
```

### 筛法
[868. 筛质数](https://www.acwing.com/problem/content/870/)
对于一个数n，求解1~n中质数的个数

#### 朴素筛法
将2到n全部数放在一个集合中，**遍历2到n，删除集合中这个数的倍数**。最后集合中剩下的数就是质数。

解释：如果一个数p没有被删掉，那么说明在2到p-1之间的所有数，p都不是其倍数，即2到p-1之间，不存在p的约数。故p一定是质数。

时间复杂度：
$$
\frac{\mathrm{n}}{2}+\frac{\mathrm{n}}{3}+\ldots .+\frac{\mathrm{n}}{\mathrm{n}}=\mathrm{n}\left(\frac{1}{2}+\frac{1}{3}+\ldots .+\frac{1}{\mathrm{n}}\right)=\mathrm{n} \ln \mathrm{n}
$$
而$\ln n=n \log _{e} n$而e = 2.71828 e=2.71828e=2.71828左右，是大于2的，所以$\ln n=n \log _{e} n < nlog_2n$
故，朴素思路筛选质数的时间复杂度大约为$nlogn$



```cpp
#include<iostream>
using namespace std;

const int N = 1e6 + 10;

int primes[N],ctn;

bool st[N];

void get_primes(int n) {
	for(int i = 2; i <= n; i++) {
		if(!st[i]) primes[ctn++] = i; // i是质数
		for(int j = i + i; j <= n; j += i) st[j] = true; // 删数
	}
}

int main() {
	int n;
	scanf("%d", &n);
	get_primes(n);
	printf("%d", ctn);
}
```
#### 埃氏筛法
其实不需要把全部数的倍数删掉，而只需要删除质数的倍数即可。

对于一个数p，判断其是否是质数，其实不需要把2到p-1全部数的倍数删一遍，只要删掉2到p-1之间的质数的倍数即可。因为，若p不是个质数，则其在2到p-1之间，一定有质因数，只需要删除其质因数的倍数，则p就能够被删掉。优化后的代码如下

代码用一个布尔数组来表示一个数是否被删除。遍历2到n，对每个数，先看一下其是否被删除了，若没有，则说明其是一个质数，随后将这个数以及其倍数全部删除（布尔数组置为true）。每当遍历到一个数时，如果这个数没有被前面的数所删掉，则说明这个数是个质数。
```cpp
#include<iostream>
using namespace std;

const int N = 1e6 + 10;

int primts[N],ctn;

bool st[N];

void get_primes(int n) {
	for(int i = 2; i <= n; i++) {
		if(!st[i]) {
			primes[ctn++] = i;
			for(int j = i; j <= n; j += i) st[j] = true;//放入判断条件里面
		}
	}
}

int main() {
	int n;
	scanf("%d", &n);
	get_primes(n);
	printf("%d", ctn);
}
```
那么优化后的时间复杂度如何呢？

原本我们需要对每个数都删掉其倍数，现在只需要对是质数的数，删掉其倍数。需要操作的数的个数明显减少了很多。要估算优化后的算法的时间复杂度，问题是，质数的个数究竟有多少个呢？

根据**质数定理**，在1到n之间，质数的个数大约为$\frac{n}{ln n}$，我们原本需要对n个数进行操作，现在只需要对$\frac{n}{ln n}$个数进行操作，所以时间复杂度就除以个$\frac{n}{ln n}$（其实这样算是不正确的），即${n}{ln n} ÷ ln n = n$，所以优化后的算法的时间复杂度大约是$O ( n )$ ，其实准确复杂度是$n log{log n}$。

这种优化后的筛选质数的方法，被称为**埃氏筛法（埃拉托斯特尼筛法）**。
![埃氏筛法图解](https://pic4.zhimg.com/80/v2-0f1d96893b746cdacf54e0bf94793a04.gif)

#### 线性筛法
下面多介绍一种**线性筛法**，其性能要优于**埃氏筛法**（在$10^6$ 下两个算法差不多，在$10^7$下线性筛法大概快一倍），其思想也类似，把每个合数，用它的某一个质因子删掉就可以了。

核心思路是：**对于某一个合数n，其只会被自己的最小质因子给筛掉。**

先上一下代码
```cpp
#include<iostream>
using namespace std;

const int N = 1e6 + 10;

int cnt;

int primes[N];

bool st[N];

void get_primes(int n){
    //外层从2~n迭代，因为这毕竟算的是1~n中质数的个数，而不是某个数是不是质数的判定
    for(int i=2;i<=n;i++){
        if(!st[i]) primes[cnt++]=i;
        for(int j=0;primes[j]<=n/i;j++){//primes[j]<=n/i:变形一下得到——primes[j]*i<=n,把大于n的合数都筛了就
        //没啥意义了
            st[primes[j]*i]=true;//用最小质因子去筛合数

            //1)当i%primes[j]!=0时,说明此时遍历到的primes[j]不是i的质因子，那么只可能是此时的primes[j]<i的
            //最小质因子,所以primes[j]*i的最小质因子就是primes[j];
            //2)当有i%primes[j]==0时,说明i的最小质因子是primes[j],因此primes[j]*i的最小质因子也就应该是
            //prime[j]，之后接着用st[primes[j+1]*i]=true去筛合数时，就不是用最小质因子去更新了,因为i有最小
            //质因子primes[j]<primes[j+1],此时的primes[j+1]不是primes[j+1]*i的最小质因子，此时就应该
            //退出循环，避免之后重复进行筛选。
            if(i%primes[j]==0) break;
        }
    }

}

int main() {
	int n;
	scanf("%d", &n);
	get_primes(n);
	printf("%d", cnt);
}

```
对上面的代码解释如下：
用 pj 来表示primes[j]，首先保证下面的实现过程一定满足**对于某一个合数n，其只会被自己的最小质因子给筛掉。**
- 当`i % p j = 0`时
`pj`一定是` i `的最小质因子，因为我们是从小到大枚举质数的，首先遇到的满足`i % p j = 0`的，`pj`一定是 i 的最小质因子，
并且`pj`一定是`p j × i`的最小质因子。
这么说可能不太好理解，假设4的最小质因子为2，写成分解质因数的形式，即为$4 = 2^2$.
则，4的倍数中最小的数，且最小质因子同样是2的，一定是给4本身，再乘以一个其最小质因子，得到的数，即8。
再举个例子，15 = 3 × 5 ，15的最小质因子是3，则15的倍数中最小的数，且最小质因子同样是3的，一定是给15乘以一个最小质因子3，即45。
<br>
- 当` i % p j ≠ 0 `时
`pj`一定不是i的质因子。并且由于是从小到大枚举质数的，那么`pj`一定小于i的全部质因子。那么`pj`就一定是`p j × i`的最小质因子。

则无论哪种情况,`pj`都一定是`pj × i`的最小质因子。

还有一个问题，为什么不用写 j < cnt？因为：
- 如果 i 是质数，那么在循环之前已经被加入到了 primes[] 中，所以一定会存在 i % primes[j] == 0 成立（两个相同的数相除，和为 1，余数为 0），break 掉。
- 如果 i 是合数，一定会存在一个最小质因子，使得 if 语句成立，break 掉；或者在这之前，因为不满足循环条件从而停止循环。


**对于某一个合数n，其只会被自己的最小质因子给筛掉。** 假设，有一个合数x，那么其一定有一个最小质因子pj，那么当枚举到$i = \frac{x}{pj}$的时候，就能把x删掉

线性筛法保证了，每个合数都会被删掉，都是被其最小质因子给删掉的，且每个数只有一个最小质因子，所以只会被删一次，因此时间复杂度是$O(N)$的.

运行时间如下:
![筛法时间性能](https://pic4.zhimg.com/80/v2-1f23d2fdde32af99f2895bf2d6269497.png)

从上往下依次是**线性筛法，埃氏筛法，朴素筛法。**


## 约数

### [AcWing 869. 试除法求约数 ](https://www.acwing.com/problem/content/871/)

给定 n 个正整数 ai，对于每个整数 ai，请你按照从小到大的顺序输出它的所有约数。
 

#### 代码实现
试除法求一个数的所有约数，和试除法判断质数的思路一样
```cpp
#include<iostream>
using namespace std;
const int N = 2e8 + 10;

int l[N], h[N];

void get_dividers(int n) {
	// 只枚举较小的约数即可
	int lctn = 0, hctn = 0;
	for(int i = 1; i <= n / i; i++) {
		if(n % i == 0) {
			l[lctn++] = i;
			if(i != n / i) h[hctn++] = n / i; // 重复约数需要排除
		}
	}
	for(int i = 0; i < lctn; i++) printf("%d ", l[i]);
	for(int i = hctn - 1; i >= 0; i--) printf("%d ", h[i]);
	printf("\n");
}

int main() {
	int m;
	scanf("%d", &m);
	while(m--) {
		int n;
		scanf("%d", &n);
		get_dividers(n);
	}
	return 0;
}
```

### [870. 约数个数](https://www.acwing.com/problem/content/872/)
**算术基本定理**：
假设一个数 N ，其分解质因数可写成,$\mathrm{N}=\mathrm{P}_{1}^{\mathrm{k}_{1}} \times \mathrm{P}_{2}^{\mathrm{k}_{2}} \times \ldots \ldots \mathrm{P}_{\mathrm{n}}^{\mathrm{k}_{\mathrm{n}}}$
则N的约数个数为$( k_1 + 1 ) × ( k_2 + 1 ) × . . . . × ( k_n + 1 ) $

其实就是排列组合。

对于 N 的每个质因子，我们在构造一个约数时，可以选择是否将其纳入。

比如对于质因子$P_1$，它的指数是$k_1$ ，则我们有$k_1+1$种选择，即：纳入 0 个$P_1$ ，纳入 1 个 $P_1$ ，…，纳入$k_1$ 个 $P_1$，对于其他质因子同理。

当所有的质因子我们都不纳入时，得到的约数就是 1 ，当所有的质因子我们全纳入时（每个质因子的指数取最大），得到的约数就是 N 本身。

一共有多少种组合方式呢？

对于每个质因子$P_i$,我们都有 $k_i + 1$种选择，总共的组合方式就是将每个质因子的选择数相乘，即得到上面的公式。

在`int`范围内的全部数，约数个数最多的一个数，其约数个数大概有1500个

#### 代码实现
```cpp
#include<iostream>
#include<unordered_map>
using namespace std;

typedef long long LL;

const int N = 1e9 + 7;

int main() {
	int m;
	scanf("%d", &m);
	unordered_map<int, int> primes; // 计数所有的质因子及其指数
	while(m--) {
		int n;
		scanf("%d", &n);
		for(int i = 2; i <= n / i; i++) {
			while(n % i == 0) {
				n /= i;
				primes[i]++;
			}
		}
		if(n > 1) primes[n]++;
	}
	unordered_map<int, int>::iterator it = primes.begin();
	LL res = 1;
	while(it != primes.end()) {
		res = (res * (it->second + 1)) % N;
		it++;
	}
	printf("%lld", res);
	return 0;
}
```

### [AcWing 871. 约数之和数](https://www.acwing.com/activity/content/problem/content/940/)
数 N 的所有约数之和等于
$$
\left(\mathrm{P}_{1}^{0}+\mathrm{P}_{1}^{1}+\ldots+\mathrm{P}_{1}^{\mathrm{k}_{1}}\right) \times \ldots . . \times\left(\mathrm{P}_{\mathrm{n}}^{0}+\mathrm{P}_{\mathrm{n}}^{1}+\ldots+\mathrm{P}_{\mathrm{n}}^{\mathrm{k}_{\mathrm{n}}}\right)
$$
将上面的式子按照乘法分配律展开，会得到如下的形式
$$
(. . \times . . .)+(. . \times \ldots)+(. . \times . .)+\ldots
$$

每一项都是一个乘积，而这个乘积，就是从每个$P_i$中选择了一项，互相乘了起来，这一个乘积就是 N 的一个约数。

#### 代码实现
```cpp
#include<iostream>
#include<unordered_map>
using namespace std;

const int N = 1e9 + 7;

typedef long long LL;

int main() {
	int m;
	scanf("%d", &m);
	unordered_map<int, int> primes;
	while(m--) {
		int n;
		scanf("%d", &n);
		for(int i = 2; i <= n / i; i++) {
			while(n % i == 0) {
				primes[i]++;
				n /= i;
			}
		}
		if(n > 1) primes[n]++;
	}
	LL res = 1;
	for(auto p : primes) {
		int a = p.first, b = p.second; // 质因数的底数和指数
		LL t = 1;
		for(int i = 0; i < b; i++) {
			t = (t * a + 1) % N;
		}
		res = (res * t) % N;
	}
	printf("%lld", res);
	return 0;
}
```

### [AcWing 872. 最大公约数 ](https://www.acwing.com/activity/content/problem/content/941/)
欧几里得算法\辗转相除法

![](https://pic4.zhimg.com/80/v2-666f3124887726c9943d7cb63cf6ea4e.png)
![](https://pic4.zhimg.com/80/v2-2aa3ed051648c3b9076b57bd00d72c95.png)

```cpp
#include<iostream>
using namespace std;

// 写代码时可以假设一定满足 a > b 
// 就算 a < b , 也会在第一次递归时调转位置
int gcd(int a, int b) {
    // b == 0 时, 直接返回a, 否则进行辗转相除
    return b ? gcd(b, a % b) : a;
}

int main() {
    int m;
    scanf("%d", &m);
    while(m--) {
        int a, b;
        scanf("%d%d", &a, &b);
        printf("%d\n", gcd(a, b));
    }
    return 0;
}

```