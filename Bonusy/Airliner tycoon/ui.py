from __future__ import annotations

import pygame
from typing import Callable, Tuple

from config import PANEL, TEXT, TEXT_DIM, ACCENT, ACCENT_DARK, DANGER, OK, BTN_H

class Button:
    def __init__(self, rect: pygame.Rect, label: str, on_click: Callable[[], None], *, enabled: bool=True):
        self.rect = rect
        self.label = label
        self.on_click = on_click
        self.enabled = enabled
        self.hover = False

    def draw(self, surf: pygame.Surface, font: pygame.font.Font):
        color = ACCENT if self.enabled else (90, 90, 90)
        if self.hover and self.enabled:
            color = ACCENT_DARK
        pygame.draw.rect(surf, color, self.rect, border_radius=6)
        txt = font.render(self.label, True, (255, 255, 255))
        surf.blit(txt, txt.get_rect(center=self.rect.center))

    def handle(self, event: pygame.event.Event):
        if not self.enabled:
            return
        if event.type == pygame.MOUSEMOTION:
            self.hover = self.rect.collidepoint(event.pos)
        elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.rect.collidepoint(event.pos):
                self.on_click()

class Label:
    def __init__(self, pos: Tuple[int, int], text: str, color=TEXT):
        self.pos = pos
        self.text = text
        self.color = color

    def draw(self, surf: pygame.Surface, font: pygame.font.Font):
        surf.blit(font.render(self.text, True, self.color), self.pos)

class Panel:
    def __init__(self, rect: pygame.Rect):
        self.rect = rect

    def draw(self, surf: pygame.Surface):
        pygame.draw.rect(surf, PANEL, self.rect, border_radius=12)

class Slider:
    """Discrete slider 0..max with -/+ buttons."""
    def __init__(self, rect: pygame.Rect, value: int, maximum: int, on_change: Callable[[int], None]):
        self.rect = rect
        self.value = value
        self.maximum = maximum
        self.on_change = on_change
        # inner layout
        self.minus_rect = pygame.Rect(rect.x+6, rect.y+6, 32, rect.h-12)
        self.plus_rect = pygame.Rect(rect.right-38, rect.y+6, 32, rect.h-12)

    def draw(self, surf: pygame.Surface, font: pygame.font.Font):
        pygame.draw.rect(surf, (60, 70, 90), self.rect, border_radius=8)
        # bar
        bar = pygame.Rect(self.rect.x+44, self.rect.y+12, self.rect.w-88, self.rect.h-24)
        pygame.draw.rect(surf, (90, 100, 120), bar, border_radius=6)
        if self.maximum > 0:
            filled_w = int(bar.w * (self.value / self.maximum))
            if filled_w > 0:
                pygame.draw.rect(surf, (140, 210, 255), pygame.Rect(bar.x, bar.y, filled_w, bar.h), border_radius=6)
        # buttons
        for r, s in ((self.minus_rect, "-"), (self.plus_rect, "+")):
            pygame.draw.rect(surf, (100, 120, 150), r, border_radius=6)
            surf.blit(font.render(s, True, (255,255,255)), (r.x + 10, r.y + 4))

        # value text
        valtxt = font.render(str(self.value), True, (255,255,255))
        surf.blit(valtxt, valtxt.get_rect(center=(self.rect.centerx, self.rect.centery)))

    def handle(self, event: pygame.event.Event):
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            if self.minus_rect.collidepoint(event.pos):
                if self.value > 0:
                    self.on_change(self.value - 1)
            elif self.plus_rect.collidepoint(event.pos):
                if self.value < self.maximum:
                    self.on_change(self.value + 1)
