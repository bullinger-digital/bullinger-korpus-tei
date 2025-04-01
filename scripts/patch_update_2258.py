import re

path = "data/letters/2258.xml"
with open(path) as fi: s = fi.read()
new_letter = '\t<text xml:lang="la">\n\
        <body>\n\
            <div>\n\
                <p>\n\
                     <s n="1" xml:lang="la" type="manual">Salutem plurimam in Christo Iesu.</s>\n\
                </p>\n\
                <p>\n\
                     <s n="2" xml:lang="la" type="manual">In nostro itinere prima nocte <placeName ref="l285">Lentzburgae</placeName> pater <persName ref="p8440">Gervasius [Schuler]</persName> lectis tuis ad illum literis admirabilem pii animi benevolentiam in nos tanquam in charissimos effundere mihi videbatur.</s>\n\
                     <s n="3" xml:lang="la" type="manual">Nam vesperi e publico diversorio nos abducens in suis aedibus ad suavissimam quietem perduxit atque summo mane per duas horas nobiscum proficiscens tam exacte nos docuit viarum notas atque piorum virorum nomina, ut ex istorum consiliis et illarum signis nos semper deinceps admoniti de via facile recta pervenimus <placeName ref="l41">Bernam</placeName>.</s>\n\
                </p>\n\
                <p>\n\
                     <s n="4" xml:lang="la" type="manual">Ibi intelleximus <persName ref="p8417">Musculum</persName>, <persName ref="p8018">Hallerum</persName> et alios doctos valde benevolos fuisse atque propensos nobis iuvandis effectos per tuas ad <persName ref="p8018">Hallerum</persName> literas.</s>\n\
                     <s n="5" xml:lang="la" type="manual">Nam plures pariter in unis aedibus congregati ad bonam coenam nos invitarunt.</s>\n\
                     <s n="6" xml:lang="la" type="manual"><persName ref="p8018">Hallerus</persName> praeterea trium dierum liberali hospitio nos gratis acceptos ducebat quotidie ad quaecunque videnda vel audienda desideravimus.</s>\n\
                     <s n="7" xml:lang="la" type="manual"><placeName ref="l280">Losannae</placeName> quoque <persName ref="p8033">Baesacus</persName><note xml:id="fn1" type="footnote" n="1"><persName ref="p8033">ThÃ©odore de BÃ¨ze</persName></note> et <persName ref="p3429">Viretus</persName> tam verbis quam factis ostendebant per tuas ad illos literas nos et commendatos et gratos fuisse.</s>\n\
                     <s n="8" xml:lang="la" type="manual">Tandem vero septimo die aprilis venimus <placeName ref="l167">Genevam</placeName>, ubi absente <persName ref="p540">Calvino</persName>, ad quem dixi me tuas literas habere, statim recepit nos commensales vir pius et probus, qui nunc infra hos paucos dies <persName ref="p540">Calvinum</persName> reversurum expectat.</s>\n\
                     <s n="9" xml:lang="la" type="manual">Intellexi igitur et agnosco paternam tuam erga me providentiam mihi et consorti meo non solum in domo tua hospitium longe gratissimum gratis exhibuisse, verum etiam in aliis locis apud alios gratiam et benignitatem longe supra nostram expectationem nobis contulisse.</s>\n\
                     <s n="10" xml:lang="la" type="manual">Atque proinde, quod tibi secundum deum acceptum fero, iamdiu est, ex quo coepi cogitare me non tam exulem e patria mea peregrinari quam concivem sanctorum in domestica dei familia nunc versari.</s>\n\
                     <s n="11" xml:lang="la" type="manual">Nullam itaque nunc sentio meam miseriam, sed curam pene incurabilem pro eis, quos in patria mea suspicor gravissimis periculis iam esse immersos.</s>\n\
                </p>\n\
                <p>\n\
                     <s n="12" xml:lang="la" type="manual">Nam Anglus quidam <placeName ref="l41">Bernam</placeName> transiens scripsit ad conterraneos suos in <placeName ref="l167">Geneva</placeName>, quod principes <placeName ref="l41">Bernenses</placeName> accepissent per literas e aula regis <placeName ref="l2464">Galliae</placeName> ad eos missas <persName ref="p18554">reginam Angliae</persName> occisam esse a plebe exasperata per eius perfidam crudelitatem.</s>\n\
                     <s n="13" xml:lang="la" type="manual">Alius tamen, qui a <placeName ref="l296">Londo</placeName> decessit 13. die martii, hodie hic mihi retulit, quod in seditione per <persName ref="p7118">Voyetum</persName><note xml:id="fn2" type="footnote" n="2"><persName ref="p7118">Thomas Wyatt</persName></note> concitata nulli sacrifci fuere suspensi neque post captum <persName ref="p7118">Voyetum</persName> nulla multitudo morte fuit mulctata.</s>\n\
                     <s n="14" xml:lang="la" type="manual">Solos dixit <persName ref="p8068">ducem Suffolkiae</persName><note xml:id="fn3" type="footnote" n="3"><persName ref="p8068">Henry Grey</persName></note> et filiam eius d. <persName ref="p1336">Ioannam</persName><note xml:id="fn4" type="footnote" n="4"><persName ref="p1336">Jane Grey</persName></note> atque maritum illius <note xml:id="fn5" type="footnote" n="5">Guildford Dudley</note> decollatos fuisse et omnes constanter in professione verae religionis perseverasse.</s>\n\
                     <s n="15" xml:lang="la" type="manual">Atque praeterea asseverabat se pro certo audivisse <persName ref="p674">Cranmerum</persName> <placeName ref="l1255">Cantuariensem</placeName> episcopum, <persName ref="p21391">Ridleum</persName> <placeName ref="l296">Londinensem</placeName> episcopum, <persName ref="p7623">Latimerum</persName> concionatorem celeberrimum et <persName ref="p7911">Halesium</persName><note xml:id="fn6" type="footnote" n="6"><persName ref="p7911">John Hales</persName></note> legisperitum pium, omnes hos pariter traductos a <placeName ref="l296">Londino</placeName> ad <placeName ref="l376">Oxonium</placeName> fuisse, ut ibi a dominis doctoribus illius academiae condemnati haereseos igni comburerentur.</s>\n\
                     <s n="16" xml:lang="la" type="manual">Ex istis omnibus nihil aliud possum ego colligere, nisi aut vivente regina gravissimam ecclesiae persecutionem aut grassante irrequieta multitudine irrecuperabilem dissipationem regni in <placeName ref="l830">Anglia</placeName> esse.</s>\n\
                     <s n="17" xml:lang="la" type="manual"> Verum enimvero cordis mei durities, quae neque istarum calamitatum commiseratione neque meorum commissorum poenitudine unquam possit in lachrymas resolvi, saepe solet mihi animum turbare, ingenium obtundere et memoriam confundere.</s>\n\
                     <s n="18" xml:lang="la" type="manual">Quare te obsecro, mi pater, in visceribus Christi Iesu coelestem patrem mecum pro me invoces, ut ipse respiciens nostras miserias, Christi merita et suas miserationes mihi condonet meam negligentiam et nequitiam, auferat cordis duritiem et tribuat resipiscentiae atque sanctificationis spiritum.</s>\n\
                     <s n="19" xml:lang="la" type="manual">Dicito, quaeso, a me atque a consorte meo <persName>Hugone</persName><note xml:id="fn7" type="footnote" n="7">Gutbertus Hugonius</note> salutem et gratias plurimas uxori tuae et omni familiae vestrae.</s>\n\
                     <s n="20" xml:lang="la" type="manual" ana="salute">Atque te etiam rogo, ut meo nomine salutares venerandos senes <persName ref="p8127">Pellicanum</persName> et <persName ref="p8171">Bibliandrum</persName> et alios doctos piosque viros, <persName ref="p8011">Gvalterum</persName>, <persName ref="p1283">Gesnerum</persName>, <persName ref="p1884">Lodovicum [Lavater]</persName>, <persName ref="p8442">Zvinglerum</persName> [!]<note xml:id="fn8" type="footnote" n="8">Vermutlich ein Verschreiber fÃ¼r <persName ref="p8442">Josua Simmler</persName>.</note> et <persName ref="p7228">Zvinglium</persName><note xml:id="fn9" type="footnote" n="9"><persName ref="p7228">Huldrych Zwingli d.J.</persName></note>.</s>\n\
                </p>\n\
                <p>\n\
                     <s n="21" xml:lang="la" type="manual">Conservet te Christus diu ad utilitatem ecclesiae suae.</s>\n\
                     <s n="22" xml:lang="la" type="manual">Vale.</s>\n\
                     <s n="23" xml:lang="la" type="manual"><placeName ref="l167">Genevae</placeName> 11. die aprilis.</s>\n\
                     <s n="24" xml:lang="la" type="manual">Filius tuus<br/><persName ref="p1911">Thomas Leverus</persName>.</s>\n\
                </p>\n\
            </div>\n\
        </body>\n\
    </text>'
m_letter = re.match(r'.*?([ \t]*<text .*?</text>).*', s, flags=re.S)
if m_letter:
    with open(path, 'w') as fo: fo.write(re.sub(re.escape(m_letter.group(1)), new_letter, s, flags=re.S))
