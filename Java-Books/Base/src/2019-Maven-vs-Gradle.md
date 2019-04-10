# 2019 Maven vs Gradle

1. 灵活性
谷歌采用gradle构建andriod不是因为构建脚本就是代码，而是因为gradle是可扩展的。比如gradle允许调用C/C++进行native 开发。另外，gradle可以扩展到其他生态圈，比如可以嵌入其他系统，因为gradle提供了一套tooling api。
Gradle和maven都遵循约定大于配置，但是maven的模型比较僵硬，一些个性化配置很难实现甚至不可能。


2. 性能
加快build速度对项目发布很重要，gradle和maven都采用了并行编译，并行依赖处理等方案。gradle的最大不同是避免不需要的工作和渐进性。主要采用以下三点：

    - a. 渐进性
    gradle 记录任务的输入和输出，仅仅运行必须的，尽可能仅仅处理更高的文件
    - b. 利用cache
    gradle对于相同的输入，重用其他gradle build输出的cache，对于跨机器的构建也可以。
    - c. Daemon进程
    gradle长期运行一个进程把build信息保存在内存


3 . 用户体验
gradle提供了Kotlin-based DSL 提升用户体验。而且gradle提供了一种交互式UIbuild scans，可以进行debug，优化build性能
4.依赖管理
两者都提供了内置的依赖管理机制，都能本地缓存依赖或者远程下载。
maven 重写依赖仅仅允许修改版本，但是gradle提供了 “依赖选择”和“替代机制”（声明一次，整个工程都生效），替换机制可以利用多个project生成复合build。

下面的例子拒绝1.5 version


Example 25.64. Component selection rule

```java
build.gradle

configurations {
    rejectConfig {
        resolutionStrategy {
            componentSelection {
                // Accept the highest version matching the requested version that isn't '1.5'
                all { ComponentSelection selection ->
                    if (selection.candidate.group == 'org.sample' && selection.candidate.module == 'api' && selection.candidate.version == '1.5') {
                        selection.reject("version 1.5 is broken for 'org.sample:api'")
                    }
                }
            }
        }
    }
}

dependencies {
    rejectConfig "org.sample:api:1.+"
}

```
替代机制如下，用groovy替代groovy-all，用log4j-over-slf4j替代log4j

Example 25.53. Changing dependency group and/or name at the resolution

```java
build.gradle

configurations.all {
    resolutionStrategy.eachDependency { DependencyResolveDetails details ->
        if (details.requested.name == 'groovy-all') {
            //prefer 'groovy' over 'groovy-all':
            details.useTarget group: details.requested.group, name: 'groovy', version: details.requested.version
        }
        if (details.requested.name == 'log4j') {
            //prefer 'log4j-over-slf4j' over 'log4j', with fixed version:
            details.useTarget "org.slf4j:log4j-over-slf4j:1.7.10"
        }
    }
}

```