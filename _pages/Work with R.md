---
title: Work with R
author: Zhuopie
date: 2022-09-01
category: Jekyll
layout: post
---

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

**1.4 查看数据格式**

```
str(kuaikan)
summary(kuaikan)

kuaikan$score <- as.numeric(kuaikan$score)
#“打分”转为数值型
kuaikan$sexstr <- as.factor(kuaikan$sexstr)
#“性别”转为因子型
> kuaikan$itemname <- as.factor(kuaikan$itemname)
#“漫画名称”转为因子型，表示有N本不同的漫画
kuaikan$name <- as.factor(kuaikan$name)
#“用户ID”转为因子型，表示有N个不同的打分人

kuaikan$createtime <- as.numeric(kuaikan$createtime)
#先把十三位时间从字符型转为数字型
kuaikan$createtime=as.POSIXct((kuaikan$createtime/1000), origin="1970-01-01",tz="Asia/Shanghai")
#再转为时间，格式类似于2022-08-04 11:41:28
```

