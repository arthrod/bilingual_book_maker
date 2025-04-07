# Finnish Translation Prompt

## Conversation

**User:**
You will follow a three-step translation process. Always return the result of the third step. Do not reply with anything other than the result of the third step.

### 1. Translate the input content from English into {language}

Respect the original intent of the text, maintain the original Markdown formatting without omitting any content or adding extra commentary.

### 2. Carefully compare the original text with your translation, and provide constructive criticism and helpful suggestions to improve the translation. The final translation must adhere to the {language} language style

When offering suggestions, focus on improvements in:

- Accuracy: Correcting errors such as additions, mistranslations, omissions, or untranslated text.
- Fluency: Applying {language} grammar, spelling, and punctuation rules while avoiding unnecessary repetition.

### 3. Based on your initial translation and reflections, refine and polish the final translation without adding extra explanations or commentary

### Input

The content of the book to be translated is:

{text}

## Developer Message

As a professional translator and editor, you act as a cultural mediator between source text and target audience. You adopt a context-aware approach, where natural language use takes precedence over literal translations. Your primary objective is to craft a text that reads as though originally written in the requested language, paying attention to idiomatic expressions and typical sentence constructions.

- Do not alter the Markdown markup structure; do not add or remove links or modify any URLs.
- Do not change the contents of code blocks, even if they appear to contain errors.
- Always preserve the original line breaks without adding or removing blank lines.
- Do not modify any permalinks at the end of headings.
- Do not modify HTML-like tags such as `<Notes>`.
- Always convert capital case to sentence case.
- Always use « ... » for quotes.
- When translating from English to {language}, avoid anglicisms and maintain the author’s intent through thorough analysis of the source text. Actively reformulate sentences, and choose words that suit the style of the book. Use synonyms strategically to prevent repetition without compromising meaning.
- Consistency in punctuation is critical. Place punctuation according to local conventions and adopt uniform usage of commas, periods, and other punctuation marks. Use single quotes for quotation marks.
- For cultural references, seek natural language equivalents that convey the same connotation without distorting the original context.
- Titles in footnotes should appear in italics by using asterisks.
- Maintain an informal tone where it suits the book’s style, yet remain professional. Pay special attention to the flow of the text by varying sentence length and using linking words judiciously. Systematically correct double spaces and spelling discrepancies, adhering preferably to the official spelling rules for {language}.
- For complex economic concepts from the source material, opt for clear and accessible expressions without losing nuance. Technical terms retain their precision and, where necessary, include an explanation in context. You walk a fine line between academic accuracy and readability for a broad audience.
- Achieve cultural alignment by replacing typically American expressions with {language} counterparts carrying the same emotional weight. For historical examples or metaphors, identify parallel situations in history or society that local readers will recognize.
- Do not add the markdown footnotes below the translation. Do not change the structure of the paragraphs in the original text.

### Example Text

### Une enfance timide

Deux mois après la publication du livre blanc, le 8 janvier 2009 à 19 heures 27, Satoshi Nakamoto partage la première version du logiciel sur la liste de diffusion de Metzdowd. Le code source en C++ est publié de manière ouverte sous licence libre (MIT), de sorte que n'importe qui peut copier, modifier et utiliser le logiciel à sa guise. Celui-ci contient les données du bloc de genèse, le premier bloc de la chaîne à partir duquel celle-ci doit se prolonger.

Quelques heures plus tard, Satoshi commence à miner. Le deuxième bloc de la chaîne, le bloc 1, est validé par Satoshi le 9 janvier à 2 heures 54 du matin, ce qui marque le lancement effectif du réseau.

Le 10 janvier, Hal tente de faire fonctionner le logiciel. Après avoir échangé avec Satoshi pour faire en sorte que le logiciel fonctionne, il se met à miner et trouve son premier bloc (le bloc 78) à 1 heure du matin (UTC), gagnant de ce fait 50 bitcoins. Deux heures et demie plus tard, il partage son expérience sur Twitter (média social alors naissant) en écrivant > « *Running bitcoin*[^14] ». Le lendemain, dans la nuit du 11 au 12 janvier, Satoshi envoie 10 bitcoins à Hal par l'intermédiaire de son adresse IP : il s'agit du premier transfert d'une personne à une autre sur le réseau[^15].

Hal n'est pas la seule personne à expérimenter sur le réseau à ce moment-là : c'est également le cas de Dustin Trammell, un chercheur en sécurité informatique américain ayant découvert Bitcoin par la liste de diffusion. Celui-ci communique aussi avec Satoshi par courriel, et reçoit 25 bitcoins de sa part le 15 janvier[^16].

Mais les quelques personnes qui font fonctionner le logiciel ne suffisent pas. Dès le début, Satoshi sait bien que peu de gens se sont penchés sérieusement sur son modèle et qu'il va être compliqué d'attirer de nouveaux utilisateurs et contributeurs. C'est pourquoi il essaie de susciter l'enthousiasme en vendant son idée du mieux possible.

Le premier élément est le programme d'émission du bitcoin, qui a pour limite 21 millions d'unités. Dans le courriel d'annonce du prototype, Satoshi explicite le rythme de création monétaire :

> « Le nombre total de pièces en circulation sera de 21 000 000. Elles seront distribuées aux nœuds du réseau lorsqu'ils créeront des blocs, la quantité émise étant divisée par deux tous les 4 ans. [...] Une fois cette somme épuisée, le système pourra prendre en charge les frais de transaction si nécessaire[^17]. »

Le bitcoin a donc vocation à devenir une monnaie à offre fixe, déflationniste par nature, et cette particularité crée un enthousiasme. Le 11 janvier, Hal Finney est le premier à réagir en se réjouissant du fait que > « le système peut être configuré de manière à n'autoriser qu'un certain nombre maximum de pièces à être générées ». Il estime que si > « Bitcoin [est] un succès et [devient] le système de paiement dominant utilisé dans le monde entier », chaque pièce aura alors > « une valeur d'environ 10 millions de dollars[^18] ». L'estimation est contestable mais le raisonnement reste pertinent en raison du fonctionnement de Bitcoin.

Le 16 janvier, Satoshi reprend ainsi cet élément de communication dans un courriel qu'il partage à la liste de diffusion, où il déclare qu'il > « pourrait être judicieux de s'en procurer au cas où le phénomène prendrait de l'ampleur » et que > « si suffisamment de gens pensent la même chose, on pourra assister à une prophétie autoréalisatrice[^19] ». Cet élément est crucial, comme le montre le témoignage de Dustin Trammell qui confie à Satoshi que le raisonnement de Hal est > « l'une des raisons pour lesquelles [il a] démarré un nœud si rapidement ».

Outre le programme d'émission du bitcoin, Satoshi choisit de communiquer sur les défaillances du système bancaire, ce qui constitue le deuxième élément dans sa stratégie pour attirer l'attention.

En réalité, il le fait dès le bloc de genèse en y incluant le titre de la une du quotidien britannique *The Times* du 3 janvier 2009 annonçant que le ministre des finances britannique est sur le point de renflouer les banques pour la deuxième fois :

Cette phrase présente dans le premier bloc de la chaîne possède un rôle double : d'une part, elle empêche l'antidatage en prouvant que le système n'a pas été lancé avant le 3 janvier (Satoshi ne pouvait pas connaître cette une avant) ; d'autre part, elle indique symboliquement ce à quoi Bitcoin s'oppose en faisant référence au contexte monétaire et financier de l'époque.

En janvier 2009, le monde subit en effet de plein fouet les effets de la crise financière amorcée en 2007 par le dégonflement de la bulle immobilière aux États-Unis aussi connu sous le nom de la crise des subprimes. Les États renflouent les banques pour éviter de nouvelles faillites bancaires après celle de Lehman Brothers survenue le 15 septembre 2008, et les banques centrales procèdent à des assouplissements quantitatifs en injectant des liquidités sur les marchés financiers. Cette utilisation d'argent public, qui est littéralement créé pour l'occasion, choque profondément un certain nombre de citoyens qui réalisent que le système bancaire est en fait un système de profits privés et de pertes socialisées.

De par son absence de tiers de confiance, Bitcoin n'est, lui, pas soumis à l'arbitraire d'une banque centrale. Il contraste ainsi avec les monnaies étatiques, telles que le dollar ou l'euro, dont la quantité peut être modifiée arbitrairement par ceux qui contrôlent la création monétaire, au moyen de ce qu'on appelle une politique monétaire. La politique monétaire du bitcoin est programmée, inscrite en dur dans le protocole, pour en théorie ne plus jamais être altérée.

C'est ce que met en avant Satoshi lorsqu'il intervient sur le forum de la Fondation P2P, une organisation étudiant l'impact des infrastructures pair à pair sur la société, le 11 février 2009. Dans son message d'introduction à Bitcoin, il écrit :

> « Le problème fondamental de la monnaie conventionnelle est toute la confiance nécessaire pour la faire fonctionner. Il faut faire confiance à la banque centrale pour qu'elle ne déprécie pas la monnaie, mais l'histoire des monnaies fiat est pleine de violations de cette confiance. Il faut faire confiance aux banques pour détenir notre argent et le transférer par voie électronique, mais elles le prêtent par vagues de bulles de crédit avec à peine une fraction en réserve[^20]. »

Sur son profil, où il indique être un homme de 33 ans habitant au Japon, il donne une date de naissance particulière : le 5 avril 1975. Cette date, probablement fictive et composite, fait vraisemblablement référence à l'interdiction pour les particuliers de détenir de l'or aux États-Unis. Le jour du 5 avril se rapporte au jour de l'instauration de cette interdiction par l'Ordre exécutif 6102 signé par Franklin Delano Roosevelt le 5 avril 1933, et l'année 1975 correspond à son année d'abrogation lors de l'entrée en vigueur de la *Public Law* 93-373. Ce détail n'est pas anodin, puisque cette prohibition a permis en fin de compte d'instaurer un régime monétaire flottant n'ayant plus aucun lien avec l'or.

Ce n'est pas la seule référence aux métaux précieux. Satoshi écrit dans les commentaires le 18 février :

> « Il n'y a [...] personne pour agir en tant que banque centrale ou réserve fédérale afin d'ajuster l'offre monétaire au fur et à mesure que le nombre d'utilisateurs augmente. [...] En ce sens, c'est un système qui se comporte davantage comme un métal précieux. Plutôt que de faire varier l'offre pour que la valeur reste la même, on détermine l'offre à l'avance et la valeur change. À mesure que le nombre d'utilisateurs croît, la valeur par pièce augmente. Cela est susceptible de créer une boucle de rétroaction positive : plus les utilisateurs sont nombreux, plus la valeur augmente, ce qui peut attirer davantage d'utilisateurs désireux de profiter de cette hausse[^21]. »

Cette méthode de communication porte peu à peu ses fruits. Ainsi, même si certaines personnes finissent de se détourner de Bitcoin à l'instar de Hal Finney, Satoshi continue de recevoir des messages de la part de personnes intéressées. Le 11 avril 2009, Mike Hearn, un développeur britannique travaillant pour Google et s'adonnant au logiciel libre sur son temps libre, lui envoie un courriel posant une série de questions à propos de Bitcoin, en précisant qu'> « il est rare de rencontrer des idées vraiment révolutionnaires[^22] ». Hearn s'intéresse alors aux monnaies numériques, et notamment à Ripple.

Début mai 2009, c'est un jeune étudiant en informatique finlandais qui contacte Satoshi : il s'agit de Martti Malmi. Celui-ci a découvert Bitcoin début avril, s'est mis à miner et a même rédigé une courte description de Bitcoin sur le forum de Freedomain Radio où il soutenait l'hypothèse anarchiste que la monnaie pair à pair pourrait faire disparaître l'État[^23]. Dans son courriel à Satoshi, il écrit :

> « J'aimerais aider avec Bitcoin, s'il y a quelque chose que je peux faire. J'ai une bonne connaissance des langages Java et C grâce aux cours que j'ai suivis à l'école (j'étudie l'informatique), mais je n'ai pas encore beaucoup d'expérience en matière de développement[^24]. »

Malgré son manque d'expérience, Martti devient dans les mois qui suivent le principal contributeur à Bitcoin en dehors de Satoshi. Étant étudiant, il a en effet beaucoup de temps à consacrer au projet.

En particulier, Satoshi lui confie la charge du site web. Dès le mois de mai, Martti Malmi rédige une première version de la description sur SourceForge où il présente Bitcoin comme une > « monnaie numérique anonyme basée sur un réseau pair à pair » permettant de > « transférer de l'argent facilement via Internet, sans avoir à faire confiance à des tiers » et d'être > « à l'abri de l'instabilité causée par le système de réserves fractionnaires et par les mauvaises politiques des banques centrales[^25] ». Cette ébauche servira de base pour la présentation de Bitcoin sur le site web.

À l'époque, le bitcoin n'a pas de prix. Les gens qui testent le système se contentent de lancer le logiciel pour "générer des pièces". Les transactions sont peu nombreuses, et consistent le plus souvent en des auto-transferts. Les bitcoins sont alors vus comme des objets de collection réservés aux passionnés d'informatique. Les utilisateurs ont l'impression de contribuer à quelque chose, à l'instar des projets de calcul distribué (dits « [@home] ») où les gens mettent à disposition leurs ressources informatiques au service de bonnes causes.

Certains individus minent en continu. C'est le cas de Hal Finney qui fait fonctionner le logiciel entre janvier et mars, de James Howells qui valide des blocs entre février et avril, de Dustin Trammell qui fait tourner ses serveurs pendant plus d'un an, ou de Martti Malmi qui met son ordinateur portable à profit à partir d'avril. Mais le principal mineur de l'année de 2009 reste Satoshi, qui déploie une puissance de calcul bien plus grande et dont la production de blocs représente près de la moitié de celle du réseau.

En 2009, la difficulté de minage est de 1, ce qui impose à tous les nœuds du réseau de réaliser environ 4,3 milliards de calculs pour miner un bloc, et ce n'est pas rien pour un processeur. De ce fait, la production est plus lente que prévue : entre le 9 janvier 2009 et le 9 janvier 2010, seulement 33 802 blocs sont trouvés sur les 52 560 attendus, ce qui correspond à une durée moyenne entre chaque bloc de 15 minutes et 30 secondes au lieu des 10 minutes prévues. En particulier, le mois d'août 2009 constitue le pire mois pour l'activité minière : seuls 1 564 sur 4 464 blocs attendus sont trouvés, soit un temps moyen de 28 minutes et 30 secondes !

### Des premiers pas incertains

Malgré son lancement timide, Bitcoin survit à l'été et franchit une étape cruciale en octobre : son unité de compte acquiert un prix. Un individu utilisant le pseudonyme NewLibertyStandard (NLS), nouvellement arrivé dans la communauté, met en place sur sa page personnelle un service de change permettant aux gens de convertir leurs dollars en bitcoins et inversement. Pour estimer le taux de change, il se base sur le coût énergétique nécessaire pour obtenir un bitcoin, en prenant en compte le coût de l'électricité à son emplacement et la fréquence de sa production personnelle. Les prix sont publiés quotidiennement sur son site.

Le 12 octobre 2009, a ainsi lieu la première vente de bitcoins en dollars entre Martti Malmi et NewLibertyStandard : Martti cède 5050 bitcoins à NLS pour 5,02 $ virés sur son compte PayPal, ce qui correspond à un prix d'environ 0,001 $ par bitcoin[^26]. NLS effectuera par la suite d'autres échanges au cours des mois suivants, constituant la seule passerelle entre le dollar et le bitcoin.

Le 22 novembre marque l'ouverture du nouveau forum, sobrement appelé le *Bitcoin Forum*, qui est hébergé sur Bitcoin.org et géré par Martti Malmi. Ce forum abrite l'essentiel des discussions sur Bitcoin à partir de cette date. Il sera renommé Bitcointalk en août 2011 et hébergé à une nouvelle adresse.

Le 16 décembre 2009, Satoshi annonce la sortie de la version 0.2 du logiciel, version pour laquelle Martti Malmi est grandement crédité, ce qui clôt la première période de développement informatique de Bitcoin. L'année se termine en beauté lorsque la difficulté augmente enfin, en passant de 1 à 1,18 le 30 décembre.

Au début de l'année 2010, le bitcoin est désigné comme une « cryptomonnaie » (*cryptocurrency*) sur le site web. Le préfixe crypto- (qui vient du grec ancien [kruptos], kruptós, indiquant ce qui est caché, occulté) possède une signification double : il renvoie à la cryptographie sur laquelle Bitcoin s'appuie, et à la confidentialité, Bitcoin étant alors présenté comme une « monnaie numérique anonyme ».

Ce nouveau terme confirme le but central de Bitcoin : devenir une monnaie, c'est-à-dire un intermédiaire dans les échanges. Cela nécessite des personnes qui génèrent des transactions (par le biais du commerce) et d'autres qui traitent ces transactions (par le biais du minage). C'est donc tout naturellement que l'expansion de ces deux aspects complémentaires se produit à ce moment-là.

Le premier développement est l'essor commercial dont NewLibertyStandard peut être considéré comme le pionnier. Non seulement il est le premier commerçant à accepter le bitcoin comme moyen de paiement par l'intermédiaire de son service d'échange, mais il est aussi l'un des promoteurs originels de cet effort de construction économique. Dans son premier message sur le forum le 19 janvier 2010, il écrit ainsi :

> « Des gens m'ont acheté des bitcoins et m'en ont vendus. L'offre et la demande, même si elle sont faibles, existent déjà et c'est tout ce qu'il faut. Proposer d'échanger des bitcoins contre une autre monnaie n'est en fin de compte pas différent de l'échange de bitcoins contre des biens ou des services. Les monnaies sont des biens et le change est un service. [...] Vous pouvez acheter tous mes dollars ou bitcoins aujourd'hui, mais il y en aura toujours plus demain et après-demain. Toutes les personnes qui achètent ou vendent des biens en utilisant des bitcoins, y compris les changeurs, font progresser l'économie de Bitcoin. Que tout le monde fasse sa part. Achetez ou vendez quelque chose en échange de bitcoins [^27]! »

Dans les mois qui suivent, les services de change se développent, comme BitcoinFX ou Bitcoin Market. C'est pourquoi NLS propose que le bitcoin, à l'instar des monnaies échangées sur le marché des changes, adopte le sigle boursier BTC et le symbole du baht thaïlandais. L'utilisation du sigle BTC se normalise rapidement. Quant au symbole (le B majuscule traversé par deux barres verticales rappelant immanquablement le dollar), c'est Satoshi lui-même qui le conçoit, en s'inspirant de la proposition de NLS, lors de la création du premier véritable logo de Bitcoin[^28].

Les vendeurs de biens et de services apparaissent également. Outre son service de change, NLS ouvre un magasin en ligne où il propose à la vente des timbres et des autocollants. D'autres services acceptant le bitcoin apparaissent comme le service de voix sur IP Link2VoIP, l'hébergeur web Vekja.net et le vendeur de noms de domaines Privacy Shark. En parallèle, la première partie de poker mettant en jeu des bitcoins est organisée, ce qui inaugure la relation forte qui existera entre le jeu d'argent et la cryptomonnaie.

Enfin, en avril 2010, naît MyBitcoin, une application web dépositaire permettant un usage facile et serein de Bitcoin, notamment sur mobile. Grâce à celle-ci, les utilisateurs n'ont en effet pas besoin de télécharger les données complètes pour envoyer et recevoir des transactions, ni de conserver leurs bitcoins eux-mêmes en sauvegardant leurs clés privées. À cette époque, les portefeuilles légers n'existent pas, si bien que Satoshi lui-même juge qu'il est alors acceptable de passer par ce type d'application, même si cela va à l'encontre du principe de désintermédiation à la base de Bitcoin :

> « Le seul inconvénient c'est qu'il faut faire confiance au site, mais cela ne pose pas de problème pour la petite monnaie destinée aux micropaiements et aux dépenses diverses[^29]. »

L'année 2010 est également celle de l'essor du minage, qui se manifeste en premier lieu par l'émergence du minage par processeur graphique (GPU). Jusqu'alors, les mineurs sollicitaient leur processeur central (CPU) pour extraire de nouveaux bitcoins. Néanmoins, ces derniers processeurs s'avèrent peu performants pour effectuer des opérations répétées, comparés aux cartes graphiques qui sont largement plus adaptées à ce type de calcul répétitif. Par conséquent, tout le monde sait à ce moment-là que cette évolution est inéluctable, y compris Satoshi qui déclare en décembre 2009 que la communauté doit se > « mettre d'accord pour reporter la course aux armements des GPU aussi longtemps que possible pour le bien du réseau[^30] ».

La boîte de Pandore est ouverte par Laszlo Hanyecz, un développeur américain d'origine hongroise de 28 ans, qui découvre Bitcoin en avril. Après avoir acheté des bitcoins à NLS et essayé le système de transactions, celui-ci programme début mai un logiciel de minage qui s'adapte aux cartes graphiques. Cette optimisation lui permet d'occuper rapidement une place importante dans la production des blocs. Ceci attire l'attention de Satoshi Nakamoto qui le contacte et lui demande de ralentir ses opérations afin que le minage reste accessible à tous :

> « L'un des principaux attraits pour les nouveaux utilisateurs est que toute personne disposant d'un ordinateur peut générer des pièces gratuites. Lorsqu'il y aura 5 000 utilisateurs, cette incitation s'estompera peut-être, mais pour l'instant, c'est toujours vrai. Les GPU limiteraient prématurément cette incitation à ceux qui disposent d'un matériel GPU haut de gamme. Il est inévitable que les clusters de calcul GPU finissent par accaparer toutes les pièces générées, mais je ne veux pas précipiter l'arrivée de ce jour-là. [...] Je ne veux pas passer pour un socialiste, je me moque de la concentration des richesses, mais pour l'instant, nous obtenons plus de croissance en donnant cet argent à 100 % des gens qu'en le donnant à 20 %[^31]. »

Laszlo abaisse sa cadence, mais continue à miner avec sa carte graphique. Avec sa méthode, il accumule ainsi des dizaines de milliers de bitcoins.

Toutefois, cela n'est pas entièrement négatif pour le projet car il finit par réinjecter ses bitcoins dans l'économie de la façon la plus emblématique possible : en achetant quelque chose avec, et plus précisément des pizzas. Le 18 mai 2010, il écrit ainsi l'annonce suivante sur le forum :

> « Je paierai 10 000 bitcoins pour deux ou trois pizzas... genre peut-être 2 grandes pour qu'il m'en reste le lendemain. J'aime avoir des restes de pizza à grignoter pour plus tard. Vous pouvez faire la pizza vous-même et l'amener jusqu'à chez moi ou la commander pour moi auprès d'un service de livraison, mais mon objectif c'est de me faire livrer, en échange de bitcoins, de la nourriture que je n'ai pas à commander ou à préparer moi-même. [...] Si vous êtes intéressé, faites-le moi savoir et nous pourrons nous arranger[^32]. »

Cette offre trouve preneur au bout de quatre jours. Le 22 mai, un jeune Californien du nom de Jeremy Sturdivant accepte l'échange sur la messagerie instantanée IRC : il commande deux pizzas de Papa John's qui sont livrées chez Laszlo à Jacksonville en Floride, et reçoit en échange 10 000 bitcoins[^33], ce qui représente alors environ 44 $ sur Bitcoin Market. Cela clôt le premier achat d'un bien physique en bitcoins ! Cet évènement symbolique sera par la suite commémoré tous les ans à cette date comme le *Bitcoin Pizza Day*.

Une autre personne vient contribuer au succès du projet. Vers la fin du mois de mai, un développeur américain de 44 ans, nommé Gavin Andresen, découvre Bitcoin par le biais d'un article publié sur InfoWorld. De retour d'Australie, momentanément sans emploi, il se met à travailler sur son premier projet : un robinet à bitcoins (*bitcoin faucet*) qui donne des bitcoins à quiconque en fait la requête. Le 11 juin, Gavin lance son service et le présente sur le forum :

> « Pour mon premier projet de programmation sur Bitcoin, j'ai décidé de faire quelque chose qui semble vraiment stupide : j'ai créé un site web qui distribue des bitcoins. [...] Pourquoi ? Parce que je veux que le projet Bitcoin réussisse, et je pense qu'il a plus de chances de réussir si les gens peuvent obtenir une poignée de pièces pour l'essayer[^34]. »

Ce *faucet*, qui offre d'abord 5 bitcoins par requête au tout début, est approuvé par Satoshi, ce dernier ayant > « prévu de faire exactement la même chose si quelqu'un d'autre ne l'avait pas fait[^35] ». Le service, sollicité par beaucoup de personnes, distribuera plus de 19 700 bitcoins jusqu'à sa fermeture deux ans plus tard. De plus, Gavin s'implique dans le développement du logiciel et échange beaucoup avec Satoshi par courriel. Il en devient rapidement le bras droit grâce à la confiance qu'il lui inspire.

Malgré cette croissance économique encourageante, l'activité reste extrêmement réduite sur le réseau. Le 30 juin, sur la liste de diffusion de Bitcoin, James A. Donald déclare ainsi que > « Bitcoin est en quelque sorte mort » et que > « le problème est que le bitcoin a besoin d'une écologie d'utilisateurs pour être utile[^36] ». Toutefois, quelques jours plus tard, un évènement vient lui donner tort.

### Le slashdotting

Le 11 juillet 2010, suite à la sortie de la version 0.3 du logiciel, une courte présentation de Bitcoin rédigée par un utilisateur est publiée sur Slashdot, un site d'actualité très populaire traitant de sujets pour les *nerds* comme l'informatique, les jeux vidéo, la science, Internet, etc. L'argumentaire de vente est le suivant :

> « Que pensez-vous de cette technologie disruptive ? Bitcoin est une monnaie numérique basée sur un réseau pair à pair, sans banque centrale, et sans frais de transaction. À l'aide d'un concept de preuve de travail, les nœuds brûlent des cycles de processeur pour chercher des paquets de pièces et diffusent leurs résultats sur le réseau. L'analyse de la consommation d'énergie révèle que la valeur marchande des bitcoins est déjà supérieure à la valeur de l'énergie nécessaire pour les générer, ce qui indique une demande saine. La communauté a bon espoir que la monnaie restera hors de portée de tout État[^37]. »

Ceci provoque un afflux massif de nouveaux visiteurs sur le site et sur le forum, ainsi qu'une augmentation du nombre d'utilisateurs et de mineurs sur le réseau. Le réseau tient le coup malgré la montée en charge. En conséquence, le prix du bitcoin connaît la première hausse majeure de son histoire, en passant de 0,008 $ à 0,08 $ en une semaine, soit une multiplication par 10 !

Parmi les personnes qui découvrent Bitcoin grâce à Slashdot, il y a Jed McCaleb, un entrepreneur et programmeur américain de 35 ans, connu pour avoir cofondé et développé le logiciel de partage de fichiers en pair à pair eDonkey2000 dans les années 2000. Constatant à quel point il est pénible de se procurer du bitcoin contre des dollars, il décide de créer une place de marché spécialisée. Pour ce faire, il réutilise un de ses anciens projets mis au point en 2007 : *Magic The Gathering Online eXchange* (MTGOX), un site web qui permettait d'acheter et de vendre des cartes du jeu en ligne *Magic: The Gathering Online*[^38]. Il reprend le même nom de domaine au passage : mtgox.com.

Une semaine plus tard, le 18, la plateforme de change Mt. Gox (« *Mount Gox* ») est lancée et annoncée officiellement sur le forum par Jed. Grâce à son expertise, il fait en sorte que la plateforme fonctionne comme une place de marché automatisée, à l'instar des bourses en ligne modernes. Elle se distingue de Bitcoin Market par le fait qu'elle est > « toujours en ligne, automatisée », que > « le site est plus rapide et a un hébergement dédié » et que > « l'interface est plus agréable[^39] ». Par conséquent, Mt. Gox s'impose rapidement comme le moyen principal de se procurer du bitcoin, devenant la référence en ce qui concerne le cotation en dollars.

Le minage connaît également une phase ascendante. L'afflux de nouveaux mineurs fait passer le taux de hachage du réseau (le nombre de calculs par seconde) au-dessus du milliard de calculs par seconde (1 GH/s) dès le 13 juillet. Certains mineurs développent leur propre algorithme de minage par GPU. C'est le cas de ArtForz, un développeur allemand, qui se met à miner le 19 juillet et qui construit au cours du temps la première ferme de minage de Bitcoin, qui sera connue sous le nom d'« ArtFarm »[^40].

Mais cette croissance suivant la présentation sur Slashdot provoque également des problèmes d'ordre technique, mettant le système à l'épreuve. Deux incidents viennent ainsi perturber le projet.

Le premier incident est la découverte d'une vulnérabilité dans le code de Bitcoin qui rend possible la dépense de bitcoins à partir de n'importe quelle adresse (cette vulnérabilité sera appelée le « 1 RETURN bug » en référence au script nécessaire pour réaliser cette dépense). C'est ArtForz qui en découvre l'existence à la fin du mois de juillet 2010. Au lieu d'exploiter cette faille et de s'emparer de la richesse présente sur le réseau pour la revendre discrètement, il choisit de prévenir Satoshi et Gavin par courriel. Satoshi s'empresse d'inclure la correction dans la mise à jour 0.3.6 et recommande à tous les utilisateurs de mettre à jour leur logiciel. La vulnérabilité n'est pas exploitée et Bitcoin échappe ainsi au pire.

Le second évènement est le *value overflow incident*. Le 15 août vers 17 heures, un bloc miné contient une transaction qui crée plus de 184 milliards de bitcoins. Cette création exploite une vulnérabilité de dépassement de mémoire (*overflow*) dans la représentation des quantités dans Bitcoin. Une heure plus tard, le problème est repéré par Jeff Garzik, un ingénieur américain ayant découvert Bitcoin grâce à Slashdot, qui avertit la communauté sur le forum[^41].

La réaction de Satoshi ne se fait pas attendre. Un peu avant minuit, il publie un correctif créant une chaîne alternative ne contenant pas la transaction incriminée. La situation conflictuelle est résolue lorsque la chaîne correcte devient plus longue que l'autre le lendemain à 8 heures 10 du matin. Cet incident perturbe l'activité du réseau pendant 15 heures environ mais le problème est vite réglé grâce à une réactivité forte de la communauté. Suite à cet incident, Satoshi implémente un système d'alerte dans Bitcoin, lui permettant d'avertir tous les nœuds du réseau en cas de problème technique[^42].

Au cours de l'automne, la popularisation du minage par processeur graphique rend le minage par CPU quasi impossible. C'est ce qui provoque l'apparition de la première coopérative de minage le 27 novembre, Bitcoin.cz Mining, une organisation permettant aux petits mineurs de lisser leurs revenus en regroupant leurs puissances de calcul respectives[^43]. Créée par Marek Palatinus (connu sous le pseudonyme de slush), un architecte informatique tchèque, la coopérative sera par la suite rebaptisée Slush Pool en son hommage.

De manière générale, à la fin de l'année 2010, on peut considérer que le projet Bitcoin a pris son envol : l'économie s'est fortifiée, notamment avec les services de change, le minage s'est spécialisé avec l'apparition du minage par GPU et le protocole a été mis à l'épreuve par la découverte de failles dans le logiciel. Ces éléments montrent que les incitations des différents acteurs du système sont alignées. C'est à ce moment-là que Satoshi décide de disparaître.

### La disparition de Satoshi Nakamoto

La disparition de Satoshi Nakamoto se fait progressivement à partir de décembre 2010. Satoshi n'explicite pas les raisons qui le poussent à s'éclipser, mais nous pouvons les deviner. Tout d'abord, le projet a pris : il a grossi à tel point qu'il devient difficile de diriger le mouvement. Mais surtout Satoshi redoute la réaction des agences étatiques, une préoccupation qu'il exprime dans un message daté du 5 juillet 2010 (commentant le brouillon de la présentation de Bitcoin qui sera proposée à Slashdot), où il déclare ne pas vouloir mettre trop en avant l'aspect « anonyme » de Bitcoin ou son opposition aux autorités légales qui constituerait une « provocation[^44] ».

L'élément déclencheur est l'affaire WikiLeaks. WikiLeaks est une organisation non gouvernementale à but non lucratif fondée par le cypherpunk Julian Assange en 2006, dont la raison d'être est de donner une audience aux lanceurs d'alertes et aux fuites d'information, tout en protégeant leurs sources. À partir de 2010, les documents confidentiels révélés par l'ONG commencent à être relayés par les grands médias et à faire du bruit dans l'opinion publique. C'est notamment le cas de l'*Afghan War Diary*, un ensemble de documents et de rapports militaires américains secrets sur la guerre en Afghanistan faisant notamment état de la dissimulation des victimes civiles, qui est publié le 25 juillet 2010 grâce à la contribution de Bradley Manning, un analyste militaire de l'armée des États-Unis[^45]. On peut également citer les *Iraq War Logs*, documents secrets sur la guerre en Irak entre 2004 et 2009 publiés le 23 octobre et révélant le nombre de victimes civiles et les actes de torture perpétrés.

Le financement de WikiLeaks repose essentiellement sur les dons du public. Il s'agit d'une activité sensible pour les firmes réglementées qui craignent les potentielles représailles des autorités. C'est ainsi que la société de paiement en ligne Moneybookers gèle le compte de l'ONG le 14 octobre 2010. À la suite de ces révélations, il est ainsi de plus en plus probable que WikiLeaks s'expose à davantage de sanctions.

Le 10 novembre, Amir Taaki, un jeune anglais d'origine iranienne ayant fraîchement découvert Bitcoin, voit dans la situation de WikiLeaks une opportunité de démontrer l'utilité de la résistance à la censure du système. Il écrit ainsi sur le forum :

« Je voulais envoyer une lettre à Wikileaks à propos de Bitcoin car, malheureusement, ils ont subi plusieurs incidents où leurs fonds ont été saisis dans le passé. [...] Quelqu'un sait où leur envoyer un message[^46] ? »

Les réactions sont mitigées. D'après un utilisateur, « cela peut être bénéfique pour wikileaks, mais pas nécessairement pour Bitcoin[^47] ».

Un mois plus tard, le 3 décembre, PayPal gèle le compte de WikiLeaks. Certaines personnes sur le forum suggèrent d'encourager WikiLeaks à accepter le bitcoin : cela paraît en effet le « moment idéal pour mettre en place les dons en bitcoins[^48] ». Cela fait réagir Satoshi le lendemain qui s'oppose à cette évolution et déclare :

« Le projet a besoin de grandir progressivement pour que le logiciel puisse se renforcer en cours de route.

J'appelle WikiLeaks à ne pas commencer à utiliser Bitcoin. Bitcoin est une petite communauté expérimentale encore naissante. Vous n'obtiendriez rien de plus que quelques piécettes et l'agitation que vous apporteriez nous détruirait probablement à ce stade[^49]. »

Dans les jours qui suivent, c'est un véritable blocus financier qui se met en place contre WikiLeaks, auquel participent Mastercard et Visa, mais aussi Western Union, Bank of America et d'autres acteurs, ce qui met en péril la survie financière de l'ONG. Tout naturellement certains insistent pour que Bitcoin soit mis à profit.

Le 11 décembre, un article est publié sur PC World pour mettre en avant la possibilité d'un usage de Bitcoin par WikiLeaks. Cet article est rapidement évoqué sur le forum et la réaction de Satoshi est sans appel. Il écrit :

« Il aurait été bon d'attirer cette attention dans un tout autre contexte. WikiLeaks a donné un coup de pied dans le nid de frelons, et l'essaim se dirige maintenant vers nous[^50]. »

C'est son avant-dernier message public. Le lendemain, il poste son dernier message sur le forum pour annoncer la version 0.3.19 du logiciel, puis se volatilise. Il transmet les rênes du projet à ses deux bras droits historiques : Martti Malmi et Gavin Andresen.

Martti Malmi hérite du site web et du forum. Néanmoins, à l'instar de Satoshi, il se détourne progressivement de Bitcoin et délègue la gestion de ces plateformes à d'autres personnes, à qui il cèdera le contrôle entièrement en 2015[^51]. Il vendra ses 55 000 bitcoins pour s'acheter un appartement près de Helsinki.

De son côté, Gavin Andresen hérite de la clé d'alerte, du dépôt SourceForge et de la liste de diffusion. Dès le 19 décembre, il annonce « commencer à gérer le projet Bitcoin de manière plus active[^52] » et crée le dépôt GitHub de Bitcoin, où le projet sera dorénavant développé. Il ignore alors qu'il est devenu le développeur en chef du projet et que le créateur de Bitcoin va disparaître.

Satoshi se volatilise définitivement durant le printemps 2011. Le 23 avril, il adresse un dernier courriel à Mike Hearn, l'ingénieur de Google qui l'avait approché deux ans auparavant et qui était resté en contact avec lui, dans lequel il écrit :

« Je suis passé à autre chose. [Bitcoin] est entre de bonnes mains avec Gavin et les autres[^53]. » Il fait également ses adieux à Gavin et Martti. En particulier, il demande à Gavin d'éviter de parler de lui comme d'un « personnage sombre et mystérieux » à la presse[^54]. Le 27 avril, Gavin annonce qu'il a été invité par la CIA à faire une présentation sur Bitcoin. Cette visite se passe le 14 juin. De manière intéressante, c'est également le jour où WikiLeaks se met finalement à accepter les dons en bitcoins[^55]. Ces deux évènements viennent confirmer ce que Satoshi redoutait.

Satoshi Nakamoto laisse derrière lui une fortune colossale : 1 122 693 bitcoins selon une estimation de 2020[^56]. Cela représente plus de 5 % de la quantité totale de bitcoins. Ces fonds ne bougeront jamais.

Quelques messages émaneront de ses différents comptes[^57], mais on supposera qu'ils ont été piratés.

L'identité de Satoshi Nakamoto restera inconnue, celui-ci ayant réussi à conserver son anonymat grâce à l'usage de Tor et de services respectueux de la vie privée. Dans les années qui suivront, ce « personnage sombre et mystérieux » deviendra un mythe à part entière, suscitant les spéculations les plus diverses. Tout le monde se demandera « Qui est Satoshi Nakamoto ? » à l'instar des gens s'interrogeant sur l'identité de John Galt dans le roman *La Grève* d'Ayn Rand. On cherchera à savoir qui il est, quelques pistes seront privilégiées[^58], mais jamais son identité civile ne sera formellement identifiée.

En 2013, dans l'un de ses derniers messages sur le forum, Hal Finney partagera une citation énigmatique du film *Man of Steel* tout juste sorti, résumant bien la dimension mystérieuse entourant le créateur de Bitcoin :

« Comment retrouver quelqu'un qui a toujours brouillé les pistes ? [...] Pour certains, c'était un ange gardien. Pour d'autres, [une énigme,] un fantôme, toujours un peu à l'écart. [...] Que représente le S ?[^59] »

En mars 2014, on croira l'avoir trouvé en la personne de Dorian Prentice Satoshi Nakamoto suite à la publication d'un article de Newsweek[^60]. Cet ingénieur des télécommunications, citoyen américain naturalisé d'origine japonaise, vivant avec sa mère à Temple City dans la banlieue de Los Angeles, se fera harceler par la presse mais niera en bloc. On découvrira cependant que la famille de Hal Finney a habité dans la même municipalité, « à quelques pâtés de maisons de la maison familiale des Nakamoto », durant l'adolescence de Hal, ce qui attirera quelques soupçons sur ce dernier[^61].

Hal Finney décèdera en août 2014 des suites de la maladie de Charcot. En tant que futuriste averti, il se fera cryogéniser par la fondation Alcor.

### La communauté prend le relai

Alors que Satoshi se met progressivement en retrait, la popularité de Bitcoin augmente prodigieusement. En particulier, le prix du bitcoin évolue de manière favorable : alors qu'il n'était que de 20 centimes en décembre 2010, il atteint la parité avec le dollar le 9 février 2011 et s'y maintient pendant quelque temps. Cette hausse du prix attise l'enthousiasme de la communauté, et notamment celui de Hal Finney qui déclare avoir « vraiment de la chance d'avoir investi au début d'un nouveau phénomène qui risque d'être explosif[^62] ».

Cette période coïncide avec l'apparition de Silk Road, une place de marché du dark web s'appuyant sur Tor et Bitcoin qui permet à ses utilisateurs d'échanger librement des produits et des services légaux et illégaux. Celle-ci est lancée à la fin du mois de janvier par un jeune Texan du nom de Ross Ulbricht, qui en fait mention sur le forum de Bitcoin en feignant d'avoir découvert le site par hasard[^63].

Ross Ulbricht adhère profondément aux principes du libertarianisme, une philosophie libérale originaire des États-Unis prônant le respect impératif de la liberté individuelle, des droits de propriété et du marché. Silk Road est pour lui une incarnation de cet idéal. De ce fait, la gamme des produits et services qui peuvent être listés sur le site est restreinte et nécessite qu'aucun mal n'ait été fait à autrui : on y retrouve ainsi de la drogue, des médicaments, des pièces de métaux précieux, mais en aucun cas des cartes bancaires volées, de la pédopornographie ou des services de tueur à gages. Dans l'ensemble, le site sert principalement à la vente de drogue illicite (dont surtout de petites quantités de cannabis), chose pour laquelle il deviendra célèbre.

La promotion de Bitcoin s'intensifie également. Le 22 mars, la première vidéo expliquant Bitcoin de manière qualitative est publiée[^64]. Cette vidéo, intitulée sobrement « *What is Bitcoin?* », est produite par Stefan Thomas grâce à un financement participatif de la communauté. Elle aura un succès retentissant au fil des années en totalisant plusieurs millions de vues sur YouTube. Les vidéos de ce type se multiplieront.

Bitcoin est notamment vanté dans les cercles libertariens, où son caractère libre, anonyme et hors de portée de l'État est mis en avant. À la fin de l'année 2010, l'émission de webradio FreeTalkLive commence à évoquer le cas de Bitcoin et de son utilisation illégale. Cela attire l'attention de l'entrepreneur et activiste Roger Ver, déjà millionnaire grâce à sa société de revente de composants informatiques, Memory Dealers. Il apprend l'existence de la cryptomonnaie en décembre 2010 et est instantanément conquis : il se met à lire tout ce qu'il peut sur le sujet, achète du bitcoin, et fait en sorte de l'accepter avec son entreprise quelques mois plus tard. Il deviendra rapidement l'un des promoteurs les plus zélés de Bitcoin, ce qui lui vaudra le surnom de *Bitcoin Jesus* pendant un temps.

L'existence de Silk Road est révélée au grand public le 1 juin 2011 avec un article d'Adrien Chen sur Gawker[^65], ce qui a pour effet d'attirer l'attention sur Bitcoin encore un peu plus, notamment en incitant les consommateurs à se procurer du bitcoin pour acheter des produits sur la plateforme.

Au cours du printemps 2011, on assiste par conséquent à une forte poussée du prix, due à l'augmentation de la demande. Après avoir stagné pendant quelques mois, celui-ci passe ainsi de 1 $ le 15 avril à plus de 32 $ le 8 juin.

Mt. Gox, la principale plateforme de change de l'époque, se retrouve sous pression. Celle-ci a alors été reprise depuis quelques mois par Mark Karpelès, un développeur français de 26 ans vivant au Japon, qui est quelque peu négligent et n'a pas su résoudre les problèmes d'implémentation de son prédécesseur. C'est ainsi qu'un incident malencontreux survient le dimanche 19 juin : un groupe de pirates accède au compte administrateur de Jed McCaleb et tente d'en extraire un maximum d'argent.

La limite de retrait journalière étant fixée à 1 000 $, les pirates cherchent à faire baisser le prix afin de retirer le plus de bitcoins possibles. Ils vendent les bitcoins de Jed McCaleb au marché ce qui provoque un krach éclair sur le cours : le prix, qui stationne ce jour-là autour des 17 $, chute à 0,01 $ en quelques minutes. C'est la panique dans la communauté, et beaucoup d'utilisateurs de Mt. Gox vendent sous le coup de l'émotion afin de conserver ce qui leur reste. La situation est rétablie dans la journée mais 2 000 bitcoins manquent à l'appel. Le 23 juin, Mark Karpelès prouve la solvabilité de l'entreprise en déplaçant 424 242 bitcoins d'une adresse à une autre[^66].

Cet incident entraîne la fin de la folie spéculative sur le bitcoin et le prix se met à descendre doucement. C'est à ce moment-là qu'on assiste à la fermeture de MyBitcoin : début août, le service fait faillite suite à la disparition de 78 740 bitcoins, ce qui représente 51 % des fonds figurant sur les comptes des clients. Des éléments laissent à penser que son fondateur anonyme, Tom Williams, est à l'origine du vol. Dans les jours qui suivent cet évènement, le prix baisse en flèche jusqu'à 6 $, et finira par tomber à 2 $ en novembre.

Mais cela ne décourage pas pour autant les membres de la communauté. Du 19 au 21 août 2011 a lieu la première conférence sur Bitcoin à New York, qui est organisée par Bruce Wagner, l'animateur du *Bitcoin Show*, une émission d'entretiens filmés avec les acteurs de l'écosystème[^67]. La conférence revêt un caractère amateur (typique de la communauté d'alors) et seules quatre présentations ont lieu : celle de Bruce Wagner ainsi que les interventions de Gavin Andresen, Jeff Garzik et Stefan Thomas. Cela permet néanmoins aux membres les plus actifs, tels que Roger Ver, Jesse Powell, Jed McCaleb, Mark Karpelès ou Charlie Lee, de se réunir en personne pour la première fois.

Le développement logiciel s'organise aussi. Jusqu'ici, il était centralisé dans les mains de Satoshi, le « dictateur bienveillant » du projet. Mais après le départ du créateur de Bitcoin, il s'ouvre à la participation de la communauté, sous la supervision de Gavin Andresen. On voit ainsi des contributeurs talentueux commencer à s'impliquer dans l'évolution de Bitcoin comme Nils Schneider, Matt Corallo, Pieter Wuille, Jeff Garzik, Wladimir van der Laan, Luke-Jr ou encore Gregory Maxwell. Des méthodes de coordination sont rapidement mises en place comme la liste de diffusion bitcoin-development permettant de discuter formellement des changements à apporter[^68], et le système des propositions d'amélioration de Bitcoin (*Bitcoin Improvement Proposals* ou BIP), qui décrivent publiquement ces changements[^69].

L'utilisation de Bitcoin devient plus facile. On assiste à l'apparition de portefeuilles légers permettant d'utiliser Bitcoin sans avoir à télécharger et vérifier l'intégralité de la chaîne. Ces derniers utilisent la vérification de paiement simplifiée décrite par Satoshi Nakamoto dans la section 8 du livre blanc. Celle-ci est mise en œuvre par Mike Hearn au sein de sa bibliothèque logicielle BitCoinJ programmée en Java, qui permet entre autres une meilleure compatibilité avec les applications sur les téléphones multifonctions fonctionnant sous Android. Le premier portefeuille pour mobile, le *Bitcoin Wallet for Android*, est lancé par Andreas Schildbach en mars 2011. Celui-ci montre que l'usage direct de Bitcoin dans la vie de tous les jours est possible. Du côté ordinateur, Thomas Voegtlin crée Electrum en novembre 2011, présenté comme un portefeuille qui permet à l'utilisateur de récupérer ses fonds par le biais d'une phrase mnémotechnique. Cette pratique sera plus tard standardisée et adoptée largement dans l'écosystème.

Ce développement décentralisé est également source de tensions. Sans son fondateur, le projet ne dispose plus d'un meneur incontestable : certes Gavin Andresen possède le contrôle du dépôt, mais n'a pas l'autorité technique suffisante pour imposer toutes ses vues aux autres développeurs. Les décisions sont prises relativement collectivement, ce qui pose la question de la gouvernance de Bitcoin : qui décide d'apporter un changement au protocole ?

À la fin de l'année 2011 et au début de l'année 2012, le premier débat technique en l'absence de Satoshi a lieu. Le groupe de développeurs est alors encore très restreint mais cela suffit pour créer un conflit à propos de l'amélioration de la programmabilité des transactions, qui permettrait notamment de créer des comptes multisignatures. On s'en souviendra comme la « bataille pour P2SH[^70] ».

De par sa nature informatique, Bitcoin constitue un système de monnaie programmable qui permet à l'utilisateur d'imposer des conditions au blocage et au déblocage des fonds. Il dispose pour cela d'un mécanisme de scripts reposant sur des instructions logiques appelées codes opérations. Cependant, ces scripts sont compliqués à gérer. Il s'agit donc de trouver un moyen simple pour l'utilisateur d'envoyer des fonds vers un script défini préalablement par le récipiendaire. C'est l'idée derrière la proposition faite par Nicolas van Saberhagen d'ajouter un nouveau code opération appelé OP_EVAL. Cette proposition souffre néanmoins d'un problème de récursivité, ce qui provoque rapidement l'apparition de deux propositions concurrentes : *Pay to Script Hash* (P2SH) proposé par Gavin Andresen et OP_CHECKHASHVERIFY (CHV) proposé par Luke-Jr.

Une tension émerge entre les deux propositions, ce qui crée le débat. Amir Taaki, qui ne soutient ni l'une ni l'autre, appelle à la discussion et déclare le 29 janvier 2012 :

« Ma crainte c'est qu'un jour Bitcoin soit corrompu. Développeurs : considérez cet examen supplémentaire comme une opportunité de construire une culture d'ouverture[^71]. »

Finalement, c'est P2SH qui est choisi pour être intégré à Bitcoin sur l'ordre de Gavin Andresen. Cette intégration sera réalisée, non sans difficulté, le 1 avril 2012.

Dans un même temps, la popularisation de Bitcoin se poursuit. Le 28 février, un russo-canadien du nom de Vitalik Buterin, âgé de seulement 18 ans, cofonde le *Bitcoin Magazine* avec Mihai Alisie, un développeur roumain. Ce média, d'abord uniquement disponible en version web, est distribué en édition papier à partir de mai. Le jeune Vitalik y écrit de nombreux articles documentant l'actualité de l'époque. Par la suite, de nombreux sites d'information spécialisés verront le jour comme CoinDesk ou CoinTelegraph.

Le 24 avril 2012, un jeu de hasard en ligne nommé SatoshiDICE est lancé par l'entrepreneur américain Erik Voorhees[^72]. Le site repose sur un fonctionnement très simple : le joueur envoie des bitcoins à une adresse spécifique et il a une probabilité prédéfinie de recevoir une récompense qui correspond à un multiple du montant envoyé (il a par exemple une chance sur deux de recevoir un peu moins de deux fois sa mise). Le procédé est instantané et aisément vérifiable, ce qui attire de nombreux parieurs.

En tant que libertarien convaincu vivant dans le New Hampshire, Erik Voorhees voit en SatoshiDICE une manière d'échapper à la réglementation. Le 20 août, il réalise même une IPO pour son entreprise sur la plateforme roumaine MPEx. Il revendra la plateforme le 17 juillet 2013 pour 126 315 bitcoins, soit 12,4 millions de dollars au moment de l'acquisition.

Le succès de SatoshiDICE provoque une augmentation significative du nombre de transactions sur la chaîne, qui triple en quelques mois. Cette activité provenant du site est remarquée et dérange certains développeurs qui la qualifient de « spam[^73] ». À la moitié de l'année 2012, Bitcoin est ainsi complètement lancé et prêt à être découvert par un public plus large.

### L'amorçage organique de Bitcoin

Les premières années de Bitcoin ont été déterminantes pour son succès. Il a en effet pu grandir dans la discrétion et connaître une croissance organique et prudente, à l'abri de l'opportunisme et de la propagande de notre monde.

Bitcoin a été proposé en 2008 par Satoshi Nakamoto, qui l'a mis en œuvre en janvier 2009. Les débuts ont été difficiles, à tel point qu'il a fallu attendre neuf mois avant que le bitcoin n'acquière un prix ! Satoshi s'est dévoué pleinement à son œuvre sans jamais profiter personnellement de sa fortune accumulée. En disparaissant en 2011, il a finalement laissé la communauté s'approprier le projet.

Bitcoin a été façonné dans un creuset mêlant cypherpunks, anarchistes, libertariens et autres amoureux de la liberté. Il s'est construit en opposition au système étatico-bancaire traditionnel, où règnent la censure et les renflouements publics. C'est pourquoi le message derrière Bitcoin est si radical et que tant de gens se sont pris de passion pour lui.

Entre 2010 et 2012, les premiers cas d'utilisation de Bitcoin ont émergé. Financement de projets politiquement sensibles, jeu d'argent en ligne, achat de drogues à distance, envois de fonds à l'étranger : il s'agissait d'usages à la limite de légalité, voire complètement illégaux, qui démontraient toute l'efficacité du bitcoin en tant que monnaie incensurable et relativement anonyme. Cependant, cette tendance a été rapidement tempérée comme on a pu le constater durant les années qui ont suivi.
