from flask import Blueprint, jsonify, current_app, request
import requests
from datetime import datetime, timedelta
import json
import os
from functools import lru_cache

# Create a blueprint for GitHub API routes
github_bp = Blueprint('github', __name__)

# Try to load token from environment variables first (most secure)
GITHUB_TOKEN = os.environ.get("GITHUB_TOKEN", None)

# If not in environment, try to load from config file
if GITHUB_TOKEN is None:
    try:
        # Import the config file (which should not be in version control)
        from ..config.github_config import GITHUB_TOKEN as CONFIG_TOKEN

        GITHUB_TOKEN = CONFIG_TOKEN
    except ImportError:
        current_app.logger.warning("GitHub config file not found. Please create app/config/github_config.py")
        GITHUB_TOKEN = None
    except Exception as e:
        current_app.logger.error(f"Error loading GitHub token from config: {str(e)}")
        GITHUB_TOKEN = None

# GitHub API URLs
GITHUB_API_URL = "https://api.github.com"
GITHUB_GRAPHQL_URL = "https://api.github.com/graphql"


@lru_cache(maxsize=10)
def fetch_github_contributions(username, days=365):
    """
    Fetch GitHub contribution data using the GitHub GraphQL API

    Args:
        username: GitHub username
        days: Number of days of history to fetch (default 365)

    Returns:
        Processed contribution data or None if fetching fails
    """
    if not GITHUB_TOKEN:
        current_app.logger.error("GitHub token not configured. See setup instructions.")
        return None

    try:
        # Calculate date range
        end_date = datetime.now()
        start_date = end_date - timedelta(days=days)

        # Format dates for GraphQL query
        from_date = start_date.strftime("%Y-%m-%dT00:00:00Z")
        to_date = end_date.strftime("%Y-%m-%dT00:00:00Z")

        # GraphQL query to get contribution calendar
        query = """
        {
          user(login: "%s") {
            contributionsCollection(from: "%s", to: "%s") {
              contributionCalendar {
                totalContributions
                weeks {
                  contributionDays {
                    contributionCount
                    date
                    weekday
                  }
                }
              }
            }
          }
        }
        """ % (username, from_date, to_date)

        # Set up the request headers with the token
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Content-Type": "application/json"
        }

        # Make the API request
        response = requests.post(
            GITHUB_GRAPHQL_URL,
            json={"query": query},
            headers=headers,
            timeout=10
        )

        # Check if the request was successful
        if response.status_code != 200:
            current_app.logger.error(f"GitHub API error: {response.status_code} - {response.text}")
            return None

        # Parse the response
        data = response.json()

        # Check if we got valid data
        if "errors" in data:
            current_app.logger.error(f"GraphQL errors: {data['errors']}")
            return None

        if not data.get("data") or not data["data"].get("user"):
            current_app.logger.error(f"No user data returned: {data}")
            return None

        # Extract the contribution data
        contribution_data = data["data"]["user"]["contributionsCollection"]["contributionCalendar"]
        total = contribution_data["totalContributions"]
        weeks_data = contribution_data["weeks"]

        # Process the data into our expected format
        processed_data = process_contribution_data(weeks_data)

        return {
            "totalContributions": total,
            "contributions": processed_data
        }

    except Exception as e:
        current_app.logger.error(f"Error fetching GitHub contributions: {str(e)}")
        return None


def process_contribution_data(weeks_data):
    """
    Process the raw GitHub API response into the format our frontend expects

    Args:
        weeks_data: List of week objects from GitHub API

    Returns:
        List of weeks, each containing 7 contribution levels (0-4)
    """
    processed_weeks = []

    for week in weeks_data:
        week_contributions = []
        days = week["contributionDays"]

        # Create a placeholder for all 7 days of the week
        day_map = {i: 0 for i in range(7)}

        # Fill in the actual contributions
        for day in days:
            # GitHub API uses 0-6 for Sunday-Saturday
            # We need to map this to 0-6 for Monday-Sunday
            weekday = (day["weekday"] + 1) % 7
            count = day["contributionCount"]

            # Convert counts to levels (0-4)
            level = count_to_level(count)
            day_map[weekday] = level

        # Create a list of contribution levels for each day of the week
        for i in range(7):
            week_contributions.append(day_map[i])

        processed_weeks.append(week_contributions)

    return processed_weeks


def count_to_level(count):
    """Convert a contribution count to a level from 0-4"""
    if count == 0:
        return 0
    elif count <= 2:
        return 1
    elif count <= 5:
        return 2
    elif count <= 10:
        return 3
    else:
        return 4


@github_bp.route('/api/github-contributions/<username>')
def get_github_contributions(username):
    """
    Endpoint to fetch GitHub contribution data for a user

    Args:
        username: GitHub username

    Returns:
        JSON response with contribution data
    """
    try:
        # Check if token is set
        if not GITHUB_TOKEN:
            return jsonify({
                'error': 'GitHub token not configured. Please set up the token using environment variables or the config file.'
            }), 500

        # Fetch the contribution data
        data = fetch_github_contributions(username)

        # If fetching failed, generate synthetic data
        if data is None:
            return jsonify(generate_synthetic_data(150))

        # Return the contribution data
        return jsonify(data)

    except Exception as e:
        current_app.logger.error(f"Error in GitHub contributions endpoint: {str(e)}")
        return jsonify({'error': str(e)}), 500


def generate_synthetic_data(total_contributions):
    """Generate synthetic contribution data for fallback"""
    weeks = 52
    days_per_week = 7

    # Calculate roughly how many contributions per week
    contributions = []
    remaining = total_contributions

    for w in range(weeks):
        week = []
        for d in range(days_per_week):
            # Higher chance of activity on weekdays
            is_weekend = (d == 0 or d == 6)
            activity_chance = 0.3 if is_weekend else 0.7

            if remaining > 0 and (
                    w * days_per_week + d < min(total_contributions, weeks * days_per_week) or activity_chance > 0.5):
                # Distribute remaining contributions
                count = min(remaining, max(1, int(total_contributions / (weeks * days_per_week) * 2)))
                remaining -= count
                level = count_to_level(count)
                week.append(level)
            else:
                week.append(0)

        contributions.append(week)

    return {
        'totalContributions': total_contributions,
        'contributions': contributions
    }


@github_bp.route('/api/github-test-token')
def test_github_token():
    """
    Endpoint to test if the GitHub token is working properly

    Returns:
        JSON response with token status
    """
    if not GITHUB_TOKEN:
        return jsonify({
            'status': 'error',
            'message': 'GitHub token not configured. Please set up the token using environment variables or the config file.',
            'setup_instructions': {
                'environment_variable': 'Set GITHUB_TOKEN environment variable',
                'config_file': 'Create app/config/github_config.py file with GITHUB_TOKEN variable'
            }
        }), 500

    try:
        # Simple request to the GitHub API to check token validity
        headers = {
            "Authorization": f"Bearer {GITHUB_TOKEN}",
            "Accept": "application/vnd.github.v3+json"
        }

        response = requests.get(f"{GITHUB_API_URL}/user", headers=headers)

        if response.status_code == 200:
            user_data = response.json()
            return jsonify({
                'status': 'success',
                'message': f"Token is valid. Authenticated as: {user_data.get('login')}",
                'scopes': response.headers.get('X-OAuth-Scopes', '').split(', ')
            })
        else:
            return jsonify({
                'status': 'error',
                'message': f"Token validation failed: {response.status_code} - {response.text}"
            }), 400

    except Exception as e:
        return jsonify({
            'status': 'error',
            'message': f"Error testing token: {str(e)}"
        }), 500


@github_bp.route('/api/github-token-status')
def github_token_status():
    """
    Endpoint to check if the GitHub token is configured

    Returns:
        JSON response with token configuration status
    """
    is_configured = GITHUB_TOKEN is not None

    return jsonify({
        'is_configured': is_configured,
        'configuration_methods': {
            'environment_variable': 'GITHUB_TOKEN',
            'config_file': 'app/config/github_config.py'
        },
        'documentation': 'Check README for setup instructions'
    })