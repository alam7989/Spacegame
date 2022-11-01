class Enemy:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        
    def row(self) -> int:
        '''Returns self._row.'''
        return self._row

    def col(self) -> int:
        '''Returns self._col.'''
        return self._col

    def move_horizontally(self, change: int) -> None:
        ''''Moves the enemy to the left by 1 column if change == -1,
        and to the right by 1 column if change == 1.'''
        self._col += change