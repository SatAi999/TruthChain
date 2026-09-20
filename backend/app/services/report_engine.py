import os
from io import BytesIO
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, HRFlowable, KeepTogether

class ReportEngine:
    @staticmethod
    def generate_pdf_report(case_data: dict) -> bytes:
        """
        Generates a professional PDF investigation report.
        """
        buffer = BytesIO()
        doc = SimpleDocTemplate(
            buffer,
            pagesize=letter,
            rightMargin=36, leftMargin=36, topMargin=36, bottomMargin=36
        )
        
        styles = getSampleStyleSheet()
        
        # Custom Styles
        title_style = ParagraphStyle(
            'ReportTitle',
            parent=styles['Heading1'],
            fontName='Helvetica-Bold',
            fontSize=22,
            leading=26,
            textColor=colors.HexColor('#0f172a'),
            spaceAfter=6
        )
        
        subtitle_style = ParagraphStyle(
            'ReportSubtitle',
            parent=styles['Normal'],
            fontName='Helvetica',
            fontSize=10,
            leading=14,
            textColor=colors.HexColor('#64748b'),
            spaceAfter=15
        )

        h2_style = ParagraphStyle(
            'Heading2Custom',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=13,
            leading=16,
            textColor=colors.HexColor('#1e293b'),
            spaceBefore=12,
            spaceAfter=6
        )

        body_style = ParagraphStyle(
            'BodyCustom',
            parent=styles['BodyText'],
            fontName='Helvetica',
            fontSize=9.5,
            leading=13.5,
            textColor=colors.HexColor('#334155')
        )

        verdict_style = ParagraphStyle(
            'VerdictStyle',
            parent=styles['Heading2'],
            fontName='Helvetica-Bold',
            fontSize=14,
            leading=18,
            textColor=colors.HexColor('#0369a1')
        )

        elements = []

        # Header
        elements.append(Paragraph("TRUTHCHAIN — CASE INVESTIGATION REPORT", title_style))
        elements.append(Paragraph(f"Case ID: {case_data.get('id')} | Generated: 2026-09-20 | Classification: RESTRICTED AUDIT TRAIL", subtitle_style))
        elements.append(HRFlowable(width="100%", thickness=1.5, color=colors.HexColor('#0f172a'), spaceAfter=15))

        # 1. Original Claim & Verdict Banner
        elements.append(Paragraph("ORIGINAL CLAIM", h2_style))
        elements.append(Paragraph(f"<i>\"{case_data.get('claim_statement')}\"</i>", body_style))
        elements.append(Spacer(1, 10))

        verdict_text = case_data.get("verdict", "PARTIALLY_SUPPORTED")
        verdict_reasoning = case_data.get("verdict_reasoning", "The available evidence supports partial completion but fails deadline requirements.")

        verdict_table_data = [
            [Paragraph(f"FINAL ASSESSMENT VERDICT: <b>{verdict_text}</b>", verdict_style)],
            [Paragraph(verdict_reasoning, body_style)]
        ]
        verdict_table = Table(verdict_table_data, colWidths=[540])
        verdict_table.setStyle(TableStyle([
            ('BACKGROUND', (0,0), (-1,-1), colors.HexColor('#f0f9ff')),
            ('BOX', (0,0), (-1,-1), 1, colors.HexColor('#0284c7')),
            ('PADDING', (0,0), (-1,-1), 10),
            ('BOTTOMPADDING', (0,0), (-1,0), 4),
        ]))
        elements.append(verdict_table)
        elements.append(Spacer(1, 15))

        # 2. Atomic Claims Table
        elements.append(Paragraph("ATOMIC CLAIM DECOMPOSITION", h2_style))
        ac_data = [["Sub-claim Statement", "Verification Subject", "Status", "Confidence"]]
        for ac in case_data.get("atomic_claims", []):
            ac_data.append([
                Paragraph(ac.get("statement", ""), body_style),
                ac.get("subject", "N/A"),
                ac.get("status", "UNVERIFIED"),
                f"{int(ac.get('confidence', 0)*100)}%"
            ])
        
        if len(ac_data) > 1:
            ac_table = Table(ac_data, colWidths=[260, 110, 100, 70])
            ac_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#e2e8f0')),
                ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor('#0f172a')),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 9),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('PADDING', (0,0), (-1,-1), 6),
            ]))
            elements.append(ac_table)
        elements.append(Spacer(1, 15))

        # 3. Contradictions Section
        elements.append(Paragraph("DETECTED CONTRADICTIONS & DISCREPANCIES", h2_style))
        contradictions = case_data.get("contradictions", [])
        if contradictions:
            for idx, c in enumerate(contradictions, start=1):
                c_text = f"<b>[{c.get('contradiction_type')}] Contradiction #{idx}</b> (Severity: {c.get('severity')})<br/>" \
                         f"• Statement A ({c.get('source_a_name', 'Source A')}): {c.get('statement_a')}<br/>" \
                         f"• Statement B ({c.get('source_b_name', 'Source B')}): {c.get('statement_b')}<br/>" \
                         f"• Resolution Status: {c.get('status')} - {c.get('resolution_summary', 'Pending evidence verification')}"
                elements.append(Paragraph(c_text, body_style))
                elements.append(Spacer(1, 6))
        else:
            elements.append(Paragraph("No severe contradictions detected across ingested sources.", body_style))
        elements.append(Spacer(1, 15))

        # 4. Timeline
        elements.append(Paragraph("CHRONOLOGICAL EVIDENCE TIMELINE", h2_style))
        events = case_data.get("events", [])
        if events:
            ev_data = [["Date", "Event Description", "Location", "Deadline Flag"]]
            for ev in events:
                is_deadline_str = "YES [DEADLINE]" if ev.get("is_deadline") else "No"
                ev_data.append([
                    ev.get("display_date", ""),
                    Paragraph(ev.get("description", ""), body_style),
                    ev.get("location", "N/A"),
                    is_deadline_str
                ])
            ev_table = Table(ev_data, colWidths=[90, 260, 100, 90])
            ev_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f1f5f9')),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 8.5),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#cbd5e1')),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(ev_table)
        elements.append(Spacer(1, 15))

        # 5. Evidence Gaps
        elements.append(Paragraph("EVIDENCE GAP ANALYSIS", h2_style))
        gaps = case_data.get("evidence_gaps", [])
        if gaps:
            for g in gaps:
                gap_text = f"• <b>Description:</b> {g.get('description')}<br/>" \
                           f"  <b>Why It Matters:</b> {g.get('why_it_matters')}<br/>" \
                           f"  <b>Next Best Evidence Requested:</b> <i>{g.get('next_best_evidence')}</i>"
                elements.append(Paragraph(gap_text, body_style))
                elements.append(Spacer(1, 6))
        else:
            elements.append(Paragraph("No open evidence gaps remaining.", body_style))
        elements.append(Spacer(1, 15))

        # 6. Audit Trail & Sources Register
        elements.append(Paragraph("SOURCE REGISTER & AUDIT TRAIL", h2_style))
        sources = case_data.get("sources", [])
        if sources:
            src_data = [["Source Name", "Format", "Source Lineage Type", "Created At"]]
            for s in sources:
                src_data.append([
                    s.get("name", ""),
                    s.get("file_type", ""),
                    s.get("source_type", "PRIMARY"),
                    str(s.get("created_at", ""))[:19]
                ])
            src_table = Table(src_data, colWidths=[200, 70, 140, 130])
            src_table.setStyle(TableStyle([
                ('BACKGROUND', (0,0), (-1,0), colors.HexColor('#f8fafc')),
                ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
                ('FONTSIZE', (0,0), (-1,0), 8.5),
                ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor('#e2e8f0')),
                ('PADDING', (0,0), (-1,-1), 5),
            ]))
            elements.append(src_table)

        doc.build(elements)
        buffer.seek(0)
        return buffer.getvalue()
