/**
 * GitHub Activity Calendar
 *
 * This script creates a GitHub-style contribution heatmap for a specified user.
 * It fetches real data from your Flask API endpoint.
 */

document.addEventListener('DOMContentLoaded', function() {
    // Initialize the GitHub calendar with your GitHub username
    initGitHubCalendar('Jakub-Nowicki', false); // false = use real data
});

/**
 * Initialize GitHub activity calendar
 * @param {string} username - GitHub username
 * @param {boolean} useDemo - Whether to use demo mode
 */
function initGitHubCalendar(username, useDemo = false) {
    const calendarContainer = document.getElementById('github-calendar');
    if (!calendarContainer) return;

    if (useDemo) {
        generateDemoCalendar(calendarContainer);
    } else {
        fetchGitHubContributions(username, calendarContainer);
    }
}

/**
 * Fetch real GitHub contribution data using our Flask endpoint
 * @param {string} username - GitHub username
 * @param {HTMLElement} container - Container element
 */
function fetchGitHubContributions(username, container) {
    // Use our Flask endpoint
    const apiUrl = `/api/github-contributions/${username}`;

    container.innerHTML = '<p class="loading-message">Loading GitHub activity data...</p>';

    fetch(apiUrl)
        .then(response => {
            if (!response.ok) {
                throw new Error('Failed to fetch GitHub data');
            }
            return response.json();
        })
        .then(data => {
            renderCalendar(data, container);
        })
        .catch(error => {
            console.error('Error fetching GitHub data:', error);
            container.innerHTML = `
                <p class="error-message">
                    Failed to load GitHub data: ${error.message}.
                    Loading demo data instead...
                </p>`;

            // Fallback to demo mode if API fails
            setTimeout(() => generateDemoCalendar(container), 2000);
        });
}

/**
 * Generate demo calendar with random contribution data
 * @param {HTMLElement} container - Container element
 */
function generateDemoCalendar(container) {
    // Generate 52 weeks (1 year) of random activity data
    const weeks = 52;
    const days = 7;

    // Generate random contribution data
    const contributions = [];
    for (let w = 0; w < weeks; w++) {
        const week = [];
        for (let d = 0; d < days; d++) {
            // Higher chance of activity on weekdays, less on weekends
            const isWeekend = (d === 0 || d === 6);
            const activityChance = isWeekend ? 0.3 : 0.6;
            const hasActivity = Math.random() < activityChance;

            if (hasActivity) {
                // Weight toward lower activity levels
                const level = Math.floor(Math.random() * 4) + 1;
                week.push(level);
            } else {
                week.push(0);
            }
        }
        contributions.push(week);
    }

    renderCalendar({contributions: contributions}, container);
}

/**
 * Render the calendar with the provided data
 * @param {Object} data - Calendar data object with contributions array
 * @param {HTMLElement} container - Container element
 */
function renderCalendar(data, container) {
    const contributions = data.contributions;

    // Create calendar container
    const calendar = document.createElement('div');
    calendar.className = 'github-calendar';

    // Add month labels
    const monthLabels = document.createElement('div');
    monthLabels.className = 'month-labels';

    // Get month abbreviations (most recent 12 months)
    const months = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec'];
    const currentDate = new Date();
    const currentMonth = currentDate.getMonth();

    // Create month labels
    let monthLabelHTML = '';
    for (let i = 0; i < 12; i++) {
        // Calculate month index going backward from current month
        const monthIndex = (currentMonth - i + 12) % 12;
        // Position month label roughly where it should appear
        const position = Math.round((11 - i) * (contributions.length / 12));

        if (i % 2 === 0) { // Show every other month to avoid crowding
            monthLabelHTML += `<div class="month-label" style="left: ${position * 12}px">${months[monthIndex]}</div>`;
        }
    }
    monthLabels.innerHTML = monthLabelHTML;

    // Create calendar grid - rotated so weeks are columns
    const gridWrapper = document.createElement('div');
    gridWrapper.className = 'calendar-grid';

    // First, transpose the data so we can iterate by days of week
    const transposed = [];
    for (let d = 0; d < 7; d++) {
        const row = [];
        for (let w = 0; w < contributions.length; w++) {
            row.push(contributions[w][d] || 0);
        }
        transposed.push(row);
    }

    // Day labels
    const dayLabels = ['Mon', '', 'Wed', '', 'Fri', '', 'Sun'];

    // Create grid rows (days of week)
    for (let day = 0; day < transposed.length; day++) {
        const weekRow = document.createElement('div');
        weekRow.className = 'calendar-row';

        // Add day label
        if (day % 2 === 0) { // Show every other day to avoid crowding
            const dayLabel = document.createElement('div');
            dayLabel.className = 'day-label';
            dayLabel.textContent = dayLabels[day];
            weekRow.appendChild(dayLabel);
        } else {
            // Empty placeholder to maintain alignment
            const emptyLabel = document.createElement('div');
            emptyLabel.className = 'day-label-empty';
            weekRow.appendChild(emptyLabel);
        }

        // Create cells for each week
        for (let week = 0; week < transposed[day].length; week++) {
            const cell = document.createElement('div');
            cell.className = 'calendar-cell';

            // Set color based on activity level
            const level = transposed[day][week];
            const color = getContributionColor(level);
            cell.style.backgroundColor = color;

            // Add tooltip
            cell.title = `${level} contribution${level !== 1 ? 's' : ''} on this day`;

            weekRow.appendChild(cell);
        }

        gridWrapper.appendChild(weekRow);
    }

    calendar.appendChild(monthLabels);
    calendar.appendChild(gridWrapper);

    // Add legend
    const legend = document.createElement('div');
    legend.className = 'calendar-legend';

    const legendItems = [
        { level: 0, label: 'No contributions' },
        { level: 1, label: 'Low' },
        { level: 2, label: 'Medium' },
        { level: 3, label: 'High' },
        { level: 4, label: 'Very high' }
    ];

    legendItems.forEach(item => {
        const legendItem = document.createElement('div');
        legendItem.className = 'legend-item';

        const colorBox = document.createElement('div');
        colorBox.className = 'legend-color';
        colorBox.style.backgroundColor = getContributionColor(item.level);

        const label = document.createElement('span');
        label.textContent = item.label;

        legendItem.appendChild(colorBox);
        legendItem.appendChild(label);
        legend.appendChild(legendItem);
    });

    calendar.appendChild(legend);

    // Replace loading message with calendar
    container.innerHTML = '';
    container.appendChild(calendar);
}

/**
 * Get the color for a contribution level
 * @param {number} level - Contribution level (0-4)
 * @returns {string} HEX color code
 */
function getContributionColor(level) {
    const colors = [
        '#161b22', // 0: No contributions
        '#0e4429', // 1: Low
        '#006d32', // 2: Medium
        '#26a641', // 3: High
        '#39d353'  // 4: Very high
    ];
    return colors[level] || colors[0];
}