import pygame
pygame.init()

pygame.joystick.init()
joysticks = [pygame.joystick.Joystick(i) for i in range(pygame.joystick.get_count())]
running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.JOYBUTTONDOWN:
            print(event)
        if event.type == pygame.JOYBUTTONUP:
            print(event)
        if event.type == pygame.JOYAXISMOTION:
            print(event)
        if event.type == pygame.JOYBALLMOTION:
            print(event)
        if event.type == pygame.JOYHATMOTION:
            print(event)
