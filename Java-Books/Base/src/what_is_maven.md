# 什么是 Maven?

Maven 是最流行的 Java 项目构建系统。

目前，绝大多数开发人员都把 Ant 当作 Java 编程项目的标准构建工具。遗憾的是，Ant 的项目管理工具（作为 make 的替代工具）不能满足绝大多数开发人员的需要。通过检查 Ant 构建文件，很难发现项目的相关性信息和其它元信息（如开发人员／拥有者、版本或站点主页）。

Maven 除了以程序构建能力为特色之外，还提供 Ant 所缺少的高级项目管理工具。由于 Maven 的缺省构建规则有较高的可重用性，所以常常用两三行 Maven 构建脚本就可以构建简单的项目，而使用 Ant 则需要十几行。事实上，由于 Maven 的面向项目的方法，许多 Apache Jakarta 项目现在使用 Maven，而且公司项目采用 Maven 的比例在持续增长。

Maven vs Ant

那么，Maven 和 Ant 有什么不同呢？在回答这个问题以前，我要强调一点：Maven 和 Ant 针对构建问题的两个不同方面。Ant 为 Java 技术开发项目提供跨平台构建任务。Maven 本身描述项目的高级方面，它从 Ant 借用了绝大多数构建任务。因此，由于 Maven 和 Ant 代表两个差异很大的工具，所以我将只说明这两个工具的等同组件之间的区别，如表 1 所示。

表 1. Maven vs Ant

|              | Maven                                | Ant       |
| ------------ | ------------------------------------ | --------- |
| 标准构建文件 | project.xml 和 maven.xml             | build.xml |
| 特性处理顺序 | \${maven.home}/bin/driver.properties |

${project.home}/project.properties  
${project.home}/build.properties  
\${user.home}/build.properties
通过 -D 命令行选项定义的系统特性 | 通过 -D 命令行选项定义的系统特性 由 任务装入的特性 |
| 构建规则 | 构建规则更为动态（类似于编程语言）；它们是基于 Jelly 的可执行 XML。 | 构建规则或多或少是静态的，除非使用 |

相关开发环境下的 Maven 插件：http://mevenide.codehaus.org/

> Maven 是一个项目管理工具，它包含了一个项目对象模型 (Project Object Model)，一组标准集合，一个项目生命周期(Project Lifecycle)，一个依赖管理系统(Dependency Management System)，和用来运行定义在生命周期阶段(phase)中插件(plugin)目标(goal)的逻辑。当你使用 Maven 的时候，你用一个明确定义的项目对象模型来描述你的项目，然后 Maven 可以应用横切的逻辑，这些逻辑来自一组共享的（或者自定义的）插件。
> Maven 有一个生命周期，当你运行 mvn install 的时候被调用。这条命令告诉 Maven 执行一系列的有序的步骤，直到到达你指定的生命周期。遍历生命周期旅途中的一个影响就是，Maven 运行了许多默认的插件目标，这些目标完成了像编译和创建一个 JAR 文件这样的工作。
> 此外，Maven 能够很方便的帮你管理项目报告，生成站点，管理 JAR 文件，等等。
