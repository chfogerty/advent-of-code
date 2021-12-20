use std::fmt::{Display, Formatter, Result};
// const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Hello, world!");
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct SnailNumber {
    first: SnailNumberContents,
    second: SnailNumberContents,
}

impl Display for SnailNumber {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        write!(f, "[{},{}]", self.first, self.second)
    }
}

impl From<&str> for SnailNumber {
    fn from(s: &str) -> Self {}
}

#[derive(Clone, Debug, Eq, PartialEq)]
enum SnailNumberContents {
    Number(Box<SnailNumber>),
    Literal(u8),
}

impl Display for SnailNumberContents {
    fn fmt(&self, f: &mut Formatter<'_>) -> Result {
        match self {
            SnailNumberContents::Number(value) => write!(f, "{}", value.as_ref()),
            SnailNumberContents::Literal(value) => write!(f, "{}", value),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    // const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        // assert_eq!(part_a(TEST_INPUT), 45);
    }

    #[test]
    fn test_b() {
        // assert_eq!(part_b(TEST_INPUT), 112);
    }
}
