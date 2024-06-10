import pygame
from pygame import mixer
import sys
import random
import math
from resource_path import resource_path

pygame.init()

# Constantes de cor
PRETO = (0, 0, 0)
BRANCO = (255, 255, 255)

# Dimensões da tela
LARGURA = 800
ALTURA = 600

# Inicializar a tela
screen = pygame.display.set_mode((LARGURA, ALTURA))
pygame.display.set_caption("Pong")

# Configuração da fonte
font_file = resource_path("font/PressStart2P-Regular.ttf")
font = pygame.font.Font(font_file, 36)

# Definir sons
mixer.music.load(resource_path("audios/A_Lua_e_a_Noite.mp3"))
mixer.music.play(-1)
som = mixer.Sound(resource_path("audios/Sound_A.wav"))

clock = pygame.time.Clock()

class Raquete:
    def __init__(self, x, y, largura, altura, velocidade):
        self.x = x
        self.y = y
        self.largura = largura
        self.altura = altura
        self.velocidade = velocidade

    def desenhar(self):
        pygame.draw.rect(screen, BRANCO, (self.x, self.y, self.largura, self.altura))

    def mover(self, dy):
        self.y += dy
        if self.y < 0:
            self.y = 0
        elif self.y > ALTURA - self.altura:
            self.y = ALTURA - self.altura

class Bola:
    def __init__(self, x, y, tamanho, velocidade, verdadeira=True):
        self.x = x
        self.y = y
        self.tamanho = tamanho
        self.velocidade = velocidade
        self.direcao = random.uniform(0, 2 * math.pi)
        self.cor = self.gerar_cor_aleatoria()
        self.verdadeira = verdadeira
        self.tempo_de_vida = 2000 if not verdadeira else None  # 2 segundos para bolas falsas

    def desenhar(self):
        pygame.draw.ellipse(screen, self.cor, (self.x, self.y, self.tamanho, self.tamanho))

    def mover(self):
        self.x += self.velocidade * math.cos(self.direcao)
        self.y += self.velocidade * math.sin(self.direcao)

        # Colisão com bordas superior e inferior
        if self.y <= 0 or self.y >= ALTURA - self.tamanho:
            self.direcao = -self.direcao
            self.cor = self.gerar_cor_aleatoria()
            if dificuldade == "dificil" and self.verdadeira:
                self.mudar_direcao_aleatoriamente()

        if self.x <= 0 or self.x >= LARGURA - self.tamanho:
            self.direcao = math.pi - self.direcao

        if self.tempo_de_vida is not None:
            self.tempo_de_vida -= clock.get_time()
            if self.tempo_de_vida <= 0:
                return False
        return True

    def reiniciar_posicao(self):
        self.x = LARGURA // 2 - self.tamanho // 2
        self.y = ALTURA // 2 - self.tamanho // 2
        self.direcao = random.uniform(0, 2 * math.pi)
        self.cor = self.gerar_cor_aleatoria()

    def mudar_direcao_aleatoriamente(self):
        angulo = random.uniform(-math.pi / 4, math.pi / 4)  # Ajuste o ângulo aleatório
        self.direcao += angulo

    def gerar_cor_aleatoria(self):
        return (random.randint(0, 255), random.randint(0, 255), random.randint(0, 255))

class JogoPong:
    def __init__(self):
        self.dificuldade = "medio"
        self.configurar_dificuldade()
        self.raquete_pc = Raquete(10, ALTURA // 2 - 30, 10, 60, self.raquete_pc_velocidade)
        self.raquete_player = Raquete(LARGURA - 20, ALTURA // 2 - 30, 10, 60, 5)
        self.bola = Bola(LARGURA // 2 - 5, ALTURA // 2 - 5, 10, self.bola_velocidade)
        self.bolas_falsas = []
        self.score_pc = 0
        self.score_player = 0
        self.controle = False
        self.vencedor = ""

    def configurar_dificuldade(self):
        if self.dificuldade == "facil":
            self.bola_velocidade = 3
            self.raquete_pc_velocidade = 3
        elif self.dificuldade == "medio":
            self.bola_velocidade = 5
            self.raquete_pc_velocidade = 5
        elif self.dificuldade == "dificil":
            self.bola_velocidade = 7
            self.raquete_pc_velocidade = 7

    def menu_principal(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                elif event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_1:
                        self.dificuldade = "facil"
                        self.configurar_dificuldade()
                        self.controle = True
                        return
                    elif event.key == pygame.K_2:
                        self.dificuldade = "medio"
                        self.configurar_dificuldade()
                        self.controle = True
                        return
                    elif event.key == pygame.K_3:
                        self.dificuldade = "dificil"
                        self.configurar_dificuldade()
                        self.controle = True
                        return

            screen.fill(PRETO)
            texto_menu = font.render("Pong", True, BRANCO)
            text_menu_rect = texto_menu.get_rect(center=(LARGURA // 2, ALTURA // 2 - 100))
            screen.blit(texto_menu, text_menu_rect)

            texto_facil = font.render("1. Facil", True, BRANCO)
            texto_facil_rect = texto_facil.get_rect(center=(LARGURA // 2, ALTURA // 2))
            screen.blit(texto_facil, texto_facil_rect)

            texto_medio = font.render("2. Medio", True, BRANCO)
            texto_medio_rect = texto_medio.get_rect(center=(LARGURA // 2, ALTURA // 2 + 50))
            screen.blit(texto_medio, texto_medio_rect)

            texto_dificil = font.render("3. Dificil", True, BRANCO)
            texto_dificil_rect = texto_dificil.get_rect(center=(LARGURA // 2, ALTURA // 2 + 100))
            screen.blit(texto_dificil, texto_dificil_rect)

            pygame.display.flip()
            clock.tick(1)

    def fim_jogo(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()
                if event.type == pygame.KEYDOWN:
                    if event.key == pygame.K_SPACE:
                        self.controle = True
                        self.reiniciar_posicoes()
                        return

            screen.fill(PRETO)
            texto_fim = font.render(f"Vencedor: {self.vencedor}", True, BRANCO)
            text_fim_rect = texto_fim.get_rect(center=(LARGURA // 2, ALTURA // 2))
            screen.blit(texto_fim, text_fim_rect)

            pygame.display.flip()

    def reiniciar_posicoes(self):
        self.raquete_pc.y = ALTURA // 2 - self.raquete_pc.altura // 2
        self.raquete_player.y = ALTURA // 2 - self.raquete_player.altura // 2
        self.bola.reiniciar_posicao()
        self.bolas_falsas = []
        self.score_pc = 0
        self.score_player = 0

    def atualizar(self):
        global dificuldade
        dificuldade = self.dificuldade

        if not self.controle:
            self.fim_jogo()
        else:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    sys.exit()

            screen.fill(PRETO)

            # Mover todas as bolas
            self.bola.mover()
            self.bolas_falsas = [bola for bola in self.bolas_falsas if bola.mover()]

            bola_rect = pygame.Rect(self.bola.x, self.bola.y, self.bola.tamanho, self.bola.tamanho)
            raquete_pc_rect = pygame.Rect(self.raquete_pc.x, self.raquete_pc.y, self.raquete_pc.largura, self.raquete_pc.altura)
            raquete_player_rect = pygame.Rect(self.raquete_player.x, self.raquete_player.y, self.raquete_player.largura, self.raquete_player.altura)

            if bola_rect.colliderect(raquete_pc_rect) or bola_rect.colliderect(raquete_player_rect):
                som.play()
                self.bola.direcao = math.pi - self.bola.direcao
                self.bola.cor = self.bola.gerar_cor_aleatoria()
                if self.dificuldade == "dificil" and self.bola.verdadeira:
                    self.bola.mudar_direcao_aleatoriamente()
                    self.gerar_bolas_falsas()

            # Verificar colisão das bolas falsas com as bordas
            for bola_falsa in self.bolas_falsas:
                if bola_falsa.y <= 0 or bola_falsa.y >= ALTURA - bola_falsa.tamanho:
                    bola_falsa.direcao = -bola_falsa.direcao
                if bola_falsa.x <= 0 or bola_falsa.x >= LARGURA - bola_falsa.tamanho:
                    bola_falsa.direcao = math.pi - bola_falsa.direcao

            # Verificar se a bola verdadeira fez ponto
            if self.bola.x <= 0:
                self.bola.reiniciar_posicao()
                self.score_player += 1
                self.bolas_falsas = []
                if self.score_player == 5:
                    self.vencedor = "Player 1"
                    self.controle = False

            if self.bola.x >= LARGURA - self.bola.tamanho:
                self.bola.reiniciar_posicao()
                self.score_pc += 1
                self.bolas_falsas = []
                if self.score_pc == 5:
                    self.vencedor = "PC"
                    self.controle = False

            if self.raquete_pc.y + self.raquete_pc.altura // 2 < self.bola.y:
                self.raquete_pc.mover(self.raquete_pc.velocidade)
            elif self.raquete_pc.y + self.raquete_pc.altura // 2 > self.bola.y:
                self.raquete_pc.mover(-self.raquete_pc.velocidade)

            fonte_score = pygame.font.Font(font_file, 16)
            score_texto = fonte_score.render(f"Score PC: {self.score_pc}       Score Player_1: {self.score_player}", True, BRANCO)
            score_rect = score_texto.get_rect(center=(LARGURA // 2, 30))
            screen.blit(score_texto, score_rect)

            # Desenhar todas as bolas
            self.bola.desenhar()
            for bola_falsa in self.bolas_falsas:
                bola_falsa.desenhar()

            self.raquete_pc.desenhar()
            self.raquete_player.desenhar()

            pygame.draw.aaline(screen, BRANCO, (LARGURA // 2, 0), (LARGURA // 2, ALTURA))

            keys = pygame.key.get_pressed()
            if keys[pygame.K_UP] and self.raquete_player.y > 0:
                self.raquete_player.mover(-self.raquete_player.velocidade)
            if keys[pygame.K_DOWN] and self.raquete_player.y < ALTURA - self.raquete_player.altura:
                self.raquete_player.mover(self.raquete_player.velocidade)

            pygame.display.flip()
            clock.tick(60)

    def gerar_bolas_falsas(self):
        self.bolas_falsas = []
        for _ in range(4):
            nova_bola = Bola(self.bola.x, self.bola.y, self.bola.tamanho, self.bola.velocidade, verdadeira=False)
            nova_bola.direcao = random.uniform(0, 2 * math.pi)
            nova_bola.cor = self.bola.gerar_cor_aleatoria()
            self.bolas_falsas.append(nova_bola)

if __name__ == "__main__":
    jogo = JogoPong()
    jogo.menu_principal()
    while True:
        jogo.atualizar()
