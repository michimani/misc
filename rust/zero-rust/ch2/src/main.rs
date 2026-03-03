fn main() {
    evaluation()
}

fn evaluation() -> () {
    println!("short-circuiting");
    println!("{}", a() || b());

    println!("\nnon-short-circuiting");
    println!("{}", a() | b());
}

fn a() -> bool {
    println!("called a");
    true
}

fn b() -> bool {
    println!("called b");
    true
}
