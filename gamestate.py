from re import L
from subprocess import list2cmdline
from unittest.mock import NonCallableMagicMock
from ship import Ship
from bullet import Bullet
from enemy import Enemy
from enemybullet import EnemyBullet
import random

class GameState:
    def __init__(self):
        self._rows = 10
        self._cols = 10
        self._field = []
        for row in range(self._rows):
            self._field.append(['empty' for col in range(self._cols)])

        self._game_over = False
        self._ship = Ship(self._rows-2, (self._cols // 2) - 1)
        self._health = 3
        self._bullets = []
        self._enemies = []
        self._enemy_bullets = []
        for row in range(3):
            for col in range(0, self._cols-3):
                self._enemies.append(Enemy(row, col))

    def health(self) -> int:
        '''Returns the health.'''
        return self._health

    def cols(self) -> int:
        '''Returns the number of cols in the field.'''
        return self._cols

    def rows(self) -> int:
        '''Returns the number of rows in the field.'''
        return self._rows

    def field(self) -> list:
        '''Returns the field.'''
        return self._field

    def ship(self) -> Ship:
        '''Returns the ship.'''
        return self._ship

    def bullets(self) -> list:
        '''Returns list of bullets.'''
        return self._bullets

    def enemies(self) -> list:
        '''Returns list of enemies.'''
        return self._enemies

    def enemy_bullets(self) -> list:
        '''Returns list of enemy bullets.'''
        return self._enemy_bullets

    def add_bullet(self, bullet: Bullet) -> None:
        '''Adds a bullet to the list of bullets.'''
        self._bullets.append(bullet)
        self._field[bullet.row()][bullet.col()] = 'bullet'

    def remove_bullet(self, bullet: Bullet) -> None:
        '''Removes a bullet from the list of bullets.'''
        self._bullets.remove(bullet)
        self._field[bullet.row()][bullet.col()] = 'empty'

    def find_enemy(self, row: int, col: int) -> None:
        '''Returns the enemy from the list of enemies that
        matches the specified row and col.'''
        for e in self._enemies:
            if (e.row() == row) and (e.col() == col):
                return e

    def remove_enemy(self, enemy: Enemy) -> None:
        '''Removes an enemy from the list of enemies.'''
        self._enemies.remove(enemy)
        self._field[enemy.row()][enemy.col()] = 'empty'

    def move_ship_H(self, change: int) -> None:
        '''Moves the ship to the right if change == 1,
        and left if change == -1.'''
        ship = self.ship()
        row = ship.row()
        col = ship.col()
        field = self.field()

        if (col + change) in range(self.cols()):
            ship.move_horizontally(change)
            field[row][col] = 'empty'
            field[self.ship().row()][self.ship().col()] = 'ship'


    def move_ship_V(self, change: int) -> None:
        '''Moves the ship up if change == 1,
        and down if change == -1.'''
        ship = self.ship()
        row = ship.row()
        col = ship.col()
        field = self.field()

        if (row + change) in range(4, self.rows()-1):
            #ship cannot go within 1 row of the enemies
            ship.move_vertically(change)
            field[row][col] = 'empty'
            field[self.ship().row()][self.ship().col()] = 'ship'
            

    def shoot_bullet(self) -> None:
        '''Creates a bullet in front of the ship.'''
        field = self.field()
        bullet = Bullet(self.ship().row()-1, self.ship().col())
        self.add_bullet(bullet)
       
    
    def move_bullet(self, bullet: Bullet) -> None:
        '''Decreases the row of the bullet by 1.'''
        row = bullet.row()
        col = bullet.col()
        field = self.field()

        field[row][col] = 'empty'
        if row == 0:
            self.remove_bullet(bullet)
        elif field[row-1][col] == 'enemy':
            self.remove_enemy(self.find_enemy(row-1, col))
            self.remove_bullet(bullet)
        else:
            bullet.move()
            #field[bullet.row()][col] = 'bullet'


    def move_all_bullets(self) -> None:
        '''Moves all bullets on the field.'''
        field = self.field()
        bullets = self.bullets()
        for b in bullets:
            row = b.row()
            col = b.col()
            self.move_bullet(b)

    def move_enemies_H(self, change: int) -> None:
        '''Changes the column of all enemies by the change.'''
        for e in self._enemies:
            e.move_horizontally(change)

    def shoot_enemy_bullet(self) -> None:
        '''Creates an enemy bullet under a random enemy.'''
        field = self.field()
        enemy_index = random.randint(0, len(self._enemies) - 1)
        enemy = self._enemies[enemy_index]
        enemy_bullet = EnemyBullet(enemy.row()+1, enemy.col())
        self.add_enemy_bullet(enemy_bullet)

    def add_enemy_bullet(self, enemy_bullet: EnemyBullet) -> None:
        '''Adds a bullet to the list of bullets.'''
        self._enemy_bullets.append(enemy_bullet)
        self._field[enemy_bullet.row()][enemy_bullet.col()] = 'enemy_bullet'

    def remove_enemy_bullet(self, enemy_bullet: EnemyBullet) -> None:
        '''Removes a bullet from the list of bullets.'''
        self._enemy_bullets.remove(enemy_bullet)
        self._field[enemy_bullet.row()][enemy_bullet.col()] = 'empty'

    def find_enemy_bullet(self, row: int, col: int) -> None:
        '''Returns the enemy bullet from the list of enemy bullets that
        matches the specified row and col.'''
        for e in self._enemy_bullets:
            if (e.row() == row) and (e.col() == col):
                return e

    def move_enemy_bullet(self, enemy_bullet: EnemyBullet) -> None:
        '''Decreases the row of the enemy bullet by 1.'''
        row = enemy_bullet.row()
        col = enemy_bullet.col()
        field = self.field()

        field[row][col] = 'empty'
        if row == self.rows()-1:
            self.remove_enemy_bullet(enemy_bullet)
        elif field[row+1][col] == 'ship':
            self.remove_enemy_bullet(enemy_bullet)
            self.decrease_health()
        else:
            enemy_bullet.move()
            field[enemy_bullet.row()][col] = 'enemy_bullet'

    def move_all_enemy_bullets(self) -> None:
        '''Moves all enemy bullets on the field.'''
        field = self.field()
        enemy_bullets = self.enemy_bullets()
        for e in enemy_bullets:
            row = e.row()
            col = e.col()
            self.move_enemy_bullet(e)


    def populate_field(self) -> None:
        field = self.field()
        for row in range(len(field)):
            for col in range(len(field[row])):
                field[row][col] = 'empty'
        field[self._ship.row()][self._ship.col()] = 'ship'
        for bullet in self.bullets():
            field[bullet.row()][bullet.col()] = 'bullet'
        for enemy in self.enemies():
            field[enemy.row()][enemy.col()] = 'enemy'
        for enemy_bullet in self.enemy_bullets():
            field[enemy_bullet.row()][enemy_bullet.col()] = 'enemy_bullet'

   
    def handle_moving(self, tick: int, change: int):
        '''Moves all bullets and enemies depending on the tick and change.'''
        if tick % 100 == 0:
            self.shoot_enemy_bullet()

        self.populate_field()
        if tick % 10 == 0:
            self.move_all_bullets()
            self.move_all_enemy_bullets()

        if tick % 100 == 0:
            self.move_enemies_H(change) 
        
    def decrease_health(self) -> None:
        self._health -= 1
        if self._health == 0:
            self._game_over = True
        
        print(self._health)

    def check_win(self) -> bool:
        '''Returns True if there are no more enemeies remaining.'''
        return len(self._enemies) == 0

    def game_over(self) -> bool:
        '''Returns whether or not the game is over.'''
        return self._game_over
