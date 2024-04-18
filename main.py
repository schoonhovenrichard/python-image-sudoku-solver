import argparse
import cv2
import numpy as np
import pytesseract
from sudoku import Sudoku


def preprocess_image(image_path):
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    blurred = cv2.GaussianBlur(gray, (7, 7), 0)  # Blur to reduce noise
    thresh = cv2.adaptiveThreshold(
        blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2
    )
    return thresh


def find_largest_contour(thresh):
    contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    max_contour = max(contours, key=cv2.contourArea)  # Find the largest contour
    return cv2.boundingRect(max_contour)


def extract_sudoku_grid_and_numbers(image_path, m, n):
    thresh = preprocess_image(image_path)
    x, y, w, h = find_largest_contour(thresh)

    # Assumption: Largest contour is the Sudoku grid, crop it
    grid = thresh[y:y+h, x:x+w]

    # Number of grid cells
    N = m * n

    sudoku_grid = np.zeros((N, N), dtype=int)
    cell_width = w // N
    cell_height = h // N

    for row in range(N):
        for col in range(N):
            cell_x = col * cell_width
            cell_y = row * cell_height
            cell = grid[cell_y:cell_y+cell_height, cell_x:cell_x+cell_width]
            frac = 0.1
            cut_w = int(frac *  cell.shape[0])
            cut_h = int(frac *  cell.shape[1])
            cell = cell[cut_w:-cut_w,cut_h:-cut_h]
            if cell.min() == cell.max():# Nothing here
                continue

            cell = 255 - cell
            cell[cell < 200] = 0
            cell[cell >= 200] = 255
            cell = cv2.resize(cell, (40, 40), interpolation=cv2.INTER_AREA)

            text = pytesseract.image_to_string(
                cell, config='--psm 10 --oem 0'
                #cell, config='--psm 10 --oem 0 -c tessedit_char_whitelist=123456789'
            )
            try:
                number = int(text.strip())
                sudoku_grid[row, col] = number
            except ValueError:
                pass

    return sudoku_grid


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description="Process some integers.")
    parser.add_argument("--image_path", type=str, help="Path to the image file containing the Sudoku grid")
    parser.add_argument("--m", type=int, default=3, help="Sudoku grid width in blocks")
    parser.add_argument("--n", type=int, default=3, help="Sudoku grid height in blocks")

    args = parser.parse_args()
    m = args.m
    n = args.n

    sudoku_grid = extract_sudoku_grid_and_numbers(args.image_path, m, n)

    print("Extracted grid:\n", sudoku_grid, "\n")

    puzzle = Sudoku(m, n, board=sudoku_grid.tolist())
    solution = puzzle.solve()
    if solution:
        print("Solved Sudoku grid:")
        print(solution.board)
    else:
        print("No solution found for this Sudoku grid.")
