# SpheroBolts
Code waarmee mensen verbinding kunnen maken met Sphero Bolts om ze te besturen met Python. Mogelijk om aan te sturen met een Xbox 360-controller.

# Benodigdheden
1. pip install bleak
2. pip install colorama

# Belangrijk!
Deze code is niet officieel van Sphero; dit hebben mijn teamgenoten en ik samen ontwikkeld.
We hebben code van een vorig project gebruikt en hebben het duidelijker gemaakt, zodat iedereen de code begrijpt.

*Zorg ervoor dat spherov3.py en sphero_constructors.py zich in dezelfde map bevinden waar je project wordt gemaakt.

# Functies van spherov3
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
<img width="391" alt="image" src="https://github.com/Research-Center-Data-Intelligence/Sphero-Swarm-Demonstrator/Images/example.png">

# XBOX Bolts
Dit is een zeer interactieve applicatie die mijn team heeft gemaakt. Wanneer je `ControllerUI.py` start, zoekt het naar alle bolten in de omgeving en vervolgens worden alle bolten in een lijstbox weergegeven. Je kunt eenvoudig een bolt selecteren en op 'Verbinden' klikken om verbinding te maken. Om te ontdekken welke bolt je in de lijst moet selecteren haal je een bolt uit de doos. Vervolgens geeft deze op het display een code weer beginnende met SB. Deze code staat aan het einde van de naam in de listbox. Nadat het verbinden is gelukt, start de bolt met een snelheid van 50 en kun je deze besturen met de joystick. Je kunt ook de snelheid verhogen door op 'RT' te drukken en om de snelheid te verlagen, druk op 'LB'. Om te stoppen, druk je op 'B'.

Let op, om te sturen moet je constant de joystick ingedrukt houden! Blijf dus bijvoorbeeld de joystick naar links duwen om de bolt in de gewenste richting te laten rollen. Het kan op het begin even wennen zijn om te ontdekken hoe je de controller gedraaid moet houden.

# Benodigheden
  pip install pygame

# Belangrijk
  Sluit je Xbox 360-controller aan voordat je dit script start."
  

<img width="302" alt="image" src="https://github.com/Research-Center-Data-Intelligence/Sphero-Swarm-Demonstrator/Images/xbox_ui.png">

     







