use std::{collections::BTreeMap, io};

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}


fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let e = parse_input!(input_line, i32);
    let mut vertices = BTreeMap::<i32, Vec<i32>>::new();
    
    for _ in 0..e as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let inputs = input_line.split(" ").collect::<Vec<_>>();
        let n_1 = parse_input!(inputs[0], i32);
        let n_2 = parse_input!(inputs[1], i32);
        vertices.entry(n_1).or_insert(Vec::new()).push(n_2);
        vertices.entry(n_2).or_insert(Vec::new()).push(n_1);
    }

    let mut visited = BTreeMap::<i32, bool>::new();
    let mut stack = Vec::<i32>::new();
    let mut continents = 0;
    let mut tiles = 0;
    for (vertex, _) in vertices.iter() {
        if !visited.contains_key(vertex) {
            stack.push(*vertex);
            while !stack.is_empty() {
                let current = stack.pop().unwrap();
                if visited.contains_key(&current) {
                    tiles += 1;
                    continue;
                }
                visited.insert(current, true);
                if let Some(neighbours) = vertices.get(&current) {
                    for neighbour in neighbours {
                        if !visited.contains_key(neighbour) {
                            stack.push(*neighbour);
                        }
                    }
                }
            }
            continents += 1;
        }
    }
    
    println!("{} {}", continents, tiles);
}
