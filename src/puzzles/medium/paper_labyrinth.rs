use std::{cmp::Reverse, collections::BinaryHeap, io};

#[derive(Clone, Copy)]
enum Direction {
    Bottom = 0x1,
    Left = 0x2,
    Top = 0x4,
    Right = 0x8,
}

impl Direction {
    fn values() -> Vec<Direction> {
        vec![
            Direction::Top,
            Direction::Right,
            Direction::Bottom,
            Direction::Left,
        ]
    }

    fn iter() -> impl Iterator<Item = Direction> {
        Direction::values().into_iter()
    }
}

#[derive(Clone, Copy, Debug, PartialEq, PartialOrd, Eq, Ord)]
struct Vec2 {
    x: usize,
    y: usize,
}

impl Vec2 {
    fn new(x: usize, y: usize) -> Vec2 {
        Vec2 { x, y }
    }

    fn new_from_stdin() -> Vec2 {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let coords = input_line.split(' ').collect::<Vec<_>>();
        Vec2 {
            x: coords[0].trim().parse().unwrap(),
            y: coords[1].trim().parse().unwrap(),
        }
    }

    fn neighbor(&self, dir: Direction) -> Vec2 {
        match dir {
            Direction::Top => Vec2::new(self.x, self.y - 1),
            Direction::Right => Vec2::new(self.x + 1, self.y),
            Direction::Bottom => Vec2::new(self.x, self.y + 1),
            Direction::Left => Vec2::new(self.x - 1, self.y),
        }
    }

    fn distance(&self, to: Vec2) -> usize {
        let dx = (self.x as i32 - to.x as i32).unsigned_abs() as usize;
        let dy = (self.y as i32 - to.y as i32).unsigned_abs() as usize;
        dx + dy
    }
}

struct Cell {
    coord: Vec2,
    walls: u8,
}

impl Cell {
    fn new(x: usize, y: usize, c: char) -> Cell {
        Cell {
            coord: Vec2::new(x, y),
            walls: c.to_digit(16).unwrap() as u8,
        }
    }

    fn has_wall(&self, dir: Direction) -> bool {
        self.walls & dir as u8 != 0
    }

    fn neighbor(&self, dir: Direction) -> Option<Vec2> {
        if self.has_wall(dir) {
            return None;
        }
        Some(self.coord.neighbor(dir))
    }
}

// Display the cell as a character
// We use lines to represent the paths we can take (without walls)
impl std::fmt::Display for Cell {
    fn fmt(&self, f: &mut std::fmt::Formatter<'_>) -> std::fmt::Result {
        let c = match self.walls {
            0x0 => '┼',
            0x1 => '┴',
            0x2 => '├',
            0x3 => '└',
            0x4 => '┬',
            0x5 => '─',
            0x6 => '┌',
            0x7 => '╶',
            0x8 => '┤',
            0x9 => '┘',
            0xa => '│',
            0xb => '╵',
            0xc => '┐',
            0xd => '╴',
            0xe => '╷',
            0xf => ' ',
            _ => unreachable!(),
        };
        write!(f, "{}", c)
    }
}

struct Labyrinth {
    cells: Vec<Vec<Cell>>,
    size: Vec2,
}

impl Labyrinth {
    fn new(size: Vec2) -> Labyrinth {
        Labyrinth {
            cells: Vec::new(),
            size,
        }
    }

    fn new_from_stdin() -> Labyrinth {
        let size = Vec2::new_from_stdin();
        let mut lab = Labyrinth::new(size);

        for y in 0..lab.size.y {
            let mut row = Vec::<Cell>::new();
            let mut input_line = String::new();
            io::stdin().read_line(&mut input_line).unwrap();
            let l = input_line.trim().to_string();
            for (x, c) in l.chars().enumerate() {
                row.push(Cell::new(x, y, c));
            }
            lab.cells.push(row);
        }

        lab
    }

    fn get_cell(&self, coord: Vec2) -> &Cell {
        &self.cells[coord.y][coord.x]
    }

    // Breadth-first search
    // We use a queue to visit all the neighbors of a cell before moving to the next one
    // This way, we ensure to find the shortest path
    // We also keep track of the previous cell of each visited cell to reconstruct the path
    // This algorithm is not optimal, but it's easy to implement and works well for small labyrinth
    fn breadth_first_search(&self, from: Vec2, to: Vec2) -> Vec<Vec2> {
        let mut path = Vec::<Vec2>::new();

        let mut queue = Vec::<Vec2>::new();
        queue.push(from);

        // Normally we track visited cells, but we can save space by using the previous cell to know if we visited it
        let mut prev = vec![vec![None; self.size.x]; self.size.y];

        // We mark the starting cell as visited by setting its previous cell to itself
        prev[from.y][from.x] = Some(from);

        let mut steps = 0;

        while !queue.is_empty() {
            steps += 1;
            let current = queue.remove(0);

            // We found the path, let's reconstruct it
            if current == to {
                let mut current = to;
                while current != from {
                    path.push(current);
                    current = prev[current.y][current.x].unwrap();
                }
                path.reverse();
                break;
            }

            // Else, visit neighbors not visited yet, and update the queue
            let cell = self.get_cell(current);
            Direction::iter().for_each(|dir| {
                if let Some(neighbor) = cell.neighbor(dir) {
                    if prev[neighbor.y][neighbor.x].is_some() {
                        return;
                    }
                    queue.push(neighbor);
                    prev[neighbor.y][neighbor.x] = Some(current);
                }
            });
        }

        eprintln!("Breadth-First Search : {} steps", steps);

        path
    }

    // Best-first search
    // We use a priority queue to visit the cell closest to the target first
    // This algorithm is more efficient than the breadth-first search, as it explores the most promising path first
    fn best_first_search(&self, from: Vec2, to: Vec2) -> Vec<Vec2> {
        let mut path = Vec::<Vec2>::new();

        let mut priority_queue = BinaryHeap::new();

        // BinaryHeap is a max-heap, so we need to reverse the order to have a min-heap
        // We use the distance already walked plus the shortest distance to the target possible as the priority
        // We also keep that walked distance to calculate future priorities
        priority_queue.push((Reverse(0 + from.distance(to)), 0, from));

        let mut prev = vec![vec![None; self.size.x]; self.size.y];
        // This time we need to track the distance walked to the cell
        prev[from.y][from.x] = Some(from);

        let mut steps = 0;

        while let Some((_priority, walked_dist, current)) = priority_queue.pop() {
            steps += 1;

            // We found the path, let's reconstruct it
            if current == to {
                let mut current = to;
                while current != from {
                    path.push(current);
                    current = prev[current.y][current.x].unwrap();
                }
                path.reverse();
                break;
            }

            // Else, visit neighbors not visited yet, and update the queue
            let cell = self.get_cell(current);
            let walked_dist = walked_dist + 1;
            Direction::iter().for_each(|dir| {
                if let Some(neighbor) = cell.neighbor(dir) {
                    if prev[neighbor.y][neighbor.x].is_some() {
                        return;
                    }
                    priority_queue.push((
                        Reverse(walked_dist + current.distance(to)),
                        walked_dist,
                        neighbor,
                    ));
                    prev[neighbor.y][neighbor.x] = Some(current);
                }
            });
        }

        eprintln!("Best-First Search : {} steps", steps);

        path
    }

    fn distance(&self, from: Vec2, to: Vec2) -> usize {
        let breadth_path = self.breadth_first_search(from, to);
        let best_path = self.best_first_search(from, to);

        // The two paths might not be the same, but they should have the same length
        assert_eq!(breadth_path.len(), best_path.len());

        best_path.len()
    }
}

impl std::fmt::Display for Labyrinth {
    fn fmt(&self, f: &mut std::fmt::Formatter) -> std::fmt::Result {
        for y in 0..self.size.y {
            for x in 0..self.size.x {
                write!(f, "{} ", self.cells[y][x])?;
            }
            writeln!(f)?;
            writeln!(f)?;
        }
        Ok(())
    }
}

fn main() {
    let start = Vec2::new_from_stdin();
    let rabbit = Vec2::new_from_stdin();
    let labyrinth = Labyrinth::new_from_stdin();

    eprintln!("Start: {:?} ; Rabbit: {:?}", start, rabbit);
    eprintln!("{}", labyrinth);

    println!(
        "{} {}",
        labyrinth.distance(start, rabbit),
        labyrinth.distance(rabbit, start)
    );
}
