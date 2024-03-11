use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

macro_rules! eprint_grid {
    ($h:expr, $grid:expr) => {
        for i in 0..$h as usize {
            eprintln!("{}", $grid[i]);
        }
        eprintln!("");
    };
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let w = parse_input!(input_line, i32);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let h = parse_input!(input_line, i32);

    let mut grid = Vec::<String>::new();
    let mut troops = Vec::<(i32, i32, char)>::new();

    let mut towers = std::collections::HashMap::<char, char>::new();
    let mut next_tower = 'A';


    for i in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let line = input_line.trim_matches('\n').to_string();
        let mut new_line = String::new();
        for (j, c) in line.chars().enumerate() {
            if c != '.' && c != '#' {
                towers.insert(next_tower, c);
                new_line.push(next_tower);
                troops.push((j as i32, i as i32, next_tower));
                next_tower = (next_tower as u8 + 1) as char;
            } else {
                new_line.push(c);
            }
        }
        grid.push(new_line);
    }

    while !troops.is_empty() {
        eprint_grid!(h, &grid);
        let mut new_troops = Vec::<(i32, i32, char)>::new();
        for (x, y, t) in troops {
            if x > 0 && grid[y as usize].chars().nth(x as usize - 1).unwrap() == '.' {
                new_troops.push((x - 1, y, t));
            }
            if x < w - 1 && grid[y as usize].chars().nth(x as usize + 1).unwrap() == '.' {
                new_troops.push((x + 1, y, t));
            }
            if y > 0 && grid[y as usize - 1].chars().nth(x as usize).unwrap() == '.' {
                new_troops.push((x, y - 1, t));
            }
            if y < h - 1 && grid[y as usize + 1].chars().nth(x as usize).unwrap() == '.' {
                new_troops.push((x, y + 1, t));
            }
        }

        new_troops.sort();
        new_troops.dedup();
        
        for (x, y, t) in new_troops.iter() {
            if new_troops.iter().filter(|(x2, y2, _)| x == x2 && y == y2).count() > 1 {
                grid[*y as usize].replace_range(*x as usize..*x as usize + 1, "+");
            } else {
                grid[*y as usize].replace_range(*x as usize..*x as usize + 1, t.to_string().as_str());
            }
        }
 
        troops = new_troops;
    }
    eprint_grid!(h, &grid);

    for (k, v) in towers.iter() {
        eprintln!("{} {}", k, v);
    }
    eprintln!("");
    
    for i in 0..h as usize {
        grid[i] = grid[i].chars().map(|c: char| if c == '.' || c == '#' || c == '+' { c } else { towers[&c] }).collect();
        println!("{}", grid[i]);
    }
}
