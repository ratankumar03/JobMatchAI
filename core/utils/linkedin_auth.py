"""
LinkedIn OAuth Integration - Fetch real job data from LinkedIn
"""
import requests
from django.conf import settings
from urllib.parse import urlencode
import json


class LinkedInAuth:
    """Handle LinkedIn OAuth authentication and job fetching"""

    def __init__(self):
        self.client_id = settings.LINKEDIN_CLIENT_ID
        self.client_secret = settings.LINKEDIN_CLIENT_SECRET
        self.redirect_uri = settings.LINKEDIN_REDIRECT_URI
        self.auth_url = "https://www.linkedin.com/oauth/v2/authorization"
        self.token_url = "https://www.linkedin.com/oauth/v2/accessToken"
        self.api_base = "https://api.linkedin.com/v2"

    def get_authorization_url(self, state=None):
        """
        Generate LinkedIn OAuth authorization URL
        Returns: Authorization URL for user to visit
        """
        params = {
            'response_type': 'code',
            'client_id': self.client_id,
            'redirect_uri': self.redirect_uri,
            'scope': 'r_liteprofile r_emailaddress',  # Basic profile and email
            'state': state or 'random_state_string'
        }

        auth_url = f"{self.auth_url}?{urlencode(params)}"
        return auth_url

    def get_access_token(self, authorization_code):
        """
        Exchange authorization code for access token
        Args:
            authorization_code: Code received from LinkedIn callback
        Returns:
            dict: Token information including access_token
        """
        try:
            payload = {
                'grant_type': 'authorization_code',
                'code': authorization_code,
                'redirect_uri': self.redirect_uri,
                'client_id': self.client_id,
                'client_secret': self.client_secret
            }

            response = requests.post(
                self.token_url,
                data=payload,
                headers={'Content-Type': 'application/x-www-form-urlencoded'}
            )

            if response.status_code == 200:
                token_data = response.json()
                print(f"[OK] LinkedIn access token obtained")
                return token_data
            else:
                print(f"[ERROR] Failed to get access token: {response.status_code}")
                print(f"Response: {response.text}")
                return None

        except Exception as e:
            print(f"[ERROR] Error getting LinkedIn access token: {e}")
            return None

    def get_user_profile(self, access_token):
        """
        Fetch LinkedIn user profile
        Args:
            access_token: LinkedIn OAuth access token
        Returns:
            dict: User profile information
        """
        try:
            headers = {
                'Authorization': f'Bearer {access_token}',
                'cache-control': 'no-cache',
                'X-Restli-Protocol-Version': '2.0.0'
            }

            # Get basic profile
            profile_url = f"{self.api_base}/me"
            response = requests.get(profile_url, headers=headers)

            if response.status_code == 200:
                profile = response.json()
                print(f"[OK] LinkedIn profile fetched")
                return profile
            else:
                print(f"[ERROR] Failed to fetch profile: {response.status_code}")
                return None

        except Exception as e:
            print(f"[ERROR] Error fetching LinkedIn profile: {e}")
            return None

    def search_jobs(self, access_token, keywords, location=None, count=25):
        """
        Search for jobs on LinkedIn
        Note: LinkedIn's Job Search API requires special partnership access
        This is a placeholder for when you have API access

        Args:
            access_token: LinkedIn OAuth access token
            keywords: Job search keywords
            location: Location to search (optional)
            count: Number of jobs to return
        Returns:
            list: Job listings from LinkedIn
        """
        try:
            # NOTE: LinkedIn Job Search API is not available in standard OAuth
            # You need LinkedIn Partnership or use LinkedIn's Job Search URLs

            print("[INFO] LinkedIn Job Search API requires Partnership access")
            print("[INFO] Redirecting users to LinkedIn job search URLs instead")

            # Generate LinkedIn job search URL
            from urllib.parse import quote
            encoded_keywords = quote(keywords)
            job_search_url = f"https://www.linkedin.com/jobs/search/?keywords={encoded_keywords}"

            if location:
                encoded_location = quote(location)
                job_search_url += f"&location={encoded_location}"

            return [{
                'title': f"LinkedIn Jobs - {keywords}",
                'company': 'Multiple Companies',
                'location': location or 'Worldwide',
                'link': job_search_url,
                'source': 'LinkedIn',
                'description': f'Search for {keywords} jobs on LinkedIn with your authenticated account',
                'posted_date': 'Live Search'
            }]

        except Exception as e:
            print(f"[ERROR] Error searching LinkedIn jobs: {e}")
            return []
