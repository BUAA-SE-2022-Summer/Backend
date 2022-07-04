# 软工开发 Tips

## 仓库管理

### commit风格

在多人协作项目中，如果代码风格统一、代码提交信息的说明准确，那么在后期协作以及Bug处理时会更加方便。Git 每次提交代码，都要写 Commit message（提交说明），否则就不允许提交。一般来说，commit message 应该清晰明了，说明本次提交的目的。在我们的小型组队开发中，也有着一些commit的约定规范，希望大家遵守。

- 要求提交的commit需要有实际意义，能让团队的成员看懂本次提交做了什么工作
- 鼓励完成一小块内容commit一次存档，不鼓励完成多项任务再commit

**一种推荐的Commit日志风格：**

```ABAP
git commit -m "<type>（<scope>）: <subject>"
```

举个栗子：

```ABAP
git commit -m "[feat](Login.vue): 我淦完了登录页的前后端对接"
git commit -m "[fix](Login.vue): 登录功能中用户名重复的bug"
git commit -m "[docs](user.md): update用户相关接口文档"
git commit -m "[style](home.vue): 修改了主页的浮动属性"
git commit -m "[refactor](home.vue): 改了打开文档功能的的屎山"
git commit -m "[test](后端某文件): 某功能的单元测试"
git commit -m "[chore](main.js): 前端的服务器连接修改"
```

下面具体解释一下上面的代码提交规范。

**（1）type**

`type`用于说明 commit 的类别，只允许使用下面7个标识。

- feat：新功能（feature）
- fix：修补bug
- docs：文档（documentation）
- style： 格式（不影响代码运行的变动）
- refactor：重构（即不是新增功能，也不是修改bug的代码变动）
- test：增加测试
- chore：构建过程或辅助工具的变动

**（2）scope**

`scope`用于说明 commit 影响的范围，比如数据层、控制层、视图层等等，视项目不同而不同。

- 对于前端而言，你需要写明该次改动影响的文件

**（3）subject**

`subject`是 commit 目的的简短描述，不超过50个字符。

> 一些有关 git commit 规范的blog给在下面供大家参考，我们的项目相对没有那么复杂，所以对git commit的格式做了一些精简以提高效率。
>
> https://segmentfault.com/a/1190000019579621
>
> https://www.ruanyifeng.com/blog/2016/01/commit_message_change_log.html

------

### 分支管理

我们使用简化版本的`Git Flow`分支管理策略，下面引用一篇博文对该策略进行讲解

#### 主要分支 (The main branches)

在中央仓库中有两个生命期无限长的主要分支：

- **Master**
- **Developer**

`origin`的`master`分支已被所有的Git用户所熟知。平行于`master`分支存在着另一个被称为`develop`的分支。

我们默认主要分支`origin/master`的`HEAD`所指向的源码总是处于**可发布**(`production-ready`)的状态。

我们默认主要分支`origin/develop`的`HEAD`所指向的源码总是处于为下次发版所做的最近的一次修改提交的状态。也有人把它称作”集成分支(`integration branch`)”，每次向仓库提交所做的自动编译(`automatic builds`)通常来自该分支。也就是说这是一个日常开发所在的分支。

当`develop`分支上的代码达到了一个稳定的点并且准备进行发版时，在该分支上所做的所有修改都应该被合并(`merged`)回`master`分支，并且打一个带有发布版本号的标签(`tag`)。

> 由于软工的开发时间较短，一般我们把master作为每天的一个存档而不是稳定版本的发版，每天晚上应该把较为稳定内容推到master。日常开发在develop分支来完成，而作为辅助的CI/CD也部署在develop分支上。

#### 辅助分支 (Supporting branches)

<img src="%E8%BD%AF%E5%B7%A5%E5%BC%80%E5%8F%91%E7%9A%84Tips.assets/20141104_main-branches@2x.png" alt="main-branches" style="zoom:67%;" />

伴随着主要分支`master`和`develop`，我们的开发模式还用了一些辅助分支来协助团队成员间的平行开发，使对功能的追踪变得轻便(`ease tracking of features`)，并且协助产品的发布，以及进行线上版本bug的快速修复。

我们所用到这些的不同类型的辅助分支包括：

- Feature branches ：功能分支
- Fix branches ：修补bug
- Docs branches ：文档分支
- Style branches ： 格式分支
- Refactor branches ：重构分支
- Test branches ：增加测试分支
- Chore branches ：构建过程或辅助工具的变动分支

从分类角度上来将，这里的分支和commit规范中的type是一一对应的。从技术角度来讲，这些分支并没有本质区别，我们是根据使用场景去给它们归类的。它们本质上只是普通的Git分支而已。当然，有时候你会觉得文档分支这一类分支的存在没有必要，新加功能的时候文档顺手就加上了，实际上我们并不强制每次分支只能包含分支含义所代表的内容，在项目的开发过程中功能分支和修补分支是最常见的分支，希望大家能鲜明地使用这两种功能分支来完成工作。

下面我们以功能分支为例讲解这些分支创建和合并的生命周期

##### 功能分支 (Feature branches)

<img src="%E8%BD%AF%E5%B7%A5%E5%BC%80%E5%8F%91%E7%9A%84Tips.assets/20141104_fb@2x.png" alt="feature-branch" style="zoom:67%;" />

分支创建自：`develop`；必须合并回：`develop`；

分支命名约定：除`master`, `develop`, `release-*`, 或`hotfix-*`等以外的任何名字。

功能分支(有时亦称主题分支(`topic branch`))是用来给一个可预见的未来即将要发布的版本开发新功能的。当开始一个新功能的开发时，我们可能并不知道该新功能将被合并入哪个发布版本。事实上一个功能分支将伴随该功能的开发过程一直存在，并最终被合并回`develop`分支(已确定将要把该新功能加入到即将发布的新版本中)或者丢弃掉(假如是一个失败的尝试)。

功能分支通常只存在于开发者的本地仓库中，并不包含在远程库`origin`中。

###### 创建功能分支

当要开发一个新功能时，从`develop`分支中切出(`branch off`)一个新分支：

```bash
$ git checkout -b myfeature develop
Switched to a new branch "myfeature"
```

###### 将已完成的新功能合并到`develop`分支

如果确定要把已完成的新功能加入到即将发布的新版中，将它合并到`develop`分支：

```bash
$ git checkout develop
Switched to branch 'develop'

$ git merge --no-ff myfeature
Updating ea1b82a..05e9557
(Summary of changes)

$ git branch -d myfeature
Deleted branch myfeature (was 05e9557).

$ git push origin develop
```

上边的`--no-ff`标记的作用是使当前的合并操作总是创建一个新的`commit`对象，即使该合并被执行为快进式(`fast-forward`)合并。这样可以避免丢失掉该功能分支的历史存在信息，并且将针对该功能的所有提交都集中到一起。来对比一下：

<img src="%E8%BD%AF%E5%B7%A5%E5%BC%80%E5%8F%91%E7%9A%84Tips.assets/20141104_merge-without-ff@2x.png" alt="merge-without-ff" style="zoom:67%;" />

对于后者的情形，想要从Git的历史信息中识别出哪些`commit`对象是针对该新功能所做的，简直不可能，除非去阅读所有的`log`信息。而且如果你想要回退到做整个新功能(比如一组提交)之前的状态，对于后者来说简直是件非常让人头疼的事，但是如果使用了`--no-ff`标记这将很容易实现。这将创建一些多余的(空的)提交(`commit`)对象，但是收益远远大于开销。

> 关于`Git Flow`的更多知识请看:point_down:
>
> [一个完美的Git 分支管理模型(Git工作流) - Matrixzk's Blog](http://matrixzk.github.io/blog/20141104/git-flow-model)

## 工具链

### 强烈推荐的辅助工具

- [GitHub Copilot · Your AI pair programmer](https://github.com/features/copilot/)

	`Copilot`是Github推出的一款AI代码生成工具。它利用github上资源丰富的开源代码进行训练，可以高效准确地帮助我们提高代码编写效率。主要功能有：

	- 写出注释，通过注释生成代码段
	- 边写边补全，猜测你下一句会是什么

	我下载时本工具出于Beta测试版本，需要向官方发生申请拿到邀请码才能使用。最近看到消息说要正式上线了，价格是每月69元，学生党可以白嫖，可以在官网看看。