
from math import log10

def calc_metrics(g, h, w, wa, n, hip=None):
    """VKİ ve yağ oranı hesaplar."""
    for v in [h, w, wa, n] + ([hip] if hip else []):
        if not isinstance(v, (int, float)) or v <= 0:
            raise ValueError("Ölçüler pozitif olmalı!")
    bmi = round(w / (h / 100) ** 2, 2)
    h, wa, n = h * 0.393701, wa * 0.393701, n * 0.393701
    g = g.lower()
    if g == 'male':
        if wa <= n:
            raise ValueError("Bel > boyun!")
        bfp = 86.010 * log10(wa - n) - 70.041 * log10(h) + 36.76
    elif g == 'female':
        if not hip:
            raise ValueError("Kalça gerekli!")
        hip = hip * 0.393701
        if wa + hip <= n:
            raise ValueError("Bel + kalça > boyun!")
        bfp = 163.205 * log10(wa + hip - n) - 97.684 * log10(h) - 78.387
    else:
        raise ValueError("Cinsiyet 'erkek'/'kadın'!")
    return bmi, round(bfp, 2)

def get_recs(g, bmi, bfp, goal):
    """Hedefe göre tavsiyeler."""
    goal = goal.lower()
    c = {"p": "- **Beslenme**: Protein: 1.8-2.5 g/kg.", "s": "- **Düzen**: 7-8 saat uyku."}
    r = []
    if goal == "kilo almak":
        r = (["VKİ düşük. Kilo al.", c["p"] + " +300-500 kalori (tavuk, yulaf).", "- **Egzersiz**: 3-4x squat, deadlift.", "- **Düzen**: 5-6 öğün, fıstık ezmesi."] if bmi < 18.5 else
             ["VKİ normal/yüksek. Kas artır.", c["p"] + " Avokado, zeytinyağı.", "- **Egzersiz**: Ağırlık, az kardiyo.", "- **Düzen**: Yemek öncesi az su."])
    elif goal == "yağ yakmak":
        if bmi >= 25 or (g == "male" and bfp > 24) or (g == "female" and bfp > 31):
            r = ["Yağ yüksek. Yağ yak.", "- **Beslenme**: -300-500 kalori, sebze, tavuk.", "- **Egzersiz**: 3-4x kardiyo, 2-3x ağırlık, HIIT."]
        else:
            r = ["Yağ normal. Fit kal.", "- **Beslenme**: Dengeli, az kalori.", "- **Egzersiz**: 3-5x kardiyo + ağırlık."]
        r += [c["s"].replace("uyku", "uyku, 10.000 adım")]
    elif goal == "vücut geliştirmek":
        r = (["Yağ düşük. Kas için kalori artır.", c["p"] + " Yulaf, fındık.", "- **Egzersiz**: 4-5x bench, squat, deadlift, pull-up (8-12x3-4 set).", "- **Düzen**: Protein shake, 1-2 gün dinlenme, antrenörle form."] if bmi < 18.5 or (g == "male" and bfp < 14) or (g == "female" and bfp < 21) else
             ["Yağ normal/yüksek. Kas + yağ kontrol.", c["p"] + " Şekeri kes.", "- **Egzersiz**: 4-5x bench, squat, deadlift, curls (6-12x3-4 set), 1-2x kardiyo.", "- **Düzen**: Program (göğüs, sırt), dinlenme."])
        r += [c["s"]]
    else:
        raise ValueError("Hedef: kilo almak/yağ yakmak/vücut geliştirmek!")
    return "\n".join(r)

def get_float(p):
    """Pozitif sayı al."""
    while True:
        try:
            v = float(input(p).strip())
            if v <= 0:
                raise ValueError
            return v
        except ValueError:
            print("Pozitif sayı gir (örn. 175.5)!")

def get_gender():
    """Cinsiyet al."""
    while True:
        g = input("Cinsiyet (erkek/kadın): ").strip().lower()
        if g in ["erkek", "kadın"]:
            return {"erkek": "male", "kadın": "female"}[g]
        print("Cinsiyet 'erkek' veya 'kadın' olmalı!")

def get_goal():
    """Hedef al."""
    while True:
        goal = input("Hedef (kilo almak/yağ yakmak/vücut geliştirmek): ").strip().lower()
        if goal in ["kilo almak", "yağ yakmak", "vücut geliştirmek"]:
            return goal
        print("Hedef: kilo almak/yağ yakmak/vücut geliştirmek!")

def main():
    print("VKİ ve Yağ Oranı Hesaplayıcı\n")
    try:
        g = get_gender()
        p = ["Boy (cm): ", "Kilo (kg): ", "Bel (cm): ", "Boyun (cm): "] + (["Kalça (cm): "] if g == "female" else [])
        v = [get_float(x) for x in p]
        bmi, bfp = calc_metrics(g, *v[:4], v[4] if g == "female" else None)
        print(f"\nSonuçlar: Yağ Oranı: %{bfp}, VKİ: {bmi}\nVKİ: {'Zayıf' if bmi < 18.5 else 'Normal' if bmi < 25 else 'Fazla Kilolu' if bmi < 30 else 'Obez'}")
        print("\nTavsiyeler:\n" + get_recs(g, bmi, bfp, get_goal()))
    except ValueError as e:
        print(f"Hata: {e}")
        main()
    except Exception as e:
        print(f"Hata: {e}. Girişleri kontrol et!")
        main()

if __name__ == "__main__":
    main()