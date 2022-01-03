use std::collections::VecDeque;
use std::fmt;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    run(data, 2)
}

fn part_b(data: &str) -> usize {
    run(data, 50)
}

fn run(data: &str, times: usize) -> usize {
    let (enhancer, mut image) = parse_data(data);
    enhance(&mut image, &enhancer, times);
    image.count_lit_pixels()
}

fn enhance(img: &mut Image, enhancer: &Enhancer, times: usize) {
    for _ in 0..times {
        img.enhance(enhancer);
    }
}

fn parse_data(data: &str) -> (Enhancer, Image) {
    let vec = data.split("\n\n").collect::<Vec<&str>>();
    (Enhancer::from(vec[0]), Image::from(vec[1]))
}

fn lit_state_to_char(b: &bool) -> char {
    match b {
        true => '#',
        false => '.',
    }
}

fn char_to_lit_state(c: &char) -> bool {
    match c {
        '#' => true,
        '.' => false,
        _ => panic!("Unrecognized character {}", c),
    }
}

fn lit_state_to_number(b: &bool) -> usize {
    match b {
        true => 1,
        false => 0,
    }
}

#[derive(Debug)]
struct Image {
    // indexed [y][x]
    data: VecDeque<VecDeque<bool>>,
    width: usize,
    height: usize,
    grid_state: bool,
}

struct Enhancer {
    enhancer: Vec<bool>,
}

impl Image {
    fn enhance(&mut self, enhancer: &Enhancer) {
        self.expand();

        let mut flip = Vec::new();

        for y in 0..self.height {
            for x in 0..self.width {
                let idx = self.get_enhancement_idx(x as isize, y as isize);
                if enhancer.enhancer[idx] != self.data[y][x] {
                    flip.push((x, y));
                }
            }
        }

        for (x, y) in flip {
            self.data[y][x] = !self.data[y][x];
        }

        // if grid state is true, next state is from last item in enhancer. If false, first item in enhancer
        self.grid_state = match self.grid_state {
            true => enhancer.enhancer[enhancer.enhancer.len() - 1],
            false => enhancer.enhancer[0],
        };
    }

    fn expand(&mut self) {
        self.width += 2;
        self.height += 2;

        for row in self.data.iter_mut() {
            row.push_front(self.grid_state);
            row.push_back(self.grid_state);
        }

        self.data
            .push_front(VecDeque::from(vec![self.grid_state; self.width]));
        self.data
            .push_back(VecDeque::from(vec![self.grid_state; self.width]));
    }

    fn get_enhancement_idx(&self, center_x: isize, center_y: isize) -> usize {
        let mut idx = 0;

        for y in center_y - 1..=center_y + 1 {
            for x in center_x - 1..=center_x + 1 {
                idx = idx << 1;
                if y < 0 || x < 0 {
                    idx += lit_state_to_number(&self.grid_state);
                } else if y as usize >= self.height || x as usize >= self.width {
                    idx += lit_state_to_number(&self.grid_state);
                } else {
                    idx += lit_state_to_number(&self.data[y as usize][x as usize]);
                }
            }
        }

        idx
    }

    fn count_lit_pixels(&self) -> usize {
        self.data.iter().fold(0, |acc, row| {
            acc + row
                .iter()
                .fold(0, |acc, pixel| acc + lit_state_to_number(pixel))
        })
    }
}

impl From<&str> for Image {
    fn from(s: &str) -> Self {
        let mut height = 0;
        let mut width = 0;
        let mut data = VecDeque::new();

        for line in s.lines() {
            height += 1;
            width = line.len();
            let row = line.chars().map(|c| char_to_lit_state(&c)).collect();
            data.push_back(row);
        }

        Image {
            data: data,
            width: width,
            height: height,
            grid_state: false,
        }
    }
}

impl fmt::Display for Image {
    fn fmt(&self, f: &mut fmt::Formatter<'_>) -> fmt::Result {
        for row in &self.data {
            for pixel in row {
                let result = write!(f, "{}", lit_state_to_char(&pixel));
                if result.is_err() {
                    return result;
                }
            }
            let result = writeln!(f, "");
            if result.is_err() {
                return result;
            }
        }

        fmt::Result::Ok(())
    }
}

impl From<&str> for Enhancer {
    fn from(s: &str) -> Self {
        Enhancer {
            enhancer: s.chars().map(|c| char_to_lit_state(&c)).collect(),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 35);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 3351);
    }
}
