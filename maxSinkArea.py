def maxSinkArea(matrix):
    """
    :type matrix: List[List[int]]
    :rtype: int
    """
    n = len(matrix)
    m = len(matrix[0])
    
    # cells that can not contain water
    edges = ({(i, j) for i in range(n) for j in [0, m-1]} \
         | {(i, j) for j in range(1, m-1) for i in [0, n-1]})
    
    max_area = 0
    
    # avoid process duplicated combinations of cells
    sequences = set()
    
    def dfs(i, j, sequence, max_in, surround_seq):
        nonlocal max_area
        surround = {(i+1, j), (i-1, j), (i, j+1), (i, j-1)}
        for y, x in surround:
            if (y, x) not in sequence:
                surround_seq.add((y, x))
            if (y, x) in edges and matrix[y][x] <= matrix[i][j]:
                edges.add((i, j))
                
        if (i, j) in edges:
            return
        sequence.add((i, j))
        
        new_max_in = max(max_in, matrix[i][j])            
        new_min_out = min(matrix[a][b] for a, b in surround_seq)
        if new_min_out > new_max_in: # surrounding cells must be higher than inside cell to contain water
            max_area = max(max_area, len(sequence) + 1)

        sequences.add(tuple(sorted(sequence | {(i, j)}))) # mark processed combination
        
        # concatenate another possible cell to sequence and do dfs
        for (y, x) in surround_seq:
            if (y, x) not in edges and (y, x) not in sequence and tuple(sorted(sequence | {(y, x)})) not in sequences:
                dfs(y, x, sequence, new_max_in, surround_seq - {(y, x)})

    for i in range(1, n-1):
        for j in range(1, m-1):
            if (i, j) not in edges:
                dfs(i, j, set(), 0, set())
                
    return max_area
