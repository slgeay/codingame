use std::io;

macro_rules! parse_input {
    ($x:expr, $t:ident) => ($x.trim().parse::<$t>().unwrap())
}

struct State {
    zones: [char; 30],
    pointer: usize,
    created_text: String,
    instructions: String,
}

impl State {
    fn new() -> Self {
        State {
            zones: [' '; 30],
            pointer: 0,
            created_text: String::new(),
            instructions: String::new(),
        }
    }

    fn left(&mut self, steps: usize) {
        for _ in 0..steps {
            if self.pointer == 0 {
                self.pointer = self.zones.len() - 1;
            } else {
                self.pointer -= 1;
            }
            self.instructions.push('<');
        }
    }
    
    fn right(&mut self, steps: usize) {
        for _ in 0..steps {
            self.pointer = (self.pointer + 1) % self.zones.len();
            self.instructions.push('>');
        }
    }

    fn increment(&mut self, steps: i32) {
        for _ in 0..steps {
            self.zones[self.pointer] = if self.zones[self.pointer] == ' ' {
                'A'
            } else if self.zones[self.pointer] == 'Z' {
                ' '
            } else {
                (self.zones[self.pointer] as u8 + 1) as char
            };
            self.instructions.push('+');
        }
    }

    fn decrement(&mut self, steps: i32) {
        for _ in 0..steps {
            self.zones[self.pointer] = if self.zones[self.pointer] == ' ' {
                'Z'
            } else if self.zones[self.pointer] == 'A' {
                ' '
            } else {
                (self.zones[self.pointer] as u8 - 1) as char
            };
            self.instructions.push('-');
        }
    }

    fn trigger(&mut self) {
        self.created_text.push(self.zones[self.pointer]);
        self.instructions.push('.');
    }

    fn display(&self) {
        println!("Zones: {:?}", self.zones);
        println!("Current Pointer: {}", self.pointer);
        println!("Created Text: \"{}\"", self.created_text);
        println!("Instructions: {}", self.instructions);
    }
    
    fn move_to_optimal_zone(&mut self, target_char: char) {
        let target_pos = pos(target_char);
        let mut best_total_instructions = i32::MAX;
        let mut best_zone = self.pointer;
    
        for zone in 0..self.zones.len() {
            let current_pos = pos(self.zones[zone]);
            let char_distance = ((target_pos as i32 - current_pos as i32 + 27) % 27).min(((current_pos as i32 - target_pos as i32 + 27) % 27));
    
            // Calculate movement instructions
            let right_steps = if zone >= self.pointer { zone - self.pointer } else { self.zones.len() + zone - self.pointer };
            let left_steps = if self.pointer >= zone { self.pointer - zone } else { self.zones.len() + self.pointer - zone };
            let movement_instructions = right_steps.min(left_steps);
    
            // Calculate total instructions (movement + character adjustment)
            let total_instructions = movement_instructions + char_distance as usize;
    
            if total_instructions < best_total_instructions as usize {
                best_total_instructions = total_instructions as i32;
                best_zone = zone;
            }
        }
    
        // Once the best zone is determined, move to it efficiently
        let right_steps = if best_zone >= self.pointer { best_zone - self.pointer } else { self.zones.len() + best_zone - self.pointer };
        let left_steps = if self.pointer >= best_zone { self.pointer - best_zone } else { self.zones.len() + self.pointer - best_zone };
    
        if right_steps.min(left_steps) == right_steps {
            self.right(right_steps);
        } else {
            self.left(left_steps);
        }
    }    
    
    fn optimize_movement(&mut self, target_char: char) {
        self.move_to_optimal_zone(target_char);
        let current_char = self.zones[self.pointer];
        let target_pos = pos(target_char);
        let current_pos = pos(current_char);

        // Calculate the shortest path to the target character
        let forward_distance = if target_pos >= current_pos {
            target_pos as i32 - current_pos as i32
        } else {
            27 + target_pos as i32 - current_pos as i32
        };

        let backward_distance = if current_pos >= target_pos {
            current_pos as i32 - target_pos as i32
        } else {
            27 + current_pos as i32 - target_pos as i32
        };

        // Decide whether to increment or decrement based on the shortest path
        if forward_distance <= backward_distance {
            self.increment(forward_distance);
        } else {
            self.decrement(backward_distance);
        }

        self.trigger();
    }
}

fn pos(char: char) -> u8 {
    if char == ' ' { 0 } else { (char as u8 - 'A' as u8) + 1 }
}

fn main() {
    let mut input_line = String::new();
    io::stdin().read_line(&mut input_line).unwrap();
    let magic_phrase = input_line.trim_matches('\n').to_string();

    let mut state = State::new();

    for target_char in magic_phrase.chars() {
        state.optimize_movement(target_char);
    }

    println!("{}", state.instructions);
}

#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_increment() {
        let mut state = State::new();
        state.increment(3);
        assert_eq!(state.zones[state.pointer], 'C');
    }

    #[test]
    fn test_decrement() {
        let mut state = State::new();
        state.zones[state.pointer] = 'D';
        state.decrement(3);
        assert_eq!(state.zones[state.pointer], 'A');
    }

    #[test]
    fn test_optimize_movement() {
        let mut state = State::new();
        state.optimize_movement('D');
        assert_eq!(state.created_text, "D");
        
        assert!(state.instructions.len() <= 5, "Instructions should be optimized");
    }

    #[test]
    fn test_full_text() {
        let mut state = State::new();
        let input_text = "HELLO WORLD";
        for char in input_text.chars() {
            state.optimize_movement(char);
        }
        
        println!("{}", state.instructions);
        println!("{}", state.instructions.len());
        assert_eq!(state.created_text, input_text);
        assert!(state.instructions.len() <= 52, "Instructions should be optimized");
    }

    #[test]
    fn test_long_spell() {
        let mut state = State::new();
        let input_text = "THREE RINGS FOR THE ELVEN KINGS UNDER THE SKY SEVEN FOR THE DWARF LORDS IN THEIR HALLS OF STONE NINE FOR MORTAL MEN DOOMED TO DIE ONE FOR THE DARK LORD ON HIS DARK THRONEIN THE LAND OF MORDOR WHERE THE SHADOWS LIE ONE RING TO RULE THEM ALL ONE RING TO FIND THEM ONE RING TO BRING THEM ALL AND IN THE DARKNESS BIND THEM IN THE LAND OF MORDOR WHERE THE SHADOWS LIE";
        for char in input_text.chars() {
            state.optimize_movement(char);
        }
        
        println!("{}", state.instructions);
        println!("{}", state.instructions.len());
        assert_eq!(state.created_text, input_text);
        assert!(state.instructions.len() <= 1479, "Instructions should be optimized");
    }
}
