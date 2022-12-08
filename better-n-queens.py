
import random

def conflicts(queens: list, N: int, col: int):
    confs = [-1 for _ in range(N)]
    for col_q, row_q in enumerate(queens):
		# if the queen is the queen we are checking for OR there is no queen in this column
        if col_q == col or row_q == -1:
            continue

        confs[row_q] += 1  # add conflict for matching row

		# diagonal upwards
        if 0 <= row_q - abs(col_q - col) < N:
            confs[row_q - abs(col_q - col)] += 1

		# diagonal downwards
        if 0 <= row_q + abs(col_q - col) < N:
            confs[row_q + abs(col_q - col)] += 1
		
    return confs


def move(queens, N, col):
	
	# find conflicts for column i
	confs = conflicts(queens, N, col)

	# select a random row with the minimum conflict
	min_conf = min(confs)
	return random.choice([i for i in range(len(confs)) if confs[i] == min_conf])




def main(N):
	queens = [-1 for _ in range(N)]

	# initialize queens in all rows
	for i in range(N):
		# puts queens in col i
		queens[i] = move(queens, N, i)
		print(f"Initialize queen {i}")
	

	# conflict initialization

	# build row and diagonal conflicts arrays
	row_confs = [-1 for _ in range(N)]
	pos_diag_confs = [-1 for _ in range(2*N-1)]
	neg_diag_confs = [-1 for _ in range(2*N-1)]

	for col, row in enumerate(queens):
		row_confs[row] += 1
		pos_diag_confs[row - col + N - 1] += 1
		neg_diag_confs[row + col] += 1
	
	# build total conflicts array
	total_confs = [None for _ in range(N)]
	for col, row in enumerate(queens):
		total_confs[col] = row_confs[row] + pos_diag_confs[row - col + N - 1] + neg_diag_confs[row + col]

	i = 0
	while sum(total_confs) > 0:
		i += 1


		# choose which random conflicting queen to move
		move_col = random.choice([i for i in range(len(total_confs)) if total_confs[i] > 0])

		# move queen in chosen column
		old_row = queens[move_col]
		new_row = move(queens, N, move_col)
		queens[move_col] = new_row

		# update total conflicts

		# recalculate conflict for the moved column
		total_confs[move_col] = 0

		for col, row in enumerate(queens):
			if col == move_col:
				continue
			
			# subtract conflict if it was conflicting with the old queen
			if row == old_row or (abs(row - old_row) == abs(col - move_col)):
				total_confs[col] -= 1
			# add conflict if it is now conflicting with the new queen
			if row == new_row or (abs(row - new_row) == abs(col - move_col)):
				total_confs[col] += 1
				total_confs[move_col] += 1
		
		print(f"Iterate Minimum Conflict {i}")

	return queens, i


main(10000)


