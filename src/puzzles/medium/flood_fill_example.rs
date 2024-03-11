use std::{io,collections::{HashMap, hash_map::Entry::{Vacant, Occupied}}};

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

// Record towers ID and use Unique IDs instead
struct TowersRegistry {
    uid_to_id: HashMap::<char, char>,
    next_uid: char
}

impl TowersRegistry {
    fn new() -> TowersRegistry {
        TowersRegistry { uid_to_id: HashMap::<char, char>::new(), next_uid: 'A' }
    }

    fn add(&mut self, id:char) -> char {
        let uid = self.next_uid;
        self.uid_to_id.insert(uid, id);
        self.next_uid = (uid as u8 + 1) as char;
        uid
    }

    fn get(&self, uid:&char) -> char {
        self.uid_to_id[uid]
    }
}

// Handle grid logic
struct Grid {
    grid: Vec::<String>
}

impl Grid {
    fn new() -> Grid {
        Grid { grid: Vec::<String>::new() }
    }

    fn push(&mut self, line: String) {
        self.grid.push(line)
    }

    fn get(&self, x: usize, y: usize) -> char {
        self.grid[y].chars().nth(x).unwrap()
    }

    fn replace(&mut self, x: usize, y: usize, c: char) {
        self.grid[y].replace_range(x..x+1, c.to_string().as_str());
    }

    fn get_line(&self, y: usize) -> &String {
        &self.grid[y]
    }
}

// Handle troops logic, notably simultaneous arrivals
struct Troops {
    troops: HashMap::<(usize, usize), char>
}

impl Troops {
    fn new() -> Troops {
        Troops { troops:HashMap::<(usize, usize), char>::new() }
    }

    fn push(&mut self, x: usize, y: usize, uid: char) {
        match self.troops.entry((x,y)) {
            Vacant(v) => {
                v.insert(uid);
            },
            Occupied(mut o) => {
                if *o.get() != uid {
                    o.insert('+');
                }
            }
        };
    }

    fn is_empty(&self) -> bool {
        self.troops.is_empty()
    }
}

fn main() {
    // Read inputs
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let w = parse_input!(input_line, usize);
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let h = parse_input!(input_line, usize);

    let mut grid = Grid::new();
    let mut towers = TowersRegistry::new();
    let mut current_troops = Troops::new();

    // Read the input grid
    for y in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let line = input_line.trim_matches('\n').to_string();
        let mut new_line = String::new();

        for (x, c) in line.chars().enumerate() {
            if c != '.' && c != '#' {
                // Register the tower and its current troops
                let uid = towers.add(c);
                new_line.push(uid);
                current_troops.push(x, y, uid);
            } else {
                new_line.push(c);
            }
        }
        grid.push(new_line);
    }

    // Deploy troops by waves    
    while !current_troops.is_empty() {
        let mut next_troops = Troops::new();

        // Compute next troops (Manhattan geometry)
        for ((x, y), t) in current_troops.troops {
            if x > 0 && grid.get(x - 1, y) == '.' {
                next_troops.push(x - 1, y, t);
            }
            if x < w - 1 && grid.get(x + 1, y) == '.' {
                next_troops.push(x + 1, y, t);
            }
            if y > 0 && grid.get(x, y - 1) == '.' {
                next_troops.push(x, y - 1, t);
            }
            if y < h - 1 && grid.get(x, y + 1)== '.' {
                next_troops.push(x, y + 1, t);
            }
        }
        
        // Deploy troops
        for ((x, y), uid) in next_troops.troops.iter() {
            grid.replace(*x, *y, *uid);
        }
 
        // Prepare next wave
        current_troops = next_troops;
    }
    
    // Replace UIDs with actual IDs and print
    for y in 0..h as usize {
        let line: String = grid
            .get_line(y)
            .chars()
            .map(|c: char| if c == '.' || c == '#' || c == '+' { c } else { towers.get(&c) }).
            collect();
        println!("{}", line);
    }
}
