from pygame import Rect, draw, mouse
from pygame.locals import MOUSEBUTTONDOWN

class Button:
    def __init__(self, text, size, font, colors):
        self.text = text
        self.size = size
        self.font = font
        self.colors = colors  # Tuple of (normal_color, hover_color)
        self.rect = Rect((0, 0), size)
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, (0, 0, 0))
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.text_position = text_rect.topleft

    def draw(self, screen):
        color = self.colors[0]  # Default color
        if self.rect.collidepoint(mouse.get_pos()):
            color = self.colors[1]  # Hover color
        draw.rect(screen, color, self.rect)
        screen.blit(self.text_surface, self.text_position)

    def is_clicked(self, event):
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                return True
        return False

    def center(self, screen_width, screen_height):
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.render_text()  # Update text position