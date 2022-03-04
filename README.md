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

17，18，和20是原来的**Exercise**，分别实现了有限坐标系、长除式的功能编写，以及雪花的视觉效果调整。
