from __future__ import annotations

import sys
import pygame

from config import *
from data import POLICIES, PolicyDef
from game_state import GameState, Policy, adjust_policy, buy_upgrade, end_turn, compute_turn_delta, Tier
from save_load import save_game, load_game
from ui import Panel, Button, Label, Slider

def init_game_state() -> GameState:
    gs = GameState()
    gs.policies = {p.key: Policy(p.key, p.name, funding=0) for p in POLICIES}
    return gs

def draw_left_panel(surf, font, gs: GameState, defs: dict[str, PolicyDef]):
    x, y = MARGIN, MARGIN
    pnl = Panel(pygame.Rect(x, y, LEFT_W - 2*MARGIN, SCREEN_H - 2*MARGIN))
    pnl.draw(surf)
    pad = 12

    title = font.render(f"Turn {gs.player.turn}", True, TEXT)
    surf.blit(title, (x+pad, y+pad))

    big = pygame.font.SysFont(None, 28)
    cash = big.render(f"Cash: ${gs.player.cash:,}", True, OK if gs.player.cash >= 0 else DANGER)
    ap = big.render(f"AP: {gs.player.action_points}", True, TEXT)
    surf.blit(cash, (x+pad, y+pad+28))
    surf.blit(ap, (x+pad, y+pad+28+26))

    inc, upk, net = compute_turn_delta(gs, {p.key: p for p in POLICIES})
    s_inc = font.render(f"Income next turn:  +${inc:,}", True, TEXT)
    s_upk = font.render(f"Upkeep next turn: -${upk:,}", True, TEXT)
    s_net = font.render(f"Net next turn:    {'+' if net>=0 else ''}${net:,}", True, OK if net>=0 else DANGER)
    surf.blit(s_inc, (x+pad, y+pad+28+26+26+10))
    surf.blit(s_upk, (x+pad, y+pad+28+26+26+10+22))
    surf.blit(s_net, (x+pad, y+pad+28+26+26+10+22+22))

def draw_right_panel(surf, font, gs: GameState, buy_buttons: list[Button]):
    x = SCREEN_W - RIGHT_W + MARGIN
    y = MARGIN
    pnl = Panel(pygame.Rect(SCREEN_W - RIGHT_W + MARGIN, y, RIGHT_W - 2*MARGIN, SCREEN_H - 2*MARGIN))
    pnl.draw(surf)

    title = font.render("Upgrades (Tiers)", True, TEXT)
    surf.blit(title, (x+12, y+12))

    big = pygame.font.SysFont(None, 28)
    rows = [
        ("Airline", "airline", gs.upgrades.airline),
        ("Airport", "airport", gs.upgrades.airport),
        ("Points", "points", gs.upgrades.points),
    ]

    buy_buttons.clear()
    yy = y + 44
    for label, attr, tier in rows:
        row_rect = pygame.Rect(x+8, yy, RIGHT_W - 2*MARGIN - 16, 46)
        pygame.draw.rect(surf, (55,65,80), row_rect, border_radius=8)
        tlabel = big.render(f"{label}: T{int(tier)}", True, TEXT)
        surf.blit(tlabel, (row_rect.x+12, row_rect.y+10))

        def make_cb(a=attr):
            return lambda: None

        btn = Button(pygame.Rect(row_rect.right-110, row_rect.y+6, 100, BTN_H-4), "Buy next", make_cb())
        btn.enabled = tier < Tier.T4
        buy_buttons.append((btn, attr))
        yy += 56

    return buy_buttons

def draw_center_panel(surf, font, gs: GameState, sliders: dict[str, Slider]):
    x = LEFT_W + MARGIN
    w = SCREEN_W - LEFT_W - RIGHT_W - 3*MARGIN
    pnl = Panel(pygame.Rect(x, MARGIN, w, SCREEN_H - 2*MARGIN))
    pnl.draw(surf)

    title = font.render("Policies", True, TEXT)
    surf.blit(title, (x+12, MARGIN+12))

    yy = MARGIN + 44
    for pdef in POLICIES:
        item_rect = pygame.Rect(x+12, yy, w-24, 64)
        pygame.draw.rect(surf, (55,65,80), item_rect, border_radius=8)
        name = font.render(pdef.name, True, TEXT)
        surf.blit(name, (item_rect.x+12, item_rect.y+8))

        pol = gs.policies[pdef.key]
        sld_rect = pygame.Rect(item_rect.x+12, item_rect.y+30, item_rect.w-24, 26)
        if pdef.key not in sliders:
            sliders[pdef.key] = Slider(sld_rect, pol.funding, pdef.max_funding, lambda v, k=pdef.key: setattr(gs.policies[k], "funding", v))
        else:
            sliders[pdef.key].rect = sld_rect
            sliders[pdef.key].maximum = pdef.max_funding
            sliders[pdef.key].value = pol.funding
        sliders[pdef.key].draw(surf, font)

        ftxt = font.render(f"Funding: {pol.funding}/{pdef.max_funding}", True, TEXT_DIM)
        surf.blit(ftxt, (item_rect.right-200, item_rect.y+6))

        yy += 76

def main():
    pygame.init()
    flags = 0
    screen = pygame.display.set_mode((SCREEN_W, SCREEN_H), flags)
    pygame.display.set_caption(TITLE)
    clock = pygame.time.Clock()
    font = pygame.font.SysFont(None, 22)

    fullscreen = False

    gs = init_game_state()

    end_turn_btn = Button(pygame.Rect(MARGIN+16, SCREEN_H - MARGIN - 48, 160, BTN_H), "End Turn", lambda: None)
    save_lbl = Label((MARGIN+16, SCREEN_H - MARGIN - 82), "S: Save   L: Load   F11: Fullscreen   ESC: Quit")
    buy_buttons: list[tuple[Button, str]] = []
    sliders: dict[str, Slider] = {}

    def do_end_turn():
        end_turn(gs, {p.key: p for p in POLICIES})
    end_turn_btn.on_click = do_end_turn

    policy_defs = {p.key: p for p in POLICIES}

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                elif event.key == pygame.K_F11:
                    fullscreen = not fullscreen
                    if fullscreen:
                        pygame.display.set_mode((0,0), pygame.FULLSCREEN)
                    else:
                        pygame.display.set_mode((SCREEN_W, SCREEN_H))
                elif event.key == pygame.K_s:
                    save_game(gs)
                elif event.key == pygame.K_l:
                    try:
                        gs = load_game()
                    except Exception as e:
                        print("Load failed:", e)

            end_turn_btn.handle(event)

            # Slider AP-aware handling
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                pos = event.pos
                for key, s in sliders.items():
                    pdef = policy_defs[key]
                    pol = gs.policies[key]
                    if s.minus_rect.collidepoint(pos):
                        if adjust_policy(gs, key, -1, pdef.ap_change_cost, pdef.max_funding):
                            s.value = pol.funding
                    elif s.plus_rect.collidepoint(pos):
                        if adjust_policy(gs, key, +1, pdef.ap_change_cost, pdef.max_funding):
                            s.value = pol.funding

        # Draw
        screen.fill(BG)
        draw_left_panel(screen, font, gs, policy_defs)
        buy_buttons = draw_right_panel(screen, font, gs, buy_buttons)

        for btn, attr in buy_buttons:
            def make_buy(a=attr):
                return lambda: buy_upgrade(gs, a)
            btn.on_click = make_buy()
            btn.draw(screen, font)

        draw_center_panel(screen, font, gs, sliders)

        end_turn_btn.draw(screen, font)
        save_lbl.draw(screen, font)

        # Handle buy buttons after drawing
        for event in pygame.event.get([pygame.MOUSEMOTION, pygame.MOUSEBUTTONDOWN]):
            for btn, _ in buy_buttons:
                btn.handle(event)

        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
