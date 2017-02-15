#!/usr/bin/env python
# -*- coding: utf-8 -*-

#
#  This program is free software: you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation, either version 3 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program.  If not, see <http://www.gnu.org/licenses/>.
#

import os
import sys

import codecs
import enchant
import ngram

from pattern.nl import parse, split
from xml.sax.saxutils import unescape

# utf-8 fix
reload(sys)
sys.setdefaultencoding('UTF8')
# /utf-8 fix

DATADIR = "data" + os.sep


def load_ngram(lang="nl"):
    dictionary_words = codecs.open(DATADIR + lang + ".dict", "r", "utf-8")
    dictionary_words = dictionary_words.read()
    return(ngram.NGram(dictionary_words.split()))

# def ngram_check(word, ngram_model)
#    return ngram_model.check(word)


def analyze_word(word, bad_sentence, correctable_sentence,
                 new_sentence, dictionary, ngram_model):
    # Treat hypenated words different.
    if word.string.find('-') > -1:
        word_first_part = word.string.split('-')[0]
        word_second_part = word.string.split('-')[1]
        if dictionary.check(word_first_part) \
                and dictionary.check(word_second_part):
            # correctspelled_word += 1
            new_sentence += u" " + word_first_part + u"-" + word_second_part
        else:
            ngram_match_first = ngram_model.search(word_first_part)
            ngram_match_second = ngram_model.search(word_second_part)
            if not ngram_match_first[0][1] == 1.0 and \
                    ngram_match_second[0][1] == 1.0:
                if not ngram_match_first[0][1] == 1.0:
                    bad_sentence = True
                    print(word_first_part, ngram_match_first[:2])
                if not ngram_match_second[0][1] == 1.0:
                    bad_sentence = True
                    print(word_second_part, ngram_match_second[:2])
            else:
                # correctspelled_word += 1
                new_sentence += u" " + word_first_part + \
                                u"-" + word_second_part

    # Continue with non hypenated words.
    else:
        if not dictionary.check(word.string):
            if not word.string.isdigit() and len(word.string) > 2:
                # print(dir(ngram_model))
                ngram_match = ngram_model.search(word.string)
                if ngram_match:
                    if not ngram_match[0][1] == 1.0:
                        if not ngram_match[0][1] > 0.5:
                            if word.string.find('str') > -1:
                                t = word.string.replace(u'str', u'straat')
                                ngram_match = ngram_model.search(t)
                                if ngram_match[0][1] > 0.5:
                                    correctable_sentence = True
                                    new_sentence += u" " + ngram_match[0][0]
                                    print word.string, " wordt ", ngram_match[0][1]
                                    # TODO: revamp to class :)
                                else:
                                    bad_sentence = True
                            else:
                                bad_sentence = True
                        else:
                            correctable_sentence = True
                            new_sentence += u" " + ngram_match[0][0]
                    # total_word_count += 1
                else:
                    bad_sentence = True
            else:
                # correctspelled_word += 1
                new_sentence += u" " + word.string
        else:
            # correctspelled_word += 1
            new_sentence += u" " + word.string
    return(bad_sentence, correctable_sentence, new_sentence)


def ocr_correct(sentences = False, lang="nl"):
    """

    """
    dictionary = enchant.Dict(lang)
    ngram_model = load_ngram(lang)

    if not sentences:
        sentences = unescape(u"""
        In verband met den NIEUWJAARSDAG zal dit blad a.s. Vrijdag 1 Januari
        niet verschijnen. Het eerstvolgend No. van „De Graafschap-Bode"
        verschijnt derhalve A.S. MAANDAG 4 JANUARI 1932. H.H. Adverteerders en
        Correspondenten verdoeken wij beleefd, daarmede rekening te willen
        houden. DE UITGEEFSTER. [ Lijders aan Maagpijn! I | Maagkramp, Zuur,
        Hartwater en siechte spijs- ; * vertering zullen baat vinden bij het
        gebruik • ■ van Maagpoeder van Apotheker BOOM. ; ■ Verkrijgbaar In de
        meeste Apotheken en • « Drogistwinkel i ƒ 1.25 per verzegelde doos. •
        |V■ ' • mmmwm as Rente over het jaar 1931 kan vanaf jjj p 2 Januari
        1932 op de Spaarbank- $ boekjes, worden bijgeschreven. %
        GEMEENTE-SPAARBANK I fS . DOETINCHEM. $ m 'w. PORTRET-ATELIERS Fa.
        BRINCKER-v. GALEN, is het adres voor goede en mooie PORTRETTEN. 24818 •
        Hamburgcrstr. 19A, Tel. 164 DOETINCHEM. : ■ - j" viiSTO^G"'"'"] * De
        Laxeerpillen van Apotheker BOOM ver- J * drijven overtollige gal en
        slijm, zuiveren het ; ; bloed en bevorderen een goeden stoelgang. ! !
        Verkrijgbaar in de meeste apotheken en dro- ; ; gistwinkels è 30 en 55
        ct. per verzegelde doos. ! i Gratis en franco wordt op aanvraag een ! S
        proefdoosje toegezonden door firma A. M. S _ A ra tiem. ï

         Berichten Lijmers. BERGH.— Vergadering Raad gemeente Woensdag
         December, voormiddags uur. Afwezig heer Spekking. Punt Ingekomen
         stukken. Secretaris leest diverse ingekomen stukken voor, waarvan
         enkele voor kennisgeving worden aangenomen andere terzijde gelegd voor
         latere behandeling. Punt Benoeming Alg. Burgerlijk Armbestuur.
         Periodiek aftredend heer Winters. Voorgedragen worden benoeming:
         WIIUCJs; LSUCIIUWUVUI. Benoemd wordt heer Winters. Punt Eenige
         voorgestelde wijzigingen begrooting gemeente over 1931 worden
         goedgekeurd. Punt Rekening 1930 Gasthuis 's-Heerenberg. rekening
         Gasthuis 's-Heerenberg over 1930 wordt goedkeuring aangeboden. heer
         gedacht, Gasthuis wijziging pachten gebracht hebben. sprekers spijt
         heeft daar niets vernomen. Spr. bepleit noodzakelijkheid
         pachtverlaging. Spr. heeft gehoord, gratis kunstmest gegeven doch acht
         spr. niet zoo'n belang; grond jaartje buiten desnoods. heer Berntsen
         acht opmerkingen heer Wilmes zeer terecht. Spr. gelooft ook, menschen
         meer geholpen worden pachtverlaging gratis kunstmest. heer voelt voor
         pachtverlaging. Besloten wordt bovenstaande opmerkingen kennis
         Gasthuisbestuur brengen. Besloten wordt rekening 1930 Gasthuis goed
         keuren. Eindcijfers Algemeene rekening ontvangst 74939.14, uitgaaf
         63988.1 S'/J. Voordeelig slot 10.950.98>/2- Eindcijfers bijzondere
         rekening ontvangst 4274.5814, uitgaaf 10760.66. Nadeelig slot 6486.07
         Punt Begrooting 1932 Gasthuis. Besloten wordt ingediende begrooting
         voor 1932 Gasthuis 's-Heerenberg goed keuren. eindcijfers algemeene
         begrooting luiden: ontvangst uitgaaf 21952 bijzondere begrooting
         ontvangst 3761.—, uitgaaf 9836.75. Nadeelig slot 6075.75. Punt
         Rekening 1930 Instelling voorkoming Armoede. ue?e rekening wordt
         aangeboden goedgekeurd. eindcijfers luiden: ontvangst 6469.80, uitgaaf
         5522.32. Voordeeiig ;aido 947.68. Punt Begrooting 1932 vorengenoemde
         Instelling. Aangeboden goedgekeurd wordt begrooting over 1932.
         eindcijfer luidt uitgaaf ontvangst 7017,61. Punt aanvulling
         leerlingenlijst onder punt genoemde instelling wordt goedgekeurd. Punt
        Leening 30.000.—. Voorgesteld wordt 30.000 leenen .egen rente hoogstens
        koers Mij.1 voor Jemeente*crediet Amsterdam. leening noodig voor
        aanbrengen archief Gemeentehuis, wegenverbetering, aankoop materieel
        voor wegenverbetering werkverschaffing. licht toe, mogelijk Januari
        a.s. Rijkssubsidie voor werkloOzepzorg anders minder wordt. heer stelt
        voor werkverschaffing Januari a.s. geval voort zetten risico verminderd
        subsidie voor rekening gemeente nemen. zegt, bedoeling heer Brar.ts:
            Wordt wegenwals voorgestelde leening bestreden? Voorz.: Neen. heer
            bepleit aanschaffen wals maar stellen. heer Kupors achf
            aanschaffing wals zeer belang gemeente; -vals behoeft niet alleen
            nieuwe wegen, doch oude wegen gebruikt worden. heer Ditzhuyzen
            voelt voor spoedige uitvoering door commissie voor werkverruiming
            geadviseerde werken. Besloten wordt voorgestelde geldleening gaan.
            Punt Afstand strooken grond voor wegenverbetering. Voorgesteld
            wordt rtrooken grond aanvaarden voor verbet:ring wegen
            's-Heerenberg, Beek toerbeek. heer Ditzhuyzen zegt, niet gronden
            Braamt Kilder voorstel genoemd worden; waar afstand dezer grondvn
            over eenige dagen feit zijn, ctelt spr. voor deze strooken grond
            thans nemen Raadsbesluit noemen. voorstel wordt aangenomen,
            aangevuld voorstel heer Ditzhuyzen. Punt Voorstel I.z. aankoop
            grond voor bouw cadaverhuisje woningen voor sociaal achterlijken
            verworpen. stellen voor perceel grond koopen Lengel, groot ruim
            H.A. Gasthuis 's-Heerenberg, prijs 2100; pacht jaar. bedoeling
            dezen grond cadaverhuisje woningen voor sociaal-achterlijken
            bouwen. heer Bern aeht verkeerde methode Gasthuis steeds gronden
            tracht verkoopen, gelegen buiten 'a-Heerenberg, bedoeling armen
            's-Heerenberg kwijt raken.De heer begrijpt :ilet, meente niet
            publiceert courant, grond nnnkoopen. zijn particulieren
            instellingen genoeg, grond willen verkoopen. lijkt net, alsof
            alleen Gasthuis! grond verkoopen. Spr. tegen voorstel, omdat geen
            publiciteit gegeven voorgenomen grondaankoop omdat prijs hoog heer
            Ditzhuyzen vorige sprekers eens. Bovendien lijkt spr, niet
            gewenscht noodslachtplaats perceel grond zetten, waar woningen voor
            sociaal achterlijken komen staap. Weth. Thuis zegt, misverstand
            aanwezig Gasthuis biedt geen grond aan, doch gevraagd bedoelden
            grond verkoopen. Gasthuis houdt grond liever zelf. liook vorri Minf
            urnn noUlotl Itwt lIVI lllVk UVtttbll) Gasthuis sociaal
            achterlijken naar andere parochie tracht schuiven, omdat deze
            menschen, wanneer 's-Heerenberg zouden blijven wonen, laste
            Gasthuis zouden komen. Voorz. licht toe, grond hard noodig wonen
            menschen woningen wijze, welke onmenschelijk noemen Daarvoor
            woningbouw hard noodig. Spr. wijst buitengewoon moeilijk grond
            koopen; voor woningen voor sociaal-achterlijken heeft niemand grond
            koop! Daarom bleef niets anders over beroep doen Gasthuis, gemeente
            grond helpen. Spr. wijst grond Zeddam veel duurder was; grond
            Lengel, aangewezen door 'icer Roording, klein. Spr. hoopt, Raad
            grondaankoop besluiten, daar hard noodig beklagenswaardige menschen
            helpen menschwaardiger woningen. heer Berntsen zegt, alleen grond
            's-Heerenberg Gasthuis koopen, omdat armen, komen wonen straks
            laste vallen Gasthuis. Voorz. zegt, naar zijn overtuiging Gasthuis
            's-Heerenberg geen grond heeft liggen tegen denzelfden prijs. heer
            Berntsen hiermede niet eens. Voorz. zegt, combinatie
            cadaverhuisje-noodslachtplaats woningen voor sociaalachterlijken
            geen bezwaar oplevert, daar terrein groot genoeg heer Roording
            wijst stukken grond Klaassen, welke liggen. Gasthuis heeft veel
            meer grond. Spr. tegen voorgestelden grondaankoop. heer Berntsen
            vreest, geheel Lengel dupe wordt voorstel; menschen bouwen woningen
            vernielen maar vruchten veld. heer Elshof raadt voorstel houden
            volgende vergadering alsnog oproep voor rondaankoop doen. Voorz.
            betoogt, grondaankoop niet langer uitgesteld worden. voorstel
            grondaankoop wordt hierna verworpen 10—3 stemmen. Vóór stemmen
            beide wethouders heer Kupers; blanco heer Diecker. Punt Vergoeding
            leermiddelen geweigerd. Schoolbestuur Kilder verzoekt vergoeding
            voor aanschaffing leermiddelen, bedrag circa 241.—. stellen voor
            aanvrage niet willigen. heer Elshof bepleit inwilliging verzoek;
            heer Gerretsen steunt het. heer betoogt, schoolbesturen zuinig
            :mogelijk moeten zijn aanvragen. De-aangevraagde, leermiddelen pcht
            spr. luxe. heer Elshof zegt, schoolbestuur toch weigerende
            beslissing beroep gaan. Waarom moet gemeente eerst gedwongen
            worden? Spr. acht aangevraagde leer» middeien geen weeide. Weth.
            Thuis zegt, schoolbesturen reeds aangeschreven zijn vooral zuinig
            zijn aanvragen. gaat voorts onderhavige aanvrage niet niet luxe
            aanvrage valt echter r.iet onder „eerste volgens 0.-wet, doch moet
            bestreden worden gewone jaarlijkscke vergoeding voor instandhouding
            school, welke ƒ„B.— leerling jaar bedraagt. heer Berntsen vreest
            leelijke jezichten belastingbetalers, Raad nakkeKjk aanvragen
            schoolbesturen inwilligt. $pr. onderwijs gaarne terwille, doch moet
            belastingdruk denken. heer Elshof zegt, Inspecteur mondeling
            Pastoor verklaard heeft, bedoelde leermiddelen noodig waren. heer
            Ditzhuyzen heeft eens deskundige gehoord, schoolbesturen vergoeding
            leerling ruimschoots kunnen; fpr. daarom tegen aangevraagde
            subsidie. Voorz. brengt hierna voorstel stemming aanvrage niet
            willigen. Hiertoe wordt besloten stemmen. Tegen heeren Elshof,
            Wilmes Gerretsen. Punt Vastgesteld wordt verordening, regelende
            beroep geweigerde bouwvergunningen, bedoeld art. Woningwet. Punt
            Reglement Spaar- Voorschotbank. Voorgesteld wordt vast stellen Raad
            overgelegd reglement voor Spaar- Voorschotbank. heer Berntsen stelt
            voor commissie benoemen voor onderzoek voorgestelde reglement. heer
            Ditzhuyzen acht beter reglement nemen, omdat spoed kunnen afschrilt
            krijgen noodig volgende zitting eens wijzigingen voorstellen.
            Hiertoe wordt besloten. Punt Onbewoonbaarverklaring. Besloten wordt
            onbewoonbaarverklaring woning 's-Heerenberg 428, toebehoorend N.V.
            Huis Bergh. Punt Voorgesteld wordt WijnantU, bewoner vorenbedoelds
            onbewoonbaarverklaards woning, bijdrage hoogste fjoo verstrekken
            voor bouw 'van nieuwe woning. Dhr. Ditzhuyjen acht slaapkamer
            nieuwe wwjing kjein; voorts vraagt spr. voorwaarde «tellen,
            materialen gemeente gekocht moeten worden. Conform voorstel
            aangevuld hetgeen dhr. JPitjhuyzen opmerkt, woedt besloten. Punt
            Winkel»Tuitln?. wnkïls mogen Zondags 8-*9'/j. 11—.12 14—18 geopend
            ïljn. Voorgesteld wordt verordening, welke volgende regelen stelt.
            Kermis geld: tlui'.'n'T winkels niet. Voor wtnkels grens wordt
            bepaald, deze Zondags li—! 14—18. open mogen zijn.Dhr. stelt voor
            winket» open laten zijn B—9l/1 11—13 Zondagmorgen, toog
            kerkganger», inkoopen willen doen. Besloten wordt bepalen, winkels
            heele gemeente e-~9l/s> 14—i& Zondag open mogen zijn. Bergplaats
            voor vuilnis Zeddam. Gi'.debcstuur Zeddam vraagt voor terrein,
            waarop liet vui'lms gestort worden. achten dezen prijs hoog. Dhr.
            Berntsen hiermede eens; Gildebestuur heeft zelf veei belang
            voorgestelde regeling. vuil wordt overal Gildegrond geworpen. Spr.
            stelt voor voorloopig vergoeding goed keuren; spr. trachten
            Giloebestuur bewegen billijker houding. voorstel-B erntsen woidt
            aangenomen. Telefooninstaila'je Gemeentehui», etc. Volgens
            telefoondienst huistelefoon* installatie voor gemeente, aangesloten
            stadsnet, jaar 355.— kosten, ongeveer meer jaar thans telefoon
            kost. Deze installatie wordt zeer noodig geacht; wordt besloten.
            Subsidie verleend Streekcommissle bsvordering Vreemdelingenverkeer.
            Ingekomen adres „Streekcommissie bevordering Vreemdelingen* verkeer
            gemeentel» Eergh, Doetinchem, Gendringen, Hummelo Keppel Wisch
            ~'s-Heerenberg", adressanten verzoe j.cent inwoner jaar subsidie,
            waarvoor goede streekpropaganda zullen opzetten, zulks
            vermeerdering inkom* sten middenstand. Voorz. stelt voor adres
            financieel moeilijke tijden voorloopig terzijde leggen. Dhr.
            Berntsen hiermede eens. Spr. betoogt, b.v. ambtenaren, wier inkomen
            vrijwel niet gedaald aanmerking genomen mindere kosten
            levensonderhoud;, vacantie zullen gaan. gaat deze menschen naar
            deze streek trekken. Juist dezen slechten tijd vindt spr. alles
            voor vreemdelingenverkeer bevorderen. Bergh heeft prachtig
            natuurschoon. Dhr. Ditzhuyzen vorige-n spreker eens. Weth. Thuis
            wijst vreemdelingenverkeer middenstandsbelang Raaa gelegenheid
            winkeliers, hotelhou* ders eens helpen. Dhr. Berntsen merkt
            Gendrmgen'een voorbeeld zijn; ofschoon daar heelemaal geen
            vreemdelingenverkeer besloot gemeente toch subsidie voor
            vreemdelingen* verkeerpropaganda verkenen. Dhr. Brants staat niet
            enthousiast tegenover, maar niet tegenhouden- Weth. Reyers zegt,
            heele gemeente voeren propaganda profiteeren ;al. Voorz. legt niet
            voor afstel, doch slechts voor uitstel voelen. Zonder hoofdelijke
            stemming wordt hierna gevraagde subsidie besloten. Adres-Wehl i.ï.
            stichting Landbouwmlnlsterle. gemeentebestuur,"van Wehl verzoekt,
            act-, haesie adres regeenng, waarin instelling af?onderiijk
            ministerie landbouw verzocht wordt Dhr. Berntsen tegen. Spr./ ziet
            a<cft' adres groep ontevredenen, buiten boerenorganisafies actie
            voeren.. Deze Prganisaties hebben altijd'bun phcht gedaan ,bij
            regeering gedaan voor landbouwers, maar konden. Spr. acht
            organisatorisch, adres Wefcl steunen. dhr- Brants verklaart zich
            tegen. Dhr. Ditahuyten meent, toch niet verkeerd naast bestaande
            organisaties anderen voor eenzelfde doel ijveren; spr. ziet zoo,
            actie niet tegenover, doch naast organisaties gevoerd wordt. Dhr.
            Berntsen nogmaals uiteen, waar* onjuist acht adres steunen; dhr.
            Ditzhuyzen vindt hierin aanleiding aanhouding beslissing verzoeken
            voor nader onderzoek. Hiertoe wordt besloten.•" Rondvraag. I>hr.
            Elsliof wijst aanwexigheid van1 grint naar Siiulerdijk, tlat
            nutteloos hoopen ligt. Voort, ander, door heer Elshof berd;
            gebracht, aandacht schenken. Dhr. Gerretsen vraagt geen vergoeding
            uitgekeerd' wordt personen, Kilder xand gebracht hebben. heer geeft
            eenige inlichtingen omtrent deze kwestie. Voorz. »egt, rekeningen
            aannemers niet zijn ingekomen. beer Berntson vraagt, staat
            aanbrengen electrische lamp Gasthui» Zed&am. Voorz. zegt,
            vooroerciding tUCCI tIIU **•**** langs Probat Heerenberg. Voorz.
            aegt onderzoek toe. heer Ditzhuyzen vraagt redmi. ging goten
            bovendorp Zeddam. Voorz. zegt toe. beer Dieeker vraagt verbetering
            Wijnbergscbe naar Sinderdijk. Voorz. belooft zullen nagaan.
            Besloten wordt Abbenhuiis Braamt bomvpremie kennen. Hierna
            sluiting.
        ïj a.s. Feestdagen offreeren wij: alle soorten binnen- buitenlandsch
        GEDISTILLEERD. LIKEUREN. WIJNEN, BOERENJONGENS, ADVOCAAT, CHAMPAGNE, COGNAC,
        PUNCH. Perlstein DOETINCHBN. Boterolie Slaolie tegen verlaagde prijzen. PAUL
        WESTHOFF HUMMELO. twentsche BANK N.V.I gevestigd Amsterdam. Kapitaal Reserve
        5t.500.000.— Ikantoor winterswijk.! Belast ziet) uitvoering ALLE Bankierszaken.
        GRATIS apparaat indien proef wilt nemen onze „SIGI" mesjetT „siGi"Man itelt
        introductie deze prima mesjes proefpakket mesjes beschikbaar tegen kleine
        vergoeding slechts 0.90 PARKET (werkelijke winkelwaarde 12.—), terwijl daarbij
        GRATIS (raai ver* tilverd, roestvrij scheerapparaat ontvangt
        beschikbaarstelling deze voorwaarden geschiedt slechts tjjdelyk alleen
        ontvangst onderstaande coupon, binnen dagen bezit moet zijn. toezending
        onder rembours 0.90 plus rembourskosten geschiedt naar volgorde
        ingekomen coupons. voorkoming abuizen verzoeken geen geld acnden.
        COUPON Verkoopkantoor „SiGi"scheerapparaten ————— Firma MEYER RIJSWIJK
        Z..H. Zend geld Lindelaan Postbus oom* prMlpikkM (101 maajae ratia
            varzltvard apparaat »««•» snor ramboura »0.00 plua rembourakoitan
            Naam: stfHt r.w-r.fT.< <S.v.p. duidelijk schrijven; diukwerk
            verzenden: cent frankeeren)
             ——BB—— FABER Hamburgerstraat Do^ichem.
        """.encode( "utf-8" ))

    misspelled_words = set()
    sentences = parse(sentences)

    bad_sentences_count = 0
    good_sentence_count = 0
    correctable_sentence_count = 0

    correctspelled_word = 0
    misspelled_word_count = 0
    total_sentences_count = 0
    total_word_count = 0

    for sentence in split(sentences):
        total_sentences_count += 1
        bad_sentence = False
        correctable_sentence = False
        new_sentence = u""

        for chunk in sentence.chunks:
            for word in chunk.words:
                bad_sentence, \
                correctable_sentence, \
                new_sentence = \
                        analyze_word(word,
                                    bad_sentence,
                                    correctable_sentence,
                                    new_sentence,
                                    dictionary,
                                    ngram_model)

        if bad_sentence:
            print u"Bad: " + u" ".join([w.string for w in sentence.words])
            bad_sentences_count += 1
        elif correctable_sentence:
            print u"Correctable (old): " + \
                    u" ".join([w.string for w in sentence.words])
            print u"Correctable (new): " + new_sentence
            correctable_sentence_count += 1
        else:
            print u"Good: " + \
                    u" ".join([w.string for w in sentence.words])
            good_sentence_count += 1

    print ("Good_sentence_count: %i" % good_sentence_count)
    print ("Bad_sentences_count: %i" % bad_sentences_count)
    # print misspelled_word

if __name__ == "__main__":
    ocr_correct()
