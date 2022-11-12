import math
import matplotlib.pyplot as plt
import matplotlib as mpl


class dataSæt:
    # Opretter en global data liste som alle metoder kan få adgang til
    def __init__(self, arr=[], debug=False):
        # Dårlig Error handling
        """Skal modtage en liste af nummer"""
        if not isinstance(arr, list):
            print("List were not given")
        else:
            # Sætter ind i data liste og sortere
            self.data = arr
        self.data.sort()

        # Debugging
        if debug:
            print(self.data)

    def maksimum(self):
        """Tager det største tal i datasættet"""
        return max(self.data)

    def minimum(self):
        """Tager det laveste tal i datasættet"""
        return min(self.data)

    def variationsbredde(self):
        """Regner variationsbredde med at tage afstanden fra det største tal i datasættet og mindste tal i datasættet"""
        return self.maksimum() - self.minimum()

    def middelværdi(self):
        """Middelværdi er et fancy ord for gennemsnit, Tages summen og dividere med længde af datasættet"""
        return sum(self.data)/len(self.data)

    def median(self, data=None):
        """Giver median som er det midderste tal i sortert datasæt, hvis datasættet er lige, er median middelværdi af de to midderste tal"""
        # Tjekker om data liste er ulige eller lige, for at finde ud om median er en middelværdi af to tal
        if data == None:
            data = self.data

        if len(data) % 2:
            return data[round((len(data))/2)-1]
        else:
            return (data[math.floor((len(data)-1)/2)] + data[math.ceil((len(data)-1)/2)])/2

    def skævhed(self, nummerReturn=False):
        """Printer ud skævhed, kan slå til hvis man ville have værdi af skævhed"""
        # Skævhed regnes og kan printes eller returnere en værdi som enten går minus, 0 eller positiv
        skævhedværdi = self.middelværdi() > self.median()
        if nummerReturn:
            return skævhedværdi
        else:
            if skævhedværdi > 0:
                return("Højre skæv")
            elif skævhedværdi < 0:
                return("Venstre skæv")
            else:
                return("Ikke skæv")

    def kvartiler(self):
        """Regner kvartiler og returnere en liste som er sortet som [1. kvartil, 2. kvartil(Median), 3. kvartil]"""
        # Regner kvartilerne 1. kvartil er regnet af median fra start til median af det stor minus en da vi tæller fra 0
        # og median tages ikke med i ulige datasæt
        # 3. kvartil er regnet af median fra median af det stor til slut af datasættet
        Q1 = self.median(self.data[:math.floor(len(self.data)/2)-1:])
        Q2 = self.median()
        Q3 = self.median(self.data[math.ceil(len(self.data)/2):])
        return [Q1, Q2, Q3]

    def kvartilbredde(self):
        """Regner afstanden mellem første kvartil og 3. kvartil"""
        Q = self.kvartiler()
        return Q[2]-Q[0]

    def fraktiler(self, procent):
        """Tager ind procent og giver fraktilen"""
        # Regner fraktil ud med at gange lændgen af datalisten procent og hvis der gives et kommatal roundes det altid op
        return self.data[math.ceil((len(self.data))*(procent/100))-1]

    def hyppighed(self):
        """Metode som giver datasættet tilbage i en dict med hyppigheden af de forskellige tal"""
        # Laver en dict for hver af de værdi vi har, efter tilføjer hvormange gange det tal kommer op igen i listen
        hyppighedDic = {}
        for i in self.data:
            hyppighedDic[i] = 0
        for i in list(hyppighedDic.keys()):
            for j in self.data:
                if i == j:
                    hyppighedDic[i] += 1
        return hyppighedDic

    def kumHyppighed(self):
        #Tjekker om man kan gå en tilbage, hvis man kan så tilføj nuværende værdi med forrige og lig det ind i dict
        hyppighedDict = self.hyppighed()
        kumHyppighedDict=hyppighedDict
        keys = list(hyppighedDict.keys())
        
        for i in range(len(keys)):
            if(not i<1):
                kumHyppighedDict[keys[i]] = kumHyppighedDict[keys[i]] + kumHyppighedDict[keys[i-1]]

        return kumHyppighedDict

    def typetal(self):
        """Metode til at give type tal(ene) i en liste"""
        # Tager hyppigheden dict og deler den op i 2 list med dens Key og Values, finder max værdien af Value listen
        # Looper over Value listen for at finde om der er flere tal med samme gentagelser i datasættet og gemmer værdiernes position
        # som jeg kan gå over Key listen og få hvilke værdier der er flest af(typetal)
        tempDic = self.hyppighed()
        keyArr = list(tempDic)
        valueArr = list(tempDic.values())
        maxVal = max(valueArr)
        posKeyArr = []
        typeTalArr = []

        for i in range(len(valueArr)):
            if maxVal == valueArr[i]:
                posKeyArr.append(i)

        for j in posKeyArr:
            typeTalArr.append(keyArr[j])
        return typeTalArr

    def frekvens(self):
        """Denne metode ville give en dict af frekvenser for talene"""
        # Tager hyppighed Values og ændre dem med at dividere dem med lændge af datasættede og ganger med 100 for at få det i procent
        frekvensHypDic = self.hyppighed()
        keyArr = list(frekvensHypDic)

        for key in keyArr:
            frekvensHypDic[key] = (frekvensHypDic[key]/len(self.data))*100

        return frekvensHypDic

    def kumFrekvens(self):
        """Tager frekvens dict og tilføjer værdierne sammen"""
        #Tjekker om man kan gå en tilbage, hvis man kan så tilføj nuværende værdi med forrige og lig det ind i dict
        frekvensDict = self.frekvens()
        kumFrekvensDict=frekvensDict
        keys = list(frekvensDict.keys())
        
        for i in range(len(keys)):
            if(not i<1):
                kumFrekvensDict[keys[i]] = kumFrekvensDict[keys[i]] + kumFrekvensDict[keys[i-1]]

        return kumFrekvensDict

    def varians(self, stik=False):
        """Stik kan sættes til True hvis datasættet er en stikprøve og ikke en populationsprøve"""
        # Tager afstand mellem alle værdierne i datasættet og middelværdien, sætter dem i anden og ligger dem sammen
        # Dividere med lændgen af datasættet eller lændge af datasættet minus 1 hvis det er en stikprøve
        µ = self.middelværdi()
        sig = 0
        for i in self.data:
            sig += (i-µ)**2
        return round((1/(len(self.data)-stik))*sig, 10)

    def spredning(self, stik=False):
        """Sæt stik til True hvis du ville have spredning af en stikprøve og ikke en populationsprøve"""
        # Spredning kan regnes med at tage varians under kvadratroden
        return round(math.sqrt(self.varians(stik)), 10)

    def boksplot(self):
        """Boksplot fra matplotlib, kør visGraf() metode for at vise denne graf efter at havet kaldet den"""
        # Definiere de forskellige kvartiler og "whiskers" lændger for dannelse af boksplot
        # plt.boxplot(self.data,whis=(0,100),vert=False)
        # print(mpl.cbook.boxplot_stats(self.data,whis=[0,100]))
        stats = {}
        stats['A'] = mpl.cbook.boxplot_stats(self.data, labels='A')[0]
        stats['A']['q1'], stats['A']['q3'], stats['A']['whishi'], stats['A']['whislo'] = [
            self.kvartiler()[0], self.kvartiler()[-1], self.maksimum(), self.minimum()]

        fig, ax = plt.subplots(1, 1)
        ax.bxp([stats['A']], positions=range(1), showfliers=False, vert=False)
        xTicksSpacing = int(self.variationsbredde()/10)
        plt.xticks(range(self.minimum()-xTicksSpacing,self.maksimum()+xTicksSpacing, xTicksSpacing))

        plt.draw()

    def histogram(self):
        """histogram fra matplotlib, kør visGraf() metode for at vise denne graf efter at havet kaldet den"""
        keys = list(self.hyppighed().keys())
        values = list(self.hyppighed().values())

        fig, ax = plt.subplots()

        # create the xticks locations
        x = range(len(keys))

        ax.bar(x, values, 0.8, align='center')

        # set the ticks and labels
        ax.set_xticks(x)
        ax.set_xticklabels(keys)
        
        plt.draw()

    def visGraf(self):
        """Viser graferne der bliver er blevet kaldt, i tilfælde man ville se begge 2 grafer, boksplot og histogram sammen eller alene"""
        plt.show()

    def deskriptorer(self):
        print("Maks: " + str(self.maksimum()))
        print("Min: " + str(self.minimum()))
        print("Variationsbredde: " + str(self.variationsbredde()))
        print("Middelværdi: " + str(self.middelværdi()))
        print("Median: " + str(self.median()))
        print("Skævhed: " + str(self.skævhed()))
        print("Kvartilerne inkl. median: " + str(self.kvartiler()))
        print("Kvartilbredde: " + str(self.kvartilbredde()))
        print("5% Frak: " + str(self.fraktiler(5)))
        print("10% Frak: " + str(self.fraktiler(10)))
        print("80% Frak: " + str(self.fraktiler(80)))
        print("Typetal: " + str(self.typetal()))
        print("Varians: " + str(self.varians()))
        print("Spredning: " + str(self.spredning()))
        print("Hyppighed Dict: " + str(self.hyppighed()))
        print("Kumuleret Hyppighed Dict: " + str(self.kumHyppighed()))
        print("Frekvens Dict: " + str(self.frekvens()))
        print("Kumuleret Frekvens Dict: " + str(self.kumFrekvens()))

x = dataSæt([0, 2, 2, 2, 4, 4, 4, 4, 7, 7, 7, 7, 7, 7, 7, 7, 7, 7, 10, 10, 10, 10, 12, 12, 12, 12, 12], True)

x.deskriptorer()
x.histogram()
x.boksplot()
x.visGraf()

