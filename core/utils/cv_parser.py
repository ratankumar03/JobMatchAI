"""
CV/Resume Parser - Extracts skills and experience from PDF and DOCX files
"""
import PyPDF2
import docx
import re
from datetime import datetime


class CVParser:
    """Parse CV/Resume and extract relevant information"""
    
    def parse_cv(self, file_path):
        """
        Parse CV and extract text content
        Args:
            file_path: Path to CV file
        Returns:
            dict: Extracted information
        """
        text_content = ""
        
        # Determine file type and extract text
        if file_path.endswith('.pdf'):
            text_content = self._extract_from_pdf(file_path)
        elif file_path.endswith(('.docx', '.doc')):
            text_content = self._extract_from_docx(file_path)
        else:
            return {'error': 'Unsupported file format'}
        
        if not text_content:
            return {'error': 'Could not extract text from file'}
        
        # Debug: Print entire CV text (safely handle Unicode)
        try:
            print("="*80)
            print("FULL CV TEXT:")
            print(text_content.encode('utf-8', errors='replace').decode('utf-8'))
            print("="*80)
        except Exception as e:
            print(f"Could not print CV text (Unicode error): {e}")
        
        # Extract information using keyword matching
        return self._extract_basic(text_content)
    
    def _extract_from_pdf(self, pdf_path):
        """Extract text from PDF file"""
        try:
            text = ""
            with open(pdf_path, 'rb') as file:
                pdf_reader = PyPDF2.PdfReader(file)
                for page in pdf_reader.pages:
                    text += page.extract_text() + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting PDF: {e}")
            return ""
    
    def _extract_from_docx(self, docx_path):
        """Extract text from DOCX file"""
        try:
            doc = docx.Document(docx_path)
            text = ""
            for paragraph in doc.paragraphs:
                text += paragraph.text + "\n"
            return text.strip()
        except Exception as e:
            print(f"Error extracting DOCX: {e}")
            return ""
    
    def _extract_basic(self, text_content):
        """Keyword-based extraction with accurate experience calculation"""
        skills = []
        
        # Common technical skills
        tech_skills = [
            'Python', 'Java', 'JavaScript', 'C++', 'C#', 'SQL', 'HTML', 'CSS',
            'React', 'Angular', 'Vue', 'Node.js', 'Django', 'Flask', 'Spring',
            'MongoDB', 'PostgreSQL', 'MySQL', 'AWS', 'Azure', 'GCP', 'Docker',
            'Kubernetes', 'Git', 'Jenkins', 'Agile', 'Scrum', 'REST API',
            'Machine Learning', 'Data Analysis', 'Excel', 'PowerPoint', 'Tableau',
            'Power BI', 'Pandas', 'NumPy', 'TensorFlow', 'Scikit-learn', 'PHP',
            'Bootstrap', 'Cisco', 'OOP', 'Full Stack', 'Web Development', 'NoSQL',
            'SQLite', 'Plotly', 'SMOTE', 'SVM', 'Random Forest', 'K-Means', 'DBSCAN'
        ]
        
        # Soft skills
        soft_skills = [
            'Communication', 'Leadership', 'Teamwork', 'Problem Solving',
            'Critical Thinking', 'Time Management', 'Project Management'
        ]
        
        text_lower = text_content.lower()
        
        # Find technical skills
        for skill in tech_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        # Find soft skills
        for skill in soft_skills:
            if skill.lower() in text_lower:
                skills.append(skill)
        
        # Calculate work experience - ONLY from EXPERIENCE section
        experience_years = self._calculate_work_experience_v2(text_content)
        
        # Find education
        education = self._extract_education(text_content)
        
        # Find job titles
        job_titles = self._extract_job_titles(text_content)
        
        return {
            'skills': ', '.join(set(skills[:25])) if skills else 'Professional skills',
            'experience_years': experience_years,
            'education': education,
            'job_titles': ', '.join(set(job_titles[:5])) if job_titles else 'Professional',
            'achievements': 'Extracted from CV',
            'industries': 'Technology, Software Development',
            'raw_text': text_content[:1000]
        }
    
    def _calculate_work_experience_v2(self, text):
        """
        NEW APPROACH: Only count dates that appear BETWEEN "EXPERIENCE" and the NEXT section
        """
        lines = text.split('\n')
        
        # Find EXPERIENCE section boundaries
        exp_start_idx = -1
        exp_end_idx = len(lines)
        
        # Section headers to look for
        section_headers = [
            'EXPERIENCE', 'WORK EXPERIENCE', 'PROFESSIONAL EXPERIENCE', 'EMPLOYMENT HISTORY',
            'CAREER HISTORY', 'Work History'
        ]
        
        stop_headers = [
            'PERSONAL PROJECTS', 'PROJECTS', 'PROJECT', 'GROUP PROJECTS',
            'EDUCATION', 'ACADEMIC', 'QUALIFICATION',
            'SKILLS', 'TECHNICAL SKILLS', 'CORE COMPETENCIES',
            'CERTIFICATIONS', 'CERTIFICATES', 'TRAINING',
            'ACHIEVEMENTS', 'AWARDS', 'HONORS',
            'PUBLICATIONS', 'RESEARCH',
            'REFERENCES', 'HOBBIES', 'INTERESTS'
        ]
        
        # Find where EXPERIENCE starts
        for i, line in enumerate(lines):
            line_upper = line.strip().upper()
            for header in section_headers:
                if line_upper == header or line_upper.startswith(header):
                    exp_start_idx = i
                    print(f"[OK] Found EXPERIENCE section at line {i}: {line.strip()}")
                    break
            if exp_start_idx != -1:
                break

        if exp_start_idx == -1:
            print("[X] No EXPERIENCE section found")
            return '0'
        
        # Find where EXPERIENCE ends (next major section)
        for i in range(exp_start_idx + 1, len(lines)):
            line_upper = lines[i].strip().upper()
            for stop_header in stop_headers:
                if line_upper == stop_header or line_upper.startswith(stop_header):
                    exp_end_idx = i
                    print(f"[OK] EXPERIENCE section ends at line {i}: {lines[i].strip()}")
                    break
            if exp_end_idx != len(lines):
                break
        
        # Extract only EXPERIENCE section text
        experience_text = '\n'.join(lines[exp_start_idx:exp_end_idx])
        try:
            print("\n" + "="*80)
            print("EXPERIENCE SECTION ONLY:")
            print(experience_text.encode('utf-8', errors='replace').decode('utf-8'))
            print("="*80 + "\n")
        except Exception as e:
            print(f"Could not print experience text (Unicode error): {e}")
        
        # Now count dates ONLY in this section
        total_months = self._count_months_in_text(experience_text)
        
        # Convert to years
        if total_months > 0:
            years = total_months / 12.0
            print(f"\n>>> FINAL: {total_months} months = {years:.1f} years\n")
            
            if years < 1:
                if total_months <= 6:
                    return f"0 ({total_months} months)"
                else:
                    return "0-1"
            elif years < 2:
                return "1"
            else:
                rounded_years = round(years)
                return str(int(rounded_years))
        
        return '0'
    
    def _count_months_in_text(self, text):
        """Count total months from date ranges in given text"""
        total_months = 0
        current_date = datetime.now()
        
        # Month mapping
        month_map = {
            'jan': 1, 'january': 1, 'feb': 2, 'february': 2,
            'mar': 3, 'march': 3, 'apr': 4, 'april': 4,
            'may': 5, 'jun': 6, 'june': 6,
            'jul': 7, 'july': 7, 'aug': 8, 'august': 8,
            'sep': 9, 'sept': 9, 'september': 9,
            'oct': 10, 'october': 10, 'nov': 11, 'november': 11,
            'dec': 12, 'december': 12
        }
        
        text_lower = text.lower()
        
        # Pattern: "Sep 2024 – Present"
        pattern1 = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[\s,]+(\d{4})\s*[-–—]\s*(present|current)'
        for match in re.finditer(pattern1, text_lower):
            month_name = match.group(1)
            year = int(match.group(2))
            month = month_map.get(month_name[:3])
            
            if month:
                months = (current_date.year - year) * 12 + (current_date.month - month)
                if 0 < months < 600:
                    total_months += months
                    print(f"  [+] Counted: {match.group(0)} = {months} months")
        
        # Pattern: "Jan 2020 - Dec 2023"
        pattern2 = r'(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[\s,]+(\d{4})\s*[-–—]\s*(jan|feb|mar|apr|may|jun|jul|aug|sep|sept|oct|nov|dec)[a-z]*[\s,]+(\d{4})'
        for match in re.finditer(pattern2, text_lower):
            start_month = month_map.get(match.group(1)[:3])
            start_year = int(match.group(2))
            end_month = month_map.get(match.group(3)[:3])
            end_year = int(match.group(4))
            
            if start_month and end_month:
                months = (end_year - start_year) * 12 + (end_month - start_month)
                if 0 < months < 600:
                    total_months += months
                    print(f"  [+] Counted: {match.group(0)} = {months} months")
        
        return total_months
    
    def _extract_education(self, text):
        """Extract education level"""
        text_lower = text.lower()
        
        if any(word in text_lower for word in ['phd', 'ph.d', 'doctorate', 'doctoral']):
            return 'PhD'
        if any(word in text_lower for word in ['master', 'm.sc', 'm.tech', 'm.a', 'mba', 'mca', 'postgraduate']):
            return "Master's Degree"
        if any(word in text_lower for word in ['bachelor', 'b.sc', 'b.tech', 'b.a', 'b.e', 'bca', 'undergraduate']):
            return "Bachelor's Degree"
        if any(word in text_lower for word in ['diploma', 'associate']):
            return 'Diploma'
        
        return 'Not specified'
    
    def _extract_job_titles(self, text):
        """Extract job titles from EXPERIENCE section only"""
        job_titles = []
        
        # Find EXPERIENCE section
        lines = text.split('\n')
        exp_start = -1
        exp_end = len(lines)
        
        for i, line in enumerate(lines):
            if 'EXPERIENCE' in line.upper():
                exp_start = i
                break
        
        if exp_start != -1:
            for i in range(exp_start + 1, len(lines)):
                if any(word in lines[i].upper() for word in ['PROJECT', 'EDUCATION', 'SKILL', 'CERTIFICATION']):
                    exp_end = i
                    break
            
            exp_text = '\n'.join(lines[exp_start:exp_end]).lower()
            
            # Look for common titles
            titles = [
                'technical researcher', 'research', 'engineer', 'developer',
                'analyst', 'manager', 'consultant', 'specialist'
            ]
            
            for title in titles:
                if title in exp_text:
                    job_titles.append(title.title())
        
        return list(set(job_titles))[:3] if job_titles else ['Professional']