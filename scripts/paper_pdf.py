"""Render docs/PAPER.md to PDF with optional ReportLab dependency."""
import html
import re
from pathlib import Path
from reportlab.lib import colors
from reportlab.lib.enums import TA_LEFT
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.lib.units import inch
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak

ROOT=Path(__file__).resolve().parents[1]

def main():
    output=ROOT/'output/pdf'
    output.mkdir(parents=True,exist_ok=True)
    styles=getSampleStyleSheet()
    styles.add(ParagraphStyle('PaperBody',fontName='Times-Roman',fontSize=10.5,leading=14,spaceAfter=7))
    styles.add(ParagraphStyle('PaperTitle',fontName='Times-Bold',fontSize=22,leading=26,spaceAfter=14))
    styles.add(ParagraphStyle('PaperSection',fontName='Helvetica-Bold',fontSize=13,leading=17,spaceBefore=13,spaceAfter=7,keepWithNext=True))
    styles.add(ParagraphStyle('PaperSubsection',fontName='Helvetica-Bold',fontSize=11,leading=14,spaceBefore=9,spaceAfter=5,keepWithNext=True))
    styles.add(ParagraphStyle('PaperTable',fontName='Helvetica',fontSize=8.5,leading=11))
    def paragraph(text,style='PaperBody'):
        return Paragraph(html.escape(text),styles[style])
    lines=(ROOT/'docs/PAPER.md').read_text().splitlines()
    story=[];i=0
    while i<len(lines):
        line=lines[i]
        if not line.strip():i+=1;continue
        if line.startswith('|'):
            rows=[]
            while i<len(lines) and lines[i].startswith('|'):
                cells=[x.strip() for x in lines[i].strip('|').split('|')]
                if not all(re.fullmatch(r'[-:]+',x) for x in cells):
                    rows.append([paragraph(x,'PaperTable') for x in cells])
                i+=1
            widths={3:[90,60,282],4:[160,90,90,92],6:[40,88,88,88,64,64]}[len(rows[0])]
            table=Table(rows,colWidths=widths,repeatRows=1,hAlign='LEFT',splitByRow=0)
            table.setStyle(TableStyle([('BACKGROUND',(0,0),(-1,0),colors.HexColor('#e7efed')),
                ('LINEBELOW',(0,0),(-1,0),.8,colors.HexColor('#37625b')),
                ('LINEBELOW',(0,1),(-1,-1),.3,colors.HexColor('#dddddd')),
                ('VALIGN',(0,0),(-1,-1),'TOP'),('TOPPADDING',(0,0),(-1,-1),7),
                ('BOTTOMPADDING',(0,0),(-1,-1),7)]))
            story.extend([table,Spacer(1,10)]);continue
        if line.startswith('# '):story.append(paragraph(line[2:],'PaperTitle'))
        elif line.startswith('### '):story.append(paragraph(line[4:],'PaperSubsection'))
        elif line.startswith('## '):
            if line=='## References':story.append(PageBreak())
            story.append(paragraph(line[3:],'PaperSection'))
        else:story.append(paragraph(line))
        i+=1
    def footer(canvas,doc):
        canvas.saveState();canvas.setFont('Helvetica',8);canvas.setFillColor(colors.HexColor('#65756f'))
        canvas.drawString(48,30,'INDUS SIGN SYSTEM | RESEARCH DRAFT | 15 OCTOBER 2026')
        canvas.drawRightString(564,30,str(doc.page));canvas.restoreState()
    doc=SimpleDocTemplate(str(output/'indus_structural_research.pdf'),pagesize=(612,792),
        rightMargin=48,leftMargin=48,topMargin=45,bottomMargin=48,
        title='Structural Constraints in the Indus Sign System',author='Codex research draft',pageCompression=1,invariant=1)
    doc.build(story,onFirstPage=footer,onLaterPages=footer)
    print(output/'indus_structural_research.pdf')

if __name__=='__main__':main()
