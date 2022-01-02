use std::collections::{HashMap, HashSet, VecDeque};
use std::hash::Hash;
use std::mem;

const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
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

fn part_b(data: &str) -> usize {
    // thanks to https://github.com/jimcasey/home/blob/master/projects/advent-of-code/2021/19/part2.py
    let mut scanners = parse_data(data);

    // the first scanner is at (0, 0, 0), so move the beacons and scanner to the "solved" containers
    let mut beacon_field = HashSet::new();
    for beacon in scanners.pop().unwrap().beacons {
        beacon_field.insert(beacon);
    }

    let mut scanner_coords = Vec::new();
    scanner_coords.push(Point(0, 0, 0));

    let mut scanner_maps = create_scanner_maps(scanners);

    while scanner_maps.len() > 0 {
        let field_neighbor_map = create_neighbor_map(&beacon_field);
        let (mut scanner, field_neighbors, scanner_neighbors, idx) =
            find_matching_neighbors(&field_neighbor_map, &scanner_maps).unwrap();

        scanner_maps.remove(idx);

        let orientation = calculate_orientation(
            triplet_to_vec(&field_neighbors),
            triplet_to_vec(&scanner_neighbors),
        );

        scanner_coords.push(orientation.0);
        scanner.update_orientation(&orientation);

        for beacon in scanner.beacons {
            beacon_field.insert(beacon);
        }
    }

    max_manhattan_distance(&scanner_coords)
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

fn manhattan_distance(left: &Point, right: &Point) -> usize {
    let delta_x = (left.0 - right.0).abs() as usize;
    let delta_y = (left.1 - right.1).abs() as usize;
    let delta_z = (left.2 - right.2).abs() as usize;

    delta_x + delta_y + delta_z
}

fn max_manhattan_distance(points: &Vec<Point>) -> usize {
    let mut distance = 0;
    for idx_a in 0..points.len() {
        for idx_b in idx_a + 1..points.len() {
            let cur_distance = manhattan_distance(&points[idx_a], &points[idx_b]);
            if cur_distance > distance {
                distance = cur_distance
            }
        }
    }

    distance
}

fn create_scanner_maps(scanners: Vec<Scanner>) -> Vec<(Scanner, NeighborMap)> {
    scanners
        .iter()
        .map(|scanner| (scanner.clone(), create_neighbor_map(&scanner.beacons)))
        .collect()
}

fn create_neighbor_map(beacons: &(impl IntoIterator<Item = Point> + Clone)) -> NeighborMap {
    // thanks to https://github.com/jimcasey/home/blob/master/projects/advent-of-code/2021/19/part1.py
    let mut neighbor_map = HashMap::new();
    for beacon in beacons.clone() {
        let mut neighbors = VecDeque::new();
        for peer in beacons.clone() {
            if peer != beacon {
                let dist = distance(&beacon, &peer);
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
        let key = (neighbors[0].0 + neighbors[1].0) * distance(&neighbors[0].1, &neighbors[1].1);
        neighbor_map.insert(FloatKey::new(key), (beacon, neighbors[0].1, neighbors[1].1));
    }

    neighbor_map
}

fn find_matching_neighbors(
    field_map: &NeighborMap,
    scanner_maps: &Vec<(Scanner, NeighborMap)>,
) -> Option<(Scanner, Triplet, Triplet, usize)> {
    for (field_key, field_neighbors) in field_map {
        for idx in 0..scanner_maps.len() {
            let (scanner, scanner_map) = scanner_maps[idx].clone();
            for (scanner_neighbors_key, scanner_neighbors) in &scanner_map {
                if scanner_neighbors_key == field_key {
                    return Option::Some((scanner, *field_neighbors, *scanner_neighbors, idx));
                }
            }
        }
    }

    Option::None
}

fn calculate_orientation(
    field_neighbors: Vec<Vec<i32>>,
    scanner_neighbors: Vec<Vec<i32>>,
) -> Triplet {
    let mut offset: [Option<i32>; 3] = [Option::None; 3];
    let mut direction: [Option<i32>; 3] = [Option::None; 3];
    let mut rotation: [Option<i32>; 3] = [Option::None; 3];

    for axis in 0..3 {
        if offset[axis] == Option::None {
            for rotation_axis in 0..3 {
                for direction_flip in vec![-1, 1] {
                    let first_offset = field_neighbors[0][axis]
                        - scanner_neighbors[0][rotation_axis] * direction_flip;
                    let second_offset = field_neighbors[1][axis]
                        - scanner_neighbors[1][rotation_axis] * direction_flip;
                    let third_offset = field_neighbors[2][axis]
                        - scanner_neighbors[2][rotation_axis] * direction_flip;

                    if first_offset == second_offset && second_offset == third_offset {
                        offset[axis] = Option::Some(first_offset);
                        direction[axis] = Option::Some(direction_flip);
                        rotation[axis] = Option::Some(rotation_axis as i32);
                    }
                }
            }
        }
    }

    let unwrapped_offset = Point(offset[0].unwrap(), offset[1].unwrap(), offset[2].unwrap());
    let unwrapped_direction = Point(
        direction[0].unwrap(),
        direction[1].unwrap(),
        direction[2].unwrap(),
    );
    let unwrapped_rotation = Point(
        rotation[0].unwrap(),
        rotation[1].unwrap(),
        rotation[2].unwrap(),
    );

    (unwrapped_offset, unwrapped_direction, unwrapped_rotation)
}

fn triplet_to_vec(points: &Triplet) -> Vec<Vec<i32>> {
    vec![
        vec![points.0 .0, points.0 .1, points.0 .2],
        vec![points.1 .0, points.1 .1, points.1 .2],
        vec![points.2 .0, points.2 .1, points.2 .2],
    ]
}

type Triplet = (Point, Point, Point);

type NeighborMap = HashMap<FloatKey, Triplet>;

#[derive(Clone, Copy, Eq, Hash, PartialEq)]
struct Point(i32, i32, i32);

#[derive(Clone, Eq, Hash, PartialEq)]
struct Scanner {
    beacons: Vec<Point>,
}

#[derive(Clone, Eq, Hash, PartialEq)]
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
        (location, direction, rotation): &(Point, Point, Point),
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

    #[test]
    fn test_b() {
        assert_eq!(part_b(TEST_INPUT), 3621);
    }
}
