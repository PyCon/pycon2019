from collections import OrderedDict
from copy import deepcopy
import csv
import os
import shutil
import sys
from django.contrib.sites.models import Site
from django.utils.text import slugify

from rtfng import Styles, Renderer, Elements
from rtfng.document.paragraph import Paragraph

from symposion.proposals.models import ProposalKind
from symposion.schedule.models import Presentation, Schedule
from pycon.models import SpecialEvent
from pycon.sponsorship.models import Sponsor, SponsorLevel

from django.core.urlresolvers import reverse


def export(pardir='program_export/'):
    # Remove the base directory, if it already exists.
    try:
        shutil.rmtree(pardir)
    except OSError:
        pass

    SpeakerBiosExporter(pardir).export()
    SponsorsExporter(pardir).export()
    PresentationsExporter(pardir).export()
    ScheduleExporter(pardir).export()
    SpecialEventsExporter(pardir).export()


def full_url(url):
    site = Site.objects.get_current()
    return 'https://' + site.domain + url


def get_paragraph_list(text):
    """Returns a list of paragraphs from a given text blob."""
    return [p.strip() for p in text.splitlines() if p.strip()]


def display(name):
    return name.replace('_', ' ').title()


def unicode_to_utf8(v):
    if isinstance(v, unicode):
        return v.encode('utf-8')
    else:
        return v


class UnicodeCSVDictWriter(csv.DictWriter):

    def writerow(self, item):
        """Data is encoded as UTF-8 before writing."""
        row = dict(
            (k, unicode_to_utf8(v))
            for k, v in item.items()
        )
        csv.DictWriter.writerow(self, row)


class BaseExporter(object):
    fields = None
    basedir = None
    description_fields = None

    def __init__(self, pardir=''):
        self.pardir = pardir
        self.csvdir = os.path.join(self.pardir, self.basedir, 'csv/')
        self.rtfdir = os.path.join(self.pardir, self.basedir, 'rtf/')
        for path in (self.csvdir, self.rtfdir):
            if not os.path.exists(path):
                os.makedirs(path)

    def get_attribute(self, obj, attr_name, split='__'):
        """Recursive retrieval of properties, attributes, and callables.

        Also allows the class to specify how to retrieve attributes.
        """
        def _inner(obj, attr_name):
            attr = getattr(obj, attr_name)
            return attr() if callable(attr) else attr
        if hasattr(self, 'prepare_' + attr_name):
            return getattr(self, 'prepare_' + attr_name)(obj)
        return reduce(_inner, attr_name.split(split), obj)

    def get_csv_path(self, filename):
        return os.path.join(self.csvdir, filename + '.csv')

    def get_rtf_path(self, filename):
        return os.path.join(self.rtfdir, filename + '.rtf')

    def write(self, filename, objects, fields=None):
        """Write data to both a csv file and an rtf file."""
        fields = deepcopy(fields or self.fields)
        for i in range(len(fields)):
            field = fields[i]
            if not (isinstance(field, tuple) or isinstance(field, list)):
                fields[i] = (field, field)
        with open(self.get_csv_path(filename), 'w') as csvfile:
            fieldnames = [fld[0] for fld in fields]
            csvwriter = UnicodeCSVDictWriter(csvfile, fieldnames)
            rtfdoc = RTFDoc("Program Export", self.get_rtf_path(filename),
                            self.description_fields)
            csvwriter.writerow(dict([(fieldname, display(fieldname))
                                     for fieldname in fieldnames]))
            for obj in objects:
                data = OrderedDict([(name, unicode(self.get_attribute(obj, getter)))
                                    for name, getter in fields])
                csvwriter.writerow(data)
                rtfdoc.add_pycon_section(data)
        rtfdoc.write()


class SpeakerBiosExporter(BaseExporter):
    fields = ['name', 'biography', 'url', 'photo_url']
    basedir = 'speakers/bios/'
    description_fields = ['biography']

    def prepare_url(self, speaker):
        return full_url(reverse('speaker_profile', args=(speaker.pk,)))

    def prepare_photo_url(self, speaker):
        try:
            return full_url(speaker.photo.url)
        except ValueError:
            return ''

    def prepare_kinds(self, speaker):
        kinds = []
        kinds.extend(list(speaker.presentations
                          .values_list('proposal_base__kind__name', flat=True)))
        kinds.extend(list(speaker.copresentations
                          .values_list('proposal_base__kind__name', flat=True)))
        return ', '.join(kinds)

    def export(self):
        queryset = Presentation.objects.exclude(cancelled=True)
        sort_key = lambda s: s.name.lower()
        all_speakers = []
        kinds = ProposalKind.objects.all()
        for kind in kinds:
            speakers = []
            for presentation in queryset.filter(proposal_base__kind=kind):
                speakers.extend(presentation.speakers())
                all_speakers.extend(presentation.speakers())
            speakers = sorted(list(set(speakers)), key=sort_key)
            filename = slugify(kind.name) + '_bios'
            self.write(filename, speakers)

        all_speakers = sorted(list(set(all_speakers)), key=sort_key)
        self.write('all', all_speakers, self.fields + ['kinds'])


class SponsorsExporter(BaseExporter):
    fields = ['name', 'external_url', 'web_description']
    basedir = 'sponsors/'
    description_fields = ['web_description']

    def prepare_web_description(self, sponsor):
        return sponsor.web_description

    def export(self):
        queryset = Sponsor.objects.exclude(active=False)
        levels = SponsorLevel.objects.all()
        for level in levels:
            sponsors = queryset.filter(level=level).order_by('name')
            filename = slugify(level.name) + '_sponsors'
            self.write(filename, sponsors)


class PresentationsExporter(BaseExporter):
    fields = [('name', 'title'), 'speakers',
              'description', 'abstract', 'url']
    basedir = 'presentations/'
    description_fields = ['description']

    def prepare_speakers(self, presentation):
        return ', '.join([s.name for s in presentation.speakers()])

    def prepare_url(self, presentation):
        return full_url(reverse('schedule_presentation_detail', args=(presentation.pk,)))

    def prepare_room(self, presentation):
        if presentation.slot:
            return ', '.join([r.name for r in presentation.slot.rooms])
        return ''

    def prepare_time(self, presentation):
        return '{0} from {1} to {2}'.format(
            presentation.slot.day.date.strftime('%b %d'),
            presentation.slot.start.strftime('%H:%M'),
            presentation.slot.end.strftime('%H:%M'),
        )

    def export(self):
        queryset = Presentation.objects.exclude(cancelled=True)
        kinds = ProposalKind.objects.all()
        for kind in kinds:
            presentations = queryset.filter(proposal_base__kind=kind)
            presentations = presentations.order_by('slot__day', 'slot__start', 'title')
            filename = slugify(kind.name)
            if kind.slug in ['talk', 'tutorial', 'poster', 'edusummit']:
                self.write(filename, presentations,
                           self.fields + ['room', 'time'])
            else:
                self.write(filename, presentations)


class SpecialEventsExporter(BaseExporter):
    fields = ['name', 'location', 'day', 'time', 'description', 'url']
    basedir = 'special_events/'
    description_fields = ['description']

    def prepare_url(self, event):
        return full_url(event.get_absolute_url())

    def prepare_day(self, event):
        return event.start.strftime('%b %d')

    def prepare_time(self, event):
        return 'from {} to {}'.format(
            event.start.strftime('%H:%M'),
            event.end.strftime('%H:%M')
        )

    def export(self):
        queryset = SpecialEvent.objects.filter(published=True).order_by('start', 'name')
        filename = 'special_events_schedule'
        self.write(filename, queryset)


class ScheduleExporter(BaseExporter):
    fields = [('name', 'title'), 'speakers', 'room', 'day', 'start', 'end',
              'url', 'abstract']
    basedir = 'schedule/'
    description_fields = []

    def prepare_abstract(self, slot):
        if slot.content and slot.content.abstract:
            return slot.content.abstract
        return ''

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

    def prepare_url(self, slot):
        if slot.content:
            return full_url(reverse('schedule_presentation_detail', args=(slot.content.pk,)))
        return ''

    def export(self):
        for schedule in Schedule.objects.all():
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
            filename = slugify(schedule.section.name) + '_schedule'
            self.write(filename, slots)


class RTFDoc(object):
    """
    High level interface over the rtfng to simplify the generation
    of the RTF documents that we export for laying out the printed
    program.
    """

    def __init__(self, title, filename=None, description_fields=None):
        self.title = title
        self.filename = filename
        self.description_fields = description_fields or []

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

        # add the document title
        self.new_section().append(self.new_title(self.title))

    def new_section(self):
        section = Elements.Section()
        self.doc.Sections.append(section)
        return section

    def new_para(self, section, style=None):
        p = Paragraph(style or self.ss.ParagraphStyles.Normal)
        section.append(p)
        return p

    def new_title(self, text, level=1):
        style = getattr(self.ss.ParagraphStyles, "Heading%d" % level)
        p = Paragraph(style)
        p.append(text)
        return p

    def write(self):
        if not self.filename or self.filename == '-':
            report = sys.stdout
        else:
            report = open(self.filename, "w")
        renderer = Renderer.Renderer()
        renderer.Write(self.doc, report)

    def add_pycon_section(self, data):
        # Shortcut for adding PyCon data sections.
        section = self.new_section()
        section.append(self.new_title(data.pop('name'), 2))
        metass = self.ss.ParagraphStyles.Metadata

        for key, value in data.items():
            if key not in self.description_fields and value:
                item = display(key) + ": " + value
                self.new_para(section, metass).append(item)

        for field in self.description_fields:
            if data[field]:
                if len(self.description_fields) > 1:
                    data[field] = field + ': ' + data[field]
                for para in get_paragraph_list(data[field]):
                    self.new_para(section, self.ss.ParagraphStyles.Normal).append(para)
