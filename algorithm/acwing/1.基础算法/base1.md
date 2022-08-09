#! https://zhuanlan.zhihu.com/p/551137643
- [基础知识Part1](#基础知识part1)
  - [快速排序](#快速排序)
    - [基本思路](#基本思路)
    - [AcWing 785. 快速排序](#acwing-785-快速排序)
    - [AcWing 786. 第k个数](#acwing-786-第k个数)
  - [归并排序](#归并排序)
    - [AcWing 787. 归并排序](#acwing-787-归并排序)
    - [AcWing 788. 逆序对的数量](#acwing-788-逆序对的数量)
  - [整数二分](#整数二分)
    - [AcWing 789. 数的范围](#acwing-789-数的范围)
  - [浮点数二分](#浮点数二分)
    - [AcWing 790. 数的三次方根](#acwing-790-数的三次方根)

# 基础知识Part1
本节主要说了：
- 快速排序、归并排序
- 整数二分、浮点数二分

## 快速排序
`quick_sort(int q[], int l, int r)`
`q`是待排序数组，`l`是待排序区间的左边界，`r`是右边界

### 基本思路

快排属于分治算法，分治算法都有三步：
1. 分成子问题
2. 递归处理子问题
3. 子问题合并

**算法步骤：**
1. 选取一个基准值`x`
可以取左边界的值`q[l]`，或右边界的值`q[r]`，或者中间位置的值`q[l + r >> 1]`

2. 根据基准值，调整区间，使得左半边区间的值全都`≤x`，右半边区间的值全都`≥x`
采用双指针，左指针`i`从左边界`l`开始，往右扫描，右指针`j`从右边界r开始，往左扫描。
当满足条件`q[i] < x`时，`i`右移；直到不满足条件时，`i`停下；开始移动`j`
当满足条件`q[j] > x`时，`j`左移；直到不满足条件时，`j`停下；交换`q[i]`和`q[j]`；
将`i`右移一位，`j`左移一位。
重复上面的操作，直到`i`和`j`相遇。此时左半区间的数都满足`≤x`，且左半区间的最后一个数的下标为`j`，右半区间的数都满足`≥x`，且右半区间的第一个数的下标为`i`。`i`和`j`之间的关系为：`i = j + 1`或`i = j`

3. 对左右两边的区间，做递归操作
递归操作`[l, j]`，`[j + 1, r]`区间，或者`[l, i - 1]`，`[i, r]`区间即可


以下搬运自[博客](https://www.acwing.com/solution/content/16777/)
**边界情况分析**
**分析**
快排属于**分治算法**，最怕的就是 n分成0和n，或 n分成n和0,这会造成**无限划分**

1.以`j`为划分时，`x`不能选`q[r]` (若以`i`为划分,则x不能选`q[l]`)

假设 `x = q[r]`

关键句子`quick_sort(q, l, j)`, `quick_sort(q, j + 1, r)`;

由于`j`的最小值是`l`,所以`q[j+1..r]`不会造成无限划分

但`q[l..j]`(即`quick_sort(q, l, j`))却可能造成无限划分，因为`j`可能为`r`

举例来说，若`x`选为`q[r]`，数组中`q[l..r-1] < x`,

那么这一轮循环结束时`i = r`, `j = r`，显然会造成无限划分

2.`do i++; while(q[i] < x)`和`do j--; while(q[j] > x)`不能用`q[i] <= x 和 q[j] >= x`

假设`q[l..r]`全相等

则执行完`do i++; while(q[i] <= x)`;之后，`i`会自增到`r+1`

然后继续执行`q[i] <= x `判断条件，造成数组下标越界(但这貌似不会报错)

并且如果之后的`q[i] <= x `(此时`i > r`) 条件也不幸成立，

就会造成一直循环下去(亲身实验)，造成内存超限(Memory Limit Exceeded)

3.`if(i < j) swap(q[i], q[j])`能否使用 `i <= j`

可以使用`if(i <= j) swap(q[i], q[j])`;

因为 `i = j` 时，交换一下`q[i],q[j]` 无影响，因为马上就会跳出循环了

4.最后一句能否改用`quick_sort(q, l, j-1), quick_sort(q, j, r)`作为划分(用i做划分时也是同样的道理,)

不能

根据之前的证明，最后一轮循环可以得到这些结论

`j <= i` 和 `q[l..i-1] <= x, q[i] >= x` 和 `q[j+1..r] >= x, q[j] <= x`

所以，`q[l..j-1] <= x` 是显然成立的，

但`quick_sort(q, j, r)`中的`q[j]` 却是 `q[j] <= x`，这不符合快排的要求

另外一点，注意`quick_sort(q, l, j-1)`, `quick_sort(q, j, r)`可能会造成无线划分

当`x`选为`q[l]`时会造成无限划分，报错为(MLE),

如果手动改为` x = q[r]`,可以避免无限划分

但是上面所说的`q[j] <= x` 的问题依然不能解决，这会造成 WA (Wrong Answer)

5.j的取值范围为`[l..r-1]`

证明:

假设 `j `最终的值为` r `,说明只有一轮循环(两轮的话 j 至少会自减两次)

说明`q[r] <= x` (因为要跳出do-while循环)

说明 `i >= r`(while循环的结束条件), `i` 为 `r` 或 `r + 1(`必不可能成立)

说明 `i` 自增到了 `r` , 说明 `q[r] >= x` 和 `q[l..r-1] < x`,

得出 `q[r] = x` 和` q[l..r-1] < x `的结论,但这与` x = q[l + r >> 1]`矛盾

反证法得出 `j` < r`

假设 `j` 可能小于` l`说明 `q[l..r] > x `,矛盾

反证法得出 `j >= l`

所以` j`的取值范围为`[l..r-1]`,不会造成无限划分和数组越界


![快速排序](https://pic4.zhimg.com/80/v2-a306279992a37c038c85eb21f756a08a.png)

### [AcWing 785. 快速排序](https://www.acwing.com/problem/content/787/)
```cpp
#include<iostream>
using namespace std;
const int N = 100010;
int n;
int q[N];

void quick_sort(int q[], int l, int r) {
    if(l >= r) return; // 递归退出条件, 不要写成 l == r, 可能会出现 l > r 的情况，可以尝试用例[1,2]
    int x = q[l + r >> 1], i = l - 1, j = r + 1; // 这里 i 置为 l - 1, j 置为 r + 1, 是因为下面更新i, j 时采用了do while循环,
    while(i < j) { // 这里不要写成 i <= j
        do i++; while(q[i] < x);// 不能写为 <= x , 那样写 i 可能会越界, 考虑 [1,1,1]。 
        // 因为基准值x是数组中的一个数，i从左往右移动的过程中，一定会遇到这个数x，此时不满足小于条件, i 一定会停下，也就变相保证了 i 不会越界。
        do j--; while(q[j] > x);// 不能写为 >= x , 因为 j 可能会越界, 原因同上
        if(i < j) swap(q[i], q[j]); // 若 i 和 j 还未相遇, 则交换2个数
    }
    quick_sort(q, l, j);
    quick_sort(q, j + 1, r);
}

int main() {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d", &q[i]);
    
    quick_sort(q, 0, n - 1);
    for(int i = 0; i < n; i++) printf("%d ", q[i]);
    return  0;
}
```

### [AcWing 786. 第k个数](https://www.acwing.com/problem/content/788/)
借用快排的思路，写出**快速选择算法**（找分界点然后切分数组，缩小查找范围），时间复杂度 O(n)。
时间复杂度可以这样想：第一层时，需要处理`n`次，然后会期望将数组切分成左右两半边，然后会选择其中一半区间，我们每次切分都期望将区间缩小为一半，所以第二层，需要处理`n/2`次，同理，第三层需要处理`n/4`。所以总的运算次数就是：
`n + n/2 + n/4 + ....` 这个结果是 `<= 2n`，所以总的时间复杂度就是 O(n)

```cpp
#include<iostream>
using namespace std;

const int N = 1e5 +10;
int n, k;
int q[N];

// 选取[l, r]区间内数组q第k小的数
int quick_select(int q[], int l, int r, int k) {
    if(l == r) return q[l]; // 找到答案
    int x = q[l + r >> 1], i = l - 1, j = r + 1;
    while(i < j) {
        while(q[++i] < x);
        while(q[--j] > x);
        if(i < j) swap(q[i], q[j]);
    }
    int left = j - l + 1;
    if(k <= left) return quick_select(q, l, j, k);
    else return quick_select(q, j + 1, r, k - left);
}

int main() {
    scanf("%d%d", &n, &k);
    for(int i = 0; i < n; i++) scanf("%d", &q[i]);
    
    printf("%d", quick_select(q, 0, n - 1, k));
    return 0;
}
```

## 归并排序
`merge_sort(int q[], int l, int r)`

*   基本思路

    1.  确定分界点，一般是中间位置

    2.  从分界点将数组切成两半，对左右两部分做递归排序

    3.  将左右两部分区间合并成一个区间（将2个有序数组，合并成1个有序数组，使用双指针即可）

### [AcWing 787. 归并排序](https://www.acwing.com/problem/content/789/)

```c++
#include<iostream>
using namespace std;
const int N = 1e6 + 10;
int n;
int q[N], tmp[N];

void merge_sort(int q[], int l, int r) {
    if(l >= r) return;
    int mid = l + r >> 1;
    merge_sort(q, l, mid);
    merge_sort(q, mid + 1, r);
    // 合并
    int i = l, j = mid + 1, k = 0;
    while(i <= mid && j <= r) {
        if(q[i] <= q[j]) tmp[k++] = q[i++];
        else tmp[k++] = q[j++];
    }
    while(i <= mid) tmp[k++] = q[i++];
    while(j <= r) tmp[k++] = q[j++];
    for(i = l, j = 0; i <= r; i++, j++) q[i] = tmp[j];
}

int main() {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d", &q[i]);
    merge_sort(q, 0, n - 1);
    for(int i = 0; i < n; i++) printf("%d ", q[i]);
}
```

### [AcWing 788. 逆序对的数量](https://www.acwing.com/problem/content/790/)
```cpp
#include<iostream>
using namespace std;

typedef long long LL;
const int N = 1e5 + 10;
int n;
int q[N], tmp[N];

// 返回区间[l, r]中的逆序对的数量
LL merge_sort(int q[], int l, int r) {
    if(l >= r) return 0;
    int mid = l + r >> 1;
    LL cnt = merge_sort(q, l, mid) + merge_sort(q, mid + 1, r); // 计算左右区间内各自的逆序对数量
    // 合并时, 计算左右两个区间中的数组成的逆序对
    int i = l, j = mid + 1, k = 0;
    while(i <= mid && j <= r) {
        if(q[i] <= q[j]) tmp[k++] = q[i++];
        else {
            cnt += mid - i + 1;
            tmp[k++] = q[j++];
        }
    }
    while(i <= mid) tmp[k++] = q[i++];
    while(j <= r) tmp[k++] = q[j++];
    for(int i = l, k = 0; i <= r; i++, k++) q[i] = tmp[k];
    return cnt;
}

int main() {
    scanf("%d", &n);
    for(int i = 0; i < n; i++) scanf("%d", &q[i]);
    LL cnt = merge_sort(q, 0, n - 1);
    printf("%lld", cnt);
    return 0;
}
```

## 整数二分
**二分的本质**

注意：**二分的本质不是单调性**。单调性可以理解为函数单调性，如一个数组是升序排列或降序排列，此时可以用二分来查找某一个数的位置。

有单调性一定可以二分，但没有单调性，也有可能能够二分。

**二分的本质是边界**。假设给定一个区间，如果能够根据某个条件，将区间划分为左右两部分，使得左半边满足这个条件，右半边不满足这个条件（或者反之）。此时就可以用二分来查找左右两部分的边界点。

![二分边界](https://pic4.zhimg.com/80/v2-106cfe66047ea1b295d4853df82be68f.png)

注意左右两半部分的边界不是同一个点，而是相邻的2个点，因为是整数二分（离散的）。上面的2个算法模板，就分别对应了**求左半部分的边界**（上图红色区域最右边的点），和**求右半部分的边界**（上图绿色区域最左边的点）

比如，我们要找上图中左边红色部分的边界点，我们取`mid = l + r >> 1`，判断一下`q[mid]`是否满足条件x，若满足，说明`mid`位置在红色区域内，我们的答案在`mid`右侧（可以取到`mid`），即`[mid, r]`，则此时更新`l = mid`；若`q[mid]`不满足条件x，则说明`mid`位置在右边的绿色区域，我们的答案在`mid`左侧（不能取到`mid`），即`[l, mid - 1]`，此时更新`r = mid - 1`。

注意，当采用`l = mid`和`r = mid - 1`这种更新方式时，计算`mid`时，要加上1（向上取整），即`mid = l + r + 1 >> 1`。否则，在`l = r - 1`时，计算`mid`时若不加1，则`mid = l + r >> 1 = l`，这样更新`l = mid`，就是`l = l`，会导致死循环。所以要向上取整，采用`mid = l + r + 1 >> 1`。

同理，当采用`r = mid` 和 `l = mid + 1`这种更新方式时，计算`mid`时不能加1，在`l = r - 1`时，若计算`mid`时加1，则`mid = l + r + 1 >> 1 = r`，这样更新`r = mid`。就是`r = r`，会导致死循环。

简单的记忆就是，仅当采用`l = mid`这种更新方式时，计算`mid`时需要加1。

### [AcWing 789. 数的范围](https://www.acwing.com/problem/content/791/)
```cpp
#include<iostream>
using namespace std;
const int N = 100010;
int arr[N];
int n,q;

int main() {
    scanf("%d%d", &n, &q);
    for(int i = 0; i < n; i++) scanf("%d", &arr[i]);
    
    while(q--) {
        int k;
        scanf("%d", &k);
        //需要找到>=x的第一个数，另一个需要找到<=x的最后一个数
        int l = 0, r = n - 1;
        while(l < r) {
            int mid = l + r >> 1;
            if(arr[mid] >= k) r = mid; //左端点mid>=k,
            else l = mid + 1;
        }
        if(arr[l] != k) printf("-1 -1\n");
        else {
            printf("%d ", l);
            l = 0, r = n - 1;
            while(l < r) {
                int mid = l + r + 1 >> 1;
                if(arr[mid] <= k) l = mid;
                else r = mid - 1;
            }
            printf("%d\n", l);
        }
    }
}
```

## 浮点数二分
相比**整数二分**，**浮点数二分**无需考虑边界问题，比较简单。

当二分的区间足够小时，可以认为已经找到了答案，如当`r - l < 1e-6` ，停止二分。

或者直接迭代一定的次数，比如循环100次后停止二分。

### [AcWing 790. 数的三次方根](https://www.acwing.com/problem/content/792/)
```cpp
#include<iostream>
using namespace std;
int main() {
    double n;
    scanf("%lf", &n);
    double l = -10000, r = 10000;
    
    while(r - l > 1e-8) {
        double mid = (l + r) / 2;
        if(mid * mid * mid >= n) r = mid;
        else l = mid;
    }
    printf("%.6f", l);
}
```