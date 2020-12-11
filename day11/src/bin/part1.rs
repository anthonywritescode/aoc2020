use std::collections::HashMap;
use std::env;
use std::fs;
use std::process;

fn main() {
    let args: Vec<String> = env::args().collect();
    if args.len() != 2 {
        println!("usage {} INPUT", args[0]);
        process::exit(1);
    }

    let mut prev = fs::read_to_string(&args[1])
        .expect("file error")
        .lines()
        .map(str::to_string)
        .collect::<Vec<String>>();

    loop {
        let mut marked: HashMap<(isize, isize), usize> = HashMap::new();
        for (y, line) in prev.iter().enumerate() {
            for (x, c) in line.chars().enumerate() {
                if c == '#' {
                    for (d_y, d_x) in [
                        (-1, -1),
                        (0, 1),
                        (0, -1),
                        (1, 0),
                        (-1, 0),
                        (1, 1),
                        (-1, 1),
                        (1, -1),
                    ]
                    .iter()
                    {
                        let y_i = y as isize + d_y;
                        let x_i = x as isize + d_x;
                        if y_i >= 0
                            && y_i < prev.len() as isize
                            && x_i >= 0
                            && x_i < line.len() as isize
                        {
                            *marked.entry((y_i, x_i)).or_insert(0) += 1;
                        }
                    }
                }
            }
        }

        let lines = (&prev)
            .iter()
            .enumerate()
            .map(|(y, line)| {
                line.chars()
                    .enumerate()
                    .map(|(x, c)| {
                        let count = marked.get(&(y as isize, x as isize)).unwrap_or(&0);
                        if c == 'L' && count == &0 {
                            '#'
                        } else if c == '#' && count >= &4 {
                            'L'
                        } else {
                            c
                        }
                    })
                    .collect::<String>()
            })
            .collect::<Vec<String>>();

        if &lines == &prev {
            let sum: usize = prev
                .iter()
                .map(|line| line.chars().filter(|c| *c == '#').count())
                .sum();
            println!("{}", sum);
            process::exit(0);
        }
        prev = lines;
    }
}
