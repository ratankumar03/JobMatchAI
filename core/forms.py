from django import forms

class CVUploadForm(forms.Form):
    """Form for CV upload"""
    file = forms.FileField(
        label='Upload Your CV',
        help_text='PDF or DOCX file (Max 10MB)',
        widget=forms.FileInput(attrs={
            'class': 'form-control',
            'accept': '.pdf,.docx,.doc'
        })
    )


class JobPreferenceForm(forms.Form):
    """Form for job preferences"""
    JOB_TYPE_CHOICES = [
        ('all', 'All Jobs'),
        ('government', 'Government Jobs'),
        ('private', 'Private/Company Jobs'),
    ]
    
    EXPERIENCE_LEVEL_CHOICES = [
        ('any', 'Any Level'),
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (2-5 years)'),
        ('senior', 'Senior Level (5+ years)'),
        ('executive', 'Executive/Leadership'),
    ]
    
    DATE_POSTED_CHOICES = [
        ('any', 'Any Time'),
        ('today', 'Posted Today'),
        ('week', 'Posted This Week'),
        ('month', 'Posted This Month'),
    ]
    
    job_type = forms.ChoiceField(
        choices=JOB_TYPE_CHOICES,
        required=False,
        initial='all',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Software Engineer, Data Analyst'
        })
    )
    
    location = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., London, Remote'
        })
    )
    
    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_LEVEL_CHOICES,
        required=False,
        initial='any',
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    
    date_posted = forms.ChoiceField(
        choices=DATE_POSTED_CHOICES,
        required=False,
        initial='any',
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Date Posted',
        help_text='Filter jobs by when they were posted'
    )


class GovernmentJobSearchForm(forms.Form):
    """Form for searching government jobs"""
    COUNTRY_CHOICES = [
        ('', 'All Countries'),
        ('UK', 'United Kingdom 🇬🇧'),
        ('USA', 'United States 🇺🇸'),
        ('India', 'India 🇮🇳'),
        ('Canada', 'Canada 🇨🇦'),
        ('Australia', 'Australia 🇦🇺'),
        ('EU', 'European Union 🇪🇺'),
        ('Singapore', 'Singapore 🇸🇬'),
        ('UAE', 'United Arab Emirates 🇦🇪'),
        ('NewZealand', 'New Zealand 🇳🇿'),
        ('Ireland', 'Ireland 🇮🇪'),
        ('Germany', 'Germany 🇩🇪'),
        ('France', 'France 🇫🇷'),
    ]
    
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Country'
    )
    
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., California, Maharashtra, Ontario'
        }),
        label='State/Province (Optional)'
    )
    
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Civil Service, Healthcare, Education'
        }),
        label='Job Title/Department'
    )


class CompanyJobSearchForm(forms.Form):
    """Form for searching company jobs"""
    COUNTRY_CHOICES = [
        ('', 'All Countries'),
        ('UK', 'United Kingdom 🇬🇧'),
        ('USA', 'United States 🇺🇸'),
        ('India', 'India 🇮🇳'),
        ('Canada', 'Canada 🇨🇦'),
        ('Australia', 'Australia 🇦🇺'),
        ('Singapore', 'Singapore 🇸🇬'),
        ('UAE', 'United Arab Emirates 🇦🇪'),
        ('Germany', 'Germany 🇩🇪'),
        ('Ireland', 'Ireland 🇮🇪'),
    ]
    
    EXPERIENCE_CHOICES = [
        ('', 'Any Experience'),
        ('fresher', 'Fresher (0-1 years)'),
        ('entry', 'Entry Level (0-2 years)'),
        ('mid', 'Mid Level (2-5 years)'),
        ('senior', 'Senior Level (5-10 years)'),
        ('lead', 'Lead/Principal (10+ years)'),
    ]
    
    COMPANY_CHOICES = [
        ('', 'All Companies'),
        # Tech Giants - USA
        ('Google', 'Google'),
        ('Microsoft', 'Microsoft'),
        ('Amazon', 'Amazon'),
        ('Apple', 'Apple'),
        ('Meta', 'Meta (Facebook)'),
        ('Netflix', 'Netflix'),
        ('Tesla', 'Tesla'),
        ('IBM', 'IBM'),
        ('Oracle', 'Oracle'),
        ('Salesforce', 'Salesforce'),
        ('Adobe', 'Adobe'),
        ('Intel', 'Intel'),
        ('Nvidia', 'Nvidia'),
        ('Cisco', 'Cisco'),
        ('Dell', 'Dell Technologies'),
        ('HP', 'HP (Hewlett Packard)'),
        ('VMware', 'VMware'),
        ('Qualcomm', 'Qualcomm'),
        ('Twitter', 'Twitter (X)'),
        ('Uber', 'Uber'),
        ('Lyft', 'Lyft'),
        ('Airbnb', 'Airbnb'),
        ('Spotify', 'Spotify'),
        ('Zoom', 'Zoom'),
        ('Slack', 'Slack'),
        ('Snapchat', 'Snapchat'),
        ('PayPal', 'PayPal'),
        ('eBay', 'eBay'),
        ('LinkedIn', 'LinkedIn'),
        ('Dropbox', 'Dropbox'),
        ('Shopify', 'Shopify'),
        ('Square', 'Square'),
        ('Stripe', 'Stripe'),
        ('GitHub', 'GitHub'),
        ('Reddit', 'Reddit'),
        ('Pinterest', 'Pinterest'),
        ('Yelp', 'Yelp'),
        # IT Services & Consulting
        ('Accenture', 'Accenture'),
        ('Deloitte', 'Deloitte'),
        ('PwC', 'PwC'),
        ('EY', 'EY (Ernst & Young)'),
        ('KPMG', 'KPMG'),
        ('McKinsey', 'McKinsey & Company'),
        ('BCG', 'Boston Consulting Group'),
        ('Bain', 'Bain & Company'),
        ('Capgemini', 'Capgemini'),
        ('Cognizant', 'Cognizant'),
        ('DXC Technology', 'DXC Technology'),
        ('Atos', 'Atos'),
        # Indian IT Companies
        ('TCS', 'TCS (Tata Consultancy Services)'),
        ('Infosys', 'Infosys'),
        ('Wipro', 'Wipro'),
        ('HCL', 'HCL Technologies'),
        ('Tech Mahindra', 'Tech Mahindra'),
        ('L&T Infotech', 'L&T Infotech'),
        ('Mphasis', 'Mphasis'),
        ('Mindtree', 'Mindtree'),
        ('Hexaware', 'Hexaware'),
        # E-commerce & Retail
        ('Walmart', 'Walmart'),
        ('Target', 'Target'),
        ('Flipkart', 'Flipkart'),
        ('Myntra', 'Myntra'),
        ('Snapdeal', 'Snapdeal'),
        ('Alibaba', 'Alibaba'),
        ('JD.com', 'JD.com'),
        # Finance & Banking
        ('JPMorgan', 'JPMorgan Chase'),
        ('Goldman Sachs', 'Goldman Sachs'),
        ('Morgan Stanley', 'Morgan Stanley'),
        ('Citibank', 'Citibank'),
        ('Bank of America', 'Bank of America'),
        ('Wells Fargo', 'Wells Fargo'),
        ('HSBC', 'HSBC'),
        ('Barclays', 'Barclays'),
        ('Standard Chartered', 'Standard Chartered'),
        ('Deutsche Bank', 'Deutsche Bank'),
        ('ICICI Bank', 'ICICI Bank'),
        ('HDFC Bank', 'HDFC Bank'),
        ('Axis Bank', 'Axis Bank'),
        ('SBI', 'State Bank of India'),
        ('Kotak Mahindra', 'Kotak Mahindra Bank'),
        # Telecom
        ('Verizon', 'Verizon'),
        ('AT&T', 'AT&T'),
        ('T-Mobile', 'T-Mobile'),
        ('Vodafone', 'Vodafone'),
        ('Airtel', 'Bharti Airtel'),
        ('Reliance Jio', 'Reliance Jio'),
        ('Vi', 'Vodafone Idea (Vi)'),
        # Automotive
        ('Ford', 'Ford'),
        ('GM', 'General Motors'),
        ('Toyota', 'Toyota'),
        ('Honda', 'Honda'),
        ('BMW', 'BMW'),
        ('Mercedes', 'Mercedes-Benz'),
        ('Volkswagen', 'Volkswagen'),
        ('Tata Motors', 'Tata Motors'),
        ('Mahindra', 'Mahindra & Mahindra'),
        # Pharma & Healthcare
        ('Pfizer', 'Pfizer'),
        ('Johnson & Johnson', 'Johnson & Johnson'),
        ('Novartis', 'Novartis'),
        ('Roche', 'Roche'),
        ('AstraZeneca', 'AstraZeneca'),
        ('GlaxoSmithKline', 'GlaxoSmithKline'),
        ('Merck', 'Merck'),
        ('Abbott', 'Abbott'),
        ('Sun Pharma', 'Sun Pharmaceutical'),
        ('Dr Reddy', 'Dr. Reddy\'s Laboratories'),
        ('Cipla', 'Cipla'),
        # FMCG & Consumer Goods
        ('Procter & Gamble', 'Procter & Gamble'),
        ('Unilever', 'Unilever'),
        ('Nestle', 'Nestle'),
        ('Coca-Cola', 'Coca-Cola'),
        ('PepsiCo', 'PepsiCo'),
        ('Mondelez', 'Mondelez International'),
        ('HUL', 'Hindustan Unilever'),
        ('ITC', 'ITC Limited'),
        # Energy & Oil
        ('Shell', 'Shell'),
        ('BP', 'BP'),
        ('ExxonMobil', 'ExxonMobil'),
        ('Chevron', 'Chevron'),
        ('TotalEnergies', 'TotalEnergies'),
        ('Reliance Industries', 'Reliance Industries'),
        # Aerospace & Defense
        ('Boeing', 'Boeing'),
        ('Airbus', 'Airbus'),
        ('Lockheed Martin', 'Lockheed Martin'),
        ('Raytheon', 'Raytheon Technologies'),
        ('Northrop Grumman', 'Northrop Grumman'),
        # Entertainment & Media
        ('Disney', 'Disney'),
        ('Warner Bros', 'Warner Bros'),
        ('Sony', 'Sony'),
        ('Comcast', 'Comcast'),
        ('NBCUniversal', 'NBCUniversal'),
        # Other Major Companies
        ('Samsung', 'Samsung'),
        ('LG', 'LG Electronics'),
        ('Siemens', 'Siemens'),
        ('Philips', 'Philips'),
        ('GE', 'General Electric'),
        ('3M', '3M'),
        ('Bosch', 'Bosch'),
        ('Honeywell', 'Honeywell'),
        ('Schneider Electric', 'Schneider Electric'),
    ]
    
    country = forms.ChoiceField(
        choices=COUNTRY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Country'
    )
    
    state = forms.CharField(
        max_length=100,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., California, London, Bangalore'
        }),
        label='State/City (Optional)'
    )
    
    job_title = forms.CharField(
        max_length=200,
        required=False,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'e.g., Software Engineer, Product Manager'
        }),
        label='Job Title/Role'
    )
    
    experience_level = forms.ChoiceField(
        choices=EXPERIENCE_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Experience Level'
    )
    
    company = forms.ChoiceField(
        choices=COMPANY_CHOICES,
        required=False,
        widget=forms.Select(attrs={'class': 'form-control'}),
        label='Company (Optional)'
    )