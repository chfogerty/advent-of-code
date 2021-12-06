// inspiration/copied from https://github.com/Crazytieguy/advent-2021/blob/master/src/bin/day5/main.rs
use std::{
    collections::HashMap,
    iter::{repeat, Chain, Rev},
    ops::RangeInclusive,
};

fn main() {
    let data = include_str!("input.txt");

    let mut vent_counts: HashMap<(u32, u32), u32> = HashMap::new();

    data.lines()
        .map(Line::from)
        .flat_map(|Line { x1, y1, x2, y2 }| {
            if x1 == x2 {
                repeat(x1)
                    .zip(list_all_points(y1, y2))
                    .collect::<Vec<(u32, u32)>>()
            } else if y1 == y2 {
                list_all_points(x1, x2)
                    .zip(repeat(y1))
                    .collect::<Vec<(u32, u32)>>()
            } else {
                list_all_points(x1, x2)
                    .zip(list_all_points(y1, y2))
                    .collect::<Vec<(u32, u32)>>()
            }
        })
        .for_each(|vent| *vent_counts.entry(vent).or_default() += 1);

    let answer = vent_counts.values().filter(|&&val| val >= 2).count();
    println!("{}", answer);
}

// a..=b doesn't produce an iterator if a > b, so chain it with (b..=a).rev() to produce an iterator that counts down if a > b
fn list_all_points(start: u32, stop: u32) -> Chain<RangeInclusive<u32>, Rev<RangeInclusive<u32>>> {
    (start..=stop).chain((stop..=start).rev())
}

#[derive(Copy, Clone, Debug)]
struct Line {
    x1: u32,
    y1: u32,
    x2: u32,
    y2: u32,
}

impl From<&str> for Line {
    fn from(s: &str) -> Self {
        let coords: Vec<u32> = s
            .split(" -> ")
            .flat_map(|point| point.split(","))
            .map(|coord| coord.parse().unwrap())
            .collect::<Vec<u32>>();

        Self {
            x1: coords[0],
            y1: coords[1],
            x2: coords[2],
            y2: coords[3],
        }
    }
}
