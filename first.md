#! https://zhuanlan.zhihu.com/p/426820287
# 一级标题

## 二级标题

### 三级标题

每写完一个段落要隔一行空行.

就像这样, 隔了一行空行.

---

分割线

**重点加粗**

*斜体*

~~删除~~两个~~之间
~~删除线~~


---
P\left(w_{1}, w_{2}, \ldots, w_{m}\right)=P\left(w_{1}\right) P\left(w_{2} \mid w_{1}\right) P\left(w_{3} \mid w_{1}, w_{2}\right) \cdots P\left(w_{m} \mid w_{1}, \ldots, w_{m-1}\right)
列表:

* 无序列表
  * 嵌套无序列表
  * 嵌套无序列表
* 无序列表
* 无序列表

1. 有序列表 1
   1. 嵌套有序列表 1
   2. 嵌套有序列表 2
2. 有序列表 2
3. 有序列表 3

---

引用文本:

> 引用别人说的话
> 就这样写
> By. OrangeX4

---

这是 `行内代码` 语法.

代码块语法:

''' python
print("Hello, World!")
'''

请将 ' 替换成 `.

```python
print("Hello, World!")
usr=input()
```

---


---

表格:

|   表头    | 表头  |
| :-------: | :---: |
| 内容(1,1) | 内容  |
|   内容    | 内容  |

---

如果想换行应该这样在后面加两个空格  
继续

Markdown Preview Enhanced 拓展功能:
任务列表:

- [x] 已经完成的事 1
- [x] 已经完成的事 2
- [x] 已经完成的事 3
- [ ] 仍未完成的事 4
- [ ] 仍未完成的事 5

==高亮== 


<font color=yellow>我是红色</font>

<font face="黑体" color=green size=5>我是黑体，绿色，尺寸为5</font>

注释:

<!-- 你看不见我 -->
<!--> 这个符号表示注释 <!-->

==hight 1==

行内公式: 

单位圆 $x^2+y^2=1$

公式块(大括号括起来居中):

$$
\begin{cases}
x=\rho\cos\theta \\
y=\rho\sin\theta \\
\end{cases} $$

上标 $x^2 + y^{12} = 1$

下标 $x_1 + y_{12} = 1$

较小的行内行分数 $\frac{1}{2}$

展示型的分式 $\displaystyle\frac{x+1}{x-1}$

开平方 $\sqrt{2}$

开 $n$ 次方 $\sqrt[n]{2}$
$\sqrt[n]{2}$


数学公式中的空格和换行都会在编译时被忽略.

输入空格:
紧贴 $a\!b$

没有空格 $ab$

小空格 $a\,b$

中等空格 $a\;b$

大空格 $a\ b$

quad 空格 $a\quad b$

两个 quad 空格 $a\qquad b$

累加 $\sum_{k=1}^n\frac{1}{k}  \quad  \displaystyle\sum_{k=1}^n\frac{1}{k}$

累乘 $\prod_{k=1}^n\frac{1}{k}  \quad  \displaystyle\prod_{k=1}^n\frac{1}{k}$

积分 $\displaystyle \int_0^1x{\rm d}x  \quad  \iint_{D_{xy}}  \quad  \iiint_{\Omega_{xyz}}$

圆括号 $\displaystyle \left(\sum_{k=1}^{n}\frac{1}{k} \right)^2$

方括号 $\displaystyle \left[\sum_{k=1}^{n}\frac{1}{k} \right]^2$

花括号 $\displaystyle \left\{\sum_{k=1}^{n}\frac{1}{k} \right\}^2$

尖括号 $\displaystyle \left\langle\sum_{k=1}^{n}\frac{1}{k} \right\rangle^2$

居中:

$$
\begin{aligned}
y &=(x+5)^2-(x+1)^2 \\
&=(x^2+10x+25)-(x^2+2x+1) \\
&=8x+24 \\
\end{aligned}
$$

左对齐:

$
\begin{aligned}
y &=(x+5)^2-(x+1)^2 \\
&=(x^2+10x+25)-(x^2+2x+1) \\
&=8x+24 \\
\end{aligned}
$

$$
\begin{cases}
k_{11}x_1+k_{12}x_2+\cdots+k_{1n}x_n=b_1 \\
k_{21}x_1+k_{22}x_2+\cdots+k_{2n}x_n=b_2 \\
\cdots \\
k_{n1}x_1+k_{n2}x_2+\cdots+k_{nn}x_n=b_n \\
\end{cases}
$$

$$
x+2 \tag{1.2}
$$




由公式 $(1.2)$ 可得到结论

$$
\begin{cases}
  (1+2)/
\end{cases}
$$






### 常用快捷键
|     Key      | Command  |
| :----------: | :------: |
| Ctrl/Cmd + B |   加粗   |
| Ctrl/Cmd + I |   斜体   |
|    ALT+S     |  删除线  |
|    Ctrl+M    | 数学环境 |
Alt+S (on Windows)	Toggle strikethrough1
Ctrl + Shift + ]	Toggle heading (uplevel)
Ctrl + Shift + [	Toggle heading (downlevel)
Ctrl/Cmd + M	Toggle math environment
Alt + C	Check/Uncheck task list item
Ctrl/Cmd + Shift + V	Toggle preview
Ctrl/Cmd + K V	Toggle preview to side

:sweat_smile:
:drooling_face:
:clown_face:

[来看看我贫瘠的仓库罢](https://github.com/vhzy/Notes/blob/main/algorithm/acwing/DynamicProgramming/dp1-%E8%83%8C%E5%8C%85%E9%97%AE%E9%A2%98.md)