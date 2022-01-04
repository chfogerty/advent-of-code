use std::collections::HashMap;

const INPUT: &str = include_str!("input.txt");
const ROLL_FREQUENCIES: [(u16, usize); 7] =
    [(3, 1), (4, 3), (5, 6), (6, 7), (7, 6), (8, 3), (9, 1)];

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_a(data: &str) -> usize {
    let mut players = parse_data(data);
    let mut die = DeterministicDie::new();

    for player in 0..=1 {
        players[player].score = 1000;
    }

    let mut current_player: isize = 0;
    while !players[current_player as usize].take_turn(&mut die) {
        current_player = (current_player - 1) * -1;
    }

    current_player = (current_player - 1) * -1;
    die.rolls * (1000 - players[current_player as usize].score) as usize
}

fn part_b(data: &str) -> usize {
    let players = parse_data(data);

    let mut mem = HashMap::new();

    let (wins_1, wins_2) = wins(
        (players[0].position, 21),
        (players[1].position, 21),
        &mut mem,
    );

    // println!("{:#?}", mem);

    wins_1.max(wins_2)
}

fn wins(
    player_1: (u16, i16),
    player_2: (u16, i16),
    mem: &mut HashMap<((u16, i16), (u16, i16)), (usize, usize)>,
) -> (usize, usize) {
    if player_2.1 <= 0 {
        return (0, 1);
    }

    let mut wins_1 = 0;
    let mut wins_2 = 0;

    for (roll, frequency) in ROLL_FREQUENCIES {
        let mut next_space = player_1.0 + roll;

        if next_space > 10 {
            next_space -= 10;
        }

        let updated_p1 = (next_space, player_1.1 - next_space as i16);
        if !mem.contains_key(&(player_2, updated_p1)) {
            let wins = wins(player_2, updated_p1, mem);

            mem.insert((player_2, updated_p1), wins);
        }

        let (w2, w1) = mem.get(&(player_2, updated_p1)).unwrap();

        wins_1 += frequency * w1;
        wins_2 += frequency * w2;
    }

    (wins_1, wins_2)
}

fn parse_data(data: &str) -> Vec<Player> {
    data.lines().map(|s| Player::from(s)).collect()
}

trait Die {
    fn roll(&mut self) -> u16;
    fn take_turn(&mut self) -> u16;
}

struct DeterministicDie {
    result_memory: HashMap<u16, u16>,
    // actually next number - 1, since it's 0-99 and dice rolls are 1-100
    next_number: u16,
    rolls: usize,
}

impl Die for DeterministicDie {
    // returns 1 - 100
    fn roll(&mut self) -> u16 {
        let ret = self.next_number;
        self.next_number = (self.next_number + 1) % 100;
        self.rolls += 1;
        return ret + 1;
    }

    fn take_turn(&mut self) -> u16 {
        let spaces_moved = self.roll() + self.roll() + self.roll();

        let result = self.result_memory.get(&spaces_moved);
        match result {
            Option::Some(&n) => n,
            Option::None => {
                let simple_result = spaces_moved % 10;
                self.result_memory.insert(spaces_moved, simple_result);
                simple_result
            }
        }
    }
}

impl DeterministicDie {
    fn new() -> Self {
        DeterministicDie {
            result_memory: HashMap::new(),
            next_number: 0,
            rolls: 0,
        }
    }
}

struct Player {
    position: u16,
    score: i16,
}

impl Player {
    fn take_turn(&mut self, die: &mut impl Die) -> bool {
        let spaces_moved = die.take_turn();
        let mut landed_space = self.position + spaces_moved;
        if landed_space > 10 {
            landed_space -= 10;
        }

        self.position = landed_space;
        self.score -= landed_space as i16;

        return self.score <= 0;
    }
}

impl From<&str> for Player {
    fn from(s: &str) -> Self {
        Player {
            position: s.split(" ").last().unwrap().parse::<u16>().unwrap(),
            score: 0,
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 739785);
    }

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 444356092776315);
    }
}
