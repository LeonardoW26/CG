import sys
import pygame

pygame.init()

#Configuração da tela
largura = 800
altura = 600

tela = pygame.display.set_mode((largura, altura))
pygame.display.set_caption("Pygame")

PRETO = (0, 0, 0)
BRANCO = (244, 255, 255)

tamanho_fonte = 50
fonte =pygame.font.SysFont(None, tamanho_fonte)

texto = fonte.render("Leonardo", True, BRANCO)
texto_rect = texto.get_rect(center=(largura/2, altura/2)) # meio

#texto_rect = texto.get_rect(center=(largura/10, altura/2)) # esquerda

#texto_rect = texto.get_rect(center=(largura/2, altura/25)) # cima

#texto_rect = texto.get_rect(center=(720, 300)) # direita centro

#texto_rect = texto.get_rect(center=(720 , 20)) # direita cima

#texto_rect = texto.get_rect(center=(720 , 580)) # direita baixo

#texto_rect = texto.get_rect(center=(80 , 580)) # esquerdo baixo

#Loop principal
while True:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()

    tela.fill(PRETO)
    tela.blit(texto, texto_rect)
    pygame.display.flip()




