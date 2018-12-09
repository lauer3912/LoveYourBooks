
fn main() {
    let x = 5;
    let raw = &x as *const i32;

    println!("{:?}", raw); // 0xf65eaff994

    let mut y = 10;
    let raw_mut = &mut y as *mut i32;

    println!("{:?}", raw_mut); // 0xf65eaff9f4
    unsafe {
        // *raw_mut 称为 解引用
        println!("raw points at {:?} is {}", raw_mut, *raw_mut); //raw points at 0x50ebf6f784 is 10
        *raw_mut = 50 + *raw_mut;
        println!("raw points at {:?} is {}", raw_mut, *raw_mut); //raw points at 0x50ebf6f784 is 60
    }
    
    fn show<'a> (_x: &'a str) -> &'a str{
        "Hello"
    }



    struct MyFooVtable {
        data: *mut (),     // 指向实际类型实例的指针
        vtable: *mut (),   // 指向实际类型对于该trait的实现的虚函数表
        destructor: fn(*mut ()),
        size: usize,
        align: usize,
        //method: fn(*const ()) -> String,
    }

    let my_fv = MyFooVtable {
        data: raw_mut,
        vtable: raw_mut,
        destructor: *show,
        size: 8usize,
        align: 8usize,
        //method: *hide,
    };

}
