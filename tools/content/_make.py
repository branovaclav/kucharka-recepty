# One-off helper that wrote the content/*.json files (kept for reference). Text in "src" fields is verbatim from the source.
import json
TR = 'https://www.toprecepty.cz'
R = {}
R['kureci-rizek'] = dict(
  slug='kureci-rizek', recipe_id='kureci-rizek', lang='cs',
  source=dict(site='Toprecepty.cz', url=TR+'/recept/23122-kureci-rizek/', title='Kuřecí řízek', author='blazena.blazkova',
              rating='4,6', rating_count='33', photo='Fotografie © Toprecepty.cz.'),
  hero=dict(file='rizek-hero.jpg', alt='Kuřecí řízek s bramborovou kaší'),
  lede='Klasikou českých Vánoc a nedělních obědů je křupavý kuřecí řízek v trojobalu. Pokud s vařením teprve začínáte a nejste si s postupem přípravy jistí, vyzkoušejte tento jednoduchý recept, podle kterého se vám řízky jistě povedou.',
  time_sub='15 min příprava + 25 min tepelná úprava', servings=['4','porce'], ingr_small='pro 4 porce',
  ingredients=[['500 g','kuřecího masa (prsní nebo stehenní)'],['','sůl'],['','mletý pepř'],['','hladká mouka'],['','strouhanka'],['2','vejce'],['100 ml','mléka'],['','olej na smažení']],
  steps=[
    dict(h='Příprava masa', p=['Maso nakrájíme na plátky. Poté ho z obou stran osolíme a opepříme.'],
         photo=dict(file='rizek-step1.jpg', alt='Naklepané plátky masa a palička na maso', caption='Náhled videa ze zdroje: „Jak krájet maso na řízky“ · © Toprecepty.cz')),
    dict(h='Příprava obalovacích směsí', p=['Připravíme 3 hluboké talíře. Do prvního vsypeme hladkou mouku, do druhého rozklepneme dvě nevařená vajíčka bez skořápky, přidáme mléko, špetku soli, trochu pepře a pořádně promícháme. Do třetího talíře nasypeme strouhanku.'],
         extras=[dict(kind='sidenote', html='Tomuhle pořadí (mouka → vejce → strouhanka) se říká <b>trojobal</b>.')]),
    dict(h='Obalování řízků', p=['Maso důkladně obalíme z obou stran v prvním talíři, pak ve druhém a nakonec ve třetím.']),
    dict(h='Dvojité obalování', p=['Pro lepší konzistenci obalu je dobré postupovat tak, že obalíme v prvním, pak v druhém, pak zase prvním, zase v druhém a nakonec ve třetím talíři.']),
    dict(h='Smažení', p=['Na pánev nalijeme dostatečné množství oleje, rozpálíme ho a řízky osmažíme.'],
         extras=[dict(kind='our-inline', html='Bez pánve to jde i v horkovzdušné fritéze — postup je níže v tipu „Varianta · horkovzdušná fritéza“. Jak poznat, že je maso hotové, najdete v tipu „Je řízek hotový?“.'),
                 dict(kind='warning', html='Rozpálený olej může vzplanout. Nikdy ho nehaste vodou — pánev přikryjte pokličkou a vypněte plyn.')]),
  ],
  tips=[
    dict(kind='source', h='Varianta · horkovzdušná fritéza', facts=[['180 °C','teplota'],['20 min','doba'],['v ½','obrátit']],
         p=['Připravené, již obalené řízky nejprve potřete z obou stran olejem – použít můžete mašlovačku nebo olej ve spreji přímo k tomuto určený.',
            'Omaštěné řízky vložte do horkovzdušné fritézy a smažte při 180 °C po dobu 20 minut. V polovině doby je obraťte, aby byly zlatavé a křupavé z obou stran.'],
         src_html='Zdroj: <a href="https://www.toprecepty.cz/tipy-triky/jak-pripravit-rizek-v-horkovzdusne-friteze/" rel="noopener">Toprecepty.cz — Jak udělat řízek v horkovzdušné fritéze?</a> (Kristýna Anna Vondálová)'),
    dict(kind='ours', h='Je řízek hotový?', big='bílé uvnitř',
         p_html=['Řízek rozkrojte v nejsilnějším místě: maso musí být uvnitř <strong>bílé, bez růžové barvy</strong>, a šťáva čirá. Když je ještě růžové, smažte dál.',
                 'Máte-li <strong>ruční vpichový teploměr</strong>, zapíchněte ho z boku do středu plátku — hotové kuřecí maso má v jádru aspoň <strong>74&nbsp;°C</strong>.',
                 'Sondu do masa z naší trouby tady použít nejde: je připojená k troubě a funguje jen při pečení v troubě — ne na pánvi ani ve fritéze.']),
  ],
  foot_extra=['<strong>Varianta pro fritézu:</strong> <a href="https://www.toprecepty.cz/tipy-triky/jak-pripravit-rizek-v-horkovzdusne-friteze/" rel="noopener">Toprecepty.cz — tipy a triky</a> (Kristýna Anna Vondálová).'],
)
R['bryndzove-halusky'] = dict(
  slug='bryndzove-halusky', recipe_id='bryndzove-halusky', lang='sk',
  source=dict(site='Varecha.sk', url='https://varecha.pravda.sk/recepty/tradicne-bryndzove-halusky/85825-recept.html', title='Tradičné bryndzové halušky',
              author='Jana Štrbková (foodblog Medové motúzy)', rating='', rating_count='', photo='Foto: Jana Štrbková.'),
  hero=dict(file='halusky-hero.jpg', alt='Bryndzové halušky s praženou slaninou a pažítkou'),
  lede='Vynikajúce bryndzové halušky, to je tradičné slovenské jedlo, ktoré nesmie chýbať na našich stoloch. Môj recept je jednoduchý, s praženou slaninkou z mangalice a nasekanou pažítkou.',
  time_sub='30 min príprava + 10 min tepelná úprava', servings=['4','porcie'], ingr_small='pre 4 porcie',
  ingredients=[['750 g','zemiaky'],['300 g','múka polohrubá'],['50 g','slanina mangalicová údená'],['250 g','ovčia bryndza'],['','soľ'],{'group':'Ozdobenie:'},['1 zväzok','pažítka'],['','cibuľka jarná']],
  steps=[
    dict(h='', p=['Do veľkého hrnca dáme variť osolenú vodu. Nadrobno nakrájanú slaninu upražíme na panvici dozlatista. Na halušky očistíme zemiaky a najemno ich nastrúhame na strúhadle. Pridáme múku, soľ a vypracujeme cesto, ktoré nesmie byť priveľmi riedke a ani tuhé, aby sa dobre pretláčalo cez sitko.'],
         extras=[dict(kind='our-inline', html='Brambory strouhejte až těsně před míchaním těsta — nastrouhané na vzduchu rychle tmavnou. Slaninu můžete místo na pánvi upražit i v horkovzdušné fritéze (viz tip níže).')]),
    dict(h='', p=['Cesto pretláčame cez sitko na halušky (alebo hádžeme z doštičky nožom namočeným do vriacej vody) do hrnca s vriacou osolenou vodou. Keď halušky vyplávajú na hladinu, necháme ich ešte chvíľku variť a vyberieme kovovým sitkom, preložíme do misky a zmiešame s masťou z upraženej slaninky, aby sa nezlepili.'],
         extras=[dict(kind='sidenote', html='Nemáte-li sítko na halušky (haluškár), poslouží druhý způsob z receptu: těsto dejte na prkénko a nožem namáčeným ve vroucí vodě ho odkrajujte po kouskách rovnou do hrnce.'),
                 dict(kind='warning', html='Vroucí voda a pára pálí. Při pretláčení držte ruce nad hrncem jen krátce a halušky vybírejte děrovanou naběračkou nebo sítkem, ne prsty.')]),
    dict(h='', p=['Bryndzu zmiešame s dvomi lyžicami vody z halušiek. Halušky môžeme v miske hneď zmiešať s bryndzou alebo bryndzu servírovať až na tanieri.']),
    dict(h='', p=['Zelenú vňať z jarnej cibuľky nakrájame nadrobno. Halušky naservírujeme na tanier, posypeme opraženou slaninou, nakrájanou cibuľkovou vňaťou a nasekanou pažítkou.']),
  ],
  tips=[
    dict(kind='ours', h='Slanina bez pánve · horkovzdušná fritéza', facts=[['180 °C','teplota'],['6–8 min','doba'],['v ½','promíchat']],
         p_html=['Nadrobno nakrájenou slaninu rozprostřete v koši fritézy a pražte dozlatova. V polovině promíchejte a hlídejte — drobné kousky zhnědnou rychle.',
                 'Vypečený tuk z dna fritézy použijte na promíchání halušek místo masti z pánve.']),
  ],
  foot_extra=[],
)
R['spagety-carbonara'] = dict(
  slug='spagety-carbonara', recipe_id='spagety-carbonara', lang='cs',
  source=dict(site='Toprecepty.cz', url=TR+'/recept/23296-autenticke-spagety-carbonara-podle-emanuela/', title='Autentické špagety carbonara podle Emanuela', author='Eliza',
              rating='4,9', rating_count='97', photo='Fotografie © Toprecepty.cz.'),
  hero=dict(file='carbonara-hero.jpg', alt='Špagety carbonara s pancettou a pecorinem'),
  lede='Pravé italské špagety carbonara podle tradiční receptury vynikají jednoduchostí a dokonale krémovou omáčkou. Kombinace pancetty, žloutků, pecorina a čerstvě mletého pepře vytvoří výrazné a jemné těstoviny, které chutnají nejlépe ihned po přípravě.',
  time_sub='15 min příprava + 20 min tepelná úprava', servings=['4','porce'], ingr_small='pro 4 porce',
  ingredients=[['400-500 g','špaget'],['150 g','pancetty (nebo anglické slaniny)'],['8','žloutků'],['4 lžíce','strouhaného pecorina'],['1 lžíce','olivového oleje'],['','mletý pepř'],['','sůl']],
  steps=[
    dict(h='Příprava slaniny', p=['Pancettu nebo anglickou slaninu nakrájíme na proužky.']),
    dict(h='', p=['Na větší pánvi rozehřejeme olivový olej. Přidáme pancettu a za občasného míchání ji opečeme dozlatova a dokřupava.']),
    dict(h='Vaření špaget', p=['Ve velkém hrnci přivedeme k varu vodu. Vodu dobře osolíme a vsypeme do ní špagety. Špagety uvaříme podle návodu na obalu na skus.'],
         extras=[dict(kind='our-inline', html='Hrnec s vodou dejte na plyn hned na začátku a přikryjte ho pokličkou — voda se uvaří rychleji a pancettu zatím v klidu nakrájíte.')]),
    dict(h='Příprava vaječné směsi', p=['Do misky dáme žloutky, nastrouhané pecorino a čerstvě mletý pepř. Směs lehce osolíme a prošleháme.']),
    dict(h='', p=['Přidáme několik lžic vody z vaření těstovin a znovu promícháme.']),
    dict(h='', p=['Uvařené špagety přendáme přímo z vody do pánve s pancettou. Promícháme a pánev odstavíme ze zdroje tepla.'],
         extras=[dict(kind='sidenote', html='<b>Odstavit</b> = sundat pánev z hořícího plynu (nebo plyn vypnout). Žloutky pak zhoustnou jen teplem horkých špaget.')]),
    dict(h='Míchání', p=['Ihned přilijeme vaječno-sýrovou směs a rychle, ale opatrně promícháme, aby vznikla krémová omáčka a žloutky se nesrazily.']),
    dict(h='Servírování', p=['Carbonara ihned podáváme, případně posypeme dalším pecorinem a čerstvě mletým pepřem.']),
  ],
  tips=[
    dict(kind='source', h='Poznámka autorky', facts=[], p=['Podle pořadu S Italem v kuchyni.'], src_html='Autorka receptu Eliza na Toprecepty.cz'),
    dict(kind='ours', h='Co s bílky', big='8 bílků',
         p_html=['Po žloutcích zbude 8 bílků. V uzavřené nádobě vydrží v lednici 2–3 dny — hodí se třeba do omelety nebo na sníh do moučníku.']),
  ],
  foot_extra=[],
)
R['palacinky'] = dict(
  slug='palacinky', recipe_id='palacinky', lang='cs',
  source=dict(site='Toprecepty.cz', url=TR+'/recept/11511-palacinky/', title='Palačinky', author='lnk-lnk',
              rating='4,1', rating_count='69', photo='Fotografie: ivulinka / Toprecepty.cz.'),
  hero=dict(file='palacinky-hero.jpg', alt='Srolované palačinky posypané cukrem se skořicí'),
  lede='Palačinky patří mezi nejoblíbenější dětská jídla. Ať už je chystáte k snídani či k obědu, vždy se po nich zapráší. Můžete je naplnit třeba domácí marmeládou a posypat Grankem, skořicí nebo jen pocukrovat. V letních měsících můžete k dozdobení využít čerstvé ovoce.',
  time_sub='20 min příprava + 25 min tepelná úprava + 30 min odležení těsta', servings=['1','dávka'], ingr_small='na 1 dávku',
  ingredients=[['2-3','vejce'],['1 l','mléka'],['400 g','hladké mouky'],['1 špetka','soli'],['1 zarovnaná lžíce','cukru krupice'],['','slunečnicový olej na smažení'],{'group':'Dále:'},['','marmeláda na potření'],['','jahody'],['','Granko'],['','skořice'],['','moučkový cukr']],
  steps=[
    dict(h='Příprava těsta', p=['Vejce rozklepneme do misky, přidáme mléko, cukr, sůl, hladkou mouku a metličkou vymícháme hladké těsto, které před smažením necháme asi 30 minut odležet.']),
    dict(h='Smažení palačinek', p=['Rozehřejeme pánev a potřeme ji olejem. Naběračkou na ni nalijeme trochu těsta a krouživým pohybem ho rozlijeme po celé ploše pánve. Zvolna smažíme asi 2 minuty a jakmile povrch zmatní, palačinku otočíme a dosmažíme i z druhé strany. Hotové palačinky odkládáme na talíř a pokračujeme ve smažení do spotřebování těsta.'],
         extras=[dict(kind='our-inline', html='První palačinka se často nepovede — pánev se teprve prohřívá. Nic se neděje, další už půjdou.')]),
    dict(h='Servírování', p=['Hotové palačinky potřeme marmeládou, složíme nebo srolujeme a dozdobíme jahodami, Grankem, skořicí nebo moučkovým cukrem.']),
  ],
  tips=[
    dict(kind='ours', h='Aby palačinky nevychladly', facts=[['60–80 °C','trouba'],['přikrýt','talířem'],['20–30 s','mikrovlnka']],
         p_html=['Hotové palačinky skládejte na talíř do trouby vyhřáté asi na 60–80 °C (obyčejný ohřev, bez grilu a bez páry) a přikryjte je druhým talířem nebo alobalem, aby nevyschly.',
                 'Vychladlou palačinku ohřejete v mikrovlnce: na talíři, přikrytou, krátce 20–30 sekund.']),
  ],
  foot_extra=[],
)
TITLES={'kureci-rizek':('Kuřecí řízek','chicken'),'bryndzove-halusky':('Bryndzové halušky','pasta-rice'),'spagety-carbonara':('Špagety carbonara','pasta-rice'),'palacinky':('Palačinky','veg')}
for k,(t,ti) in TITLES.items(): R[k].update(title=t, tint=ti)
for k,v in R.items():
    json.dump(v, open(k+'.json','w',encoding='utf-8'), ensure_ascii=False, indent=1)
print('ok', list(R))
