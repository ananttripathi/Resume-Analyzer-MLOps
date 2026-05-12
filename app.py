"""
Gradio Frontend Application
Interactive web interface for Resume Analyzer.
"""

import gradio as gr
import os
import sys
from typing import Tuple
import logging

# Add src to path
sys.path.insert(0, os.path.dirname(__file__))

from src.resume_parser import ResumeParser
from src.nlp_processor import NLPProcessor
from src.job_matcher import JobMatcher
from src.ats_scorer import ATSScorer
from src.utils import setup_logging, log_analysis, format_skills_list, load_json

# Setup logging
setup_logging()
logger = logging.getLogger(__name__)

# Initialize components
logger.info("Initializing Resume Analyzer components...")
resume_parser = ResumeParser()
nlp_processor = NLPProcessor()
job_matcher = JobMatcher()
ats_scorer = ATSScorer()

# Load sample job database
try:
    job_database = load_json("data/job_database.json")
    logger.info(f"Loaded {len(job_database.get('jobs', []))} sample jobs")
except:
    job_database = {"jobs": []}
    logger.warning("No job database found")


def analyze_resume(
    resume_file,
    job_description: str = ""
) -> Tuple[str, str, str, str, str]:
    try:
        if resume_file is None:
            return "⚠️ Please upload a resume file", "", "", "", ""

        # Parse resume
        logger.info(f"Processing: {resume_file}")
        parsed_data = resume_parser.parse_file(resume_file)
        resume_text = parsed_data['cleaned_text']

        # Extract information
        skills = nlp_processor.extract_skills(resume_text)
        experience_years = nlp_processor.calculate_experience_years(resume_text)
        experiences = nlp_processor.extract_experience(resume_text)
        education = nlp_processor.extract_education(resume_text)

        # Calculate ATS score
        ats_results = ats_scorer.calculate_score(resume_text, job_description)

        # ── Design tokens ────────────────────────────────────────────────────
        C_BG       = "#fafafa"
        C_CARD     = "white"
        C_BORDER   = "#f3f4f6"
        C_TEXT     = "#171717"
        C_MUTED    = "#737373"
        C_ACCENT   = "#6366f1"
        C_SUCCESS  = "#16a34a"
        C_WARNING  = "#d97706"
        C_ERROR    = "#dc2626"
        CARD_STYLE = f"background:{C_CARD};border:1px solid {C_BORDER};border-radius:12px;padding:20px;margin:12px 0;"
        SHADOW     = "box-shadow:0 1px 3px rgba(0,0,0,0.06);"

        # ── Overview ─────────────────────────────────────────────────────────
        overview = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">

  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Analysis complete</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">Resume Overview</h2>
  </div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(200px,1fr));gap:12px;margin:16px 0;">
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">File</p>
      <p style="margin:0;font-size:14px;font-weight:600;color:{C_TEXT};">{os.path.basename(resume_file)}</p>
      <p style="margin:4px 0 0 0;font-size:13px;color:{C_MUTED};">{parsed_data['word_count']} words</p>
    </div>
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Experience</p>
      <p style="margin:0;font-size:28px;font-weight:700;color:{C_TEXT};">{experience_years}</p>
      <p style="margin:0;font-size:13px;color:{C_MUTED};">years</p>
    </div>
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Skills found</p>
      <p style="margin:0;font-size:28px;font-weight:700;color:{C_ACCENT};">{sum(len(s) for s in skills.values())}</p>
      <p style="margin:0;font-size:13px;color:{C_MUTED};">identified</p>
    </div>
  </div>

  <div style="{CARD_STYLE}{SHADOW}">
    <p style="margin:0 0 12px 0;font-size:13px;font-weight:600;color:{C_TEXT};">Contact</p>
"""
        if parsed_data['metadata'].get('emails'):
            overview += f"<p style='margin:4px 0;font-size:13px;color:{C_MUTED};'>✉️ {parsed_data['metadata']['emails'][0]}</p>"
        if parsed_data['metadata'].get('phones'):
            overview += f"<p style='margin:4px 0;font-size:13px;color:{C_MUTED};'>📱 {parsed_data['metadata']['phones'][0]}</p>"
        if parsed_data['metadata'].get('linkedin'):
            overview += f"<p style='margin:4px 0;font-size:13px;color:{C_MUTED};'>🔗 {parsed_data['metadata']['linkedin']}</p>"
        overview += "</div></div>"

        # ── ATS Score ─────────────────────────────────────────────────────────
        score = ats_results['overall_score']
        score_color = C_SUCCESS if score >= 80 else C_WARNING if score >= 60 else C_ERROR
        dash_offset = 440 - (440 * score / 100)

        ats_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">

  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">ATS compatibility</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">Score Breakdown</h2>
  </div>

  <div style="{CARD_STYLE}{SHADOW}text-align:center;padding:32px;">
    <div style="display:inline-block;position:relative;width:160px;height:160px;">
      <svg width="160" height="160" style="transform:rotate(-90deg);">
        <circle cx="80" cy="80" r="64" fill="none" stroke="{C_BORDER}" stroke-width="16"/>
        <circle cx="80" cy="80" r="64" fill="none" stroke="{score_color}" stroke-width="16"
                stroke-dasharray="402" stroke-dashoffset="{402 - (402 * score / 100):.1f}"
                stroke-linecap="round"/>
      </svg>
      <div style="position:absolute;top:50%;left:50%;transform:translate(-50%,-50%);text-align:center;">
        <div style="font-size:36px;font-weight:800;color:{score_color};">{score}</div>
        <div style="font-size:11px;color:{C_MUTED};">/ 100</div>
      </div>
    </div>
    <p style="margin:16px 0 0 0;font-size:15px;font-weight:600;color:{score_color};">Grade: {ats_results['grade']}</p>
  </div>

  <div style="display:grid;grid-template-columns:repeat(auto-fit,minmax(180px,1fr));gap:12px;margin:16px 0;">
"""
        for idx, (category, data) in enumerate(ats_results['category_scores'].items()):
            cat_name = category.replace('_', ' ').title()
            cat_score = data['score']
            ats_display += f"""
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">{cat_name}</p>
      <p style="margin:0 0 8px 0;font-size:22px;font-weight:700;color:{C_TEXT};">{cat_score:.0f}<span style="font-size:13px;color:{C_MUTED};">/100</span></p>
      <div style="background:{C_BORDER};height:6px;border-radius:3px;overflow:hidden;">
        <div style="background:{C_ACCENT};height:100%;width:{cat_score}%;"></div>
      </div>
    </div>
"""
        ats_display += "</div>"
        ats_display += f"""
  <div style="{CARD_STYLE}{SHADOW}">
    <p style="margin:0 0 12px 0;font-size:13px;font-weight:600;color:{C_TEXT};">Key findings</p>
"""
        for feedback in ats_results['feedback'][:5]:
            icon = "✅" if "Excellent" in feedback or "good" in feedback.lower() else "⚠️"
            ats_display += f"<p style='margin:6px 0;font-size:13px;color:{C_MUTED};padding:8px 0;border-bottom:1px solid {C_BORDER};'>{icon} {feedback}</p>"
        ats_display += "</div></div>"

        # ── Skills ────────────────────────────────────────────────────────────
        skill_colors = {
            'programming': C_ACCENT,
            'web':         '#0891b2',
            'data_science':'#7c3aed',
            'cloud':       '#0284c7',
            'database':    '#d97706',
            'tools':       '#059669',
            'soft_skills': '#db2777',
        }

        skills_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">

  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Skills portfolio</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">{sum(len(s) for s in skills.values())} skills identified</h2>
  </div>
"""
        if skills:
            for category, skill_list in skills.items():
                cat_name = category.replace('_', ' ').title()
                color = skill_colors.get(category, C_MUTED)
                badge_bg = color + "18"
                skills_display += f"""
  <div style="{CARD_STYLE}{SHADOW}">
    <p style="margin:0 0 12px 0;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:{color};padding-bottom:8px;border-bottom:1px solid {C_BORDER};">
      {cat_name} · {len(skill_list)}
    </p>
    <div style="display:flex;flex-wrap:wrap;gap:6px;">
"""
                for skill in skill_list:
                    skills_display += f"""
      <span style="background:{badge_bg};color:{color};border:1px solid {color}30;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">{skill}</span>
"""
                skills_display += "</div></div>"
        else:
            skills_display += f"<p style='color:{C_MUTED};font-size:14px;'>No specific skills detected. Consider adding a dedicated skills section.</p>"
        skills_display += "</div>"

        # ── Job Match ─────────────────────────────────────────────────────────
        job_match_display = ""
        recommendations_display = ""

        if job_description and job_description.strip():
            similarity = job_matcher.calculate_similarity(resume_text, job_description)
            jd_skills = nlp_processor.extract_skills(job_description)
            all_resume_skills = [s for sl in skills.values() for s in sl]
            all_jd_skills    = [s for sl in jd_skills.values() for s in sl]
            skill_gap = job_matcher.analyze_skill_match(all_resume_skills, all_jd_skills)
            match_pct = similarity * 100
            match_color = C_SUCCESS if similarity >= 0.7 else C_WARNING if similarity >= 0.5 else C_ERROR

            job_match_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">

  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Job match</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">Compatibility Analysis</h2>
  </div>

  <div style="{CARD_STYLE}{SHADOW}text-align:center;padding:28px;">
    <p style="margin:0 0 8px 0;font-size:12px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">Semantic match score</p>
    <p style="margin:0;font-size:52px;font-weight:800;color:{match_color};">{match_pct:.1f}%</p>
  </div>

  <div style="display:grid;grid-template-columns:1fr 1fr;gap:12px;margin:12px 0;">
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 10px 0;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:{C_SUCCESS};">✅ Matching · {len(skill_gap['matching_skills'])}</p>
      <div style="display:flex;flex-wrap:wrap;gap:5px;max-height:180px;overflow-y:auto;">
"""
            if skill_gap['matching_skills']:
                for skill in skill_gap['matching_skills'][:15]:
                    job_match_display += f"<span style='background:#f0fdf4;color:{C_SUCCESS};border:1px solid #bbf7d0;padding:3px 10px;border-radius:16px;font-size:11px;font-weight:500;'>{skill}</span>"
            else:
                job_match_display += f"<p style='color:{C_MUTED};font-size:13px;'>None found</p>"

            job_match_display += f"""
      </div>
    </div>
    <div style="{CARD_STYLE}{SHADOW}">
      <p style="margin:0 0 10px 0;font-size:12px;font-weight:700;text-transform:uppercase;letter-spacing:.06em;color:{C_ERROR};">❌ Missing · {len(skill_gap['missing_skills'])}</p>
      <div style="display:flex;flex-wrap:wrap;gap:5px;max-height:180px;overflow-y:auto;">
"""
            if skill_gap['missing_skills']:
                for skill in skill_gap['missing_skills'][:15]:
                    job_match_display += f"<span style='background:#fef2f2;color:{C_ERROR};border:1px solid #fecaca;padding:3px 10px;border-radius:16px;font-size:11px;font-weight:500;'>{skill}</span>"
            else:
                job_match_display += f"<p style='color:{C_MUTED};font-size:13px;'>All required skills matched!</p>"

            job_match_display += f"""
      </div>
    </div>
  </div>

  <div style="{CARD_STYLE}{SHADOW}">
    <p style="margin:0 0 8px 0;font-size:13px;font-weight:600;color:{C_TEXT};">Skill coverage</p>
    <div style="background:{C_BORDER};height:8px;border-radius:4px;overflow:hidden;">
      <div style="background:{C_ACCENT};height:100%;width:{skill_gap['match_percentage']:.1f}%;"></div>
    </div>
    <p style="margin:6px 0 0 0;font-size:12px;color:{C_MUTED};">{skill_gap['total_matched']} of {skill_gap['total_required']} required skills found</p>
  </div>
</div>
"""
            recommendations = job_matcher.generate_recommendations(
                resume_text, job_description, all_resume_skills
            )

            recommendations_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">
  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">AI suggestions</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">Recommendations</h2>
  </div>
  <div style="{CARD_STYLE}{SHADOW}">
"""
            for i, rec in enumerate(recommendations, 1):
                recommendations_display += f"""
    <div style="padding:12px 0;border-bottom:1px solid {C_BORDER};display:flex;gap:12px;align-items:flex-start;">
      <span style="background:{C_ACCENT};color:white;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;">{i}</span>
      <p style="margin:0;font-size:13px;color:{C_TEXT};line-height:1.5;">{rec}</p>
    </div>
"""
            recommendations_display += "</div></div>"

            log_analysis(
                os.path.basename(resume_file),
                ats_results['overall_score'],
                similarity
            )
        else:
            job_match_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">
  <div style="{CARD_STYLE}{SHADOW}text-align:center;padding:48px 20px;">
    <p style="font-size:40px;margin:0 0 12px 0;">📝</p>
    <p style="margin:0 0 8px 0;font-size:16px;font-weight:600;color:{C_TEXT};">No job description provided</p>
    <p style="margin:0;font-size:13px;color:{C_MUTED};">Paste a JD above to get match %, skill gaps, and tailored recommendations.</p>
  </div>
</div>
"""
            tips = [
                "Add a job description above for personalized recommendations",
                "Ensure your resume has clear sections: Experience, Education, Skills",
                "Use action verbs and quantifiable achievements",
                "Keep formatting simple and ATS-friendly — avoid tables and graphics",
            ]
            tips_html = "".join(
                '<div style="padding:12px 0;border-bottom:1px solid ' + C_BORDER + ';display:flex;gap:12px;align-items:flex-start;">'
                '<span style="background:' + C_ACCENT + ';color:white;border-radius:50%;width:22px;height:22px;display:inline-flex;align-items:center;justify-content:center;font-size:11px;font-weight:700;flex-shrink:0;">' + str(i) + '</span>'
                '<p style="margin:0;font-size:13px;color:' + C_TEXT + ';line-height:1.5;">' + tip + '</p></div>'
                for i, tip in enumerate(tips, 1)
            )
            recommendations_display = f"""
<div style="font-family:'Inter',sans-serif;padding:4px;">
  <div style="{CARD_STYLE}{SHADOW}border-left:4px solid {C_ACCENT};">
    <p style="margin:0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.06em;color:{C_MUTED};">General tips</p>
    <h2 style="margin:4px 0 0 0;font-size:20px;font-weight:700;color:{C_TEXT};">Best Practices</h2>
  </div>
  <div style="{CARD_STYLE}{SHADOW}">{tips_html}</div>
</div>
"""
        return (
            overview,
            ats_display,
            skills_display,
            job_match_display,
            recommendations_display
        )

    except Exception as e:
        logger.error(f"Analysis failed: {e}", exc_info=True)
        error_msg = f"""
<div style="font-family:'Inter',sans-serif;padding:20px;background:#fef2f2;border-radius:12px;border-left:4px solid #dc2626;color:#991b1b;">
    <p style="margin:0 0 8px 0;font-weight:600;">Analysis failed</p>
    <p style="margin:0;font-size:13px;">{str(e)}</p>
    <p style="margin:12px 0 0 0;font-size:12px;color:#b91c1c;">Please try again with a different file.</p>
</div>
"""
        return error_msg, "", "", "", ""


def create_interface():
    custom_css = """
    @import url('https://fonts.googleapis.com/css2?family=Inter:wght@400;500;600;700;800&display=swap');

    * { font-family: 'Inter', sans-serif !important; box-sizing: border-box; }

    body, .gradio-container { background: #fafafa !important; }

    .gradio-container { max-width: 1200px !important; margin: auto !important; padding: 24px !important; }

    /* Primary button */
    .gr-button-primary, button[data-testid="submit-btn"], .primary {
        background: #171717 !important;
        border: none !important;
        font-weight: 600 !important;
        font-size: 14px !important;
        padding: 10px 28px !important;
        border-radius: 8px !important;
        color: white !important;
        transition: background 0.2s !important;
    }
    .gr-button-primary:hover, .primary:hover {
        background: #404040 !important;
    }

    /* Inputs */
    .gr-input, .gr-textarea, input, textarea {
        border-radius: 8px !important;
        border: 1px solid #e5e7eb !important;
        font-size: 13px !important;
        background: white !important;
        color: #171717 !important;
        transition: border-color 0.2s !important;
    }
    .gr-input:focus, .gr-textarea:focus, input:focus, textarea:focus {
        border-color: #6366f1 !important;
        box-shadow: 0 0 0 3px rgba(99,102,241,0.12) !important;
        outline: none !important;
    }

    /* Cards / panels */
    .gr-box, .gr-panel, .gr-form {
        background: white !important;
        border: 1px solid #f3f4f6 !important;
        border-radius: 12px !important;
        box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important;
    }

    /* File upload */
    .gr-file {
        border: 2px dashed #e5e7eb !important;
        border-radius: 12px !important;
        background: #fafafa !important;
        transition: border-color 0.2s !important;
    }
    .gr-file:hover { border-color: #6366f1 !important; }

    /* Tabs */
    .tabs { border-radius: 12px !important; overflow: hidden !important; background: white !important; border: 1px solid #f3f4f6 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.05) !important; }
    .tab-nav { background: #fafafa !important; padding: 6px !important; border-bottom: 1px solid #f3f4f6 !important; }
    .tab-nav button { font-size: 13px !important; font-weight: 500 !important; padding: 8px 16px !important; border-radius: 6px !important; color: #737373 !important; transition: all 0.2s !important; }
    .tab-nav button:hover { background: #f3f4f6 !important; color: #171717 !important; }
    .tab-nav button[aria-selected="true"] { background: white !important; color: #6366f1 !important; font-weight: 600 !important; box-shadow: 0 1px 3px rgba(0,0,0,0.08) !important; }

    label { font-weight: 500 !important; color: #374151 !important; font-size: 13px !important; }
    h1, h2, h3 { font-weight: 700 !important; color: #171717 !important; }
    """

    with gr.Blocks(css=custom_css, title="Resume Analyzer — ML Career Hub", theme=gr.themes.Base()) as demo:

        # Header
        gr.HTML("""
        <div style="padding:32px 0 24px 0;border-bottom:1px solid #f3f4f6;margin-bottom:24px;">
          <p style="margin:0 0 4px 0;font-size:11px;font-weight:600;text-transform:uppercase;letter-spacing:.08em;color:#6366f1;">ML Career Hub</p>
          <h1 style="margin:0 0 8px 0;font-size:28px;font-weight:800;color:#171717;">Resume Analyzer</h1>
          <p style="margin:0;font-size:14px;color:#737373;">Upload your resume and optionally paste a job description to get an ATS score, skill gap analysis, and AI recommendations.</p>
          <div style="display:flex;gap:8px;flex-wrap:wrap;margin-top:16px;">
            <span style="background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">✅ ATS Optimization</span>
            <span style="background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">🎯 Skills Extraction</span>
            <span style="background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">📊 Job Matching</span>
            <span style="background:#eef2ff;color:#4338ca;border:1px solid #c7d2fe;padding:4px 12px;border-radius:20px;font-size:12px;font-weight:500;">💡 AI Recommendations</span>
          </div>
        </div>
        """)

        with gr.Row():
            with gr.Column(scale=2):
                resume_input = gr.File(
                    label="Resume",
                    file_types=[".pdf", ".docx", ".txt"],
                    type="filepath"
                )
                job_desc_input = gr.Textbox(
                    label="Job Description (optional)",
                    placeholder="Paste the job description here for ATS match score and personalized recommendations…",
                    lines=10
                )
                analyze_btn = gr.Button("🔍 Analyze Resume", variant="primary", size="lg")

                gr.HTML("""
                <div style="margin-top:16px;padding:16px;background:white;border:1px solid #f3f4f6;border-radius:12px;">
                  <p style="margin:0 0 8px 0;font-size:12px;font-weight:600;color:#374151;">Quick tips</p>
                  <p style="margin:3px 0;font-size:12px;color:#737373;">• Supported: PDF, DOCX, TXT (max 10 MB)</p>
                  <p style="margin:3px 0;font-size:12px;color:#737373;">• Add a JD for a personalised ATS match score</p>
                  <p style="margin:3px 0;font-size:12px;color:#737373;">• Processing takes ~5–10 seconds</p>
                </div>
                """)

        gr.HTML("""<div style="margin:28px 0 16px 0;padding-bottom:12px;border-bottom:1px solid #f3f4f6;">
          <h2 style="margin:0;font-size:18px;font-weight:700;color:#171717;">Results</h2>
        </div>""")

        with gr.Tabs():
            with gr.Tab("Overview"):
                overview_output = gr.HTML()
            with gr.Tab("ATS Score"):
                ats_output = gr.HTML()
            with gr.Tab("Skills"):
                skills_output = gr.HTML()
            with gr.Tab("Job Match"):
                job_match_output = gr.HTML()
            with gr.Tab("Recommendations"):
                recommendations_output = gr.HTML()

        analyze_btn.click(
            fn=analyze_resume,
            inputs=[resume_input, job_desc_input],
            outputs=[overview_output, ats_output, skills_output, job_match_output, recommendations_output]
        )

        gr.HTML("""
        <div style="margin-top:40px;padding-top:20px;border-top:1px solid #f3f4f6;display:flex;align-items:center;justify-content:space-between;flex-wrap:wrap;gap:12px;">
          <p style="margin:0;font-size:12px;color:#a3a3a3;">Built with Transformers · Sentence-BERT · FastAPI · Gradio</p>
          <p style="margin:0;font-size:12px;color:#a3a3a3;">© 2025 ML Career Hub · Anant Tripathi</p>
        </div>
        """)

    return demo


if __name__ == "__main__":
    logger.info("Starting Gradio application...")
    demo = create_interface()
    demo.launch(
        server_name="0.0.0.0",
        server_port=7860,
        share=False
    )
