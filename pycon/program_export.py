import csv
import os
import shutil
import sys

from rtfng import Styles, Renderer, Elements
from rtfng.document.paragraph import Paragraph

from symposion.proposals.models import ProposalKind
from symposion.schedule.models import Presentation, Schedule
from symposion.sponsorship.models import Sponsor, SponsorLevel

from django.core.urlresolvers import reverse


def out(msg):
    if not msg.endswith("\n"):
        msg += "\n"
    sys.stdout.write(msg)


def export(pardir='program_export/'):
    # Remove the base directory, if it already exists.
    try:
        shutil.rmtree(pardir)
    except OSError:
        out("Creating directory for export at `{0}`.".format(pardir))
    else:
        out("Removed existing files located in `{0}` directory.".format(pardir))

    SpeakerBiosExporter(pardir).export()
    SponsorsExporter(pardir).export()
    PresentationsExporter(pardir).export()
    ScheduleExporter(pardir).export()


class UnicodeCSVDictWriter(csv.DictWriter):

    def writerow(self, item):
        """Data is encoded as UTF-8 before writing."""
        for k, v in item.items():
            if isinstance(v, unicode):
                del item[k]
                item[k] = v.encode('utf-8')
        csv.DictWriter.writerow(self, item)


class BaseExporter(object):
    fieldnames = None
    basedir = None

    def __init__(self, pardir='', **kwargs):
        for kwarg, value in kwargs.items():
            setattr(self, kwarg, value)
        self.pardir = pardir

        self.csvdir = os.path.join(self.get_dir(), 'csv/')
        self.rstdir = os.path.join(self.get_dir(), 'rst/')
        for path in (self.csvdir,):
            if not os.path.exists(path):
                os.makedirs(path)

    def get_attribute(self, obj, attr_name, split='__'):
        """Recursive retrieval of properties, attributes, and callables."""
        def _inner(obj, attr_name):
            attr = getattr(obj, attr_name)
            return attr() if callable(attr) else attr
        if hasattr(self, 'prepare_' + attr_name):
            return getattr(self, 'prepare_' + attr_name)(obj)
        return reduce(_inner, attr_name.split(split), obj)

    def get_dir(self):
        return os.path.join(self.pardir, self.basedir)

    def get_csv_path(self, filename):
        return os.path.join(self.csvdir, filename + '.csv')

    def get_rst_path(self, filename):
        return os.path.join(self.rstdir, filename + '.rst')

    def export_csv(self, filename, objects, fieldnames=None):
        fieldnames = self.fieldnames if fieldnames is None else fieldnames
        with open(self.get_csv_path(filename), 'w') as csvfile:
            csvwriter = UnicodeCSVDictWriter(csvfile, fieldnames)
            for obj in objects:
                row = dict([(name, unicode(self.get_attribute(obj, name)))
                            for name in fieldnames])
                csvwriter.writerow(row)


class SpeakerBiosExporter(BaseExporter):
    fieldnames = ['name', 'biography', 'url_for_bio']
    basedir = 'speakers/bios/'

    def prepare_url_for_bio(self, speaker):
        return reverse('speaker_profile', args=(speaker.pk,))

    def prepare_kinds(self, speaker):
        kinds = []
        kinds.extend(list(speaker.presentations.values_list('proposal_base__kind__name', flat=True)))
        kinds.extend(list(speaker.copresentations.values_list('proposal_base__kind__name', flat=True)))
        return ', '.join(kinds)

    def export(self):
        out("Exporting speaker bios to `{0}`.".format(self.get_dir()))
        queryset = Presentation.objects.exclude(cancelled=True)
        sort_key = lambda s: s.name.lower()
        all_speakers = []
        kinds = [ProposalKind.objects.get(name=name)
                 for name in ['Talk', 'Poster', 'Tutorial', 'Lightning Talk']]
        for kind in kinds:
            speakers = []
            for presentation in queryset.filter(proposal_base__kind=kind):
                speakers.extend(presentation.speakers())
                all_speakers.extend(presentation.speakers())
            speakers = sorted(list(set(speakers)), key=sort_key)
            filename = kind.name.lower().replace(' ', '_') + '_bios'
            out("\tExporting {0} {1} speakers.".format(len(speakers), kind.name))
            self.export_csv(filename, speakers)

        all_speakers = sorted(list(set(all_speakers)), key=sort_key)
        self.export_csv('all', all_speakers, self.fieldnames + ['kinds'])


class SponsorsExporter(BaseExporter):
    fieldnames = ['name', 'external_url', 'print_description',
                  'web_description']
    basedir = 'sponsors/'

    def prepare_print_description(self, sponsor):
        if sponsor.print_description_benefit:
            return sponsor.sponsor_benefits.get(benefit__name='Print Description').text
        return ''

    def prepare_web_description(self, sponsor):
        if sponsor.company_description_benefit:
            return sponsor.sponsor_benefits.get(benefit__name='Company Description').text
        return ''

    def export(self):
        out("Exporting sponsors to `{0}`.".format(self.get_dir()))
        queryset = Sponsor.objects.exclude(active=False)
        levels = SponsorLevel.objects.all()
        for level in levels:
            sponsors = queryset.filter(level=level).order_by('name')
            filename = level.name.lower().replace(' ', '_') + '_sponsors'
            out("\tExporting {0} {1} level sponsors.".format(sponsors.count(), level.name))
            self.export_csv(filename, sponsors)


class PresentationsExporter(BaseExporter):
    fieldnames = ['title', 'speakers', 'proposal__get_audience_level_display',
                  'proposal__category__name', 'description', 'url']
    basedir = 'presentations/'

    def prepare_speakers(self, presentation):
        return ', '.join([s.name for s in presentation.speakers()])

    def prepare_url(self, presentation):
        return reverse('schedule_presentation_detail', args=(presentation.pk,))

    def prepare_room(self, presentation):
        return ', '.join([r.name for r in presentation.slot.rooms])

    def prepare_time(self, presentation):
        return '{0} from {1} to {2}'.format(
            presentation.slot.day.date.strftime('%b %d'),
            presentation.slot.start.strftime('%H:%M'),
            presentation.slot.end.strftime('%H:%M'),
        )

    def export(self):
        out("Exporting presentations to `{0}`.".format(self.get_dir()))
        queryset = Presentation.objects.exclude(cancelled=True)
        kinds = [ProposalKind.objects.get(name=name)
                 for name in ['Talk', 'Poster', 'Tutorial', 'Lightning Talk']]
        for kind in kinds:
            presentations = queryset.filter(proposal_base__kind=kind)
            presentations = presentations.order_by('slot__day', 'slot__start', 'title')
            filename = kind.name.lower().replace(' ', '_') + 's'
            out("\tExporting {0} {1} presentations.".format(presentations.count(), kind.name))
            if kind.name in ['Talk', 'Tutorial']:
                self.export_csv(filename, presentations,
                                self.fieldnames + ['room', 'time'])
            else:
                self.export_csv(filename, presentations)


class ScheduleExporter(BaseExporter):
    fieldnames = ['title', 'speakers', 'room', 'day', 'start', 'end',
                  'audience_level', 'category', 'url']
    basedir = 'schedule/'

    def prepare_title(self, slot):
        if slot.content:
            return slot.content.title
        return slot.kind.label

    def prepare_speakers(self, slot):
        if slot.content:
            return ', '.join([s.name for s in slot.content.speakers()])
        return ''

    def prepare_room(self, slot):
        return ', '.join([r.name for r in slot.rooms])

    def prepare_audience_level(self, slot):
        if slot.content:
            return slot.content.proposal.get_audience_level_display()
        return ''

    def prepare_category(self, slot):
        if slot.content:
            return slot.content.proposal.category.name
        return ''

    def prepare_url(self, slot):
        if slot.content:
            return reverse('schedule_presentation_detail', args=(slot.content.pk,))
        return ''

    def export(self):
        out("Exporting schedules to `{0}`.".format(self.get_dir()))
        schedules = [Schedule.objects.get(section__name=name)
                     for name in ['Talks', 'Tutorials']]

        for schedule in schedules:
            slots = []
            for slot_kind in schedule.slotkind_set.all():
                for slot in slot_kind.slot_set.all():
                    if slot.content and slot.content.cancelled:
                        continue
                    slots.append(slot)
            slots.sort(key=lambda s: s.rooms[0].name if s.rooms else '')
            slots.sort(key=lambda s: s.end)
            slots.sort(key=lambda s: s.start)
            slots.sort(key=lambda s: s.day.date)
            filename = schedule.section.name.lower().replace(' ', '_') + '_schedule'
            out("\tExporting {0} slots in {1} schedule.".format(len(slots), schedule.section.name))
            self.export_csv(filename, slots)


class RTFDoc(object):
    """
    High level interface over the rtfng to simplify the generation
    of the RTF documents that we export for laying out the printed
    program.
    """

    def __init__(self, title, filename=None):
        self.title = title
        self.filename = filename

        # setup document styles
        self.doc = Elements.Document()
        self.doc.SetTitle(self.title)
        self.ss = self.doc.StyleSheet
        NormalText = self.ss.ParagraphStyles.Normal
        self.metastyle = NormalText.Copy()
        self.metastyle.TextStyle.textProps.size = 16
        self.metastyle.TextStyle.textProps.italic = True
        self.ps = Styles.ParagraphStyle('Metadata', self.metastyle.TextStyle)
        self.ss.ParagraphStyles.append(self.ps)

        # Document title
        section = self.new_section()
        section.append(self.new_title(self.title))

    def new_section(self):
        section = Elements.Section()
        self.doc.Sections.append(section)
        return section

    def new_para(self, section, style=None):
        if not style:
            style = self.ss.ParagraphStyles.Normal
        p = Paragraph(style)
        section.append(p)
        return p

    def new_title(self, text, level=1):
        style = getattr(self.ss.ParagraphStyles, "Heading%d" % level)
        p = Paragraph(style)
        p.append(text)
        return p

    def add_talk(self, title, metadata, abstract,
                 admin_url=None, public_url=None):
        section = self.new_section()
        section.append(self.new_title(title, 2))

        metass = self.ss.ParagraphStyles.Metadata
        self.new_para(section, metass).append(metadata)

        if admin_url:
            self.new_para(section, metass).append(admin_url)

        if public_url:
            self.new_para(section, metass).append(public_url)

        if not isinstance(abstract, list):
            abstract = [abstract]

        for para in abstract:
            p = self.new_para(section, self.ss.ParagraphStyles.Normal)
            p.append(para)

    def add_sponsor(self, name, desc, admin_url=None):
        section = self.new_section()
        section.append(self.new_title(name, 2))
        metass = self.ss.ParagraphStyles.Metadata

        if admin_url:
            self.new_para(section, metass).append(admin_url)

        if not isinstance(desc, list):
            desc = []

        for para in desc:
            p = self.new_para(section, self.ss.ParagraphStyles.Normal)
            p.append(para)

    def add_bio(self, name, bio, admin_url=None, public_url=None):
        section = self.new_section()
        section.append(self.new_title(name, 2))
        metass = self.ss.ParagraphStyles.Metadata

        if admin_url:
            self.new_para(section, metass).append(admin_url)

        if public_url:
            p = self.new_para(section, metass).append(public_url)

        if not isinstance(bio, list):
            bio = []

        for para in bio:
            p = self.new_para(section, self.ss.ParagraphStyles.Normal)
            p.append(para)

    def write(self):
        if not self.filename or self.filename == '-':
            report = sys.stdout
        else:
            report = open(self.filename, "w")
        renderer = Renderer.Renderer()
        renderer.Write(self.doc, report)
