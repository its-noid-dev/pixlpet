import pygame
import os
import random
import sys

pygame.init()

screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("PIXL Pet")

blue = (100, 180, 240)
green = (100, 200, 100)
white = (255, 255, 255)
black = (0, 0, 0)
red = (200, 50, 50)

if getattr(sys, "frozen", False):
    a = os.path.join(sys._MEIPASS, "assets")
else:
    if os.path.exists("assets/pet_idle.png"):
        a = "assets"
    else:
        a = "PixelPet/assets"

pet_idle = pygame.image.load(os.path.join(a, "pet_idle.png"))
pet_happy = pygame.image.load(os.path.join(a, "pet_happy.png"))
pet_eat = pygame.image.load(os.path.join(a, "pet_eat.png"))
pet_sleep = pygame.image.load(os.path.join(a, "pet_sleep.png"))

food = pygame.image.load(os.path.join(a, "icon_food.png"))
play = pygame.image.load(os.path.join(a, "icon_play.png"))
sleep = pygame.image.load(os.path.join(a, "icon_sleep.png"))

pet_idle = pygame.transform.scale(pet_idle, (256, 256))
pet_happy = pygame.transform.scale(pet_happy, (256, 256))
pet_eat = pygame.transform.scale(pet_eat, (256, 256))
pet_sleep = pygame.transform.scale(pet_sleep, (256, 256))

food = pygame.transform.scale(food, (50, 50))
play = pygame.transform.scale(play, (50, 50))
sleep = pygame.transform.scale(sleep, (50, 50))

hunger = 100
happiness = 100
energy = 100

pet = pet_happy
alive = True

message = ""
message_time = 0
action_time = 0
depletion_time = pygame.time.get_ticks()

font = pygame.font.SysFont(None, 30)

running = True

while running:

    now = pygame.time.get_ticks()

    for event in pygame.event.get():

        if event.type == pygame.QUIT:
            running = False

        if event.type == pygame.MOUSEBUTTONDOWN:

            x, y = event.pos

            if not alive:

                if 250 < x < 550 and 250 < y < 350:

                    hunger = 100
                    happiness = 100
                    energy = 100

                    pet = pet_happy
                    alive = True

                    message = "PIXL is back!"
                    message_time = now
                    depletion_time = now

            if alive:

                if 100 < x < 300 and 500 < y < 570:

                    if hunger < 100:
                        hunger += 10

                        if hunger > 100:
                            hunger = 100

                        pet = pet_eat
                        action_time = now
                        message = "PIXL is eating!"
                    else:
                        message = "PIXL is not hungry!"

                    message_time = now

                if 300 < x < 500 and 500 < y < 570:

                    if energy <= 20:
                        message = "PIXL is too tired!"

                    elif happiness >= 80:
                        message = "PIXL is already happy!"

                    else:
                        happiness += 10
                        energy -= 10

                        if happiness > 100:
                            happiness = 100

                        if energy < 0:
                            energy = 0

                        pet = pet_happy
                        action_time = now
                        message = "PIXL is playing!"

                    message_time = now

                if 500 < x < 700 and 500 < y < 570:

                    if energy < 80:

                        energy += 20
                        hunger -= 10

                        if energy > 100:
                            energy = 100

                        if hunger < 0:
                            hunger = 0

                        pet = pet_sleep
                        action_time = now
                        message = "PIXL is sleeping!"

                    else:
                        message = "PIXL is not sleepy!"

                    message_time = now

    if alive and now - depletion_time >= 600000:

        depletion_time = now

        stat = random.choice(["hunger", "happiness", "energy"])
        amount = random.randint(5, 10)

        if stat == "hunger":
            hunger -= amount
            if hunger < 0:
                hunger = 0
            message = "Hunger -" + str(amount)

        if stat == "happiness":
            happiness -= amount
            if happiness < 0:
                happiness = 0
            message = "Happiness -" + str(amount)

        if stat == "energy":
            energy -= amount
            if energy < 0:
                energy = 0
            message = "Energy -" + str(amount)

        message_time = now

    if hunger <= 0 or energy <= 0:
        alive = False

    if alive and now - action_time > 2000:

        if happiness > 80:
            pet = pet_happy
        else:
            pet = pet_idle

    if now - message_time > 3000:
        message = ""

    screen.fill(blue)

    pygame.draw.rect(
        screen,
        green,
        (0, 450, 800, 150)
    )

    screen.blit(
        font.render("Hunger: " + str(hunger), True, black),
        (20, 20)
    )

    screen.blit(
        font.render("Happiness: " + str(happiness), True, black),
        (20, 50)
    )

    screen.blit(
        font.render("Energy: " + str(energy), True, black),
        (20, 80)
    )

    if message:
        screen.blit(
            font.render(message, True, black),
            (300, 30)
        )

    if alive:

        screen.blit(pet, (272, 180))

        pygame.draw.rect(screen, white, (100, 500, 200, 70))
        pygame.draw.rect(screen, white, (300, 500, 200, 70))
        pygame.draw.rect(screen, white, (500, 500, 200, 70))

        screen.blit(food, (175, 510))
        screen.blit(play, (375, 510))
        screen.blit(sleep, (575, 510))

    else:

        screen.blit(
            font.render("PIXL PET IS DEAD", True, red),
            (315, 150)
        )

        pygame.draw.rect(
            screen,
            white,
            (250, 250, 300, 100)
        )

        screen.blit(
            font.render("RESPAWN", True, black),
            (350, 285)
        )

    pygame.display.update()

pygame.quit()
