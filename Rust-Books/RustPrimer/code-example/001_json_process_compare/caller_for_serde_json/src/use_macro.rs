//声明宏的导出及应用方式
//#[macro_export] 用来声明该宏导出，可以用于外部调用模块使用
//macro_rules! 宏定义语句
#[macro_export]
macro_rules! say_hello {
    () => (print!("\n"));
    ($($arg:tt)*) => ({
        println!($($arg)*);
    })
}

// 定义调用主函数， 使用 pub 关键字说明该函数，可以被外部调用者使用
pub fn main() {

    // 调用包内定义的宏
    say_hello!("use inter macro");

    // The type of `john` is `serde_json::Value`
    let john = json!({
      "name": "John Doe",
      "age": 43,
      "phones": [
        "+44 1234567",
        "+44 2345678"
      ]
    });

    println!("first phone number: {}", john["phones"][0]);

    // Convert to a string of JSON and print it out
    println!("{}", john.to_string());
}

#[cfg(feature = "enable_call_try_use_foo")]
pub fn try_use_foo() {
    say_hello!("Hi I'm using try_use_foo ...");
}