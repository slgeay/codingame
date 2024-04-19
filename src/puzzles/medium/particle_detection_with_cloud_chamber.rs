
use std::f64::consts::PI;
use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => {
        $x.trim().parse::<$t>().unwrap()
    };
}

#[derive(Clone, Copy)]
struct Point {
    x: f64,
    y: f64,
}

// Line equation: ax + by = c
struct Line {
    a: f64,
    b: f64,
    c: f64,
}

fn find_perpendicular_bisector(p1: Point, p2: Point) -> Line {
    let midpoint = Point {
        x: (p1.x + p2.x) / 2.0,
        y: (p1.y + p2.y) / 2.0,
    };
    let slope = if (p2.x - p1.x).abs() < 1e-6 {
        PI / 2.0
    } else {
        (p2.y - p1.y) / (p2.x - p1.x)
    };

    let a = -1.0 / slope;
    let b = -1.0;
    let c = midpoint.y - a * midpoint.x;
    Line { a, b, c }
}

fn solve_linear_equations(f: Line, g: Line) -> Option<Point> {
    let det = f.a * g.b - g.a * f.b;
    if det.abs() < 1e-6 {
        return None;
    }
    let x = (f.b * g.c - g.b * f.c) / det;
    let y = (g.a * f.c - f.a * g.c) / det;
    Some(Point { x, y })
}

fn compute_radius(ascii_art: &[Vec<char>]) -> Option<i32> {
    let mut points = vec![];

    // Find the points on the circumference of the circle
    for (i, line) in ascii_art.iter().enumerate() {
        for (j, char) in line.iter().enumerate() {
            if *char == ' ' {
                points.push(Point {
                    x: j as f64,
                    y: i as f64,
                });
                // Only take the first point of each line to ensure their order on the circumference
                break;
            }
        }
    }

    // Select three points from the list
    if points.len() < 3 {
        panic!("Not enough points to define a circle");
    }
    let p1 = points[0];
    let p2 = points[points.len() / 2];
    let p3 = points[points.len() - 1];

    // Calculate the perpendicular bisectors
    let f = find_perpendicular_bisector(p1, p2);
    let g = find_perpendicular_bisector(p2, p3);

    // Find the intersection point (center of the circle)
    match solve_linear_equations(f, g) {
        Some(center) => {
            let radius = ((p1.x - center.x).powi(2) + (p1.y - center.y).powi(2)).sqrt();
            Some((radius / 10.).round() as i32 * 10)
        }
        None => None,
    }
}

fn find_particle(b: f64, v: f64, radius: i32) -> Option<String> {
    let c = 299792458.0;
    let gamma = 1.0 / (1.0 - v.powi(2)).sqrt();
    let g = 1e6 * gamma * v / (b * radius as f64 * c);

    let mut best_particle: Option<(String, f64)> = None;
    for (symbol, q, m) in [
        ("e-", -1, 0.511),
        ("p+", 1, 938.0),
        ("alpha", 2, 3727.0),
        ("pi+", 1, 140.0)
    ] {
        let g_p = (q as f64).abs() / m;
        let diff = (g - g_p).abs();
        if diff < 0.5 {
            match best_particle {
                Some((_, best_diff)) => {
                    if diff < best_diff {
                        best_particle = Some((symbol.to_string(), diff));
                    }
                }
                None => best_particle = Some((symbol.to_string(), diff)),
            }
        }
    }
    best_particle.map(|(symbol, _)| symbol)
}

fn main() {
    // Input
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let w = parse_input!(input_line, i32); // width of ASCII-art picture (one meter per column)
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let h = parse_input!(input_line, i32); // height of ASCII-art picture (one meter per line)
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let b = parse_input!(input_line, f64); // strengh of magnetic field (tesla)
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let v = parse_input!(input_line, f64); // speed of the particle (speed-of-light unit)
    let mut ascii_art = vec![vec![]; h as usize];
    for i in 0..h as usize {
        let mut input_line = String::new();
        io::stdin().read_line(&mut input_line).unwrap();
        let line = input_line.trim_matches('\n').to_string(); // lines of ASCII-art picture
        ascii_art[i] = line.chars().collect();
    }

    match compute_radius(&ascii_art) {
        None => println!("n0 inf"),
        Some(radius) => {
            match find_particle(b, v, radius) {
                Some(symbol) => println!("{} {}", symbol, radius),
                None => println!("I just won the Nobel prize in physics !"),
            }
        }    
    }
}
