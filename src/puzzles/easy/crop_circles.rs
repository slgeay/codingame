use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let instructions = input_line.trim_matches('\n').to_string();
    let mut field = [[true;19];25];

    for mut instruction in instructions.split(' ') {
        let mut mode = 0;
        if instruction.starts_with("PLANTMOW") {
            mode = 2;
            instruction = &instruction[8..];
        } else if instruction.starts_with("PLANT") {
            mode = 1;
            instruction = &instruction[5..];
        }

        let mut chrs = instruction.chars();
        let x = (chrs.next().unwrap() as usize)-('a' as usize);
        let y = (chrs.next().unwrap() as usize)-('a' as usize);
        let r = parse_input!(chrs.as_str(), usize) as f32 / 2.0;
        for j in 0..25 {
            for i in 0..19 {
                if (((x-i).pow(2)+(y-j).pow(2)) as f32).sqrt() <= r {
                    match mode {
                        0 => field[j][i] = false,
                        1 => field[j][i] = true,
                        2 => field[j][i] = !field[j][i],
                        _ => ()
                    }
                }
            }
        }
    }

    for j in 0..25 {
        for i in 0..19 {
            print!(
                "{}", 
                match field[j][i] {
                    true => "{}",
                    false => "  "
                }
            )
        }
        println!()
    }
}
