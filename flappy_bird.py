import pygame
import random
import sys
import os


pygame.init()


genislik, yukseklik = 400, 600
ekran = pygame.display.set_mode((genislik, yukseklik))
pygame.display.set_caption("Flappy Bird")
saat = pygame.time.Clock()

BEYAZ = (255, 255, 255)
MAVI = (135, 206, 250)
YESIL = (0, 200, 0)
KIRMIZI = (200, 0, 0)
GRI = (50, 50, 50)


font = pygame.font.SysFont("Arial", 28)
buyuk_font = pygame.font.SysFont("Arial", 48)


boru_genislik = 60


HIGHSCORE_FILE = "highscore.txt"


renkler = [
    (255, 0, 0),      
    (255, 127, 0),    
    (255, 255, 0),    
    (0, 0, 255),      
    (75, 0, 130),     
    (148, 0, 211)     
]
renk_index = 0.0  


def yuksek_skoru_oku():
    if os.path.exists(HIGHSCORE_FILE):
        with open(HIGHSCORE_FILE, "r") as f:
            return int(f.read())
    return 0


def yuksek_skoru_kaydet(skor):
    en_yuksek = yuksek_skoru_oku()
    if skor > en_yuksek:
        with open(HIGHSCORE_FILE, "w") as f:
            f.write(str(skor))

def boru_uret(bosluk):
    yukseklik_ust = random.randint(100, 400)
    ust = pygame.Rect(genislik, 0, boru_genislik, yukseklik_ust)
    alt = pygame.Rect(genislik, yukseklik_ust + bosluk, boru_genislik, yukseklik)
    return ust, alt


def buton(cizim_yazi, x, y, gen, yuk, renk, metin_rengi=BEYAZ):
    rect = pygame.Rect(x, y, gen, yuk)
    pygame.draw.rect(ekran, renk, rect, border_radius=10)
    ekran.blit(cizim_yazi, (x + (gen - cizim_yazi.get_width()) // 2, y + (yuk - cizim_yazi.get_height()) // 2))
    return rect


def zorluk_secimi():
    while True:
        ekran.fill(MAVI)
        baslik = buyuk_font.render("Zorluk Seç:", True, BEYAZ)
        ekran.blit(baslik, (genislik//2 - baslik.get_width()//2, 120))

        kolay_yazi = font.render("Kolay", True, BEYAZ)
        orta_yazi = font.render("Orta", True, BEYAZ)
        zor_yazi = font.render("Zor", True, BEYAZ)

        rect_kolay = buton(kolay_yazi, 120, 200, 160, 50, YESIL)
        rect_orta = buton(orta_yazi, 120, 270, 160, 50, (255, 165, 0))
        rect_zor = buton(zor_yazi, 120, 340, 160, 50, KIRMIZI)

        pygame.display.flip()

        
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.MOUSEBUTTONDOWN:
                if rect_kolay.collidepoint(etkinlik.pos):
                    return 3, 180  
                elif rect_orta.collidepoint(etkinlik.pos):
                    return 4, 150
                elif rect_zor.collidepoint(etkinlik.pos):
                    return 5, 120  


def ana_menu():
    while True:
        ekran.fill(MAVI)
        baslik = buyuk_font.render("Flappy Bird", True, BEYAZ)
        ekran.blit(baslik, (genislik//2 - baslik.get_width()//2, 120))

        basla_yazi = font.render("Başla", True, BEYAZ)
        cikis_yazi = font.render("Çıkış", True, BEYAZ)
        rect_basla = buton(basla_yazi, 120, 250, 160, 50, YESIL)
        rect_cikis = buton(cikis_yazi, 120, 320, 160, 50, KIRMIZI)

        pygame.display.flip()

        
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.MOUSEBUTTONDOWN:
                if rect_basla.collidepoint(etkinlik.pos):
                    return
                elif rect_cikis.collidepoint(etkinlik.pos):
                    pygame.quit()
                    sys.exit()


def oyun_bitti_ekrani(skor):
    yuksek_skoru_kaydet(skor)
    highscore = yuksek_skoru_oku()

    if skor >= 30:
        unvan = "Efsane Kuş :)"
    elif skor >= 20:
        unvan = "Usta Kuş :)"
    elif skor >= 10:
        unvan = "Deneyimli :)"
    else:
        unvan = "Acemi Kuş :)"

    while True:
        ekran.fill(GRI)
        yazi1 = buyuk_font.render("Oyun Bitti!", True, BEYAZ)
        yazi2 = font.render(f"Skorun: {skor}", True, BEYAZ)
        yazi3 = font.render(f"Yüksek Skor: {highscore}", True, BEYAZ)
        yazi4 = font.render(f"Ünvanın: {unvan}", True, BEYAZ)
        yeniden_yazi = font.render("Yeniden Başla", True, BEYAZ)

        ekran.blit(yazi1, (genislik//2 - yazi1.get_width()//2, 100))
        ekran.blit(yazi2, (genislik//2 - yazi2.get_width()//2, 180))
        ekran.blit(yazi3, (genislik//2 - yazi3.get_width()//2, 220))
        ekran.blit(yazi4, (genislik//2 - yazi4.get_width()//2, 260))

        rect_restart = buton(yeniden_yazi, 120, 340, 200, 50, YESIL)
        pygame.display.flip()

        
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.MOUSEBUTTONDOWN:
                if rect_restart.collidepoint(etkinlik.pos):
                    return


def oyun(boru_hizi, bosluk):
    global renk_index
    kus_y = 300
    kus_hiz = 0
    yercekimi = 0.5
    zipla = -8
    skor = 0
    borular = list(boru_uret(bosluk))

    while True:
        ekran.fill(MAVI)

        
        for etkinlik in pygame.event.get():
            if etkinlik.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if etkinlik.type == pygame.KEYDOWN and etkinlik.key == pygame.K_SPACE:
                kus_hiz = zipla
            if etkinlik.type == pygame.MOUSEBUTTONDOWN and etkinlik.button == 1:
                kus_hiz = zipla

    
        kus_hiz += yercekimi
        kus_y += kus_hiz

        
        for i in range(len(borular)):
            borular[i].x -= boru_hizi

        
        if borular[0].x < -boru_genislik:
            borular = borular[2:]
            borular.extend(boru_uret(bosluk))
            skor += 1

        
        kus_rect = pygame.Rect(50 - 15, int(kus_y) - 15, 30, 30)

        
        for boru in borular:
            if kus_rect.colliderect(boru):
                return skor

        
        if kus_y > yukseklik or kus_y < 0:
            return skor

        
        renk_index += 0.05
        if renk_index >= len(renkler):
            renk_index = 0.0
        aktif_renk = renkler[int(renk_index)]

        
        pygame.draw.circle(ekran, aktif_renk, (50, int(kus_y)), 15)

        
        for boru in borular:
            pygame.draw.rect(ekran, YESIL, boru)

        
        skor_yazi = font.render(f"Skor: {skor}", True, BEYAZ)
        ekran.blit(skor_yazi, (10, 10))

        pygame.display.flip()
        saat.tick(60)


while True:
    ana_menu()
    hiz, bosluk = zorluk_secimi()
    skor = oyun(hiz, bosluk)
    oyun_bitti_ekrani(skor)
