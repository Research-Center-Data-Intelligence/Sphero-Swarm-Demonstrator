# SpheroBolts
Code waarmee mensen verbinding kunnen maken met Sphero Bolts om ze te besturen met python.

# Benodigdheden
1. pip install bleak
2. pip install colorama

# Belangrijk!
Deze code is niet officieel van Sphero; dit hebben mijn teamgenoten en ik samen ontwikkeld.
We hebben code van een vorig project gebruikt en hebben het duidelijker gemaakt, zodat iedereen de code begrijpt.

*Zorg ervoor dat spherov3.py en sphero_constructors.py zich in dezelfde map bevinden waar je project wordt gemaakt.

# Functies
In onze spherov3-code hebben we twee klassen:

1.Scanner
* Deze klasse bevat een scan-methode. Wanneer de methode wordt aangeroepen, krijg je alle bolts te zien.

* De scan-methode bevat ook een debug-argument met twee opties die je kunt gebruiken:
  debug = "bolts" OF debug = "readable" -- dit geeft de MAC-adressen van alle beschikbare bolts in een lijst;
  Geen Debug - dit print alle bolts met namen en mac adres in de opdrachtregel.
  
* Dit scant de omgeving voor beschikbare bolts en laat zien welke bolts je kunt verbinden.
  
2.spherov3_connector
* Deze klasse bevat 4 functies:
  
  .connect - Dit maakt verbinding met het MAC-adres van de bolt dat je hebt opgegeven. <mark>Argumenten(Mac_address)</mark>
  
  .roll - Nadat je verbinding is gelukt, kun je met de 'roll'-functie je bolt besturen. Deze functie vereist twee verplichte argumenten (snelheid, richting), waarbij de snelheid aangeeft hoe snel de bolt moet rollen en de richting aangeeft waarheen de bolt moet rollen. Bijvoorbeeld: (50, 180) betekent dat de bolt met een snelheid van 50 naar 180 graden rolt, dus naar voren.

  .rest_yaw - Dit brengt de bolt terug naar de standaardpositie. -Geen Argumenten

  .disconnect - Sluit de verbinding met de bolt af. -Geen Argumenten


# Voorbeeld:
<img width="391" alt="image" src="https://github.com/MuhammadHasoun/SpheroBolts/assets/159450804/0ad2e31a-16a9-4458-9a17-3941d0e43a9f">


     







