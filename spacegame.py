#from unittest.mock import NonCallableMagicMock
import pygame
from gamestate import GameState
import sys

class SpaceGame:
    def __init__(self):
        self._gamestate = GameState()

    def run(self) -> None:
        pygame.init()
        self.resize_surface((360, 780))
        clock = pygame.time.Clock()

        i =-1
        change = -1
        while True:
            i = (i+1) % 300
            if i == 0:
                change *= -1
            self._gamestate.handle_moving(i, change)
            self.draw_game()
            if not self.handle_events():
                break
            if self._gamestate.game_over():
                break
        pygame.quit()
        sys.exit()

    
    def resize_surface(self, size: tuple[int, int]) -> None:
        '''Resizes the surface and updates relevant variables.'''
        pygame.display.set_mode(size, pygame.RESIZABLE)

    def draw_grid(self) -> None:
        '''Draws lines marking the rows and columns of the field.'''
        surface = pygame.display.get_surface()
        sw = surface.get_width()
        sh = surface.get_height() 
        box_length = sw // self._gamestate.cols()
        box_height = sh // self._gamestate.rows()

        for x in range (0, sw, box_length):
            for y in range(0, sh, box_height):
                box = pygame.Rect(
                    x, y, box_length, box_height
                )
                pygame.draw.rect(surface, pygame.Color(100, 100, 100), box, 1)

    def draw_object(self, object: str, row: int, col: int) -> None:
        '''Draws an object on the surface.'''
        surface = pygame.display.get_surface()
        sw = surface.get_width()
        sh = surface.get_height() 
        box_length = sw // self._gamestate.cols()
        box_height = sh // self._gamestate.rows()
        box = pygame.Rect(box_length * col, box_height * row, box_length, box_height)
        color = pygame.Color(255, 0, 0) #default red enemy

        if object == 'ship':
            color = pygame.Color(0, 0, 255) #blue ship
        elif object == 'bullet':
            color = pygame.Color(255, 255, 255) #white bullets
        elif object == 'enemy_bullet':
            color = pygame.Color(255, 217, 0) #yellow enemy bullets
        
        pygame.draw.ellipse(surface, color, box)
        

    def draw_field(self) -> None:
        '''Draws all enemies and the ship.'''
        field = self._gamestate.field()

        for row in range(len(field)):
            for col in range(len(field[row])):
                if field[row][col] != 'empty':
                    self.draw_object(field[row][col], row, col)
                    


    def draw_game(self) -> None:
        '''Draws the entire surface and objects on the surface.'''

        surface = pygame.display.get_surface()
        sw = surface.get_width()
        sh = surface.get_height() 
        surface.fill(pygame.Color(0, 0, 0))
        
        #self.draw_grid()
        self.draw_field()

        #print health
        health = self._gamestate.health()
        health_str = ''
        for h in range(health):
            health_str += '* '
        font_obj = pygame.font.SysFont('malgungothic', 20, bold=True, italic=False)
        surface_obj = font_obj.render('Lives: ' + health_str, True, pygame.Color(255, 255, 255))
        text_rect_obj = surface_obj.get_rect()
        text_rect_obj.center = (100, sh - 30)
        surface.blit(surface_obj, text_rect_obj)

        #print winning message
        if self._gamestate.check_win():
            font_obj = pygame.font.SysFont('malgungothic', 50, bold=True, italic=False)
            surface_obj = font_obj.render('You Won!', True, pygame.Color(255, 255, 255))
            text_rect_obj = surface_obj.get_rect()
            text_rect_obj.center = (sw/2, sh/2)
            surface.blit(surface_obj, text_rect_obj)
            

        pygame.display.flip()
        

    
    def handle_events(self) -> bool:
        '''Responds to all relevant events.'''
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
                self.resize_surface(event.size)
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT: # or pygame.K_a
                    self._gamestate.move_ship_H(-1)
                elif event.key == pygame.K_RIGHT:
                    self._gamestate.move_ship_H(1)
                elif event.key == pygame.K_DOWN:
                    self._gamestate.move_ship_V(1 )
                elif event.key == pygame.K_UP:
                    self._gamestate.move_ship_V(-1)
                elif event.key == pygame.K_SPACE:
                    self._gamestate.shoot_bullet()
        return True



if __name__ == '__main__':
    SpaceGame().run()