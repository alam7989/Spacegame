class EnemyBullet:
    def __init__(self, row, col):
        self._row = row
        self._col = col
        
    def row(self) -> int:
        '''Returns self._row.'''
        return self._row

    def col(self) -> int:
        '''Returns self._col.'''
        return self._col

    def move(self) -> None:
        ''''Moves the bullet down by one row.
        (Increases self.row by 1)'''
        self._row += 1