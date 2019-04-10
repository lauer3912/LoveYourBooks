# ES6 与 ES5 的区别

> JavaScript 简介
> JavaScript 一种动态类型、弱类型、基于原型的客户端脚本语言，用来给 HTML 网页增加动态功能。
> JavaScript 由三部分组成：
> ECMAScript（核心）+DOM（文档对象模型）+BOM（浏览器对象模型）
> ECMAScript 作为核心，规定了语言的组成部分：语法、类型、语句、关键字、保留字、操作符、对象
> DOM 把整个页面映射为一个多层节点结果，开发人员可借助 DOM 提供的 API，轻松地删除、添加、替换或修改任何节点。
> BOM 支持可以访问和操作浏览器窗口的浏览器对象模型，开发人员可以控制浏览器显示的页面以外的部分
> ES5 简介
> ECMAScript 第五个版本，增加了以下特性
> 1、strict 模式
> 2、Array 的 every、some、forEach、filter、indexOf、lastIndexOf、isArray、map、reduce、reduceRight 等方法
> 3、Object 方法
> ES6
> ECMAScript 第六个版本，增加的新特性：
> 1、块级作用域 关键字 let，常量 const
> 2、对象字面量的属性赋值简写
> 3、赋值解构
> 4、函数参数-默认值、参数打包、数组展开（Default、Rest、Spread）
> 5、箭头函数 Arrow functions
> 简化了代码形式，默认 return 表达式结果
> 自动绑定语义 this，即定义函数时的 this。
> 6、字符串模板 Template strings
> 7、Iterators（迭代器）+for..of
> 迭代器的 next 方法，调用会返回：
> （1）返回迭代对象的一个元素：{done:false, value:elem}
> （2）如果已经达到迭代对象的末端：{done:true, value:retVal}
> 8、生成器（Generators）
> 9、Class，有 constructor、extends、super
> 10、Modules
> （1）具有 CommonJS 的精简语法、唯一导出出口（single exports）和循环依赖（cyclic dependencies）的特点
> （2）类似 AMD，支持异步加载和可配置的模块加载
> 11、四种集合类型，Map+Set+WeakMap+WeakSet
> 12、一些新的 API
> Math+Number+String+Array+Object APIs
> 13、Proxies
> 使用代理（Proxy）监听对象的操作，包括 get、set、has、deleteProperty、apply、construct、getOwnPropertyDescriptor、defineProperty、getPrototypeOf、setPrototypeOf、enumerate、ownKeys、preventExtensions、isExtensible。
> 14、Symbols
> 一种基本类型，通过调用 symbol 函数产生，接收一个可选的名字参数，该函数返回的 symbol 是唯一的。
> 15、Promises
> 是处理异步操作的对象，使用了 Promise 对象之后可以用一种链式调用的方式来组织代码，让代码更直观

## 主要区别

1.  ES6 新增了 let 命名
1.  ES6 新增了 const 常量命名
1.  ES6 新增了 块级作用域
1.  ES6 新增了 箭头函数
1.  ES6 新增了 class、extends、supper 关键字
1.  ES6 新增了 变量的解构赋值
1.  ES6 新增了 模板字符串（反引号）
1.  ES6 新增了 模板中可以嵌套函数
1.  ES6 新增了 函数参数的默认值
1.  ES6 新增了 rest 语法
1.  ES6 新增了 本地模块导入导出

## ES6 新增了 let 命名

> ES6 新增了 let 命令，用来声明变量。它的用法类似于 var，但是所声明的变量，只在 let 命令所在的代码块内有效。
> let 不像 var 存在变量提升，即变量一定要声明之后才能使用

```js
{
  var a = 1;
  let b = 1;
}
a;
b; // error
```

## ES6 新增了 const 常量命名

## ES6 新增了 块级作用域

> ES5 只有全局作用域和函数作用域，没有块级作用域

## ES6 新增了 箭头函数

> 这个恐怕是 ES6 最最常用的一个新特性了，用它来写 function 比原来的写法要简洁清晰很多:

```js
function(i){ return i + 1; } //ES5
(i) => i + 1 //ES6
```

简直是简单的不像话对吧...
如果方程比较复杂，则需要用{}把代码包起来：

```js
function(x, y) {
    x++;
    y--;
    return x + y;
}
(x, y) => {x++; y--; return x+y}
```

除了看上去更简洁以外，arrow function 还有一项超级无敌的功能！
长期以来，JavaScript 语言的 this 对象一直是一个令人头痛的问题，在对象方法中使用 this，必须非常小心。例如：

```js
class Animal {
  constructor() {
    this.type = "animal";
  }
  says(say) {
    setTimeout(function() {
      console.log(this.type + " says " + say); /// error
    }, 1000);
  }
}

var animal = new Animal();
animal.says("hi"); //undefined says hi
```

运行上面的代码会报错，这是因为 setTimeout 中的 this 指向的是全局对象。所以为了让它能够正确的运行，传统的解决方法有两种：

1.传统方法：第一种是将 this 传给 self,再用 self 来指代 this

```js
   says(say){
       var self = this;
       setTimeout(function(){
           console.log(self.type + ' says ' + say)
       }, 1000)
```

2.传统方法：第二种方法是用 bind(this),即

```js
   says(say){
       setTimeout(function(){
           console.log(this.type + ' says ' + say)
       }.bind(this), 1000)
```

但现在我们有了箭头函数，就不需要这么麻烦了：

```js
class Animal {
  constructor() {
    this.type = "animal";
  }
  says(say) {
    setTimeout(() => {
      console.log(this.type + " says " + say);
    }, 1000);
  }
}
var animal = new Animal();
animal.says("hi"); //animal says hi
```

当我们使用箭头函数时，函数体内的 this 对象，就是定义时所在的对象，而不是使用时所在的对象。
并不是因为箭头函数内部有绑定 this 的机制，实际原因是箭头函数根本没有自己的 this，它的 this 是继承外面的，因此内部的 this 就是外层代码块的 this。

## ES6 新增了 class、extends、supper 关键字

> 这三个特性涉及了 ES5 中最令人头疼的的几个部分：原型、构造函数，继承...你还在为它们复杂难懂的语法而烦恼吗？你还在为指针到底指向哪里而纠结万分吗？有了 ES6 我们不再烦恼！ES6 提供了更接近传统语言的写法，引入了 Class（类）这个概念。新的 class 写法让对象原型的写法更加清晰、更像面向对象编程的语法，也更加通俗易懂。

```js
class Animal {
  constructor() {
    this.type = "animal";
  }
  says(say) {
    console.log(this.type + " says " + say);
  }
}

let animal = new Animal();
animal.says("hello"); //animal says hello

class Cat extends Animal {
  constructor() {
    super();
    this.type = "cat";
  }
}

let cat = new Cat();
cat.says("hello"); //cat says hello
```

上面代码首先用 class 定义了一个“类”，可以看到里面有一个 constructor 方法，这就是构造方法，而 this 关键字则代表实例对象。简单地说，constructor 内定义的方法和属性是实例对象自己的，而 constructor 外定义的方法和属性则是所有实例对象可以共享的。

Class 之间可以通过 extends 关键字实现继承，这比 ES5 的通过修改原型链实现继承，要清晰和方便很多。上面定义了一个 Cat 类，该类通过 extends 关键字，继承了 Animal 类的所有属性和方法。

super 关键字，它指代父类的实例（即父类的 this 对象）。子类必须在 constructor 方法中调用 super 方法，否则新建实例时会报错。这是因为子类没有自己的 this 对象，而是继承父类的 this 对象，然后对其进行加工。如果不调用 super 方法，子类就得不到 this 对象。

ES6 的继承机制，实质是先创造父类的实例对象 this（所以必须先调用 super 方法），然后再用子类的构造函数修改 this。

## ES6 新增了 变量的解构赋值

ES6 允许按照一定模式，从数组和对象中提取值，对变量进行赋值，这被称为解构（Destructuring）

```js
let [a, b, c] = [1, 2, 3];
```

看下面的例子：
ES5 的写法

```js
let cat = "ken";
let dog = "lili";
let zoo = { cat: cat, dog: dog };
console.log(zoo); //Object {cat: "ken", dog: "lili"}
```

ES6 的写法

```js
let cat = "ken";
let dog = "lili";
let zoo = { cat, dog };
console.log(zoo); //Object {cat: "ken", dog: "lili"}
```

反过来可以这么写：

```js
let dog = { type: "animal", many: 2 };
let { type, many } = dog;
console.log(type, many); //animal 2
```

## ES6 新增了 模板字符串（反引号）

```js
$("#list").html(`
<ul>
  <li>first</li>
  <li>second</li>
</ul>
`);
```

## ES6 新增了 模板中可以嵌套函数

> 模板中可以嵌套函数

```js
function fn() {
  return "Hello World";
}

`foo ${fn()} bar`;
// foo Hello World bar
```

## ES6 新增了 函数参数的默认值

default 很简单，意思就是默认值。大家可以看下面的例子，调用 animal()方法时忘了传参数，传统的做法就是加上这一句 type = type || 'cat' 来指定默认值。

> ES5

```js
function log(x, y) {
  y = y || "World";
  console.log(x, y);
}

log("Hello"); // Hello World
log("Hello", "China"); // Hello China
log("Hello", ""); // Hello World

function animal(type) {
  type = type || "cat";
  console.log(type);
}
animal();
```

> ES6

```js
function log(x, y = "World") {
  console.log(x, y);
}
log("Hello"); // Hello World
log("Hello", "China"); // Hello China
log("Hello", ""); // Hello

function animal(type = "cat") {
  console.log(type);
}
animal();
```

## ES6 新增了 rest 语法

```js
function animals(...types) {
  console.log(types);
}
animals("cat", "dog", "fish"); //["cat", "dog", "fish"]
```

而如果不用 ES6 的话，我们则得使用 ES5 的 arguments。

## ES6 新增了 本地模块导入导出

众所周知，在 ES6 以前 JavaScript 并不支持本地的模块。人们想出了 AMD，RequireJS，CommonJS 以及其它解决方法。现在 ES6 中可以用模块 import 和 export 操作了。在 ES5 中，你可以在 <script></script>中直接写可以运行的代码（简称 IIFE），或者一些库像 AMD。然而在 ES6 中，你可以用 export 导入你的类。下面举个例子，在 ES5 中,module.js 有 port 变量和 getAccounts 方法:

```js
 module.exports = {
   port: 3000,
   getAccounts: function() {
     ...
   }
 }
```

在 ES5 中，main.js 需要依赖 require(‘module’) 导入 module.js：

```js
// ES5
var service = require(‘module.js‘);
console.log(service.port); // 3000
```

但在 ES6 中，我们将用 export and import。例如，这是我们用 ES6 写的 module.js 文件库：

```js
 export var port = 3000;
 export function getAccounts(url) {
   ...
 }
```

如果用 ES6 来导入到文件 main.js 中，我们需用 import {name} from ‘my-module’语法，例如：

```js
import {port, getAccounts} from ‘module‘;
console.log(port); // 3000
```

或者我们可以在 main.js 中把整个模块导入, 并命名为 service：

```js
import * as service from ‘module‘;
console.log(service.port); // 3000
```
