import requests, time
from threading import Thread


class ThreadResult:
    package = []

    @classmethod 
    def add (self, item) :
        self.package.append(item)

    @classmethod 
    def print (self) :
        print(self.package)


def getGoogleAppStore(url):
    prefixUrl = "https://play.google.com/store/apps/details?id="
    res = requests.get(prefixUrl + url)
    # print(" url : {0} , length : {1}".format(url, len(res.text)) )
    if len(res.text) == 1673 :
        ThreadResult.add(url)
    else: 
        return True

def filteredAliveThread(t):
    return isinstance( t, Thread) and t.is_alive()


crwlingJob = ["com.rastafarian","com.rasanenl.linearquestm","com.rAs.android.sukufesrootcloaker","com.rareartifact.teeoffmobileB6260341","com.rareartifact.canadausagolfcoursesA81E8685","com.rapcio4master.free.mp3.music.download","com.raon.karaokeG2","com.raniolgamesinc.pollybravo","com.ranger2music.mp3.free.music.copyleft.downloade","com.rane.solidwallpaper","com.RandomPlays.Skyfall","com.ramzan_apps.bayanat","com.ramesp.amissed","com.ramentech.voizlator.app","com.ramentech.cardcamera.paid","com.ramadan.emiratesnationalday","com.ralf89.seccalculs","com.raiyi.yellowchina","com.rain.bomb","com.railwork.SR","com.rafitomusico.mp3.music.download","com.raf82o1w91wz","com.radiostreams.radiomaneleonline","com.radios.en.linea.de.argentina","com.radiolive.britsh","com.radiolist.inforlist","com.radiolight.senegal","com.radiolight.nigeria","com.radiokong.arabesk","com.radio.redbull.rock","com.radian.qodari.studioapp","com.racing_games.cg.motorbike","com.racingvictoria","com.racingmotogames.snowmoto","com.racingmedia.pjh.test23","com.rachma12.ranat_maghribia","com.racergame.cityracing3e.egame","com.RabbitRush.org","com.RabbitApps.SpaceMonkey","com.r8i.g9c","com.r7dev.saucerecipes","com.qwerty.interactive.toiletQuest","com.quwenba.note2cnmanual","com.quoord.jamiiforums.activity","com.qunhe.rendershow","com.quizmine.organicchemistry","com.quizmine.androidpsychology","com.quipack.a.b4fab72c976ca6e00010042b8","com.quickmobile.asnt2014","com.quickcode.hd.fantasyhdphotoframes.vq2","com.qufan.texas","com.queerkorea.queerkorea","com.queenlight.tubeemp3MusiiicPlaay","com.queeng.android.play","com.quantum.mobile.parachute.landing","com.quan.mzw","com.qualson.testapp","com.qualson.ballantines21","com.qualcomm.qaps.mobile.approvals","com.qrcodereader.qrscanning.pro","com.qpon","com.qooga.parkpacker","com.qodu.avtsppevwm.adventuresuperpacevilwordsman","com.qk35k8fybywm","com.qiyi.video.hburl","com.qisheng.dayima","com.qin.qin.Hearts.activity","com.qihoo.appstoree","com.qigame.lock.global.zhangxiaohespace","com.qigame.lock.global.snowbear","com.qigame.lock.global.porcupinefish","com.qigame.lock.global.player","com.qigame.lock.global.home","com.qigame.lock.global.hauntedhouse2","com.qigame.lock.global.alienlanding","com.qiaohu","com.qf365.JujinShip00290","com.qdw.dollstest","com.qdazzle.shushan.xiaoye","com.qdazzle.mlxz.zf49you","com.qdazzle.lx.zf49you","com.qczrfb1relgn","com.QbotIndustries.treecapitator","com.qbao.avalon.tldk","com.qajoo.cerikancilbuaya","com.pysmart.smartphoneoptimizer","com.PyramidaGames.PianoTab3","com.py1ai11m5118","com.pvzcard.pvzsuper","com.puzzles.petsjigsawpuzzlegame","com.puzzlehouse.flappy48","com.putule.mimap","com.pushapp.palmeralabs.pullups","com.purepushpro.extremecarmountainrace4x4hillclimb","com.purefairy.frozenmagic","com.Pumpkins.Photo.Frames","com.pumpkinday.smartblocks","com.pululustudio.myweatherreporter","com.pukapukadeli.gamecollection","com.pugfuglygames.lw.retrosnake","com.pudding.gg.photo","com.pubu.fishingoffline","com.publishervn.app.tuvi","com.pubappbasic.guideforwhatsapp","com.pub","com.ptungawuphoodrgrand.newtvremote","com.pTricKg.PhoneVolumeToggle","com.PTGameStudio.DiamondSwapBlast","com.PtGameStudio.CrazyCakeMatch3","com.psychictxt.psychictxtapplication","com.psychedelicwallpaperslaland","com.PSVStudio.DanceHero","com.PSVStudio.ClaraAndHippo","com.PSVGamestudio.HippoPony","com.pss.fallingleaf","com.pshegger.bfkeyboard","com.ps.sonicbiochem","com.prstudio.radio.argentina","com.protoplus.chainreaction","com.PROTEAMS.backgroundswallpapershdfree2015","com.prossimaisola.rentit","com.promptdesignstudio.littleeinsteinscoloringgame","com.promethylhosting.bitcoinbzdashboard","com.promega.colonycounter","com.projectsexception.catchy","com.projectpol.gpc.saltblueuser","com.ProjectKids.NurseryPoems","com.ProjectCS.sktnotes","com.PROJECT19.PJS","com.project.ubigate","com.project.TimeWidget","com.project.calendar","com.project.bukchon","com.prograssing.android.sshutdowndemo","com.programmingthomas.vegas","com.programmerworld.DoYouKnow","com.program.toy.adailycall","com.progeny.russiantv","com.profitininternet.book.AOVBJDUFIIIWVVOFS","com.profenapps.AdventureSonicMickey","com.productsshukustegnoaxuf.electricscreenjoke","com.productsdadsetsymath.remotecontrolmedia","com.ProCorrector.XPN.procorrector","com.proboxbaixarmp3.mp3.downloader.music.mp3music.","com.pro.mp3videoconverter","com.PrizeClawEggsGame","com.privacylock.space","com.prisma.cartoon","com.PrincessFitnessAndSpa","com.prettywallpapers.prettypictures.girls.girly.fu","com.pretty.asian.girl.wallpaper.rev1188544","com.preschool.kidsmathgames","com.prereleaft.matgos","com.premiumlw.sky","com.predictivetechnologies.soccerpredictor","com.PreAlgebra_U","com.PrankSolarBatteryCharger","com.practicapps.contactsorter","com.pr.mod45","com.pr.mod41","com.pppoe.Springflower","com.ppn.mp3.merger.cut","com.powernapp.dankmlgsoundboard","com.poweramp.theme.power_skins_monsters","com.POTKPOT.WeedLWP","com.pose.howtophotoposing","com.portal.memorygamekids","com.pornoyt.howtodraw3d","com.popularwallpaper.dandelion","com.popularradiostations.freereggaemusic","com.popularradiostations.freecelticmusic","com.popularapp.periodcalendar.jp","com.Popular2016Ringtones.Best.GalaxyRingtones","com.popueditor.camara.candcamselfie","com.popsong.shark.evoguide","com.PopovGrisha.SparrowsWallpapers","com.popartoys.safaribook","com.pool8ball.snooker20162","com.Pool.Ball.Shooter","com.pook.smj.ch0931.zimon","com.pooja.HalloweenMakeoverSalon","com.pooandplay.icehockeyteamcanada","com.ponkuki.supernote.theme.yololoyorolIreland","com.ponkuki.supernote.theme.woogood","com.ponkuki.supernote.theme.theygaveyougavemex","com.ponkuki.supernote.theme.beodeulspringnyang","com.ponkuki.golocker.theme.sosotamwenyeol","com.ponkuki.golocker.theme.pipinoteminttraining","com.ponkuki.golocker.theme.mongreldog","com.ponkuki.golocker.theme.lovelypatternpink","com.ponkuki.golocker.theme.fallingloveshygirl","com.Polypod.MozartZero","com.PolymorphicDissociation.PointlessButtons","com.polymerprice","com.polycatdev.laser","com.polins.models4","com.polilabs.poliballs","com.pokkt.NinjaKid","com.pokerplay.headsup","com.pokercity.yzddz.iqiyi","com.pokercity.bydrqp.sogou","com.pokercity.bydrqp.downjoy","com.poker.spade.sexy.bikini.girl.wallpapers","com.pokemon.pokemontcg","com.poetstudios.pop.bubbledeluxe","com.podo.musicdownloadfree.music.mp3.downloader.pr","com.pococraft.Fishroom","com.pocketmon.youku","com.pocketks.crazy.busdriver.google.hillclimb","com.pocketdietitian","com.pnrtec.mpos","com.pnr","com.pnixgames.gogo","com.pnisoft.pohange","com.pnf.smartschool","com.pnf.smartboard","com.pnf.sketch.t2.bt","com.pmpsheet.pro","com.pmp.ppmoney","com.plus.FuturePlus","com.plum.crazyhairyface","com.plp.mobile","com.plhero.translate","com.plhero.mp4hdplay","com.pledge51.nigerianconstitution","com.playsync.hang_drum_integral","com.playsimple.mydevicesensors","com.playrix.township.chukong.baidu","com.playplace.commando.war.adventure.shooting","com.playpiegames.wiz.android.kr.latalemobile","com.playmous.dashmasters","com.playinggarden.whatsappimagesFriends","com.playingapps.mipelidiaria","com.Player.MP3.GROMPA.BARKOM","com.playcreek.MiniDashmod","com.playcrab.ares.dzm.zongle","com.play3rdeye.museumedu","com.play.ludo.board.game.free","com.play.game2.UnicornDashk","com.platoevolved.townz","com.platinumapps.facedroid","com.platformstory.dirtysoonsil","com.plantynet.silvercareparent","com.PLANI.theme.ptslocktheme1s.TurtleSilhouette","com.PLANI.launcher.theme.ColorFood","com.PLANI.launcher.theme.ColoredPaper","com.pksoft.logicmaster2free","com.pkerdfcvge.beautyvideo","com.pkapps.generalknowledge","com.pk51.snk.kof97","com.pjfx.picsmix","com.pizzarest.dishtw","com.pizus.comics","com.pixystudio.gpscoordinates","com.pixjuegos.pixfrogger.free","com.pixel_nest.stockagent.paid","com.pixelsoft.thuglifephotocreator","com.pixamore.barney_stinson_epic_quotes","com.pix.arts.FlappyFrogFree","com.piti.webviewtester","com.pitchervbatter.stats.pvb","com.pirlove.swapmyface","com.pirate.run.game","com.pinoyapps.presdebate2016","com.pinkwallpaper.lovepink.lovepictures.flowers.ro","com.pinkpointer.jigsaw.flowers","com.pinkoink.harmattan.theme","com.Pingram.YouCamMakeupEditor","com.pingping.mirror.effect","com.pilatesfit.thecenterpilates","com.pikasapps.valentinesdaywallpapershd","com.pikasapps.moon.wallpapers","com.pikasapps.lockscreen.wallpapers","com.pikasapps.buenasnochesfotos","com.pikasapps.aurora.wallpapers","com.picturegird2016","com.picturedemo65","com.picturedemo56","com.pictosoft.teamguardian.onestore.kr","com.picpie","com.pickle.CitySniper","com.pichchdev.AndroidMemoryCleanerFree","com.piaci.listener.app","com.physio.pocket","com.phuttystudios.barbilliardsscorer","com.phummeak.khmerroengthai","com.photo_frames.calendar_photo_frames_hd","com.photores.sk00700s","com.PhotoGlassesEditor","com.photoframe.suit.photoframes","com.photoframe.bikinisuit.frames","com.photoeditorwriteonphoto.explosives","com.photoeditorapps.vampirecamera","com.photoeditorapps.masqueradephotocamera","com.photoeditorapps.hdr","com.photoeditor.bellydancephotomontage","com.photoart.slution.cutebabyframe","com.Photoappszone.collage","com.photo.master.pro.edit.effects","com.phonegap_test","com.phonegap.gaeulho","com.phonegap.Feasts","com.phonedeco.themecontents.theme_10004459","com.phonedeco.themecontents.theme_10004280","com.phonator.service.tangentbord","com.phls2rtjgq0u","com.philips.brushbusters","com.philio.me.home.automation2015","com.phdisciples.churchapp_001","com.pha99.modmortalgunz","com.pha99.furnituremods","com.pgramtu.ablackjac896","com.pg.catdroneflightsimulator","com.pg.boatcaptainusacruisetour","com.pfizer.us.pfizerevents","com.petkit.android","com.petfit.petfitrenewal","com.peternpartners.newsq","com.pet.coloring.butterflies","com.perion.mymaps","com.perfect.fgsm","com.perfect.editory","com.perfactpick.perfact","com.pereng.alternativemusicstreaming","com.percent.djjelly","com.perapps.guess_the_reptile","com.pepipepipepi.Euro2016FootballCarSoccerLeague","com.pepgames.championshipfootballgames","com.penji.tutor","com.penguin.semuworker","com.penguin.ice.adventure","com.penguin.aggregatemanage","com.pengpeng.coollauncher","com.penfour.taptaplock","com.pelletiere.android.busangerswebapp","com.pelipets.sdscanner","com.pdt.androidmagicball","com.pds.sharkrevenge2016","com.pds.juicyflow","com.pds.hungrycrocodile3d","com.pds.fallingfootball","com.pds.carsstunts3d","com.pdragon.aa","com.pdfuj55018.flashplayertutorial","com.pdcc.bubbleshooter","com.pcremote","com.pbj.piccombocheat","com.pawga.radio","com.paulart.pipboy2000.clockwidget","com.patosoft.cookinglola","com.patience.revisited","com.Pati.PW","com.pathuku","com.pathgather","com.pathfinder.pushbutton","com.pastatarifleri","com.pasta","com.passsong.hanja","com.passportphoto.android.passportphotoplus","com.passenger.bmo","com.passbook.mobilebank","com.pasha.roostersounds","com.pasawahanappmaker.malay.malaysia.korea.korean.","com.pasawahanappmaker.english.mongolia.mongolian.d","com.Pasa.Winter.Season.Keyboard.Themes","com.partykidsmobile.android_newbornbabyjungle3","com.partykidsmobile.android_babyforestadventure2","com.partner.jonfca","com.parrot.urlripper","com.parolam3e.music.downloader.mp3","com.paraso.player.music.downloader.mp3.descargar.m","com.paras1.applock","com.paranoic.Android_Lollipop_5_Live_WP","com.paramtech.love.quotes.pics","com.paralikykmp3.mp3.music.downloader.free","com.paragolagames.heroesofdota2","com.paprika3.jangki","com.paperlit.android.sardegnaquotidiano","com.paperlit.android.rdd","com.papamusico3s.mp3.music.downloader.free","com.paopaolong.bubbleshoot","com.pantech.app.polarisoffice","com.pantech.app.mediapannel","com.pantech.app.appsplay.iconpack.h365.miniPrinces","com.pansi.msg.lang.ja","com.panicartstudios.herosiegepockethh","com.pangyoo.radioactive3D","com.pangyoo.radioactive","com.pangelements.android.pangelements","com.Pangam_Gaurav.SecretVideoRecorderPro","com.pandako.register","com.panda.portuguese.biblechildren","com.panda.cameraphotoeditor41005","com.pancheprojects.stars","com.panasonic.avc.pj.catalog","com.panapp.guesssupasitthai","com.panagola.app.iphotovr","com.pampamdev.heightestimator","com.palmorder.smartbusiness","com.palelublendut.threepvnasnaoi","com.palace4musa.copyleft.music.downloader.mp3","com.pak.pakistanprayertime","com.pagiodevelop.yugiohrulingnew","com.padmobslne.wallpaperlin","com.padfoot.silencio","com.pad.damagecalc","com.pacworld","com.pacman.flying","com.packofthemes.gosmsprothemeromantic","com.pacadventure","com.pablo.ThreeDAthletics","com.pa.gridframe2","com.p2xemtivi","com.ozy.easy.ram.booster","com.oymind.manikur","com.oxo.pregnant.mommy","com.ovnis.reales","com.overchunk.videoguideforcoc","com.outthinking.livecamerabokesh","com.outthinking.eaglehunting","com.outspokenkid.cattimer","com.outgoing.mainok","com.ourpalm.buliangren.youku","com.ourgame.mahjong.lenovo","com.ourdeal.android","com.oup.elt.grammar","com.ouah4.ouah_04_01_n","com.ouah14.ouah_14_23_n","com.ouah10.ouah_10_39_n","com.ouah07.ouah_07_01","com.otwei351.mzdhu800","com.otakuclub.animewallpaper","com.otakuapps.grendizeradventures","com.ospisoft.bugscolor","com.osmino.citywifi.moscow","com.osmar2013.messageflirt","com.oscarbaro.aircraftdogfightraid","com.osaka_trip_wor","com.os.shooter.invaders2.chicken","com.os.classicmegaman.x","com.orpine.benmingfo","com.orionsmason.foodpuzzlefree","com.originalgames.spintopspong","com.originalapp.malaysiaweather","com.orgrose.cyberedufunction","com.orgoniteapps.buildbattlehalloween","com.orcraphics.bop3baldeagleanalogclock","com.orchidfreegames.jellysweetsjourney","com.orbotix.drivesample","com.orangutandevelopment.orangutanwearflashlight","com.orangeairstudio.guesslittleprincessponydolls","com.orange.myorange.omd","com.orange.cacaoring_20111026_02","com.orange.cacaoring_0118_08","com.oppo.compass","com.OppanaGames.LuxuryPoliceCar","com.OPOAE.magazine.JapaneseHairstyle2016","com.operap.operabundle","com.openbusiness.Business_calculations_rus","com.open.engine.astor","com.opar.mobile.aplayer","com.opanaklab.mynumber","com.op.test2","com.op.test1","com.oozware.icookie.cookienet","com.ooxy.gen.zlap.io","com.oomglive.citynight","com.oo5rv3nof54m","com.onsf.jungleadventures.jungleworldformario","com.onse.on.value","com.onlygames.arrowslash","com.onlinegamefree.MaroonIvory","com.onlineeducare.skeletalsystem","com.onhappydays.shopsmatch.free","com.onez.malb","com.onexsoftech.indianrailenquiry","com.onexsoftech.diwaliphotoframes","com.onetwocm.o2o.pos.giftcard","com.onetwocm.memories","com.onetwocm.echoss.pair","com.onetshadow.pokemonshadow.onetlinkup","com.onetoone.util.suneung.hanmun","com.onetapsolutions.morneau.activity","com.oneprofarm.forfarmers","com.onemore.d2","com.onemightyroar.beansprout.free","com.Onemannotasoldier","com.OneGameOneMonth.Ballooble","com.onedial.androiddialer","com.onecoincloud","com.oneapps.videosoftware","com.oneapps.forexfactory","com.oncall.flashalert","com.oms.islamics","com.omotenshi_travelguide.omotenashi","com.omning.edupresso_study_q","com.omexteam.best_ram_cleaner_speed_booster.clean_","com.omal9ol0aa92","com.om.springflowerphotoframe","com.om.hoardingphotoframe","com.om.flowerphotoframe","com.om.airplanephotoframe","com.olympusthemes.dumbways","com.ollie.livewallpaper.SwirlyFree","com.olive.stamp","com.olia.widget.LitaWrestler","com.olegnovsoft.tilewaterfall","com.olegkorrr.oleg.kamnigoroskop","com.oldschool.Balda","com.olcoop.app","com.olav.logolicious","com.olauapps.sutichhoathuytien","com.olauapps.sutichhoaphonglan","com.olauapps.sutichhoamaivang","com.olangames.android.keyknight","com.ol.wv","com.oktomo.wheel","com.oktagongames.olympicquiz","com.okgyh331.qzbqw696","com.ok8s.app","com.oilandgasnewsonline.app","com.ohoo.grieta.googleplus","com.ogow.activity","com.OGF.OGF","com.og.dog.race.hunter.hound.sim","com.ofice.steve.pike.epiphany","com.offonkorea.smcallcustomer","com.odvgroup.simulatordrivingcartwo","com.odvgroup.cardsgoodmorning","com.odnklassac.weathermenow3","com.octys.mygpsae","com.OCTO_Games.Revolution_Does_NOTDIE","com.Ocgfm.CraftingGuideforMinecraftFree","com.oceanicsoftware.altitudeprofile_turkish_free","com.oceaniaapps.superhero","com.obium.soar","com.oaisy.puzzle.monuments","com.o2o64aaoo2m2","com.o0mmn0cy00y","com.nzluv.bathroomdecor","com.nzincorp.papabravo","com.nzin.app.mindtest.market.naver.free","com.nzafar.butterflylock","com.nxp.mifaresdksample","com.nxlab3.flashlightuhd","com.nvidia.TigerWarpES","com.nvidia.Tiger3DES","com.nvidia.ThreadedRenderingVk","com.nvidia.ThreadedRendering","com.nvidia.TextWheelES","com.nvidia.SoftShadows","com.nvidia.SkinningAppVk","com.nvidia.ShuffleIntrinsicsVk","com.nvidia.ShapedTextES","com.nvidia.OptimizationApp","com.nvidia.NvCommandList","com.nvidia.NormalBlendedDecal","com.nvidia.MultiDrawIndirect","com.nvidia.ModelTestVk","com.nvidia.Mercury","com.nvidia.HelloVulkan","com.nvidia.HDR","com.nvidia.FXAA","com.nvidia.DeferredShadingMSAA","com.nvidia.CursiveES","com.nvidia.CubemapRendering","com.nvidia.ConservativeRaster","com.nvidia.ComputeWaterSimulation","com.nvidia.ComputeParticles","com.nvidia.CascadedShadowMapping","com.nvidia.BlendedAA","com.nvidia.Basic","com.nve5vjskvrw6","com.nutri.musica.newmp3.finddownloadmusic.gratuit","com.nutreek.jooleem","com.Nussygame.DeckDeFantasy","com.nurse_shift.kangoshi","com.NurseryRhymesChildrenSongs","com.nurinmaru.farm0099a","com.nurinmaru.farm0080","com.nurimedia.psyedu1contest","com.nurijigap.app","com.nummolt.fractions.reading","com.nummolt.fractions.add","com.nullwire.qotd.chalkboard","com.nuker.MonsterPang","com.ntu.one_stop","com.ntt.choibai.tienlen","com.ntsshop.yifeitong","com.ntss.topfreehdmp3player","com.ntss.axvideoplayer","com.ntouch.game.matgo21","com.ntouch.game.matgo08","com.ntonapps.gpxwaypointreaderfree","com.nsolutions.IPInstaller","com.ns.SchoolHorrorEscape","com.nqnnnpn.noknlnnnp","com.npc.sankuo.uc","com.npc.sankuo.DK","com.npc.owner.myunist_info","com.np.musicvideos","com.NP.Funny.Photo.Editor","com.no_burden_featured.mfilms","com.noveo.vkmessenger","com.novelromantis.indroid","com.novapps.pur.pic","com.nougatstudios.trooperskin","com.nothingkill.wispvod","com.nos_network.lovestage_batt","com.nos_network.battery_widget_mens","com.norinori15","com.nordstrom.rack.app","com.nordicsemi.utsolCar","com.nop.carwash","com.noormediaapps.womenpartywearphotosuit","com.noormediaapps.womenfashionsuit","com.noormediaapps.womenfashionpantssuit","com.noonorng.cartoonringtones","com.noodlecake.sagesolitaire.humble","com.noodlecake.framed.humble","com.noobmakers.themoneygameslot","com.noobmakers.luckyladycharmdeluxeslot","com.noobmakers.bookoffairyslot","com.nonoapps.ganharmassamuscularrapido","com.nojoke.talkingdog","com.nojoke.realtalkinggirl","com.nojoke.pianokeyboard","com.nojoke.dancingtalkinggirl","com.noen.maihue.camerapro","com.nobujang.mygirlfriend5","com.nobexinc.wls_85754189.rc","com.nobexinc.wls_48300360.rc","com.nobexinc.wls_44371318.rc","com.nobexinc.wls_18214939.rc","com.nobexinc.wls_04800042.rc","com.nnk21.pocketdecorationmod21","com.nnjzkchisfee","com.nmsoft.fundingclubpointcheck","com.nml4awvoag7g","com.nmbible.com","com.nlucas.notificationtoaster.theme.jellybean","com.nlucas.notificationtoaster.theme.ics2","com.nlucas.notificationtoaster.theme.honeycomb","com.nle.grse","com.NKSOL.RunHero","com.nkmfree.nkmplayer","com.nkadim.fighters","com.nk.waw","com.nirwanadev.worldguide.atarms","com.ninjagame.ninjafighting.swordking3d","com.ninjacyborg.profiles","com.nineyi.shop.s001139","com.ninetyeightideas.nycmaps","com.ninegame.gamecenter","com.nine.Ringtone","com.nil.bella","com.NikolaySmorgun.SomethingforSilentHill2","com.NikolaySmorgun.ShortcutsforiBooksAuthor","com.nightowl.client","com.nighto.mp3listen.musicamuziekmp3.freemusique","com.nightmotobikeracing.challengepeedridebikeer","com.nicolatesser.androidquiztemplate","com.nicolasc.apps.LimiteurDeVitesse","com.nicksoft.tanks","com.NickGames.SmartBallMazeMaze","com.nicegame.goodstart.avea.zesfe.vjozrk","com.niceapp.qrtika.daolnwodnnm","com.nice2meet.funnyanimalcoloringbook","com.nice2meet.biblecoloringbook","com.nhnent.toastpromotion.demoinventory","com.nhnent.sk10396","com.nhnent.fashiongo","com.nhn.android.band.b","com.nhelearning.m.nhelearning","com.nhatvm.toefl_practice_test","com.nhacxuan.nhactet","com.nh.beacon","com.ngu.myanmartv","com.ngpinc.MyShoppleG2936","com.ngontinh.tieuthuyet.tungtheuoc","com.ngn.ledflashlight","com.ngaz.ihqp.dihg","com.nfcqr196","com.nfacedownloader.download","com.Nexus.RandalsMonday","com.nextwebart.senego","com.nextreaming.app.handel","com.NextGameStudio.PianoKid","com.nexon.dn2","com.nexamuse.applockerpro","com.NewYearGreetingCarDsBestHD2017","com.NewTypeMath.ProtoMath","com.newomg.videodownloadero","com.newitventure.mttvnepal","com.newfriendstango.tangochat","com.newflash.ledlights","com.newera.commando.police.strike","com.Newdolph.asd","com.newcamchat.chat","com.NewbornCareGames","com.newbestsublang.ort","com.newbee.lyzt.byledou.qh","com.nevil.blockheroes","com.neuralplay.android.klondike","com.network.dictionary","com.netsummitapps.puddingrecipes","com.netsummitapps.muffin","com.netstick.kardashianlikes","com.netschool","com.netmaru.cbh","com.netgames834.CharmingPrincessMakeup","com.netease.nieapp","com.netease.l10.ewan.snail","com.netease.l10.ewan","com.netease.gfxm3.downjoy","com.netease.gamecenter","com.netease.dhxy.ewan","com.netease.bjx.youku","com.nete.extreme.farming.tractor.kids","com.neronov.aleksei.antarcticaanimals","com.nerdislandstudios.dccircuitbuilder","com.NeonGameStudios.MemoryPursuit","com.neon.mp2audioconverter","com.neom.teccom","com.Neokeuljeteo.Card_draw_camera","com.neogb.feedbinreader","com.neocrew.game","com.NeoCortex.FireShowForKids","com.neo.zipline","com.nemo.yelimfuneral","com.nemo.sottabaegim","com.nemo.snsdhostel","com.nemo.okqr","com.nemo.jumunjin","com.nemo.jukbangmall","com.nemo.honam4760","com.nemo.gvpension","com.nemo.bigpop","com.nemo.autosky","com.nemo.anyauto24","com.nemo.alokong","com.nekyo.mikke","com.neggig.livewallpapervideo","com.neezen.tamjung2","com.neezen.daebung","com.neezen.atom.sample","com.neezen.appevent.ae384","com.neezen.appevent.ae200","com.nee.magicsymbol.activity","com.neckdetailbrave.buttfly","com.ne.beautywatchfree","com.ndstudio.cutecubes.sinas.weibo","com.ndstech.lip","com.ndstech.aeng","com.ndhse.dokuuhj","com.ndb.Ncallapp","com.ndb.mobile","com.ncza.pikapika.chuuadventure","com.ncpaclassic","com.ncin.gcmprj","com.Ncbtour.travelmaker.main","com.nbss","com.nbiosis.noksan","com.NBF_DIGIPASS","com.naxosaudiobooks.adventcalendar2014","com.navinfo.wedrive.music","com.navi.promp3downloadfree","com.Naverquke.dgame","com.naver.www.doubledh","com.naver.helloworld","com.naturewallpaperhdea","com.natewren.pastyiconsfree","com.narvii.amino.x46","com.narvii.amino.x22","com.naruto.sharingan.eyes","com.naretdeveloper.marukowallpapers","com.narendramodiapp","com.narae.wallpaper_aj1","com.narae.smsring_058","com.narae.smsring_012","com.nanyibang.nomi","com.nanum.nuri","com.namo.ssem","com.names.god.AOVMNDOXSZTERHVV","com.namcobandaigames.conan2","com.nam.bestcan","com.nakas.VirtualReality360VideoPlayer","com.nak4u3rgizi0","com.naiznoiz.smokecontrolkey","com.naixious.beautifulhomeexteriordesign","com.NailArtStepByStepDesign.Billionest","com.NailartideasDIY.damonicsapp","com.nahian.hairfallremedy","com.nagasebros.TW2000_New","com.nafham.education","com.nadstech.animaisparaascriancas","com.n2game.marin.biggame.one","com.n225zero.NumplaZero","com.n225zero.FreeCellZero","com.n1qo9ja9s3d6","com.n.sproutv","com.m_hi.ipcs","com.mzadqatar.mzadqatar","com.myzap.cb","com.myxgwxxzchosdbkauyxn","com.mythwar.th.game","com.mytaste.mytaste","com.mystudy","com.mystudio.Pandarush","com.mysounds.funnybabyringtones","com.mysitecreations.ukghb1897","com.myshots.screenshot","com.mysampleapp.androiddoorlockserver","com.mypocketgames.uazoffroad","com.myndos.kamemyndos","com.myname.light.weight.clock.lwp","com.mymusicvideotube","com.mykaishi.xinkaishi","com.myibbx0ye1g7","com.myhome.game","com.mygame.home","com.mydragon.notes","com.mycustomerconnect.saviorplumbing","com.mycomputersathi.allnepalivideos","com.mycompany.soundmeter","com.mycompany.myteam.mypush","com.mycompany.myteam.myapp2","com.mycompany.myteam.myapp","com.mycompany.myteam.indexeddb","com.mycompany.Jqb7g2Ja","com.myappway.MagicCatsGame","com.myapps.vocalizacion","com.myapps.lovehd2","com.myandroid.LedSign","com.my1980s.gamcu","com.my.photoviewer","com.my.home","com.my.game.MarbleForest","com.my.D16001590","com.mxt.simplememo","com.mxdroid.cuentocaperucita","com.mwvnsnut.ekvoxecg","com.mwpnews.book_au","com.mwkorea.openwallet","com.mw243315botaniculalivewallpapers","com.mw243315botaniculalivewallpaper","com.mw243315botaniculahdlivewallpapers","com.mventus.selfcare.view","com.MutuDeveloper.OneRepublicSongsLyrics","com.music_videos_for_kids","com.musicparadisetubidy178v1.downloader.music.mp3.","com.musicparadiseprov179v1.downloader.mp3.music.fr","com.musicparadisepromp3192v2.baixar.gratis.musicas","com.musicmp3downloaderformusic.musicloader","com.musicmaniac.mp3.freemusicdownload","com.musicdownloadmp3best31.baixar.musicas.mp3.musi","com.musicbox.newbell.cp38","com.music6downloader.musicloader","com.music.player.equalizer","com.music.paradise.download.may1403","com.music.musicas.muziek.musique.descargar.downloa","com.music.mp3.gratis.free.download.downloader.baix","com.music.guhusik","com.Mushfiq.ProgressiveHouseMusicRadio","com.Mushfiq.BoleroMusicRadio","com.musami.madrid11.live.wallpapers","com.muratos.memorymatch","com.muratos.learn_hindi_vocabulary","com.muratos.learn_clothes_french","com.murarka.liftoffvr","com.muomgames.bussimulatorrealtraffic","com.MundusLtd.Space3DLW","com.multiplanos.main.sudokuquiz","com.multi.hello_kwak","com.muhammadsakil.tafseer_usmani","com.muhall.drumvrt","com.mugua.kxvideo","com.MuFaEntertainment.SnowyCarDrift","com.MuFaEntertainment.MinibusDrift","com.mubiquo.shell","com.mtsgames.policechasedown","com.mtsgames.killshotsniper","com.mtsgames.frontiertargetsniper","com.mtsgames.citydrivingtest","com.mtp.newvideosongs","com.mtdata.vancouvertaxi","com.mt.photostudio.frame.photo.funnyfacechanger","com.msvdevelopment.shpargalkiru.free","com.msvdevelopment.itportug.free","com.msvdevelopment.enromanian.free","com.msvdevelopment.enfr","com.msvdevelopment.enes","com.msolution2.msolution_02_40","com.msiano.marksiano.e_field","com.msgcopy.kaoke.a335","com.msfutures.Morgan","com.msd.android.free","com.msbahi_os.LovePics","com.ms.gameddz","com.ms.dark.hero","com.mrx.jingangjingqwjs","com.mrx.dfxsxlx","com.mrtstudios.mobile.c","com.mrgenius.djelectromixpad","com.mrgames.linebirdgooglefree","com.mrgames.jjanguhexalgt","com.mr384.CustomizeVibrator","com.mqs.bundesligaatquiz2014","com.mqgames.sjq","com.mptv.twansa","com.mpsong2","com.mpsls.td2","com.mpp.bff.sticker","com.mplus07.mplus_07_28_n","com.mplus.mplus_12_37_n","com.mplus.mplus_12_31_n","com.mplus.mplus_10_35_n","com.mplay.caudo.cuoinam.caudohailao","com.mpi.hci.kalq","com.mpcapp","com.mpac.app","com.mp3playermm.ouayer","com.mp3musicdownloaderv162v3.free.music.mp3.downlo","com.mp3musicdownload88.downloader.mp3.music.free.m","com.mp3musicdownload88.download.music.free.mp3.bai","com.mp3boo.lastfm.museopen.freemusicarchive","com.mp3.music.musicas.musique.descargar.download.b","com.mp3.music.baixar.tubidy.skull.ares","com.mp3.free.player","com.mp3.download.music.tubemate.gtunes.descargar.p","com.mp3.bul.indir.cok.hizli.fmd","com.mp.pharmacytrucksimulator","com.mp.guardianstuntexpress","com.mp.endlesswastelandracer","com.mp.CarTransporters3Dse","com.mozhang.XbirdsSec.bd","com.movuphaghdevs.batterycalibration","com.movinapp.dict.enhk.free","com.movilibo.MB00940039","com.movile.vivomeushow","com.movie_sub_sanjungjm","com.movie_sub_PA10024","com.movie_sub_PA10004","com.movie.video.downloader.mp4play","com.movie.easy.easymovie","com.movaudio.ecomposer","com.mouseschedule.mouseschedule","com.motomuto.fitlightcontroller","com.motionpixtheater.accuplacer_cards","com.mosoyo.dandelion","com.morningshine.phototocartoon","com.morningshine.cameffect","com.morningenter.kr3go","com.morningenter.amicell","com.moregas.simplyNotes","com.moreapps.tintin","com.more.unique","com.mooteam.wordsearch2015","com.moonton.magicrush.qihoo","com.MoonGlaive.WallDecorationIdeas","com.MoonGlaive.KitchenCabinetsDesignIdeas","com.moongci.balloon","com.moon.sortmaster","com.moon.ext.mbm2","com.moodclip.main","com.moocho.moocho","com.monterobros.foosball","com.monte.color.match.game.live.wallpaper","com.monstergames.snail.bob","com.monsmile.projecth.android.test","com.monsmile.mpx.devaosext","com.monsap.ninjacameraanimeeditor","com.monsap.ninjaanimecamera","com.monotype.android.font.zzzz9","com.monotype.android.font.zzzz8","com.monotype.android.font.zzzz7","com.monotype.android.font.zzzz6","com.monotype.android.font.zzzz5","com.monotype.android.font.zzzz4","com.monotype.android.font.zzzz3","com.monotype.android.font.zzzz2","com.monotype.android.font.zzzz17","com.monotype.android.font.zzzz16","com.monotype.android.font.zzzz15","com.monotype.android.font.zzzz13","com.monotype.android.font.zzzz12","com.monotype.android.font.zzzz11","com.monotype.android.font.zzzz10","com.monotype.android.font.zzzz1","com.monotype.android.font.zznn","com.monotype.android.font.zzioR","com.monotype.android.font.zxxcvv","com.monotype.android.font.zna","com.monotype.android.font.zli","com.monotype.android.font.ziniqhftnfhrRmffu","com.monotype.android.font.yyyyyu","com.monotype.android.font.Yujeongfont","com.monotype.android.font.YP_jjjo","com.monotype.android.font.yoongubook","com.monotype.android.font.YoonBomnalL"]

maxThreadCount = 1000
threadlist = []
closeAppList = []
start = time.time()
while( len(crwlingJob) >= 1 ):
    if len(threadlist) >= maxThreadCount :
        # 전체 내역중에 종료된 내역이 있는지 체크.
        # threadlist = list(filter( lambda t: isinstance( t, Thread) and t.is_alive() , threadlist))
        threadlist = list(filter( filteredAliveThread , threadlist))
    else :
        # threadlist = list(filter( filteredAliveThread , threadlist))
        url = crwlingJob.pop()
        workThread = Thread(target=getGoogleAppStore , args=(url,))
        threadlist.append(workThread)
        workThread.start()
        # workThread.join()
        # time.sleep(0.3)

print(" sub time : {0}".format(time.time() - start ))

while ( len(threadlist) >=  1  ):
    threadlist = list(filter( filteredAliveThread , threadlist))

# ThreadResult.print()

print(" time : {0}".format(time.time() - start ))