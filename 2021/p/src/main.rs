const INPUT: &str = include_str!("input.txt");

fn main() {
    println!("Part A: {}", part_a(INPUT));
    println!("Part B: {}", part_b(INPUT));
}

fn part_b(data: &str) -> isize {
    let bitstream = BitStream::from(data);
    let (envelope, _) = parse_packet(&bitstream.stream[..]);
    envelope.get_value()
}

fn part_a(data: &str) -> usize {
    let bitstream = BitStream::from(data);
    let (envelope, _) = parse_packet(&bitstream.stream[..]);
    envelope.sum_version()
}

fn char_to_bits(c: char) -> Vec<u8> {
    match c {
        '0' => vec![0, 0, 0, 0],
        '1' => vec![0, 0, 0, 1],
        '2' => vec![0, 0, 1, 0],
        '3' => vec![0, 0, 1, 1],
        '4' => vec![0, 1, 0, 0],
        '5' => vec![0, 1, 0, 1],
        '6' => vec![0, 1, 1, 0],
        '7' => vec![0, 1, 1, 1],
        '8' => vec![1, 0, 0, 0],
        '9' => vec![1, 0, 0, 1],
        'A' => vec![1, 0, 1, 0],
        'B' => vec![1, 0, 1, 1],
        'C' => vec![1, 1, 0, 0],
        'D' => vec![1, 1, 0, 1],
        'E' => vec![1, 1, 1, 0],
        'F' => vec![1, 1, 1, 1],
        _ => panic!("Unrecognized character {}", c),
    }
}

fn number_from_bits(bits: &[u8]) -> u16 {
    let mut val = 0;
    for bit in bits {
        val = (val << 1) + *bit as u16;
    }

    val
}

fn type_from_id(id: u8) -> PacketType {
    match id {
        0 => PacketType::Sum,
        1 => PacketType::Product,
        2 => PacketType::Min,
        3 => PacketType::Max,
        4 => PacketType::Literal,
        5 => PacketType::Greater,
        6 => PacketType::Less,
        7 => PacketType::Equal,
        _ => PacketType::Operator,
    }
}

fn parse_value_from_bits(bits: &[u8]) -> (isize, usize) {
    let mut idx = 0;
    let mut val = 0;
    while idx < bits.len() {
        val = (val << 4) + number_from_bits(&bits[idx + 1..=idx + 4]) as isize;

        if bits[idx] == 0 {
            break;
        }

        idx += 5;
    }

    (val, idx + 5)
}

fn parse_packet(bits: &[u8]) -> (Packet, usize) {
    let version = number_from_bits(&bits[0..3]) as u8;
    let id = number_from_bits(&bits[3..6]) as u8;

    if type_from_id(id) == PacketType::Literal {
        let (value, bits_used) = parse_value_from_bits(&bits[6..]);
        let packet = Packet {
            version: version,
            id: id,
            value: Some(value),
            sub_packets: None,
        };

        (packet, bits_used + 6)
    } else {
        let sub_packet_kind = match bits[6] {
            1 => SubPacketType::Packets,
            0 => SubPacketType::Bits,
            _ => panic!("Not possible to match {} for sub packet type", bits[6]),
        };

        let (sub_packets, bits_used) = parse_sub_packets(&bits[7..], sub_packet_kind);
        let packet = Packet {
            version: version,
            id: id,
            value: None,
            sub_packets: Some(sub_packets),
        };

        (packet, bits_used + 7)
    }
}

fn parse_sub_packets_by_packet(bits: &[u8], packet_count: usize) -> (Vec<Packet>, usize) {
    let mut total_bits_used = 0;
    let mut packets = Vec::new();

    while packets.len() < packet_count {
        let (packet, bits_used) = parse_packet(&bits[total_bits_used..]);
        total_bits_used += bits_used;
        packets.push(packet);
    }

    (packets, total_bits_used)
}

fn parse_sub_packets_by_bit(bits: &[u8], bit_count: usize) -> (Vec<Packet>, usize) {
    let mut total_bits_used = 0;
    let mut packets = Vec::new();

    while total_bits_used < bit_count {
        let (packet, bits_used) = parse_packet(&bits[total_bits_used..]);
        total_bits_used += bits_used;
        packets.push(packet);
    }

    (packets, total_bits_used)
}

fn parse_sub_packets(bits: &[u8], kind: SubPacketType) -> (Vec<Packet>, usize) {
    match kind {
        SubPacketType::Bits => {
            let bit_count = number_from_bits(&bits[0..15]);
            let (packets, bits_used) = parse_sub_packets_by_bit(&bits[15..], bit_count as usize);
            (packets, bits_used + 15)
        }
        SubPacketType::Packets => {
            let packet_count = number_from_bits(&bits[0..11]);
            let (packets, bits_used) =
                parse_sub_packets_by_packet(&bits[11..], packet_count as usize);
            (packets, bits_used + 11)
        }
    }
}

struct BitStream {
    // either 1 or 0
    stream: Vec<u8>,
}

impl From<&str> for BitStream {
    fn from(s: &str) -> Self {
        let stream = s
            .trim()
            .chars()
            .flat_map(|c| char_to_bits(c))
            .collect::<Vec<u8>>();
        BitStream { stream: stream }
    }
}

#[derive(Clone, Debug, Eq, PartialEq)]
struct Packet {
    version: u8,
    id: u8,
    value: Option<isize>,
    sub_packets: Option<Vec<Packet>>,
}

#[derive(Copy, Clone, Eq, PartialEq)]
enum PacketType {
    Sum,
    Product,
    Min,
    Max,
    Literal,
    Greater,
    Less,
    Equal,
    Operator,
}

#[derive(Copy, Clone, Eq, PartialEq)]
enum SubPacketType {
    Bits,
    Packets,
}

impl Packet {
    fn get_type(&self) -> PacketType {
        type_from_id(self.id)
    }

    fn sum_version(&self) -> usize {
        if self.get_type() == PacketType::Literal {
            self.version as usize
        } else {
            let children_sum: usize = self
                .sub_packets
                .as_ref()
                .unwrap()
                .iter()
                .map(|packet| packet.sum_version())
                .sum();
            self.version as usize + children_sum
        }
    }

    fn get_value(&self) -> isize {
        match self.get_type() {
            PacketType::Sum => self
                .sub_packets
                .as_ref()
                .unwrap()
                .iter()
                .map(|packet| packet.get_value())
                .sum(),
            PacketType::Product => self
                .sub_packets
                .as_ref()
                .unwrap()
                .iter()
                .fold(1, |acc, packet| acc * packet.get_value()),
            PacketType::Min => self
                .sub_packets
                .as_ref()
                .unwrap()
                .iter()
                .map(|packet| packet.get_value())
                .min()
                .unwrap(),
            PacketType::Max => self
                .sub_packets
                .as_ref()
                .unwrap()
                .iter()
                .map(|packet| packet.get_value())
                .max()
                .unwrap(),
            PacketType::Literal => self.value.unwrap(),
            PacketType::Greater => {
                let packets = self.sub_packets.as_ref().unwrap();
                match packets[0].get_value() > packets[1].get_value() {
                    true => 1,
                    false => 0,
                }
            }
            PacketType::Less => {
                let packets = self.sub_packets.as_ref().unwrap();
                match packets[0].get_value() < packets[1].get_value() {
                    true => 1,
                    false => 0,
                }
            }
            PacketType::Equal => {
                let packets = self.sub_packets.as_ref().unwrap();
                match packets[0].get_value() == packets[1].get_value() {
                    true => 1,
                    false => 0,
                }
            }
            PacketType::Operator => panic!("Unknown operator {}", self.id),
        }
    }
}

#[cfg(test)]
mod tests {
    use super::*;
    const TEST_INPUT1: &str = include_str!("test_input1.txt");
    const TEST_INPUT2: &str = include_str!("test_input2.txt");
    const TEST_INPUT3: &str = include_str!("test_input3.txt");
    const TEST_INPUT4: &str = include_str!("test_input4.txt");
    const TEST_INPUTB: &str = include_str!("test_input_b1.txt");

    #[test]
    fn test_a1() {
        assert_eq!(part_a(TEST_INPUT1), 16);
    }

    #[test]
    fn test_a2() {
        assert_eq!(part_a(TEST_INPUT2), 12);
    }

    #[test]
    fn test_a3() {
        assert_eq!(part_a(TEST_INPUT3), 23);
    }

    #[test]
    fn test_a4() {
        assert_eq!(part_a(TEST_INPUT4), 31);
    }

    #[test]
    fn test_b() {
        let answers = vec![3, 54, 7, 9, 1, 0, 0, 1];
        let lines = TEST_INPUTB.lines().collect::<Vec<&str>>();

        for idx in 0..answers.len() {
            assert_eq!(part_b(lines[idx]), answers[idx]);
        }
    }
}
