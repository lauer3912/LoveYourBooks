# Spring Boot

Spring Boot是由Pivotal团队提供的全新框架，其设计目的是用来简化新Spring应用的初始搭建以及开发过程。该框架使用了特定的方式来进行配置，从而使开发人员不再需要定义样板化的配置。通过这种方式，Spring Boot致力于在蓬勃发展的快速应用开发领域(rapid application development)成为领导者。

## 特点

1. 创建独立的Spring应用程序
2. 嵌入的Tomcat，无需部署WAR文件
3. 简化Maven配置
4. 自动配置Spring
5. 提供生产就绪型功能，如指标，健康检查和外部配置
6. 绝对没有代码生成并且对XML也没有配置要求 [1] 

## 安装步骤

从最根本上来讲，Spring Boot就是一些库的集合，它能够被任意项目的构建系统所使用。简便起见，该框架也提供了命令行界面，它可以用来运行和测试Boot应用。框架的发布版本，包括集成的CLI（命令行界面），可以在Spring仓库中手动下载和安装。一种更为简便的方式是使用Groovy环境管理器（Groovy enVironment Manager，GVM），它会处理Boot版本的安装和管理。Boot及其CLI可以通过GVM的命令行gvm install springboot进行安装。在OS X上安装Boot可以使用Homebrew包管理器。为了完成安装，首先要使用brew tap pivotal/tap切换到Pivotal仓库中，然后执行brew install springboot命令。
要进行打包和分发的工程会依赖于像Maven或Gradle这样的构建系统。为了简化依赖图，Boot的功能是模块化的，通过导入Boot所谓的“starter”模块，可以将许多的依赖添加到工程之中。为了更容易地管理依赖版本和使用默认配置，框架提供了一个parent POM，工程可以继承它。

```xml
<?xml version="1.0" encoding="utf-8"?>

<project xmlns="http://maven.apache.org/POM/4.0.0" xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance" xsi:schemaLocation="http://maven.apache.org/POM/4.0.0  http://maven.apache.org/xsd/maven-4.0.0.xsd">  
  <modelVersion>4.0.0</modelVersion>  
  <groupId>com.example</groupId>  
  <artifactId>myproject</artifactId>  
  <version>1.0.0-SNAPSHOT</version>  
  <!-- Inherit defaults from Spring Boot -->  
  <parent> 
    <groupId>org.springframework.boot</groupId>  
    <artifactId>spring-boot-starter-parent</artifactId>  
    <version>1.0.0.RC1</version> 
  </parent>  
  <!-- Add typical dependencies for a web application -->  
  <dependencies> 
    <dependency> 
      <groupId>org.springframework.boot</groupId>  
      <artifactId>spring-boot-starter-web</artifactId> 
    </dependency>  
    <dependency> 
      <groupId>org.springframework.boot</groupId>  
      <artifactId>spring-boot-starter-actuator</artifactId> 
    </dependency> 
  </dependencies>  
  <repositories> 
    <repository> 
      <id>spring-snapshots</id>  
      <url>http://repo.spring.io/libs-snapshot</url> 
    </repository> 
  </repositories>  
  <pluginRepositories> 
    <pluginRepository> 
      <id>spring-snapshots</id>  
      <url>http://repo.spring.io/libs-snapshot</url> 
    </pluginRepository> 
  </pluginRepositories>  
  <build> 
    <plugins> 
      <plugin> 
        <groupId>org.springframework.boot</groupId>  
        <artifactId>spring-boot-maven-plugin</artifactId> 
      </plugin> 
    </plugins> 
  </build>
</project>

```