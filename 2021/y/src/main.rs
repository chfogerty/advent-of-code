const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
}

fn part_a(data: &str) -> usize {
    let mut steps = 0;
    let mut board = parse_data(data);

    while update(&mut board) {
        steps += 1;
    }

    steps + 1
}

fn parse_data(data: &str) -> Vec<Vec<char>> {
    data.lines().map(|line| line.chars().collect()).collect()
}

fn update(board: &mut Vec<Vec<char>>) -> bool {
    let width = board[0].len();
    let height = board.len();

    let mut board_updated = false;

    // east
    for row in board.into_iter() {
        let to_update: Vec<_> = (0..width)
            .filter(|&idx| row[idx] == '>' && row[(idx + 1) % width] == '.')
            .collect();

        board_updated = board_updated || !to_update.is_empty();

        for idx in to_update {
            row[idx] = '.';
            row[(idx + 1) % width] = '>';
        }
    }

    for col in 0..width {
        let to_update: Vec<_> = (0..height)
            .filter(|&idx| board[idx][col] == 'v' && board[(idx + 1) % height][col] == '.')
            .collect();

        board_updated = board_updated || !to_update.is_empty();

        for idx in to_update {
            board[idx][col] = '.';
            board[(idx + 1) % height][col] = 'v';
        }
    }

    board_updated
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 58);
    }
}
