# 嵌套集合模型

[TOC]

## 前言

在日常编码中，我们经常遇到处理分层数据的需求。分层数据即分类、组织机构等有层次关系的数据，然而关系型数据库没有层次关系，简单的平面化列表无法表现分层特性。


    1、介绍一直使用的邻接表模型的缺陷和不足
    2、介绍嵌套集合模型
    3、嵌套集合模型的优点和缺陷
    4、总结
    
## 邻接表模型

通常我们使用邻接表模型来模拟层级模型的树结构

```
CREATE TABLE category(
    category_id INT(10) AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    parent_id INT(10) DEFAULT NULL
);
```

如上所示的数据库表，表中的每项包含了指向其父项的指示器，最上层的父项为空。该表可以很明显的父子之间的层级关系，通过指向父项的指示器构建出一个树模型，其图如下所示。

<img src="https://github.com/TinyWoodL/application-argorithm/blob/master/assets/category_tree.png?raw=true">

### 对邻接表的操作

创建层次模型之后，我们就可以进行相关的增删改查操作来满足不同的业务需求，那么对邻接表该如何查询来满足需求？

1、**获得整棵树**

处理分层数据时首要任务通常是获得整棵树。

使用纯 SQL 编码通常是使用自连接，假设实际树结构分四层（如上图），则编码如下：
```
SELECT t1.name AS lev1, t2.name as lev2, t3.name as lev3, t4.name as lev4
    FROM 
    category AS t1
        LEFT JOIN category AS t2 ON t2.parent = t1.category_id
        LEFT JOIN category AS t3 ON t3.parent = t2.category_id
        LEFT JOIN category AS t4 ON t4.parent = t3.category_id
    WHERE t1.name = 'ELECTRONICS';

+-------------+----------------------+--------------+-------+
| lev1        | lev2                 | lev3         | lev4  |
+-------------+----------------------+--------------+-------+
| ELECTRONICS | TELEVISIONS          | TUBE         | NULL  |
| ELECTRONICS | TELEVISIONS          | LCD          | NULL  |
| ELECTRONICS | TELEVISIONS          | PLASMA       | NULL  |
| ELECTRONICS | PORTABLE ELECTRONICS | MP3 PLAYERS  | FLASH |
| ELECTRONICS | PORTABLE ELECTRONICS | CD PLAYERS   | NULL  |
| ELECTRONICS | PORTABLE ELECTRONICS | 2 WAY RADIOS | NULL  |
+-------------+----------------------+--------------+-------+
```

很明显，这个编码不仅复杂，而且受到树的层级限制，每增加一层就要修改 SQL，当层级很多时 SQL 也会变的很庞大.

目前实际处理的时候是将所有的分类检索出来，再通过规则生成正确的树结构。

2、**获取单一路径**

检索单一路径见展示分类面包屑层级，以定位当前用户的层级。

同样使用 SQL 的自连接
```
SELECT t1.name AS lev1, t2.name as lev2, t3.name as lev3, t4.name as lev4
    FROM category AS t1
        LEFT JOIN category AS t2 ON t2.parent = t1.category_id
        LEFT JOIN category AS t3 ON t3.parent = t2.category_id
        LEFT JOIN category AS t4 ON t4.parent = t3.category_id
    WHERE t1.name = 'ELECTRONICS' AND t4.name = 'FLASH';

+-------------+----------------------+-------------+-------+
| lev1        | lev2                 | lev3        | lev4  |
+-------------+----------------------+-------------+-------+
| ELECTRONICS | PORTABLE ELECTRONICS | MP3 PLAYERS | FLASH |
+-------------+----------------------+-------------+-------+
```

目前实际处理的方式是先获取整个树，再在代码中筛选出目标分类的面包屑。

3、**获取叶子节点**

见于要操作底层节点的业务，这个业务在 SQL 上是比较简单的：

```
SELECT t1.name FROM category AS t1 LEFT JOIN category as t2
    ON t1.category_id = t2.parent
        WHERE t2.category_id IS NULL;
```

### 邻接表的缺陷

通过上面的介绍，我们可以看到邻接表存在着部分问题：

    1、获取整棵树通过 SQL 十分复杂且依赖于分类的层级。
    2、获取单一路径 SQL 同样依赖与层级。

## 嵌套层级模型

嵌套模型不视分类为树的结构，而是将他视为集合的模型，不同的层级则是集合的嵌套。

<img src="https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/NestedSetModel.svg/800px-NestedSetModel.svg.png">

>[wiki](https://en.wikipedia.org/wiki/Nested_set_model#Example)

在该模型中嵌套关系使用节点的左值和右值来替代：
```
CREATE TABLE nested_category (
    category_id INT AUTO_INCREMENT PRIMARY KEY,
    name VARCHAR(20) NOT NULL,
    lft INT NOT NULL,
    rgt INT NOT NULL
);
```

### 对嵌套模型数据查询

在嵌套模型中对整体树的查询和单一路径就变的简单了。

通过自连接把父节点连接到子节点上来检索整树:
```
SELECT node.name
    FROM
    nested_category AS node,
    nested_category AS parent
        WHERE node.lft BETWEEN parent.lft 
            AND parent.rgt
            AND parent.name = 'ELECTRONICS'
    ORDER BY node.lft;

```

检索出叶子节点，我们只要查找满足rgt=lft+1的节点:
```
SELECT name FROM nested_category
    WHERE rgt = lft + 1;
```

检索单一路径:
```
SELECT parent.name
    FROM 
    nested_category AS node,
    nested_category AS parent
        WHERE node.lft BETWEEN parent.lft 
            AND parent.rgt
            AND node.name = 'FLASH'
    ORDER BY parent.lft;
```

**Q1**:如何检索节点深度，子树深度，节点的直接子节点。

通过上面的查询我们会发现使用 SQL 编写查询**不再和层级数量相关**，这意味着使用嵌套模型可以创建不限层级的分类。

### 新增和移除节点的问题

1、**新增节点**：

因为使用了左值和右值，很明显，新增节点的时候不再是简单的插入一条数据，而且需要调整其他节点的左右值。

这里不再给出增加的 SQL 操作。

**Q2**：虽然嵌套模型优化了查询操作，但是却导致新增操作更加复杂。邻接表是插入简单但查询复杂，这两个该如何取舍？扩展到其他业务，当多种方案各有优劣的时候如何取舍？

2、**删除节点**：

删除叶子节点和新增一样，也要处理左右值的更新。

删除中间节点的时候，要考虑遗留子节点的问题。

## 总结

使用嵌套模型可以帮助我们解决一些问题：
    
    1、查询更方便
    2、层级不限制深度
    
但是又会带来新的问题：

    1、导致插入困难
    2、删除节点更加麻烦
    3、不允许多个父类
    4、~~~
    
**Q3**:尝试实现一个新的categoryService,使用嵌套模型去完善add, getTree, findCategoryBreadcrumbs, delete等方法。