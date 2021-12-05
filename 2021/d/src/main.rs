use std::fs::File;
use std::io::{BufRead, BufReader};

fn main() {
    let file = File::open("input.txt").expect("[ ERROR ] Failed to open file!");
    let mut reader = BufReader::new(file);

    let mut boards: Vec<Board> = Vec::new();
    let mut won: Vec<bool> = Vec::new();
    let mut called_numbers_str: String = String::new();

    reader.read_line(&mut called_numbers_str).unwrap();
    let called_numbers = called_numbers_str.split(",");

    let mut fill_x: usize;
    let mut fill_y: usize = 0;

    // build the boards
    for line_result in reader.lines() {
        fill_x = 0;
        let line = line_result.unwrap();
        if line.len() == 0 {
            boards.push(Board::new());
            won.push(false);
            fill_y = 0;
        } else {
            let board_numbers = line.split(' ');
            for board_number in board_numbers {
                match board_number.trim().parse::<u32>() {
                    Err(_e) => {}
                    Ok(n) => {
                        boards
                            .last_mut()
                            .unwrap()
                            .set_square_number(fill_x, fill_y, n);

                        fill_x += 1;
                    }
                }
            }
            fill_y += 1;
        }
    }

    // call the numbers
    let mut first_winner_found = false;
    let mut last_winner_idx: usize = 0;
    let mut last_winner_score: u32 = 0;
    for number in called_numbers {
        let n = number.trim().parse::<u32>().unwrap();

        for board_idx in 0..boards.len() {
            if boards[board_idx].call(&n) {
                if !first_winner_found {
                    println!(
                        "First winner: {} Score: {}",
                        board_idx,
                        boards[board_idx].score(&n)
                    );
                    first_winner_found = true;
                }

                if !won[board_idx] {
                    last_winner_idx = board_idx;
                    last_winner_score = boards[board_idx].score(&n);
                    won[board_idx] = true;
                }
            }
        }
    }

    println!(
        "Last winner: {} Score: {}",
        last_winner_idx, last_winner_score
    );
}

#[derive(Copy, Clone)]
struct Square {
    number: u32,
    called: bool,
}

impl Square {
    fn new() -> Square {
        Square {
            number: 0,
            called: false,
        }
    }
}

#[derive(Copy, Clone)]
struct Board {
    board: [[Square; 5]; 5],
}

impl Board {
    fn call(&mut self, number: &u32) -> bool {
        let (found, x, y) = self.find_square(number);

        if !found {
            return false;
        }

        self.set_square_called(x, y);

        self.check_win(x, y)
    }

    fn check_win(&self, set_x: usize, set_y: usize) -> bool {
        let mut row_win = true;
        let mut col_win = true;

        for x in 0..5 {
            row_win = row_win && self.board[x][set_y].called;
        }

        for y in 0..5 {
            col_win = col_win && self.board[set_x][y].called;
        }

        row_win || col_win
    }

    fn find_square(&self, number: &u32) -> (bool, usize, usize) {
        for x in 0..5 {
            for y in 0..5 {
                if self.board[x][y].number == *number {
                    return (true, x, y);
                }
            }
        }

        return (false, 0, 0);
    }

    fn new() -> Board {
        Board {
            board: [[Square::new(); 5]; 5],
        }
    }

    fn score(&self, last_called_number: &u32) -> u32 {
        let mut sum: u32 = 0;
        for x in 0..5 {
            for y in 0..5 {
                if !(self.board[x][y].called) {
                    sum += self.board[x][y].number;
                }
            }
        }

        sum * last_called_number
    }

    fn set_square_number(&mut self, x: usize, y: usize, number: u32) {
        self.board[x][y].number = number;
    }

    fn set_square_called(&mut self, x: usize, y: usize) {
        self.board[x][y].called = true;
    }
}
