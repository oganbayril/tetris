from pygame import Rect, draw, mouse
from pygame.locals import MOUSEBUTTONDOWN

class Button:
    def __init__(self, text, size, font, colors, surface_rect=None, clickable=True, clicked=False, text_color=(0, 0, 0)):
        self.text = text
        self.rect = Rect((0, 0), size)
        self.font = font
        self.colors = colors  # Tuple of (normal_color, hover_color), color of the button
        self.surface_rect = surface_rect
        self.clickable = clickable
        self.clicked = clicked # Indicates if the button has been clicked
        self.text_color = text_color # Color of the text
        self.render_text()

    def render_text(self):
        self.text_surface = self.font.render(self.text, True, self.text_color)
        text_rect = self.text_surface.get_rect(center=self.rect.center)
        self.text_position = text_rect.topleft

    def draw(self, screen):
        color = self.colors[0]
        mouse_x, mouse_y = mouse.get_pos()

        if self.surface_rect:
            mouse_x -= self.surface_rect.x
            mouse_y -= self.surface_rect.y

        if self.rect.collidepoint((mouse_x, mouse_y)) or self.clicked:
            color = self.colors[1]

        draw.rect(screen, color, self.rect)
        screen.blit(self.text_surface, self.text_position)

    def is_clicked(self, event):
        if not self.clickable or not event:
            return False
        if event.type == MOUSEBUTTONDOWN and event.button == 1:
            mouse_x, mouse_y = event.pos

            if self.surface_rect:
                mouse_x -= self.surface_rect.x
                mouse_y -= self.surface_rect.y

            if self.rect.collidepoint((mouse_x, mouse_y)):
                self.clicked = True
                return True
        return False

    def center(self, screen_width, screen_height):
        self.rect.center = (screen_width // 2, screen_height // 2)
        self.render_text()  # Update text position