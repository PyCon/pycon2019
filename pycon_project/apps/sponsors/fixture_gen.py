from fixture_generator import fixture_generator

from sponsors.models import SponsorLevel, Sponsor


@fixture_generator(SponsorLevel, Sponsor)
def pycon_2010_sponsors():
    level_names = [
        "Diamond",
        "Platinum",
        "Gold",
        "Silver",
        "Patron",
        "Vendor I",
        "Media",
    ]
    levels = {}
    for pos, name in enumerate(level_names):
        levels[name] = SponsorLevel.objects.create(order=pos, name=name)
    
    def create_sponsor(name, url, level):
        return Sponsor.objects.create(
            name=name,
            external_url=url,
            level=levels[level]
        )
    
    create_sponsor("Google", "http://code.google.com/opensource/", "Diamond")
    
    create_sponsor("CCP Games", "http://www.ccpgames.com/", "Platinum")
    
    create_sponsor("Walt Disney Animation Studios", "http://www.disneyanimation.com/", "Gold")
    create_sponsor("neg-ng", "http://www.net-ng.com/", "Gold")
    create_sponsor("socialserve.com", "http://www.socialserve.com/", "Gold")
    create_sponsor("ActiveState", "http://www.activestate.com/", "Gold")
    create_sponsor("White Oak", "http://www.woti.jobs/", "Gold")
    create_sponsor("Canonical", "http://www.canonical.com/", "Gold")
    create_sponsor("Microsoft", "http://ironpython.net/", "Gold")
    create_sponsor("Sauce Labs", "http://www.saucelabs.com/", "Gold")
    create_sponsor("Rackspace Cloud", "http://www.rackspacecloud.com/", "Gold")
    create_sponsor("ESRI", "http://www.esri.com/", "Gold")
    create_sponsor("Oracle", "http://wiki.oracle.com/page/Python", "Gold")
    
    create_sponsor("Enthought", "http://www.enthought.com/", "Silver")
    create_sponsor("Wingware", "http://www.wingware.com/", "Silver")
    create_sponsor("Imaginary Landscape", "http://www.chicagopython.com/", "Silver")
    create_sponsor("Emma", "http://www.myemma.com/", "Silver")
    create_sponsor("Visual Numerics", "http://www.vni.com/", "Silver")
    create_sponsor("Hiidef", "http://hiidef.com/", "Silver")
    create_sponsor("Breadpig", "http://www.breadpig.com/", "Silver")
    create_sponsor("Accense Technology", "http://www.accense.com/", "Silver")
    create_sponsor("Tummy", "http://www.tummy.com/", "Silver")
    
    create_sponsor("ZeOmega", "http://www.zeomega.com/", "Patron")
    
    create_sponsor("O'Reilly", "http://www.oreilly.com/", "Vendor I")
    
    create_sponsor("Linux Journal", "http://www.linuxjournal.com/", "Media")
    create_sponsor("Linux Pro Magazine", "http://www.linuxpromagazine.com/", "Media")
    create_sponsor("Ubuntu User", "http://ubuntu-user.com/", "Media")
    create_sponsor("Code Magazine", "http://www.code-magazine.com/", "Media")
    create_sponsor("Startup Riot", "http://startupriot.com/", "Media")
    create_sponsor("Bit", "http://thebitsource.com/", "Media")
