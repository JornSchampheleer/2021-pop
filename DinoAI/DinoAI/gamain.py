#  Copyright (c) 2020.
#  By Jorn Schampheleer
#  Textures copyrighted by google, extracted from the game by chirag64 (https://github.com/chirag64/t-rex-runner-bot)

import pygame
from DinoAI.DinoAI.GameObjects.ground import Ground
from DinoAI.DinoAI.GameObjects.obstacle_spawner import ObstacleSpawner
from DinoAI.DinoAI.GAHelpers.geneticsengine import GeneticsEngine

pygame.init()
GROUND_HEIGHT = 100
white = 255, 255, 255
black = 0, 0, 0

FPS = 30


def do_events(speed_multiplier):
    for event in pygame.event.get():  # Check for events
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_SPACE:
                speed_multiplier = speed_multiplier % 11 + 1
    return speed_multiplier


def draw(deltatime, game_display, score, speed_multiplier, geneticsengine: GeneticsEngine, drawables):
    game_display.fill(black)
    draw_score(game_display, score)
    draw_evolution_info(game_display, geneticsengine.current_gen, geneticsengine.dinosaurs,
                        geneticsengine.best_dinosaur)
    draw_speed(game_display, speed_multiplier)
    for drawable in drawables:
        drawable.update(deltatime)
        drawable.draw(game_display)

    pygame.display.update()


def draw_score(display, score):
    font = pygame.font.SysFont(None, 24)
    img = font.render(str(score), True, white)
    display.blit(img, (20, 20))


def draw_evolution_info(display, generation, dinosaurs, best_dinosaur):
    font = pygame.font.SysFont(None, 24)
    img = font.render("Generation: " + str(generation), True, white)
    display.blit(img, (20, 40))
    img = font.render("Alive dinosaurs: " + str(len([dino for dino in dinosaurs if dino.alive])), True, white)
    display.blit(img, (20, 60))
    img = font.render("Best dinosaur: " + str(best_dinosaur.dna), True, white)
    display.blit(img, (20, 80))
    img = font.render("Best score: " + str(best_dinosaur.score), True, white)
    display.blit(img, (20, 100))


def draw_speed(display, speed_multiplier):
    font = pygame.font.SysFont(None, 24)
    img = font.render("Speed: x" + str(speed_multiplier), True, white)
    display.blit(img, (20, 120))


def main():
    # Initialize game
    size = width, height = 640, 480
    game_display = pygame.display.set_mode(size)

    genetics_engine = GeneticsEngine(height - GROUND_HEIGHT)

    lastframe = pygame.time.get_ticks()  # Get ticks returns current time in milliseconds
    game_clock = pygame.time.Clock()

    speed_multiplier = 1

    # This is the evolutionary loop
    while genetics_engine.current_gen < genetics_engine.n_generations:
        ground = Ground(height, GROUND_HEIGHT)
        obstaclespawner = ObstacleSpawner(width, height - GROUND_HEIGHT)

        alive_dinosaurs = genetics_engine.dinosaurs

        # This is the game loop for one generation
        game_loop(game_clock, lastframe, speed_multiplier, game_display,
                                 alive_dinosaurs, obstaclespawner, ground, genetics_engine)

        # all dinosaurs are dead, begin next generation
        genetics_engine.evolve()
    print([dino.score for dino in genetics_engine.dinosaurs])


def game_loop(game_clock, lastframe, speed_multiplier, game_display,
              alive_dinosaurs, obstaclespawner, ground, genetics_engine):
    score = 0
    speed = 100
    while len(alive_dinosaurs):
        t = pygame.time.get_ticks()  # Get current time
        deltatime = (t - lastframe) / 1000.0  # Find difference in time and then convert it to seconds
        lastframe = t  # Set lastFrame as the current time for next frame.
        # Do speed_range steps within one frametime, this can increase speed
        for i in range(speed_multiplier):
            score += 1
            obstaclespawner.update(deltatime)

            speed_multiplier = do_events(speed_multiplier)

            if speed < 160 and score % 300 == 0:
                speed += 10
                obstaclespawner.increase_speed(speed)
                ground.increase_speed(speed)

            draw(deltatime, game_display, score, speed_multiplier, genetics_engine,
                 alive_dinosaurs + [ground] + obstaclespawner.obstacles)
            for dinosaur in genetics_engine.dinosaurs:
                if not dinosaur.alive:
                    continue
                dinosaur.score = score
                gamestate = obstaclespawner.get_next_obstacle_xy(dinosaur)
                if gamestate is not None:
                    [dino.react(gamestate) for dino in alive_dinosaurs]
                if obstaclespawner.is_colliding(dinosaur):
                    dinosaur.alive = False

            alive_dinosaurs = [dino for dino in genetics_engine.dinosaurs if dino.alive]
        game_clock.tick(FPS)  # Lock fps to 30

        if score > 20000:
            # Probably found an invincible dino that's going to play forever
            print("Found best dino with dna: " + str(genetics_engine.best_dinosaur.dna))
            break

    return score, speed


if __name__ == "__main__":
    main()
