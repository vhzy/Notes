#! https://zhuanlan.zhihu.com/p/551239851
- [基础知识Part2](#基础知识part2)
  - [高精度](#高精度)
    - [高精度加法](#高精度加法)
    - [高精度减法](#高精度减法)
    - [高精度乘法](#高精度乘法)
    - [高精度除法](#高精度除法)
  - [前缀和](#前缀和)
    - [一维前缀和](#一维前缀和)
    - [二维前缀和](#二维前缀和)
  - [差分](#差分)
    - [一维差分](#一维差分)
    - [二维差分](#二维差分)
  - [前缀和&差分 小结](#前缀和差分-小结)
      - [一维](#一维)
      - [二维](#二维)

# 基础知识Part2
本节主要说了：
- 高精度
- 前缀和
- 差分

主要框架借鉴自[博客](https://blog.csdn.net/vcj1009784814/article/details/116381700)

## 高精度

*   `A + B`：两个大整数相加
*   `A - B`：两个大整数相减
*   `A × b`：一个大整数乘一个小整数
*   `A ÷ b`：一个大整数除以一个小整数

`A × B` 和 `A ÷ B` 见的不多，课程中没有讲。

**大整数的存储**：用一个数组来存大整数的每一位上的数。

为了方便运算，这里将大整数的个位，存到数组的第一位，大整数的最高位，存到数组的最后一位，即采用小端序。

### 高精度加法
[AcWing 791. 高精度加法](https://www.acwing.com/problem/content/description/793/)

```cpp
#include <iostream>
using namespace std;

const int N = 100010;
int A[N], B[N], C[N];

int Add(int a[], int b[], int c[], int cnt) {

    int t = 0;//t表示进位

    for (int i=1; i<=cnt; i++) {
        t += a[i] + b[i];//进位加上a和b第i位上的数
        c[i] = t % 10;//c的值就是进位的个位数
        t /= 10;//把t的个位数去掉只剩下十位数，即只剩下这个位置的进位
    }
    if (t) c[++cnt] = 1;//如果t==1，表示还有一个进位，要补上

    return cnt;
}

int main() {

    string a, b;
    cin >> a >> b;  


    //A和B倒着放进int数组，因为有进位，倒着放容易处理
    int cnt1 = 0;
    for (int i=a.size()-1; i>=0; i--)
        A[++cnt1] = a[i] - '0';

    int cnt2 = 0;
    for (int i=b.size()-1; i>=0; i--)
        B[++cnt2] = b[i] - '0';

    int tot = Add(A, B, C, max(cnt1, cnt2));

    //因为A和B是倒着放的，所以C也要倒着输出
    for (int i=tot; i>=1; i--)
        cout << C[i];
        return 0;
}
    
```

### 高精度减法
`A - B`

先判断一下`A`和`B`的相对大小，若

*   `A >= B`，则直接计算减法
*   `A < B`，计算`B - A`，并在结果前面加上负号`-`
*   `前导0`的处理

高精度减法的流程，也是模拟人手动做减法的流程，当某一位不够减时，会有**借位**的概念

[AcWing 792. 高精度减法](https://www.acwing.com/problem/content/794/)

```cpp
// C++
#include<iostream>
#include<vector>
#include<string>

using namespace std;
// 比较 A 和 B 的大小, 当 A >= B 时, 返回true, 否则返回false
bool cmp(vector<int> &A, vector<int> &B) {
    if(A.size() != B.size()) return A.size() > B.size(); // 长度不相等时, 直接比较A和B的长度即可
    else {
        for(int i = A.size() - 1; i >= 0; i--) {
            if(A[i] != B[i]) return A[i] > B[i]; // 长度相等时, 从最高位开始进行比较, 只要有一位不同, 就能得出大小关系
        }
        return true; // A和B相等
    }
}

vector<int> sub(vector<int> &A, vector<int> &B) {
    vector<int> C;
    // 用一个变量t来表示借位
    for(int i = 0, t = 0; i < A.size(); i++) {
        t = A[i] - t;   // 该位的运算结果为 : A[i] - B[i] - t , 即2数相减, 再减借位
        if(i < B.size()) t -= B[i];
        C.push_back((t + 10) % 10); // 当运算结果为负数, 则需要+10, 先+10再模10, 能够涵盖运算结果为整数或负数2种情况
        if(t < 0) t = 1; // 当原始运算结果为负数时, 表示需要借位, 将 t 置为 1
        else t = 0; // 否则将借位 t 重新置为 0 
    }
    // 去除前缀的0。 当长度 > 1 , 且最高位为 0 时, 移除最高位
    while(C.size() > 1 && C.back() == 0) C.pop_back();
    return C;
}

int main() {
    
    string a, b;
    cin >> a >> b;
    vector<int> A, B;
    for(int i = a.size() - 1; i >= 0; i--) A.push_back(a[i] - '0');
    for(int i = b.size() - 1; i >= 0; i--) B.push_back(b[i] - '0');
    
    if(cmp(A, B)) {
        vector<int> C = sub(A, B);
        for(int i = C.size() - 1; i >= 0; i--) printf("%d", C[i]);
    } else {
        vector<int> C = sub(B, A);
        printf("-");
        for(int i = C.size() - 1; i >= 0; i--) printf("%d", C[i]);
    }
     return 0;
}
   
```

### 高精度乘法
`A × b`

把`b`看成一个整体，和`A`的每一位去做乘法。例如：`123 × 12`。

首先从`A`的最低位开始，计算`3 × 12`，得`36`，则结果中的个位为：`36 % 10 = 6`，产生的进位为`36 / 10 = 3`；继续下一位，计算`2 × 12`，得`24`，加上进位`3`，得`27`，结果中的十位为：`27 % 10 = 7`，产生的进位是`27 / 10 = 2`；继续下一位，`1 × 12 + 2 = 14`，则百位上的结果为`14 % 10 = 4`，产生进位`14 / 10 = 1`，则最终结果为`1476`。

[AcWing 793. 高精度乘法](https://www.acwing.com/problem/content/795/)
```cpp
// C++
#include<iostream>
#include<vector>
#include<string>
using namespace std;

vector<int> multi(vector<int> &A, int b) {
    vector<int> C;
    int t = 0;
    for(int i = 0; i < A.size(); i++) {
        t += b * A[i];
        C.push_back(t % 10);
        t /= 10;
    }
    if(t > 0) C.push_back(t);
    // 去掉前缀0
    while(C.size() > 1 && C.back() == 0) C.pop_back();
    return C;
}

int main() {
    string a;
    int b;
    cin >> a >> b;
    vector<int> A;
    for(int i = a.size() - 1; i >= 0; i--) A.push_back(a[i] - '0');
    
    vector<int> C = multi(A, b);
    
    for(int i = C.size() - 1; i >= 0; i--) printf("%d", C[i]);
    return 0;
    }
```

### 高精度除法

`A ÷ b`

算法的流程，是模拟人手动做除法的流程。从最高位除起，依次做商和取余。每一轮的余数，乘以10，加上下一位的数，作为下一轮的被除数。

注意跟之前三种算法不同的是，在除法中，数组第0位存高位，而不是低位。
同样也要注意`前导0`的去除。

[AcWing 794. 高精度除法](https://www.acwing.com/problem/content/796/)

```cpp
#include<iostream>
#include<vector>
#include<algorithm>
using namespace std;
//int r=0;
vector<int> div(vector<int> &A,int B,int &r){//r传入r的地址，便于直接对余数r进行修改
    vector<int> C;
    for(int i=0;i<A.size();i++){//对A从最高位开始处理
        r=r*10+A[i];//将上次的余数*10在加上当前位的数字，便是该位需要除的被除数
        C.push_back(r/B);//所得即为商在这一位的数字
        r=r%B;
    }
    //由于在除法运算中，高位到低位运算，因此C的前导零都在vector的前面而不是尾部，vector只有删除最后一个数字pop_back是常数复杂度，而对于删除第一位没有相应的库函数可以使用，而且删除第一位，其余位也要前移，
    //因此我们将C翻转，这样0就位于数组尾部，可以使用pop函数删除前导0
    reverse(C.begin(),C.end());
    while(C.size()>1&&C.back()==0) C.pop_back();
    return C;
}
int main(){
    string a;
    int B,r=0; //代表余数
    cin>>a>>B;
    vector<int> A;
    for(int i=0;i<a.size();i++) A.push_back(a[i]-'0');//注意这次的A是由高为传输至低位，由于在除法的手算过程中，发现从高位进行处理
    //for(int i=0;i<A.size();i++) cout<<A[i];
    //cout<<B;
    auto C = div(A,B,r);
    for(int i=C.size()-1;i>=0;i--) cout<<C[i];//将C从最高位传给最低位
    cout<<endl<<r;//输出余数
    cout<<endl;
    return 0;
}
```

## 前缀和

前缀和思想，是用来快速求解任意一段区间的所有数的和。时间复杂度O(1)

### 一维前缀和

假设有一个数组：a1，a2，a3，a4，a5，…，an（注意，下标从1开始）

前缀和 Si = a1 + a2 + a3 + … + ai （即前`i`个数的和）

显然的，前缀和满足 Si = Si-1 + ai ，特殊的，我们可以定义S0 = 0，这样，任何区间`[l, r]`，我们都可以用 $S_r - S_{l-1}$ 这样的公式来计算，而不需要对边界进行特殊处理（当`l = 1`时，求`[l, r]`的所有数的和，其实就是求 Sr）。

前缀和的最大作用，就是用来**求任意一段区间的所有数的和**。比如，要求区间`[l, r]`的全部元素的和。若没有前缀和数组，则我们需要遍历原数组，时间复杂度为O(n)。若有前缀和数组，**我们只需要计算 $S_r - S_{l-1}$**，时间复杂度为O(1)。
因为 $S_r = a_1 + a_2 + a_3 + … + a_{l-1} + a_l + … + a_r}

而 $S_{l-1} = a_1 + a_2 + a_3 + … + a_{l-1}$

[AcWing 795. 前缀和](https://www.acwing.com/problem/content/797/)
```cpp
// C++
#include<iostream>
using namespace std;

const int N = 1e5 + 10;
int s[N];

int main() {
    int n, m;
    scanf("%d%d", &n, &m);
    for(int i = 1; i <= n; i++) {
        scanf("%d", &s[i]);
        s[i] += s[i - 1]; // 输入数组和计算前缀和放在一起
    };
    while(m--) {
        int l, r;
        scanf("%d%d", &l, &r);
        printf("%d\n", s[r] - s[l - 1]);
    }
    return 0;
}
```

### 二维前缀和
上面的数组前缀和可能过于简单，下面是进阶版：**矩阵前缀和**（二维）

假设有如下的矩阵

a11 ，a12，a13，a14，…，a1n

a21，a22，a23，a24，…， a2n

…

…

am1，am2，am3，am4，…，amn

前缀和 Sij 表示点 aij 及其左上角区域的所有数的和。

经过简单推导（面积计算），可以得到$S_{ij} = S_{i-1,j} + S_{i,j-1} + a_{ij} - S_{i-1,j-1}$

![](https://pic4.zhimg.com/80/v2-68f2e3b41b211d3365c5a784f41b4b79.png)
![](https://pic4.zhimg.com/80/v2-9b2011f6d8c774450adf8f5616849c37.png)

若要计算左上角边界点为`[x1, y1]`，右下角点为`[x2, y2]`，这2个点之间部分的子矩阵的和（也是求任意一段区间内所有数的和），经过简单推导，能够得到下面的公式

$S = S_{x_2,y_2} - S_{x_1-1,y_2} - S_{x_2,y_1-1} + S_{x_1-1,y_1-1}$（由于矩阵中是离散的点，所以计算时边界需要减掉1）

![](https://pic4.zhimg.com/80/v2-6050d1f730a381b62d5ef9b612a68655.png)
![](https://pic4.zhimg.com/80/v2-b86221806634aef209a4bd002e6b0c2e.png)

```c++
// C++
#include<iostream>
using namespace std;

const int N = 1010;
int a[N][N];
int n, m, q;

int main() {
    scanf("%d%d%d", &n, &m, &q);
    for(int i = 1; i <= n; i++) {
        for(int j = 1; j <= m; j++) {
            scanf("%d", &a[i][j]);
            a[i][j] += a[i - 1][j] + a[i][j - 1] - a[i - 1][j - 1]; // 输入和计算前缀和同时进行
        }
    }
    
    while(q--) {
        int x1, x2, y1, y2;
        scanf("%d%d%d%d", &x1, &y1, &x2, &y2);
        printf("%d\n", a[x2][y2] - a[x1 - 1][y2] - a[x2][y1 - 1] + a[x1 - 1][y1 - 1]);
    }
    
    return 0;
}
```

## 差分

差分，是前缀和的逆运算

### 一维差分
假设有一个数组，a1，a2，a3，a4，a5，…，an

针对这个数组，构造出另一个数组，b1，b2，b3，b4，b5，…，bn

使得`a`数组是`b`数组的前缀和，即使得 ai = b1 + b2 + … + bi

此时，称`b`数组为`a`数组的差分

如何构造`b`数组呢：

b1 = a1，b2 = a2 - a1，b3 = a3 - a2，…，bn = an - an-1

实际可以不用如此来构造，在输入数组`a`时，可以先假想数组`a`和数组`b`的全部元素都是0。然后每次进行一次**插入操作**（指的是对数组`a`的`[l, r]`区间的每个数加上常数`C`），比如

对`a`数组区间`[1,1]`，加（插入）常数a1；对区间`[2,2]`，加常数a2，…，这样在输入数组`a`的同时，就能够快速构造出其差分数组`b`

**差分的作用**：

若要对`a`数组中`[l, r]`区间内的全部元素都加上一个常数`C`，若直接操作`a`数组的话，时间复杂度是O(n)。而如果操作其差分数组`b`，则时间复杂度是O(1)。这是因为，数组`a`是数组`b`的前缀和数组，只要对 bl 这个元素加`C`，则`a`数组从`l`位置之后的全部数都会被加上`C`，但`r`位置之后的所有数也都加了`C`，所以我们通过对 br+1 这个数减去`C`，来保持`a`数组中`r`位置以后的数的值不变。

于是，对`a`数组的`[l, r]`区间内的所有数都加上一个常数`C`，就可以转变为对 $b_l$ 加`C`，对$b_{r+1}$ 减 `C`。


[AcWing 797. 差分](https://www.acwing.com/activity/content/problem/content/831/)
```cpp
// C++
#include<iostream>
using namespace std;

const int N = 1e5 + 10;
int n, m;
int a[N]; // 使用一个数组即可

// 对[l, r]区间, 加上常数 c
void insert(int l, int r, int c) {
    // 直接操作差分数组
    a[l] += c;
    a[r + 1] -= c;
}

int main() {
    scanf("%d%d", &n, &m);
    for(int i = 1; i <= n; i++) { //注意下标从1开始
        int t;
        scanf("%d", &t);
        insert(i, i, t); // 构造差分数组
    }
    while(m--) {
        int l, r, c;
        scanf("%d%d%d", &l, &r, &c);
        insert(l, r, c);
    }
    // 计算差分数组的前缀和, 还原原数组
    for(int i = 1; i <= n; i++) {
        a[i] += a[i - 1];
        printf("%d ", a[i]);
    }
    return 0;
    }
```

### 二维差分
即差分矩阵

对于矩阵`a`，存在如下一个矩阵`b`

b11 ，b12，b13，b14，…，b1n

b21，b22，b23，b24，…， b2n

…

…

bm1，bm2，bm3，bm4，…，bmn

使得aij = 矩阵`b`中`[i, j]`位置的左上角的所有数的和

称矩阵`b`为矩阵`a`的差分矩阵。

同样的，如果期望对矩阵`a`中左上角为`[x1, y1]`，右下角为`[x2, y2]`的区域内的全部元素，都加一个常数`C`，则可以转化为对其差分矩阵`b`的操作。

先对`b`中`[x1, y1]`位置上的元素加`C`，这样以来，`a`中`[x1, y1]`这个点的右下角区域内的所有数都加上了`C`，但是这样就对`[x2, y2]`之后的区域也都加了`C`。我们对`[x2, y2]`之外的区域需要保持值不变，所以需要进行减法。对bx2+1,y1 减掉`C`，这样下图红色区域都被减了`C`，再对bx1,y2+1减掉`C`，这样下图蓝色区域都被减了`C`，而红色区域和蓝色区域有重叠，重叠的区域被减了2次`C`，所以要再加回一个`C`，即对bx2+1,y2+1 加上一个`C`。这样，就完成了对`[x1, y1]`，`[x2, y2]`区域内的所有数（下图绿色区域），都加上常数`C`。

![](https://pic4.zhimg.com/80/v2-9208bccf070eb29298b66f1e917670bb.png)
![](https://pic4.zhimg.com/80/v2-99a8e334e3a0a9a058f42b43af5a7a92.png)

总结起来，对原矩阵`a`，在`[x1, y1]`到`[x2, y2]`区域内的全部元素加`C`，可以转换为对其差分矩阵`b`做如下操作

*   bx1,y1 + C
*   bx1,y2+1 - C
*   bx2+1,y - C
*   bx2+1,y2+1 + C

简单记忆为：对`b`的`[x1, y1]`加`C`，对`[x2, y2]`这个点，分别取`x2 + 1`，`y2 + 1`（另一个轴则取`y1`和`x1`），减`C`，然后对`[x2 + 1, y2 + 1]`加`C`

构造矩阵`b`，采用与上面相同的方式，先假设矩阵`a`和矩阵`b`的元素全都为0，此时矩阵`b`是矩阵`a`的差分矩阵，依次进行插入操作即可。

即对矩阵`a`的`[1,1]`到`[1,1]`，加`a[1][1]`，对`[1,2]`到`[1,2]`，加`a[1][2]`，…，如此即可构造出矩阵`b`

[AcWing 798. 差分矩阵](https://www.acwing.com/problem/content/description/800/)
```c++
// C++
#include<iostream>
using namespace std;
const int N = 1010;
int a[N][N];
int n, m, q;

void insert(int x1, int y1, int x2, int y2, int c) {
    a[x1][y1] += c;
    a[x2 + 1][y1] -= c;
    a[x1][y2 + 1] -= c;
    a[x2 + 1][y2 + 1] += c;
}

int main() {
    scanf("%d%d%d", &n, &m, &q);
    for(int i = 1; i<= n; i++) {
        for(int j = 1; j<= m; j++) {
            int t;
            scanf("%d", &t);
            insert(i, j, i, j, t);
        }
    }
    while(q--) {
        int x1, y1, x2, y2, c;
        scanf("%d%d%d%d%d", &x1, &y1, &x2, &y2, &c);
        insert(x1, y1, x2, y2, c);
    }
    // 将差分矩阵还原成前缀和
    for(int i = 1; i <= n; i++) {
        for(int j = 1; j <= m; j++) {
            a[i][j] += a[i - 1][j] + a[i][j - 1] - a[i - 1][j - 1];
            printf("%d ", a[i][j]);
        }
        printf("\n");
    }
}
```

## 前缀和&差分 小结

*   **前缀和**是用来：求任意区间的所有数的和，时间复杂度O(1)

*   **差分**是用来：对任意区间内的所有数加上一个常数，时间复杂度O(1)

*   **前缀和**与**差分**互为**逆运算**

*   前缀和，差分的题目，**数组下标从1开始取**，可以避免对边界特殊处理。

下面称S为a的前缀和数组（矩阵），或者称a为S的差分数组（矩阵）。

#### 一维

**前缀和** Si = Si-1 + ai，数组a任意区间`[l, r]`的和等于 Sr - Sl-1

**差分** ai = Si - Si-1 ，但实际不会这样构造差分数组，直接定义一个函数 `insert(int l, int r, int c)`，表示对`S`数组的`[l, r]`区间内的所有数加`c`。初始时，假想`S`数组和`a`数组全为0，对`i` = 1~n。每次调用`insert(i, i, S[i])`，即完成对差分数组`a`的构造。其中`insert`函数定义如下

```c
void insert(int l, int r, int c) {
    // 对前缀和数组S的[l, r]区间的所有元素加上一个常数C, 只需要对S的差分数组a, 对a[l]加C, 对a[r + 1]减C
    a[l] += c;
    a[r + 1] -= c;
}

```

#### 二维

**前缀和** Si,j = Si-1,j + Si,j-1 - Si-1,j-1 + ai,j，矩阵a任意区间`[x1, y1]`到`[x2, y2]`的所有元素的和等于Sx2,y2 - Sx1-1,y2 - Sx2,y1-1 + Sx1-1,y1-1

简单记忆为，`[x2, y2]`的前缀和，减去，取 `x2`，`y2`（另一个轴取`y1 - 1`，`x1 - 1`）的前缀和，由于有重叠部分被减了2次，所以再加上`[x1 - 1, y1 - 1]`的前缀和

**差分** ai,j ，这里也和一维差分一样的构造方式。直接定义一个函数`insert(int x1, int y1, int x2, int y2, int c)`。初始时，假想`S`矩阵和`a`矩阵全为0，对于每个点`[i, j]`，每次调用`insert(i, j, i, j, S[i][j])`，即完成对差分矩阵`a`的构造。其中`insert`函数定义如下

```c
void insert(int x1, int y1, int x2, int y2, int c) {
    a[x1][y1] += c;
    a[x2 + 1][y1] -= c;
    a[x1][y2 + 1] -= c;
    a[x2 + 1][y2 + 1] += c;
}
```