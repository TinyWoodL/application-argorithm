# 一致性哈希

[TOC]

## 讲讲遇到的问题

### Redis 集群
我们为了保证 Redis 的高可用，不仅搭建 Redis 的集群，实现数据的读写分离，对单表数据量过大的情况，还进行分表。

假设一个网站，使用 Redis 存储图片资源，key 为图片名称，value 为图片的实际服务器地址，我们需要根据文件名查找图片所在的服务器，则我们可以进行分表，如下图所示：

<img src="https://github.com/TinyWoodL/application-argorithm/blob/master/assets/redis-1.jpg?raw=true">

这时如果用户想获取一张名为 a.png 的图片，由于不确定在哪一台 Redis 服务器上，需要对每个都遍历。这显然是不可取的方法。更好的方式是通过 Hash，将每个资源定位到特定的服务器上，如下图所示：

<img src="https://github.com/TinyWoodL/application-argorithm/blob/master/assets/redis-2.jpg?raw=true">

假设有四台服务器，此时通过公式 hash(a,png) % 4 可以定位到第二台服务器，避免了遍历。

### Hash 的问题

前面的 hash 算法存在缺陷：当服务器的数量变化的时候，所有的缓存位置都要改变。即当增加一台服务器时，公式变成了 hash(a.png) % 5，此时原来的缓存都是失效的，需要对数据重新做缓存。同样当一台服务器失效后，产生的后果也是一样的。

## 什么是一致性哈希

一致性哈希对 2^32 取模，即将整个 hash 空间构成一个虚拟的圆环，如下图所示：

<img src="https://github.com/TinyWoodL/application-argorithm/blob/master/assets/hash-1.jpg?raw=true">
 
这样我们对每个缓存服务器使用 hash 进行一个哈希（如使用ip或者主机名），最后所有的服务器都分布在环上。
这样，我们只要使用相同的 hash 算法对数据的 key 进行计算，得到此数据在环上的位置，从此位置沿环顺时针遇到的第一台服务器就是定位的服务器。寻址过程如下图所示：

<img src="https://github.com/TinyWoodL/application-argorithm/blob/master/assets/hash-3.jpg?raw=true">

根据算法，此时 ObjectA、B、C、D都被指向到了对应的服务器，不必再做遍历寻址

**Q1**：在一致性哈希下， 增加、减少新的服务器，会如何处理

**Q2**: 如何实现较少服务器的时候，服务器在环上的均匀分布

>[摘自https://zhuanlan.zhihu.com/p/34985026](https://zhuanlan.zhihu.com/p/34985026)

## 哈希算法的好坏判断：

对于动态变化的 Cache 环境，对于判断哈希算法好坏有4个定义：

* 平衡性（balance）：指哈希的结果要能够尽可能的分布到所有的缓冲中去，这样可以使得所有的缓冲空间都得到利用。
* 单调性（Monotonicity）：对新增加的缓冲内容，不会影响原有的缓冲。
* 分散性（Spread）：尽量避免相同的内容被不同的终端映射到不同的缓冲区中
* 负载（load）：对于一个特定的缓冲区而言，也可能被不同的用户映射为不同的内容。这样的情况也要努力避免

## 实现代码

