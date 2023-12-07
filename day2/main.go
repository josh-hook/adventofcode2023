package main

import (
	"bufio"
	"bytes"
	"errors"
	"flag"
	"fmt"
	"io"
	"os"
	"strconv"
	"time"
	"unicode"
)

func max(a, b int) int {
	if a > b {
		return a
	}
	return b
}

func main() {
	filePath := flag.String("file", "", "path to the input file")
	flag.Parse()

	file, err := os.Open(*filePath)
	if err != nil {
		panic(fmt.Errorf("open file: %w", err))
	}

	start := time.Now()
	r := bufio.NewReader(file)
	sum := 0
	for {
		line, _, err := r.ReadLine()
		if err != nil {
			if errors.Is(err, io.EOF) {
				break
			}
			panic(fmt.Errorf("read file: %w", err))
		}
		splitIdx := bytes.IndexRune(line, ':')
		if splitIdx == -1 {
			panic(fmt.Errorf("no colon in line: %s", string(line)))
		}

		// Iterate over the game and pull out the numbers.
		// " 3 blue, 4 red; 1 red, 2 green, 6 blue; 2 green"
		found := make(map[rune]int, 3)
		for i := splitIdx + 1; i < len(line); i++ {
			b := line[i]
			if unicode.IsDigit(rune(b)) {
				// Find the rest of the number
				j := i + 1
				for ; line[j] != ' '; j++ {
				}

				num, err := strconv.Atoi(string(line[i:j]))
				if err != nil {
					panic(fmt.Errorf("convert string to int: %s", string(line[i:j])))
				}

				colour := rune(line[j+1])
				if colour != 'b' && colour != 'r' && colour != 'g' {
					panic(fmt.Errorf("unknown colour in line '%x': %s", colour, line))
				}
				found[colour] = max(found[colour], num)
				i = j
			}
		}

		sum += found['b'] * found['r'] * found['g']
	}

	fmt.Println(sum)
	fmt.Printf("Time taken: %f\n", time.Since(start).Seconds())
}
