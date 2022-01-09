use std::collections::HashMap;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    let data = parse_data(data);
    let commands = data.iter().rev().collect::<Vec<&Command>>();

    let mut states = HashMap::new();

    for command in commands {
        for x in command.x.0.max(-50)..=command.x.1.min(50) {
            for y in command.y.0.max(-50)..=command.y.1.min(50) {
                for z in command.z.0.max(-50)..=command.z.1.min(50) {
                    if !states.contains_key(&(x, y, z)) {
                        states.insert((x, y, z), command.state);
                    }
                }
            }
        }
    }

    states.values().filter(|v| **v).count()
}

fn part_b(data: &str) -> isize {
    let commands = parse_data(data);

    let mut cores: Vec<Command> = Vec::new();
    for command in commands {
        let mut toadd = match command.state {
            true => vec![command],
            false => Vec::new(),
        };

        for core in &cores {
            let intersection = core.intersect(&command);
            match intersection {
                Some(cuboid) => toadd.push(cuboid),
                None => {}
            };
        }

        cores.append(&mut toadd);
    }

    cores.iter().map(|cmd| cmd.count()).sum()
}

fn parse_data(data: &str) -> Vec<Command> {
    data.lines().map(|line| Command::from(line)).collect()
}

fn range_intersect(left: (isize, isize), right: (isize, isize)) -> bool {
    return !(left.1 < right.0 || right.1 < left.0);
}

#[derive(Clone, Copy, Debug)]
struct Command {
    x: (isize, isize),
    y: (isize, isize),
    z: (isize, isize),
    state: bool,
}

impl Command {
    fn count(&self) -> isize {
        match self.state {
            true => self.volume(),
            false => -1 * self.volume(),
        }
    }

    fn intersect(&self, other: &Command) -> Option<Command> {
        if range_intersect(self.x, other.x)
            && range_intersect(self.y, other.y)
            && range_intersect(self.z, other.z)
        {
            return Some(Command {
                x: (self.x.0.max(other.x.0), self.x.1.min(other.x.1)),
                y: (self.y.0.max(other.y.0), self.y.1.min(other.y.1)),
                z: (self.z.0.max(other.z.0), self.z.1.min(other.z.1)),
                state: !self.state,
            });
        }

        None
    }

    fn volume(&self) -> isize {
        let x = self.x.1 - self.x.0 + 1;
        let y = self.y.1 - self.y.0 + 1;
        let z = self.z.1 - self.z.0 + 1;

        x * y * z
    }
}

impl From<&str> for Command {
    fn from(s: &str) -> Self {
        let split = s.split(" ").collect::<Vec<&str>>();
        let state = match split[0] {
            "on" => true,
            "off" => false,
            _ => panic!("Unknown state {}", split[0]),
        };

        let ranges = split[1]
            .split(",")
            .map(|raw_range| raw_range[2..].split(".."))
            .map(|range| {
                range
                    .map(|n| n.parse::<isize>().unwrap())
                    .collect::<Vec<isize>>()
            })
            .collect::<Vec<Vec<isize>>>();

        let x = (ranges[0][0], ranges[0][1]);
        let y = (ranges[1][0], ranges[1][1]);
        let z = (ranges[2][0], ranges[2][1]);

        Command {
            x: (x.0.min(x.1), x.0.max(x.1)),
            y: (y.0.min(y.1), y.0.max(y.1)),
            z: (z.0.min(z.1), z.0.max(z.1)),
            state: state,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT1: &str = include_str!("test_input1.txt");
    const TEST_INPUT2: &str = include_str!("test_input2.txt");
    const TEST_INPUT3: &str = include_str!("test_input3.txt");

    #[test]
    fn test_a1() {
        assert_eq!(part_a(TEST_INPUT1), 590784);
    }

    #[test]
    fn test_a2() {
        assert_eq!(part_a(TEST_INPUT2), 39);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT3), 2758514936282235);
    }

    #[test]
    fn test_b2() {
        assert_eq!(part_b(TEST_INPUT2), 39);
    }
}
