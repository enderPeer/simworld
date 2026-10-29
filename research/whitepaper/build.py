"""Render the reviewed white-paper manuscript without running the simulation.

Use the publication's recorded font family for matching pagination. On Linux,
Liberation Serif/Sans are accepted alternatives; inspect the resulting PDF.
"""
from pathlib import Path
from datetime import datetime, timezone
import json
import os
from reportlab.pdfgen import canvas
from reportlab.platypus import (SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle,
                               PageBreak, KeepTogether, Flowable)
from reportlab.lib import colors
from reportlab.lib.styles import ParagraphStyle
from reportlab.lib.enums import TA_LEFT, TA_CENTER, TA_JUSTIFY
from reportlab.lib.pagesizes import A4
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont

WORK = Path(__file__).resolve().parent
ROOT = WORK.parents[1] if WORK.name == 'whitepaper' and WORK.parent.name == 'research' else WORK.parent
OUT = ROOT / 'output' / 'whitepaper'
OUT.mkdir(parents=True, exist_ok=True)
import argparse
parser = argparse.ArgumentParser(description=__doc__)
parser.add_argument('--manuscript', type=Path, default=WORK/'manuscript.json')
parser.add_argument('--output', type=Path, default=OUT/'SimWorld_Research_White_Paper.pdf')
parser.add_argument('--font-dir', type=Path, help='Directory containing Times New Roman and Arial TTF files')
args = parser.parse_args()
font_dir = args.font_dir or Path('C:/Windows/Fonts')
font_files = [('Body','times.ttf'), ('BodyBold','timesbd.ttf'), ('BodyItalic','timesi.ttf'),
              ('Sans','arial.ttf'), ('SansBold','arialbd.ttf')]
if not (font_dir/'times.ttf').exists() and args.font_dir is None:
    font_dir = Path('/usr/share/fonts/truetype/liberation2')
    font_files = [('Body','LiberationSerif-Regular.ttf'), ('BodyBold','LiberationSerif-Bold.ttf'),
                  ('BodyItalic','LiberationSerif-Italic.ttf'), ('Sans','LiberationSans-Regular.ttf'),
                  ('SansBold','LiberationSans-Bold.ttf')]
for name, filename in font_files:
    pdfmetrics.registerFont(TTFont(name, str(font_dir / filename)))
pdfmetrics.registerFontFamily('Body',normal='Body',bold='BodyBold',italic='BodyItalic',boldItalic='BodyBold')
pdfmetrics.registerFontFamily('Sans',normal='Sans',bold='SansBold',italic='Sans',boldItalic='SansBold')
PAGE_W,PAGE_H=A4
WIDTH=PAGE_W-108
styles={
 'body':ParagraphStyle('body',fontName='Body',fontSize=11,leading=15,spaceAfter=8,alignment=TA_JUSTIFY),
 'small':ParagraphStyle('small',fontName='Body',fontSize=9.2,leading=12,spaceAfter=7),
 'h1':ParagraphStyle('h1',fontName='SansBold',fontSize=15,leading=19,spaceBefore=4,spaceAfter=14,keepWithNext=True),
 'h2':ParagraphStyle('h2',fontName='SansBold',fontSize=11.3,leading=15,spaceBefore=12,spaceAfter=6,keepWithNext=True),
 'title':ParagraphStyle('title',fontName='SansBold',fontSize=27,leading=33,spaceAfter=15),
 'subtitle':ParagraphStyle('subtitle',fontName='Body',fontSize=16,leading=21,spaceAfter=18),
 'meta':ParagraphStyle('meta',fontName='Sans',fontSize=9,leading=13,spaceAfter=18),
 'caption':ParagraphStyle('caption',fontName='Sans',fontSize=8.8,leading=11.7,spaceBefore=6,spaceAfter=11),
 'equation':ParagraphStyle('equation',fontName='Body',fontSize=11,leading=16,spaceBefore=5,spaceAfter=10,alignment=TA_CENTER),
 'cell':ParagraphStyle('cell',fontName='Sans',fontSize=8.4,leading=11.2),
 'headcell':ParagraphStyle('headcell',fontName='SansBold',fontSize=8.5,leading=11.2,textColor=colors.white),
 'ref':ParagraphStyle('ref',fontName='Body',fontSize=9.3,leading=12.2,spaceAfter=11),
 'code':ParagraphStyle('code',fontName='Courier',fontSize=8.1,leading=11,spaceAfter=8),
}

class Architecture(Flowable):
    def __init__(self):
        Flowable.__init__(self); self.width=WIDTH; self.height=208
    def draw(self):
        c=self.canv
        groups=[('Implemented reduced model','Quanta and thermal populations | nuclei | capture',142),
                ('Proposed physical and biological models','Atomic structure | chemistry | matter | planet | life',83),
                ('Proposed agents and institutions','Learning | technology | society | monetary systems',24)]
        for title,subtitle,y in groups:
            c.setStrokeColor(colors.HexColor('#87929C')); c.setFillColor(colors.HexColor('#F4F6F8'))
            if y<140: c.setDash(3,2)
            else: c.setDash()
            c.roundRect(7,y,WIDTH-14,46,3,fill=1,stroke=1); c.setDash()
            c.setFillColor(colors.black); c.setFont('SansBold',10)
            c.drawCentredString(WIDTH/2,y+29,title)
            c.setFont('Sans',8.8); c.drawCentredString(WIDTH/2,y+13,subtitle)
        c.setStrokeColor(colors.HexColor('#54697C'))
        for y in [130,71]:
            c.line(WIDTH/2,y+12,WIDTH/2,y-1)
            c.line(WIDTH/2,y-1,WIDTH/2-3,y+4); c.line(WIDTH/2,y-1,WIDTH/2+3,y+4)
        c.setFont('Sans',8.2); c.drawCentredString(WIDTH/2,5,'Shared contracts proposed across levels: conservation, provenance, error and replay')

def paragraph(text,style='body'):
    text=text.replace('<sub>', '<sub rise="2" size="8">').replace('<super>', '<super rise="4" size="8">')
    if style in ('cell','headcell'): text=text.replace('\n','<br/>')
    return Paragraph(text,styles[style])

def table(block):
    rows=block['rows']; widths=[WIDTH*x for x in block['widths']]
    data=[[paragraph(str(v),'headcell' if ri==0 else 'cell') for v in row] for ri,row in enumerate(rows)]
    t=Table(data,colWidths=widths,repeatRows=1,hAlign='LEFT')
    t.setStyle(TableStyle([
      ('BACKGROUND',(0,0),(-1,0),colors.HexColor('#263C50')),
      ('ROWBACKGROUNDS',(0,1),(-1,-1),[colors.white,colors.HexColor('#F3F5F7')]),
      ('GRID',(0,0),(-1,-1),0.45,colors.HexColor('#D9D9D9')),
      ('VALIGN',(0,0),(-1,-1),'MIDDLE'),
      ('LEFTPADDING',(0,0),(-1,-1),7),('RIGHTPADDING',(0,0),(-1,-1),7),
      ('TOPPADDING',(0,0),(-1,-1),7),('BOTTOMPADDING',(0,0),(-1,-1),7),
    ]))
    return t

def page_footer(c,doc):
    c.saveState(); c.setFont('Sans',8); c.setFillColor(colors.HexColor('#555555'))
    c.drawString(54,32,'SimWorld research white paper v1.1 | 29 October 2026')
    c.drawRightString(PAGE_W-54,32,str(doc.page))
    c.restoreState()

class ResearchDocument(SimpleDocTemplate):
    def afterFlowable(self,flowable):
        if isinstance(flowable,Paragraph) and flowable.style.name in ('h1','title'):
            title=flowable.getPlainText()
            key='outline_'+str(getattr(self,'_outline_count',0))
            self._outline_count=getattr(self,'_outline_count',0)+1
            self.canv.bookmarkPage(key)
            self.canv.addOutlineEntry(title,key,level=0,closed=False)

def render():
    manuscript=json.loads(args.manuscript.read_text(encoding='utf-8'))
    # A fixed publication date keeps PDF identifiers reproducible without
    # suggesting ReportLab's default invariant timestamp of January 2000.
    os.environ.setdefault('SOURCE_DATE_EPOCH', str(int(datetime.fromisoformat(
        manuscript['date']).replace(tzinfo=timezone.utc).timestamp())))
    story=[]
    for b in manuscript['blocks']:
        kind=b['type']
        if kind=='break': story.append(PageBreak())
        elif kind=='space': story.append(Spacer(1,b['points']))
        elif kind=='table': story.extend([table(b),Spacer(1,7)])
        elif kind=='diagram': story.append(Architecture())
        else: story.append(paragraph(b['text'],kind))
    target=args.output
    target.parent.mkdir(parents=True, exist_ok=True)
    doc=ResearchDocument(str(target),pagesize=A4,rightMargin=54,leftMargin=54,
                         topMargin=49,bottomMargin=51,
                         title='SimWorld Research White Paper v1.1',
                         author='',subject='Architecture, implementation evidence and validation agenda',
                         pageCompression=1)
    doc.build(story,onFirstPage=page_footer,onLaterPages=page_footer,
              canvasmaker=lambda *a, **kw: canvas.Canvas(*a, **{**kw, 'invariant': 1}))
    print(str(target))

render()
