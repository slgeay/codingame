use std::{collections::HashMap, fmt::Display, io};

const MAX_SOLUTION: i32 = 12;

macro_rules! parse_input {
    ($x:expr, $t:ident) => {
        $x.trim().parse::<$t>().unwrap()
    };
}

#[derive(Clone, Copy)]
enum Operator {
    Add,
    Sub,
    Mul,
    Div,
}

impl Operator {
    fn values() -> Vec<Operator> {
        vec![Operator::Add, Operator::Sub, Operator::Mul, Operator::Div]
    }

    fn apply(&self, a: i32, b: i32) -> Option<i32> {
        match self {
            Operator::Add => Some(a + b),
            Operator::Sub => Some(a - b),
            Operator::Mul => Some(a * b),
            Operator::Div => {
                if b == 0 || a % b != 0 {
                    None
                } else {
                    Some(a / b)
                }
            }
        }
    }

    fn is_commutative(&self) -> bool {
        match self {
            Operator::Add | Operator::Mul => true,
            Operator::Sub | Operator::Div => false,
        }
    }
}

impl Display for Operator {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        match self {
            Operator::Add => write!(f, "+"),
            Operator::Sub => write!(f, "-"),
            Operator::Mul => write!(f, "*"),
            Operator::Div => write!(f, "/"),
        }
    }
}

struct Operation {
    op: Operator,
    left: i32,
    right: i32,
}

impl Operation {
    fn new(op: Operator, left: i32, right: i32) -> Operation {
        Operation { op, left, right }
    }

    fn to_string(&self, known_values: &HashMap<i32, Expression>) -> String {
        let left = known_values
            .get(&self.left)
            .unwrap()
            .to_string(known_values);
        let right = known_values
            .get(&self.right)
            .unwrap()
            .to_string(known_values);
        format!("({} {} {})", left, self.op, right)
    }

    fn apply(&self) -> Option<i32> {
        self.op.apply(self.left, self.right)
    }
}

struct Expression {
    value: i32,
    size: i32,
    op: Option<Operation>,
}

impl Expression {
    fn to_string(&self, known_values: &HashMap<i32, Expression>) -> String {
        match &self.op {
            Some(op) => op.to_string(known_values),
            None => self.value.to_string(),
        }
    }

    fn apply(&self) -> Option<i32> {
        match &self.op {
            Some(op) => op.apply(),
            None => Some(self.value),
        }
    }
}

fn solve(n: i32, a: i32) -> i32 {
    let mut known: HashMap<i32, Expression> = HashMap::new();
    known.insert(
        a,
        Expression {
            value: a,
            size: 1,
            op: None,
        },
    );

    let mut known_per_size: HashMap<i32, Vec<i32>> = HashMap::new();
    known_per_size.insert(1, vec![a]);

    for size in 2..=MAX_SOLUTION {
        let mut new_known: HashMap<i32, Expression> = HashMap::new();
        let mut new_known_per_size: Vec<i32> = Vec::new();
        for operator in Operator::values() {
            for left_size in 1..size {
                let right_size = size - left_size;
                if left_size > right_size && operator.is_commutative() {
                    continue;
                }

                for left in known_per_size.get(&left_size).unwrap() {
                    for right in known_per_size.get(&right_size).unwrap() {
                        let left_value = *left;
                        let right_value = *right;
                        let result = operator.apply(left_value, right_value);

                        if result.is_none() {
                            continue;
                        }

                        let result = result.unwrap();
                        if known.contains_key(&result) || new_known.contains_key(&result) {
                            continue;
                        }

                        let expression = Expression {
                            value: result,
                            size,
                            op: Some(Operation::new(operator, left_value, right_value)),
                        };

                        if result == n {
                            eprintln!("{} = {}", n, expression.to_string(&known));
                            return size;
                        }

                        new_known.insert(result, expression);
                        new_known_per_size.push(result);
                    }
                }
            }
        }
        known.extend(new_known);
        known_per_size.insert(size, new_known_per_size);
    }

    12
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let n = parse_input!(input_line, i32);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let a = parse_input!(input_line, i32);

    let result = solve(n, a);
    println!("{}", result);
}
