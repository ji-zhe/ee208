# 上机实验（1）：PARSE



## 实验内容

本次实验是对网络爬虫的初次尝试。 

在从指定URL获取**HTML**文档的基础上，本次实验实现的主要功能有：

* 提取**HTML**文档中的所有URL，并打印到指定文本文件中

* 提取**HTML**文档中所有图片的**source**，并打印到指定文本文件中

* 针对特定网页[知乎日报](http://daily.zhihu.com/)，编写解析程序，把网页中的链接，图片地址，文字标题分组打印到文件

注：**Ubuntu**自带**python 3**



由于编程语言的选择，使用的库也相对于模板有一些调整。

本次实验使用到的库有：

* sys
* requests
* urllib
* beautifulsoup4
* re



由于**python 2**为**Ubuntu**系统的默认python版本

以**beautifulsoup**库为例，若要为**python 3**装库，则需使用

```
pip3 install beautifulsoup4
```

若系统中未曾安装**pip3**，则需要使用

```
sudo apt install python3-pip
```

进行安装后再装库。



## 关于库的简要说明



### requests库

利用requests库实现的功能是，获取网页内容

利用requests库中的get，发送HTML请求，接受HTML文档。其返回类型为`requests.Response`。

若未能获取正常的HTML文档回复，`requests.Response.raise_for_status`会产生一个**HTTPError**。



### urllib库

本次使用了`urllib.parse.urljoin`函数。

该函数实际上是替代了作业PPT中的urlparse库中的urljoin函数

目的是在提取网页中的URL时，将相对URL根据url-base补充为绝对路径URL



### re库

本实验使用正则表达式库（re）对网页中的标签的属性进行字符串匹配

从而获得具有特定属性的标签，以达到信息筛选的功能。





## 代码使用

第一题与第二题的代码用法相似

功能分别是提取url和提取图片源。

以第一题为例

若命令行当前目录即代码所在目录，

可以在命令行中用如下命令使用：

```
python3 ./ex1.py [url]
```

进行网络爬取。

其中**url**可以是任何可访问的网页url

要求url要完整，例如："http://www.baidu.com"。

url两侧引号不做要求。

若URL没有给出，则默认解析[上海交通大学官网]("http://www.sjtu.edu.cn")

运行结果会打印在当前目录下，文件名为res1.txt和res2.txt中。



第三题由于解析方式是针对[知乎日报](http://daily.zhihu.com/)设计，

所以不接受自定义url，使用方式为

```
python3 ./ex3.py
```

答案打印在**res3.txt**中
