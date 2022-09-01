---
title: Work with R
author: Zhuopie
date: 2022-09-01
category: Jekyll
layout: post
---

**1. 函数attach、detach、wih**

和stata相比，R使用上面的函数就可以实现对某个数据框的处理；stata无法同时存储多个待处理的数据集，只能通过同时运行多个stata程序来实现

在with中，使用特殊赋值符号<<-即可将复制对象保存在with以外的全局环境中

**2. 数据框**

数据框是最常见的数据形式，也是stata的数据展示形式，可以通过以下方式创建

```yaml
mydata <- data.frame(col1,col2,col3,...)
```


实例标识符（case identifier）看通过row.names指定

```yaml
mydata <- data.frame(col1,col2,col3,.... row.names=XX)
```

