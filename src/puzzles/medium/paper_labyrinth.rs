use std::io;

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

#[derive(Clone, Copy, Debug, PartialEq)]
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
    fn pathfinding(&self, from: Vec2, to: Vec2) -> Vec<Vec2> {
        let mut path = Vec::<Vec2>::new();

        let mut visited = vec![vec![false; self.size.x]; self.size.y];
        let mut queue = Vec::<Vec2>::new();
        let mut prev = vec![vec![None; self.size.x]; self.size.y];

        queue.push(from);
        visited[from.y][from.x] = true;

        while !queue.is_empty() {
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
                    if visited[neighbor.y][neighbor.x] {
                        return;
                    }
                    queue.push(neighbor);
                    visited[neighbor.y][neighbor.x] = true;
                    prev[neighbor.y][neighbor.x] = Some(current);
                }
            });
        }

        path
    }

    fn distance(&self, from: Vec2, to: Vec2) -> usize {
        let path = self.pathfinding(from, to);
        eprintln!("{:?}", path);
        path.len()
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

    eprintln!("{:?} {:?}", start, rabbit);
    eprintln!("{}", labyrinth);

    println!(
        "{} {}",
        labyrinth.distance(start, rabbit),
        labyrinth.distance(rabbit, start)
    );
}
