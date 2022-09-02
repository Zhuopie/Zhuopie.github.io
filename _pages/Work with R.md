---
title: Work with R
author: Zhuopie
date: 2022-09-01
category: Jekyll
layout: post
---



#### **内含公式，请再刷新一次**

**0.1 安装和加载R的包**

```
install.packages()

library()
```

**0.2 打开项目路径**

```
getwd()
```

**1.1 函数attach、detach、wih**

和stata相比，R使用上面的函数就可以实现对某个数据框的处理；stata无法同时存储多个待处理的数据集，只能通过同时运行多个stata程序来实现

在with中，使用特殊赋值符号<<-即可将复制对象保存在with以外的全局环境中

**1.2 数据框**

数据框是最常见的数据形式，也是stata的数据展示形式，可以通过以下方式创建

```
mydata <- data.frame(col1,col2,col3,...)
```


实例标识符（case identifier）看通过row.names指定

```
mydata <- data.frame(col1,col2,col3,.... row.names=XX)
```

**1.3 手动修改数据**

在定义一个数据集（例如mydata）后，如果想要修改该数据集，可以使用

```
mydata <- eedit(mydata)

fix(mydata)
```

用read.xlsx函数可以将excel中的数据导入到R中

```
path <- "C:/Users/lzp57/Desktop/快看_20220816.xlsx"
#路径需要用/

install.packages("readxl")
library(readxl)

kuaikan <- read_excel(path,sheet = 1)
save.image("C:/Users/lzp57/Desktop/EmpiricalIO/kuaikan_test.RData")
#保存一个workspace 默认的文件格式为.RData
```

**1.4 清理数据Example**

```
str(kuaikan)
summary(kuaikan)

kuaikan$score <- as.numeric(kuaikan$score)
#“打分”转为数值型
kuaikan$sexstr <- as.factor(kuaikan$sexstr)
#“性别”转为因子型
kuaikan$itemname <- as.factor(kuaikan$itemname)
#“漫画名称”转为因子型，表示有N本不同的漫画
kuaikan$name <- as.factor(kuaikan$name)
#“用户ID”转为因子型，表示有N个不同的打分人

kuaikan$createtime <- as.numeric(kuaikan$createtime)
#先把十三位时间从字符型转为数字型
kuaikan$createtime=as.POSIXct((kuaikan$createtime/1000), origin="1970-01-01",tz="Asia/Shanghai")
#再转为时间，格式类似于2022-08-04 11:41:28

kuaikan$date <- format(kuaikan$createtime, "%Y/%m/%d")
#生成新变量，只提取年月日

install.packages("readr")
#提取数字的包
kuaikan$readmsg <- parse_number(kuaikan$readmsg)

kuaikan$createtimestr <- NULL
#删除多余的变量
```

#### **2.1 实战项目1：模拟数据并估计离散选择模型**

根据以下模型，首先模拟数据，然后估计出提前设定的参数
$$
y_{i k}=1\left\{k=\operatorname{argmax}_{k=1,2} \beta x_k+\varepsilon_{i k}\right\}
$$
其中，$\varepsilon_{ik}$ 服从第一类极值分布，且为独立同分布；$\beta=0.2$，$x_{1}=0$，$x_2=1$ ; 假定$i=1000$

【注释：上述模型指的是$i\times k$ (具体地，$i\times 2$)维度的数据，对于每一个个体$i$，抽取2个随机的$\varepsilon$以后，比较$\beta x_1+\varepsilon_{i1}$和$\beta x_2+\varepsilon_{i2}$的值，将较大的结果赋值为1，否则赋值为0

在离散选择模型的框架下，该模型可以理解为：参数$k$表示两种不同的商品，变量$x$为商品的某种特征，取值为1或0，参数$\beta$为消费者对于该特征的偏好特征，由于该参数没有下标，其中暗含的假设是所有消费者对该特征的评价一致，也可以理解为是所有消费者对于该特征的平均偏好；潜变量$\beta x+\varepsilon$意味着消费者对该商品的总体偏好程度，用$\varepsilon$来刻画消费者个人的特异性偏好

那么，若$y_{i1}=1$，则消费者偏好商品1，否则消费者偏好商品2，消费者只能偏好1和2中的某一个】

Step 1：首先完成以下的数据构造

```
## # A tibble: 2,000 × 3
##        i     k     x
##    <int> <int> <dbl>
##  1     1     1     0
##  2     1     2     1
##  3     2     1     0
##  4     2     2     1
##  5     3     1     0
##  6     3     2     1
##  7     4     1     0
##  8     4     2     1
##  9     5     1     0
## 10     5     2     1
## # … with 1,990 more rows
## # ℹ Use `print(n = ...)` to see more rows
```

Step 2：随机生成第一类极值分布的数据，随机种子为1，完成以下的数据构造

```
## # A tibble: 2,000 × 4
##        i     k     x       e
##    <int> <int> <dbl>   <dbl>
##  1     1     1     0  0.281 
##  2     1     2     1 -0.167 
##  3     2     1     0  1.93  
##  4     2     2     1  1.97  
##  5     3     1     0  0.830 
##  6     3     2     1 -1.06  
##  7     4     1     0 -0.207 
##  8     4     2     1  0.617 
##  9     5     1     0  0.0444
## 10     5     2     1  1.92  
## # … with 1,990 more rows
## # ℹ Use `print(n = ...)` to see more rows
```

Step 3：计算潜变量的值，形成以下的数据构造

```
## # A tibble: 2,000 × 5
##        i     k     x       e  latent
##    <int> <int> <dbl>   <dbl>   <dbl>
##  1     1     1     0  0.281   0.281 
##  2     1     2     1 -0.167   0.0331
##  3     2     1     0  1.93    1.93  
##  4     2     2     1  1.97    2.17  
##  5     3     1     0  0.830   0.830 
##  6     3     2     1 -1.06   -0.863 
##  7     4     1     0 -0.207  -0.207 
##  8     4     2     1  0.617   0.817 
##  9     5     1     0  0.0444  0.0444
## 10     5     2     1  1.92    2.12  
## # … with 1,990 more rows
## # ℹ Use `print(n = ...)` to see more rows
```

Step 4：得到$y$的值，形成以下的数据构造

```
## # A tibble: 2,000 × 6
##        i     k     x       e  latent     y
##    <int> <int> <dbl>   <dbl>   <dbl> <dbl>
##  1     1     1     0  0.281   0.281      1
##  2     1     2     1 -0.167   0.0331     0
##  3     2     1     0  1.93    1.93       0
##  4     2     2     1  1.97    2.17       1
##  5     3     1     0  0.830   0.830      1
##  6     3     2     1 -1.06   -0.863      0
##  7     4     1     0 -0.207  -0.207      0
##  8     4     2     1  0.617   0.817      1
##  9     5     1     0  0.0444  0.0444     0
## 10     5     2     1  1.92    2.12       1
## # … with 1,990 more rows
## # ℹ Use `print(n = ...)` to see more rows
```

由于设定了随机扰动项服从第一类极值分布，且为独立同分布，可以得到，在给定参数$\beta$的值后，$y_{ik}=1$的概率为
$$
p_{i k}(\beta)=\frac{\exp \left(\beta x_k\right)}{\exp \left(\beta x_1\right)+\exp \left(\beta x_2\right)}
$$
由此构造似然函数，在已知条件下，观察到该样本的似然值为（这里需要注意，只有$y=1$的个体才会被观察到，因此$y_{i1}$意味着第$i$个消费者选择了第一种产品，$y_{j2}$意味着第$j$个消费者选择了第二种产品，再插一句，在实际的需求函数估计中，我们只能看到整体的市场份额，我们现在正在处理的模型属于中间过程，因为我们无法获得每一个消费者选择的数据）
$$
L(\beta)=\prod_{i=1}^{1000} p_{i 1}(\beta)^{y_{i 1}}\left[1-p_{i 1}(\beta)\right]^{1-y_{i 1}}
$$
上面这个式子意味着，对于样本中的1000个个体，每个人的选择都是独立的，因此前面使用了连乘来表示联合概率，针对每个人的选择，如果个体$i$选择了产品1，则概率为$p_{i1}$，如果个体$i$选择了产品2，则概率为$1-p_{i1}$，这里用$p_{i 1}(\beta)^{y_{i 1}}\left[1-p_{i 1}(\beta)\right]^{1-y_{i 1}}$巧妙地同时表示了两种情况，只要知道$y_{ik}$就可以计算出相应的概率，相应的对数似然函数为：
$$
l(\beta)=\sum_{i=1}^{1000}\left\{y_{i 1} \log p_{i 1}(\beta)+\left(1-y_{i 1}\right) \log \left[1-p_{i 1}(\beta)\right\}\right.
$$
Step 4：写一个函数，用来计算给定$\beta$后的似然值，将该函数命名为`loglikelihood_A1`

Step 5： 计算当$\beta=0, 0.1, 0.2, ... , 1$的时候的似然值，使用包`ggplot2`绘图，横轴为$\beta$，纵轴为似然值

Step 6：找到并报告使得似然函数值最大的$\beta$值，使用`optim`函数来得到这一结果，可以使用`Brent`方法在-1到1区间来寻找（最优的）参数

```
## $par
## [1] 0.2371046
## 
## $value
## [1] -0.6861689
## 
## $counts
## function gradient 
##       NA       NA 
## 
## $convergence
## [1] 0
## 
## $message
## NULL
```

 

