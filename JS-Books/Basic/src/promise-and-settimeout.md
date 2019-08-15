# Promise 与 setTimout 谁先执行？

## 首先，要理解 JavaScript 的线程机制

JavaScript 是单线程语言，也就是说同一个事件只能做一件事。JavaScript 的单线程，与它的用途有关，作为浏览器脚本语言，JavaScript 的主要用途是与用户交互，以及操作 DOM。这决定了它只能是单线程，否则会带来很多复杂的同步问题。为了利用多核 CPU 的计算能力，虽然 HTML5 提出了 Web Worker，允许 JavaScript 脚本创建多个线程，但是子线程完全受主线程控制，且不得操作 DOM 和 BOM。所以，依然没有改变 JavaScript 是单线程的本质。
为了解决单线程导致的线程等待资源，cpu 空闲，而其他任务一直等待的问题。将所有的任务分为两种，一种是同步任务，一种是异步任务。同步任务指的是，在主线程上排队执行的任务，只有前一个任务执行完毕，才能执行下一个任务。异步任务指的是，不进入主线程，而进入“任务队列”的任务，自由“任务队列”通知主线程，某个异步任务可以执行了，该任务才会进入主线程执行。
主任务和任务队列示意图：

![](images/js-run.png)

执行过程：
（1）所有的同步任务都在主线程上指向，形成一个执行栈
（2）主线程之外，还存在一个“任务队列”。只要异步任务有了运行结果，就在“任务队列”之中放置一个事件。
（3）一旦“执行栈”中的所有同步任务执行完毕，系统就会读取“任务队列”，将可执行的任务放在主线程执行。任务队列是一个先进先出的数据结构，排在前面的事件，优先被主线程读取。
（4）主线程不断重复上面的第三步。
只要主线程空了，就会去读取“任务队列”。
Event Loop（事件轮询）
主线程从“任务队列”中读取事件，这个过程是循环不断的，所以整个过程的这种运行机制又称为 Event Loop（事件循环）。

## 其次要理解什么是宏任务和微任务

javascript 的宏任务和微任务

宏任务有 Event Table、Event Queue，微任务有 Event Queue

1. 宏任务：包括整体代码 script，setTimeout，setInterval；
2. 微任务：Promise，process.nextTick

> 注：Promise 立即执行，then 函数分发到微任务 Event Queue，process.nextTick 分发到微任务 Event Queue

### 原理

任务进入执行栈----同步任务还是异步任务----同步的进入主线程，异步的进入 Event Table 并注册函数。当指定的事情完成时，Event Table 会将这个函数移入 Event Queue。主线程内的任务执行完毕为空，会去 Event Queue 读取对应的函数，进入主线程执行。上述过程会不断重复，也就是常说的 Event Loop(事件循环)。

```js
setTimeout(function() {
  console.log("宏任务setTimeout"); //先遇到setTimeout，将其回调函数注册后分发到宏任务Event Queue
  //如果setTimeout设置时间，那它会先把函数放到宏任务Event Table,等时间到了再放入宏任务Event Queue里面
});
new Promise(function(resolve) {
  console.log("微任务promise"); //new Promise函数立即执行
  resolve(); //必须resolve执行才能执行then
}).then(function() {
  console.log("微任务then"); //then函数分发到微任务Event Queue
});
console.log("主线程console");

//执行顺序结果： 微任务promise、主线程console、微任务then、宏任务setTimeout
```

#### 事件循环原理

```js
// 伪代码
while (1) {
  // 有可执行的微任务吗？
  if (has_micro_task) {
    process_all_micro_tasks(); // 执行所有的微任务
    process_one_new_macro_task(); // 开始执行新的宏任务
  } else {
    process_one_new_macro_task(); // 开始执行新的宏任务
  }
}
```

### 示例代码 1：

```js
setTimeout(function() {
  console.log(1);
}, 0);
new Promise(function(a, b) {
  console.log(2);
  for (var i = 0; i < 10; i++) {
    i == 9 && a();
  }
  console.log(3);
}).then(function() {
  console.log(4);
});
console.log(5);

/// 执行输出结果： 2， 3， 5， 4， 1
```

### 示例代码 2：

```js
console.log("1主线程"); //整体script作为第一个宏任务进入主线程
setTimeout(function() {
  //setTimeout，其回调函数被分发到宏任务Event Queue（执行规则：从上到下排序，先进先执行）中
  console.log("2宏任务");
  process.nextTick(function() {
    console.log("3宏任务里面的微任务");
  });
  new Promise(function(resolve) {
    console.log("4微任务");
    resolve();
  }).then(function() {
    console.log("5微任务");
  });
});
process.nextTick(function() {
  //process.nextTick()其回调函数被分发到微任务Event Queue中
  console.log("6微任务");
});
new Promise(function(resolve) {
  //Promise，new Promise直接执行，输出7
  console.log("7微任务");
  resolve();
}).then(function() {
  console.log("8微任务"); //then被分发到微任务Event Queue中,排在process.nextTick微任务后面。
});
setTimeout(function() {
  //setTimeout，其回调函数被分发到宏任务Event Queue中,排在前面的setTimeout后面
  console.log("9宏任务");
  process.nextTick(function() {
    console.log("10宏任务里面的微任务");
  });
  new Promise(function(resolve) {
    console.log("11微任务");
    resolve();
  }).then(function() {
    console.log("12微任务");
  });
});

//执行结果： 1主线程、7微任务、6微任务、8微任务、2宏任务、4微任务、3宏任务里面的微任务、5微任务、
```
