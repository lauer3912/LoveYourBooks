# Spring MVC

Spring MVC属于SpringFrameWork的后续产品，已经融合在Spring Web Flow里面。Spring 框架提供了构建 Web 应用程序的全功能 MVC 模块。使用 Spring 可插入的 MVC 架构，从而在使用Spring进行WEB开发时，可以选择使用Spring的Spring MVC框架或集成其他MVC开发框架，如Struts1(现在一般不用)，Struts 2(一般老项目使用)等。

## 框架

通过策略接口，Spring 框架是高度可配置的，而且包含多种视图技术，例如 JavaServer Pages（JSP）技术、Velocity、Tiles、iText和POI。Spring MVC 框架并不知道使用的视图，所以不会强迫开发者只使用 JSP 技术。Spring MVC 分离了控制器、模型对象、过滤器以及处理程序对象的角色，这种分离让它们更容易进行定制。

## 优点

Lifecycle for overriding binding, validation, etc，易于同其它View框架（Tiles等）无缝集成，采用IOC便于测试。
它是一个典型的教科书式的mvc构架，而不像struts等都是变种或者不是完全基于mvc系统的框架，对于初学者或者想了解mvc的人来说我觉得 spring是最好的，它的实现就是教科书！第二它和tapestry一样是一个纯正的servlet系统，这也是它和tapestry相比 struts所具有的优势。而且框架本身有代码，看起来容易理解。

## 单元测试

关于Spring MVC Controller 层的单元测试
测试准备工作：
1、搭建测试Web环境
```java
@RunWith(UnitilsJUnit4TestClassRunner.class)
@SpringApplicationContext({
"classpath:*.xml","file:src/main/webapp/WEB-INF/spring-configuration/*.xml",
"file:src/main/webapp/WEB-INF/*.xml"
})
```
2、注入Controller 类
```java
@Controller
BeanControllercontroller;
```
3、编写测试数据
测试数据的文件名一定要与测试类的文件名相同，比如测试数据BeanControllerTest.xml ，测试类 BeanControllerTest。

4、注入测试数据

```java
@Test
@DataSet
publicvoidtestBean(){}
```


## 常用注解

MVC已经是现代Web开发中的一个很重要的部分，下面介绍一下Spring MVC的一些使用心得。
之前的项目比较简单，多是用JSP 、Servlet + JDBC 直接搞定，在项目中尝试用 Struts(Struts MVC)+Spring+Hibernate, 严格按照分层概念驱动项目开发，因项目需求一直不断变化，功能不断扩充、增强，技术构建也几经改变到目前有个稳定的应用，体会了很多感受，这次先对 Spring MVC 层进行一些个人总结。
MVC作为WEB项目开发的核心环节，正如三个单词的分解那样，C（控制器）将V（视图、用户客户端）与M（javaBean:封装数据）分开构成了MVC ，这边不去讨论项目中是否应用MVC ，也不针对MVC的实现原理进行讲解，而是探讨实践中如何从应用SSH, 到Struts(Struts MVC)+Spring+Hibernate的演化过程。
先看 Struts 如何与 Spring 结合处理一次简单的请求响应代码，前台可以设为用 AJAX 调用：
