use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => {
        $x.trim().parse::<$t>().unwrap()
    };
}

#[derive(PartialEq)]
enum Order {
    Pre,
    In,
    Post,
    Level,
}

struct Tree {
    node: Option<Box<Node>>,
}

impl Tree {
    fn new() -> Tree {
        Tree { node: None }
    }

    fn insert(&mut self, value: i32) {
        match self.node {
            Some(ref mut node) => node.insert(value),
            None => self.node = Some(Box::new(Node::new(value))),
        }
    }

    fn order(&self, order: &Order) -> Vec<i32> {
        match *order {
            Order::Pre | Order::In | Order::Post => self.pip_order(order),
            Order::Level => self.level_order(),
        }
    }

    fn pip_order(&self, order: &Order) -> Vec<i32> {
        let mut result = Vec::new();
        if let Some(ref node) = self.node {
            if *order == Order::Pre {
                result.push(node.value);
            }
            result.append(&mut node.left.order(order));
            if *order == Order::In {
                result.push(node.value);
            }
            result.append(&mut node.right.order(order));
            if *order == Order::Post {
                result.push(node.value);
            }
        }
        result
    }

    fn level_order(&self) -> Vec<i32> {
        let mut result = Vec::new();
        let mut queue = Vec::new();
        queue.push(self);
        while !queue.is_empty() {
            let tree = queue.remove(0);
            if let Some(ref node) = tree.node {
                result.push(node.value);
                queue.push(&node.left);
                queue.push(&node.right);
            }
        }
        result
    }
}

struct Node {
    value: i32,
    left: Tree,
    right: Tree,
}

impl Node {
    fn new(value: i32) -> Node {
        Node {
            value,
            left: Tree::new(),
            right: Tree::new(),
        }
    }

    fn insert(&mut self, value: i32) {
        if value < self.value {
            self.left.insert(value);
        } else {
            self.right.insert(value);
        }
    }
}

fn main() {
    let mut input_line = String::new();
    let _ = io::stdin().read_line(&mut input_line);

    let mut tree = Tree::new();

    let mut inputs = String::new();
    io::stdin().read_line(&mut inputs).unwrap();
    for i in inputs.split_whitespace() {
        tree.insert(parse_input!(i, i32));
    }

    for order in &[Order::Pre, Order::In, Order::Post, Order::Level] {
        println!(
            "{}",
            tree.order(order)
                .iter()
                .map(|x| x.to_string())
                .collect::<Vec<String>>()
                .join(" ")
        );
    }
}
