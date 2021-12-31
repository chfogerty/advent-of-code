use std::collections::{HashMap, HashSet, VecDeque};
use std::mem;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
}

fn part_a(data: &str) -> usize {
    let scanners = parse_data(data);
    let mut unique_beacons = HashSet::new();
    for scanner in scanners {
        let map = create_neighbor_map(&scanner.beacons);
        for (k, _) in map {
            unique_beacons.insert(k);
        }
    }

    unique_beacons.len()
}

fn parse_data(data: &str) -> Vec<Scanner> {
    data.split("\n\n").map(|s| Scanner::from(s)).collect()
}

fn distance(left: &Point, right: &Point) -> f64 {
    let delta_x = left.0 - right.0;
    let delta_y = left.1 - right.1;
    let delta_z = left.2 - right.2;

    let distance_sq = delta_x * delta_x + delta_y * delta_y + delta_z * delta_z;
    (distance_sq as f64).sqrt()
}

fn manhattan_distance(left: &Point, right: &Point) -> u64 {
    let delta_x: u64 = (left.0 - right.0).abs() as u64;
    let delta_y: u64 = (left.1 - right.1).abs() as u64;
    let delta_z: u64 = (left.2 - right.2).abs() as u64;

    delta_x + delta_y + delta_z
}

fn create_neighbor_map(beacons: &Vec<Point>) -> HashMap<FloatKey, (Point, Point, Point)> {
    // thanks to https://github.com/jimcasey/home/blob/master/projects/advent-of-code/2021/19/part1.py
    let mut neighbor_map = HashMap::new();
    for beacon in beacons {
        let mut neighbors = VecDeque::new();
        for peer in beacons {
            if peer != beacon {
                let dist = distance(beacon, peer);
                if neighbors.len() == 0 {
                    neighbors.push_front((dist, peer));
                } else if neighbors.len() == 1 {
                    if dist > neighbors[0].0 {
                        neighbors.push_back((dist, peer));
                    } else {
                        neighbors.push_front((dist, peer));
                    }
                } else {
                    if dist < neighbors[0].0 {
                        neighbors.push_front((dist, peer));
                        neighbors.pop_back();
                    } else if dist < neighbors[1].0 {
                        neighbors.pop_back();
                        neighbors.push_back((dist, peer));
                    }
                }
            }
        }
        let key = (neighbors[0].0 + neighbors[1].0) * distance(neighbors[0].1, neighbors[1].1);
        neighbor_map.insert(
            FloatKey::new(key),
            (*beacon, *neighbors[0].1, *neighbors[1].1),
        );
    }

    neighbor_map
}

#[derive(Clone, Copy, Eq, PartialEq)]
struct Point(i32, i32, i32);

struct Scanner {
    beacons: Vec<Point>,
    location: Option<Point>,
    direction: Option<Point>,
    rotation: Option<Point>,
}

#[derive(Hash, Eq, PartialEq)]
struct FloatKey {
    mantissa: u64,
    exp: i16,
    sign: i8,
}

impl From<&str> for Scanner {
    fn from(s: &str) -> Self {
        Scanner {
            beacons: s.lines().collect::<Vec<&str>>()[1..]
                .iter()
                .map(|&line| Point::from(line))
                .collect(),
            location: Option::None,
            direction: Option::None,
            rotation: Option::None,
        }
    }
}

impl From<&str> for Point {
    fn from(s: &str) -> Self {
        let coords = s
            .split(",")
            .map(|s| s.parse().unwrap())
            .collect::<Vec<i32>>();
        Point(coords[0], coords[1], coords[2])
    }
}

impl Scanner {
    fn update_orientation(
        self: &mut Scanner,
        (location, direction, rotation): (&Point, &Point, &Point),
    ) {
        for idx in 0..self.beacons.len() {
            let xyz = vec![
                self.beacons[idx].0,
                self.beacons[idx].1,
                self.beacons[idx].2,
            ];

            self.beacons[idx].0 = xyz[rotation.0 as usize] * direction.0 + location.0;
            self.beacons[idx].1 = xyz[rotation.1 as usize] * direction.1 + location.1;
            self.beacons[idx].2 = xyz[rotation.2 as usize] * direction.2 + location.2;
        }

        self.location = Option::Some(*location);
        self.rotation = Option::Some(*rotation);
        self.direction = Option::Some(*direction);
    }
}

impl FloatKey {
    fn new(val: f64) -> Self {
        let (mant, exp, sign) = FloatKey::integer_decode(val);
        Self {
            mantissa: mant,
            exp: exp,
            sign: sign,
        }
    }

    fn integer_decode(val: f64) -> (u64, i16, i8) {
        let bits: u64 = unsafe { mem::transmute(val) };
        let sign: i8 = if bits >> 63 == 0 { 1 } else { -1 };
        let mut exponent: i16 = ((bits >> 52) & 0x7ff) as i16;
        let mantissa = if exponent == 0 {
            (bits & 0xfffffffffffff) << 1
        } else {
            (bits & 0xfffffffffffff) | 0x10000000000000
        };
        exponent -= 1023 + 52;
        (mantissa, exponent, sign)
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT: &str = include_str!("test_input.txt");

    #[test]
    fn test_a() {
        assert_eq!(part_a(TEST_INPUT), 79);
    }
}
