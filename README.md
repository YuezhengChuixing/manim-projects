# manim-projects
乐正垂星的个人manim项目库。存放了B站视频的源码与一些个人练习。乐正垂星的B站主页：https://space.bilibili.com/2057313067

## manim项目

manim项目存储于`/projectfiles`目录下，文件夹名称有简单分类：

### Toturial

表明该项目是依照教程写的。该教程可能来自于：

[manim kindergarten 的教程文档](https://docs.manim.org.cn/index.html)

[cigar666 在B站发布的图文教程](https://www.bilibili.com/read/cv2539928?from=search)

[manim kindergarten 在B站发布的视频教程](https://www.bilibili.com/video/BV1p54y197cC)

或一些其它我已经想不起来的教程。

### Exercise

表明该项目的编写目的为实现某些简单功能。这类项目具有实验性质，可能基于某些限制，无法实现一些功能。（不然为什么会有一些编号缺了呢？）

- 07 (Exercise 1)

实现图片文件的逐像素导入（为此我还一天速成了PIL）。

- 08 (Exercise 2)

实验动画的并行编写功能，具体表现为16\*16图片的逐像素控制。本功能的真正实现要比 09 晚。

- 09 (Exercise 3)

实验动画的控制参数（`run_time`，`lag_ratio`之类较为简单的参数）。在08的第一次尝试失败后找了个简单一点的小目标。

- 10 (Exercise 4)

实验`TextMobject`与`TexMobject`两个类的使用，因为按[视频教程](https://www.bilibili.com/video/BV1p54y197cC)写的代码老是报错。后来才知道这两个类在更新后消失了。

### Video

表明该项目的编写目的为制作视频动画。在编写新功能时会使用一个新的**Exercise**，但是为了本库的可读性，把它们统一命名成了**Video**。

- 16~20 (Video 1)

视频[《拉格朗日插值法》](https://www.bilibili.com/video/BV1TR4y1j745 "【拉格朗日插值法的本质】拉格朗日，孙子，与每个人都能推出来的插值法")的代码。

17，18，和20是原来的**Exercise**，分别实现了有限坐标系、长除式的功能编写，以及雪花的视觉效果调整。视频代码分散于这些文件中。

- 22~24 (Video 2)

视频[《抛物线弓形的面积》](https://www.bilibili.com/video/BV1ZL411w7Jc "【抛物线弓形的面积】水平宽铅垂高，抛物线，与自相似性")的代码。

22与24是**Exercise**，其中22实现了抛物线弓形，24集中实现了一批图形对象。这些实现被应用在了23的制作中。视频代码集中于23。

- 27、28 (Video 3)

视频[《Winograd算法》](https://www.bilibili.com/video/BV15S4y1B7kj "【人工智能芯片入门】卷积、对偶性、与Winograd算法")的代码。

28是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了27的制作中。视频代码集中于27。


- 30、31 (Video 4)

视频[《定速抛体的包络线》](https://www.bilibili.com/video/BV19v4y1F7BC "【乐正垂星】定速抛体的包络线")的代码。

31是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了30的制作中。视频代码集中于30。

- 36、37 (Video 5)

视频[《完美加密与现代密码学初探》](https://www.bilibili.com/video/BV1ce4y1q778 "【乐正垂星】恺撒密码，完美加密，与现代密码学初探")的代码。

37是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了36的制作中。视频代码集中于36。

视频中所使用的svg图像来自[@BioCraft](https://space.bilibili.com/182765092 "BioCraft的b站个人空间")的创作，图片遵循CC BY-SA协议。

- 40、41 (Video 6)

视频[《凸透镜的成像变换》](https://www.bilibili.com/video/BV1Ze411A7k6 "【乐正垂星】光学题，凸透镜，和射影几何")的代码。

41是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了40的制作中。视频代码集中于40。

视频中所使用的svg图像来自[@BioCraft](https://space.bilibili.com/182765092 "BioCraft的b站个人空间")的创作，图片遵循CC BY-SA协议。

- 42、43 (Video 7)

视频[《母函数》](https://www.bilibili.com/video/BV1QM411A73c "【乐正垂星】母函数是可以被理解的？！")的代码。

43是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了42的制作中。视频代码集中于42。

- 44、45 (Video 8)

视频[《渐开线与弧度方程》](https://www.bilibili.com/video/BV1rs4y1n7ZE "【乐正垂星】开！摆！——渐开线，摆线，与弧度方程")的代码。

45是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了44的制作中。视频代码集中于44。

___

在45之后的文件，基于独立于manim库的`additional/additional.py`文件，使用时需将其手动添加至manimlib的`__init__.py`文件中。`additional.py`文件集中整理了一些常用的类。

`000-Template`中，`old_Template.py`基于更改之前的代码，`Template.py`基于更改之后的代码。

___

- 47、48 (Video 9)

视频[《复数与代数数论》](https://www.bilibili.com/video/BV1cL411e7ia "【乐正垂星】复数不是一切的答案")的代码。

48是**Exercise**，集中实现了一批图形对象与一批动画效果。这些实现被应用在了47的制作中。视频代码集中于47。

